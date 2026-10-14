"""Tests of dashboard/build.py (offline, stdlib only): python3 -m unittest discover -s dashboard -p "test_*.py" """
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402

SAMPLE = Path(__file__).resolve().parent / "sample" / "positions.json"
NOW = datetime(2026, 10, 13, 8, 17, tzinfo=timezone.utc)


def sample():
    return json.loads(SAMPLE.read_text())


class PageData(unittest.TestCase):
    def test_sample_gives_the_page_its_numbers(self):
        doc = B.page_data(sample(), {}, NOW)
        self.assertEqual(doc["name"], "Tidebot")
        self.assertEqual((doc["snapshot_utc"], doc["equity_snap"]), ("2026-10-13T08:07:12Z", 1250.0))
        self.assertEqual([p["coin"] for p in doc["positions"]], ["BTC", "ETH", "SOL"])
        eth = doc["positions"][1]
        self.assertEqual((eth["side"], eth["qty"], eth["entry"], eth["mark"], eth["stop"]), ("Short", 0.3, 2600.0, 2530.0, 2700.0))
        self.assertFalse(doc["marks_live"])
        self.assertTrue(doc["orders_read"])
        self.assertEqual(doc["history"], sorted(doc["history"], key=lambda h: h["utc"]))

    def test_kraken_marks_reprice_and_the_snapshot_marks_stay(self):
        doc = B.page_data(sample(), {"BTC": 84000.0}, NOW)
        btc, eth = doc["positions"][:2]
        self.assertEqual((btc["mark"], btc["mark_snap"], eth["mark"]), (84000.0, 83500.0, 2530.0))
        self.assertTrue(doc["marks_live"])

    def test_futures_now_reads_the_perpetuals(self):
        tickers = {"tickers": [{"symbol": "PF_XBTUSD", "markPrice": 84000.5, "fundingRate": 0.84},
                               {"symbol": "PF_ETHUSD", "markPrice": "NaN", "fundingRate": 0.1},
                               {"symbol": "pf_solusd", "markPrice": 101.25}]}
        with mock.patch.dict(os.environ, {"NO_NETWORK": ""}), \
                mock.patch.object(B, "get", return_value=json.dumps(tickers).encode()) as get:
            marks, rates = B.futures_now(["BTC", "ETH", "SOL", "XRP"])
        self.assertEqual(marks, {"BTC": 84000.5, "SOL": 101.25})
        self.assertEqual(list(rates), ["BTC"])                        # Kraken's USD per coin per hour, per dollar
        self.assertAlmostEqual(rates["BTC"], 0.84 / 84000.5)
        self.assertIn("futures.kraken.com", get.call_args[0][0])
        with mock.patch.dict(os.environ, {"NO_NETWORK": ""}), mock.patch.object(B, "get", side_effect=OSError("down")):
            self.assertEqual(B.futures_now(["BTC"]), ({}, {}))

    def test_no_liquidation_figures_reach_the_page(self):
        snap = sample()
        self.assertIn('"liq": 6496', json.dumps(snap))                 # the snapshot has them: prices, margin, fills
        self.assertIn('"kind": "liquidation"', json.dumps(snap))
        text = json.dumps(B.page_data(snap, {}, NOW))
        self.assertNotIn("liq", text)
        self.assertNotIn("maint", text)
        self.assertNotIn("liquidation", (Path(__file__).resolve().parent / "template.html").read_text().lower())

    def test_odd_rows_are_left_out(self):
        snap = sample()
        snap["positions"] += [
            {"coin": "<script>", "side": "Long", "qty": 1, "entry": 1, "mark": 1},
            {"coin": "DOGE", "side": "Sideways", "qty": 1, "entry": 1, "mark": 1},
            {"coin": "ADA", "side": "Long", "qty": "NaN", "entry": 1, "mark": 1},
            {"coin": "LTC", "side": "Long", "qty": True, "entry": 1, "mark": 1},
            "not a position",
            {"coin": "AVAX", "side": "Short", "qty": 3, "entry": 20, "mark": 19},
        ]
        snap["history"] += [{"utc": "yesterday", "equity": 1}, {"utc": "2026-10-13T08:00:00Z", "equity": "Infinity"}]
        doc = B.page_data(snap, {}, NOW)
        self.assertEqual([p["coin"] for p in doc["positions"]], ["BTC", "ETH", "SOL", "AVAX"])
        self.assertEqual(len(doc["history"]), len(sample()["history"]))

    def test_a_snapshot_without_time_or_value_is_not_used(self):
        for bad in ({"equity": 1.0}, {"snapshot_utc": "2026-10-13T08:00:00Z", "equity": "NaN"}, {"snapshot_utc": "now", "equity": 1}):
            with self.assertRaises(ValueError):
                B.page_data(bad, {}, NOW)


class Transfers(unittest.TestCase):
    def test_deposits_pass_through_oldest_first_and_odd_ones_are_left_out(self):
        snap = sample()
        snap["transfers"] = [{"utc": "2026-10-13T06:54:52Z", "usd": 239.4}, {"utc": "2026-10-12T10:00:00Z", "usd": None},
                             {"utc": "yesterday", "usd": 1.0}, "not a transfer", {"utc": "2026-10-11T00:00:00Z", "usd": "NaN"},
                             {"utc": "2026-10-10T00:00:00Z", "usd": -50, "asset": "usd", "id": 9}]
        self.assertEqual(B.page_data(snap, {}, NOW)["transfers"], [
            {"utc": "2026-10-10T00:00:00Z", "usd": -50.0}, {"utc": "2026-10-11T00:00:00Z", "usd": None},
            {"utc": "2026-10-12T10:00:00Z", "usd": None}, {"utc": "2026-10-13T06:54:52Z", "usd": 239.4}])

    def test_a_move_worth_less_than_a_cent_is_left_out(self):
        snap = sample()
        snap["transfers"] = [{"utc": "2026-10-13T06:54:52Z", "usd": 239.4},
                             {"utc": "2026-10-13T10:25:55Z", "usd": 0.0},     # as Kraken's log gave it on 13 Oct
                             {"utc": "2026-10-13T10:30:00Z", "usd": -0.004},
                             {"utc": "2026-10-13T10:40:00Z", "usd": 0.01}]
        self.assertEqual(B.page_data(snap, {}, NOW)["transfers"], [
            {"utc": "2026-10-13T06:54:52Z", "usd": 239.4}, {"utc": "2026-10-13T10:40:00Z", "usd": 0.01}])

    def test_no_list_is_unknown_not_none_moved(self):
        snap = sample()
        del snap["transfers"]
        self.assertIsNone(B.page_data(snap, {}, NOW)["transfers"])
        self.assertEqual(B.page_data(sample(), {}, NOW)["transfers"], [{"utc": "2026-10-01T12:30:00Z", "usd": 200.0}])


class FreshStart(unittest.TestCase):
    def test_the_page_starts_with_the_value_right_after_the_deposit(self):
        snap = sample()
        snap["history"] = [{"utc": "2026-10-12T00:00:00Z", "equity": 96.81}, {"utc": "2026-10-13T06:01:59Z", "equity": 20.40},
                           {"utc": "2026-10-13T08:26:32Z", "equity": 262.57}]
        snap["transfers"] = [{"utc": "2026-10-10T00:00:00Z", "usd": 50.0}, {"utc": "2026-10-13T06:54:52Z", "usd": 239.4},
                             {"utc": "2026-10-13T09:00:00Z", "usd": -10.0}]
        snap["results"] = [{"coin": "XRP", "usd": -38.2, "since": "2026-10-07T20:11:19Z"},
                           {"coin": "BTC", "usd": -0.4, "since": "2026-10-13T06:55:10Z"}]
        doc = B.page_data(snap, {}, NOW, "2026-10-13T06:54:52Z")
        self.assertEqual([h["utc"] for h in doc["history"]], ["2026-10-13T06:54:52Z", "2026-10-13T08:26:32Z"])
        self.assertAlmostEqual(doc["history"][0]["equity"], 20.40 + 239.4)       # the 10 Oct move is in the 06:01 value
        self.assertEqual(doc["transfers"], [{"utc": "2026-10-13T09:00:00Z", "usd": -10.0}])
        self.assertEqual([(c["coin"], c["usd"]) for c in doc["coins"]], [("BTC", -0.4), ("XRP", -38.2)])  # losses stay

    def test_a_point_at_the_start_is_kept_and_no_start_shows_everything(self):
        snap = sample()
        start = snap["history"][2]["utc"]
        self.assertEqual(B.page_data(snap, {}, NOW, start)["history"], [h for h in B.history(snap) if h["utc"] >= start])
        self.assertEqual(B.page_data(snap, {}, NOW)["history"], B.history(snap))
        self.assertEqual(B.utc(B.FRESH_START), B.FRESH_START)


class Coins(unittest.TestCase):
    def test_no_results_are_unknown_not_none(self):
        self.assertIsNone(B.coins(None))
        self.assertIsNone(B.page_data({**sample(), "results": None}, {}, NOW)["coins"])
        self.assertEqual(B.coins([]), [])

    def test_results_pass_through_in_page_order_and_odd_rows_are_left_out(self):
        got = B.coins([{"coin": "DOGE", "usd": 0.4, "since": "2026-10-08T14:48:59Z"},
                       {"coin": "XRP", "usd": -38.2, "since": "2026-10-07T20:11:19Z"},
                       {"coin": "BTC", "usd": "NaN", "since": "2026-10-07T20:11:12Z"},
                       {"coin": "b@d", "usd": 1.0, "since": "2026-10-07T20:11:12Z"},
                       {"coin": "SOL", "usd": 1.0, "since": "bad time"}, "not a row"])
        self.assertEqual(got, [{"coin": "BTC", "usd": None, "funding": None, "since": "2026-10-07T20:11:12Z"},
                               {"coin": "XRP", "usd": -38.2, "funding": None, "since": "2026-10-07T20:11:19Z"},
                               {"coin": "DOGE", "usd": 0.4, "funding": None, "since": "2026-10-08T14:48:59Z"}])

    def test_the_sample_gives_each_coin_and_no_fills_reach_the_page(self):
        doc = B.page_data(sample(), {}, NOW)
        self.assertEqual([c["coin"] for c in doc["coins"]], ["BTC", "ETH", "SOL", "XRP"])
        self.assertNotIn("fills", json.dumps(doc))
        self.assertNotIn("open_funding", json.dumps(doc))


class Funding(unittest.TestCase):
    def test_funding_of_each_position_and_coin_passes_through(self):
        doc = B.page_data(sample(), {}, NOW)
        btc, eth = doc["positions"][:2]
        self.assertEqual((btc["funding"], btc["funding_since"], btc["funding_rate"]), (-0.35, "2026-10-10T09:12:40Z", 1.2e-05))
        self.assertEqual((eth["funding"], eth["funding_since"]), (0.12, "2026-10-11T14:02:11Z"))
        self.assertEqual([(c["coin"], c["usd"], c["funding"]) for c in doc["coins"]],
                         [("BTC", -1.84, -0.52), ("ETH", -9.37, 0.05), ("SOL", 4.21, -0.08), ("XRP", -11.6, -0.31)])

    def test_kraken_rates_now_replace_the_snapshots(self):
        doc = B.page_data(sample(), {"BTC": 84000.0}, NOW, None, {"BTC": -3e-06})
        self.assertEqual([p["funding_rate"] for p in doc["positions"]], [-3e-06, 2e-05, 4.2e-05])

    def test_a_snapshot_from_before_the_split_has_no_funding_figures(self):
        snap = sample()
        for p in snap["positions"]:
            p.pop("funding_since")
            p["funding"] = None
        for r in snap["results"]:
            r.pop("funding")
        snap["positions"][0]["funding_since"] = "yesterday"
        doc = B.page_data(snap, {}, NOW)
        self.assertEqual({(p["funding"], p["funding_since"]) for p in doc["positions"]}, {(None, None)})
        self.assertEqual({c["funding"] for c in doc["coins"]}, {None})

    def test_page_writes_funding_rates_per_hour(self):
        node = shutil.which("node")
        if not node:
            self.skipTest("node not installed")
        html = (Path(__file__).resolve().parent / "template.html").read_text()
        helpers = [re.search(r"\n  const %s = .*?;\n" % name, html, re.S).group(0) for name in ("MINUS", "fix", "signed")]
        fn = re.search(r"\n  const hourly = x => \{\n.*?\n  \};\n", html, re.S).group(0)
        js = "".join(helpers) + fn + "console.log(JSON.stringify([1.127e-5, 3.3216e-6, -2e-5, 0, 1.25e-4].map(hourly)));"
        r = subprocess.run([node, "-e", js], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout), ["+0.0011%/h", "+0.00033%/h", "−0.0020%/h", "0.0000%/h", "+0.0125%/h"])


class Page(unittest.TestCase):
    def test_written_page_and_data(self):
        doc = B.page_data(sample(), {}, NOW)
        doc["name"] = "</script><script>alert(1)</script>"            # nothing in the data can end the script tag
        with tempfile.TemporaryDirectory() as d:
            B.write(doc, Path(d))
            html = (Path(d) / "index.html").read_text()
            data = json.loads((Path(d) / "data.json").read_text())
        self.assertEqual(data["name"], doc["name"])
        self.assertNotIn("__DATA__", html)
        self.assertEqual(html.count("</script>"), 2)                  # the template's own two
        inline = re.search(r'<script id="data" type="application/json">(.*?)</script>', html, re.S).group(1)
        self.assertEqual(json.loads(inline), data)

    def test_page_script_parses(self):
        node = shutil.which("node")
        if not node:
            self.skipTest("node not installed")
        html = (Path(__file__).resolve().parent / "template.html").read_text()
        js = re.findall(r"<script>(.*?)</script>", html, re.S)
        self.assertEqual(len(js), 1)
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
            f.write(js[0])
        try:
            r = subprocess.run([node, "--check", f.name], capture_output=True, text=True)
        finally:
            os.unlink(f.name)
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_page_leaves_deposits_out_of_the_gain(self):
        """The page's result(): the change minus net deposits, and the returns between deposits chained."""
        node = shutil.which("node")
        if not node:
            self.skipTest("node not installed")
        html = (Path(__file__).resolve().parent / "template.html").read_text()
        fn = re.search(r"\n  function result\(pts, moves\) \{\n.*?\n  \}\n", html, re.S).group(0)
        pts = [{"t": 0, "v": 96.81}, {"t": 10, "v": 20.40}, {"t": 30, "v": 262.57}, {"t": 40, "v": 260.21}]
        cases = [[{"t": 20, "usd": 239.4}], [], None, [{"t": 20, "usd": None}],
                 [{"t": 20, "usd": 239.4}, {"t": 25, "usd": -100.0}], [{"t": 5, "usd": -96.81}]]
        js = fn + f"console.log(JSON.stringify({json.dumps(cases)}.map(m => result({json.dumps(pts)}, m))));"
        r = subprocess.run([node, "-e", js], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        (dep, none, unknown, unvalued, two, emptied) = json.loads(r.stdout)
        self.assertAlmostEqual(dep["gain"], 260.21 - 96.81 - 239.4)
        self.assertAlmostEqual(dep["pct"], 20.40 / 96.81 * 260.21 / (20.40 + 239.4) - 1)
        for plain in (none, unknown, unvalued):                       # no deposits, or none that can be left out
            self.assertAlmostEqual(plain["gain"], 260.21 - 96.81)
            self.assertAlmostEqual(plain["pct"], (260.21 - 96.81) / 96.81)
        self.assertAlmostEqual(two["gain"], 260.21 - 96.81 - 139.4)
        self.assertAlmostEqual(two["pct"], 20.40 / 96.81 * 1 * 260.21 / (20.40 + 239.4 - 100.0) - 1)   # no point between
        self.assertIsNone(emptied["pct"])                             # everything taken out: no percentage

    def test_no_snapshot_builds_nothing(self):
        with mock.patch.dict(os.environ, {"SNAPSHOT_FILE": "/nonexistent/positions.json"}), \
                mock.patch.object(B, "write", side_effect=AssertionError("written")):
            self.assertEqual(B.main(), 3)


if __name__ == "__main__":
    unittest.main()
