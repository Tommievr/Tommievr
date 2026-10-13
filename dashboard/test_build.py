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


def fill(utc, coin="SOL", side="buy", qty=1.0, price=100.0, kind="taker", pnl=0.0):
    return {"utc": utc, "coin": coin, "side": side, "qty": qty, "price": price, "kind": kind, "pnl": pnl}


class PageData(unittest.TestCase):
    def test_sample_gives_the_page_its_numbers(self):
        doc = B.page_data(sample(), {}, NOW)
        self.assertEqual(doc["name"], "Tidebot")
        self.assertEqual((doc["snapshot_utc"], doc["equity_snap"], doc["maint"]), ("2026-10-13T08:07:12Z", 1250.0, 60.0))
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

    def test_futures_marks_reads_the_perpetuals(self):
        tickers = {"tickers": [{"symbol": "PF_XBTUSD", "markPrice": 84000.5}, {"symbol": "PF_ETHUSD", "markPrice": "NaN"},
                               {"symbol": "pf_solusd", "markPrice": 101.25}]}
        with mock.patch.dict(os.environ, {"NO_NETWORK": ""}), \
                mock.patch.object(B, "get", return_value=json.dumps(tickers).encode()) as get:
            self.assertEqual(B.futures_marks(["BTC", "ETH", "SOL", "XRP"]), {"BTC": 84000.5, "SOL": 101.25})
        self.assertIn("futures.kraken.com", get.call_args[0][0])
        with mock.patch.dict(os.environ, {"NO_NETWORK": ""}), mock.patch.object(B, "get", side_effect=OSError("down")):
            self.assertEqual(B.futures_marks(["BTC"]), {})

    def test_maintenance_margin_from_a_liquidation_price_when_the_snapshot_has_none(self):
        snap = sample()
        del snap["maint"]
        snap["positions"][1]["liq"] = 6496.0
        doc = B.page_data(snap, {}, NOW)
        self.assertAlmostEqual(doc["maint"], 1250.0 + 0.3 * (2530.0 - 6496.0))     # a short: value - side*qty*(mark-liq)
        for p in snap["positions"]:
            p["liq"] = None
        self.assertIsNone(B.page_data(snap, {}, NOW)["maint"])

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

    def test_no_list_is_unknown_not_none_moved(self):
        snap = sample()
        del snap["transfers"]
        self.assertIsNone(B.page_data(snap, {}, NOW)["transfers"])
        self.assertEqual(B.page_data(sample(), {}, NOW)["transfers"], [{"utc": "2026-10-01T12:30:00Z", "usd": 200.0}])


class Trades(unittest.TestCase):
    def test_no_fill_list_is_unknown_not_empty(self):
        self.assertIsNone(B.trades(None))
        self.assertEqual(B.trades([]), [])

    def test_parts_of_one_order_and_a_stepwise_liquidation_are_one_trade(self):
        fills = [fill("2026-10-13T00:50:49Z", "XRP", "sell", 18, 1.3161, "liquidation", -1.5786),
                 fill("2026-10-13T00:51:00Z", "XRP", "sell", 16, 1.3146, "liquidation", -1.4272),
                 fill("2026-10-13T00:50:49Z", "BTC", "sell", 0.0003, 81091, "liquidation", -0.5855),
                 fill("2026-10-08T14:48:59Z", "ETH", "buy", 0.003, 2529.4),
                 fill("2026-10-08T14:48:59Z", "ETH", "buy", 0.02, 2529.2)]
        got = B.trades(fills)
        self.assertEqual([(t["coin"], t["side"], t["kind"], t["fills"]) for t in got],
                         [("XRP", "sell", "liquidation", 2), ("BTC", "sell", "liquidation", 1), ("ETH", "buy", "taker", 2)])
        xrp = got[0]
        self.assertEqual((xrp["utc"], xrp["end"], xrp["qty"]), ("2026-10-13T00:50:49Z", "2026-10-13T00:51:00Z", 34))
        self.assertAlmostEqual(xrp["price"], (18 * 1.3161 + 16 * 1.3146) / 34)
        self.assertAlmostEqual(xrp["value"], 18 * 1.3161 + 16 * 1.3146)
        self.assertAlmostEqual(xrp["pnl"], -1.5786 - 1.4272)
        self.assertIsNone(got[2]["end"])

    def test_a_gap_another_side_or_kind_starts_a_new_trade(self):
        fills = [fill("2026-10-10T10:00:00Z"), fill("2026-10-10T10:14:00Z"),          # within 15 min: one
                 fill("2026-10-10T10:30:00Z"),                                         # 16 min later: new
                 fill("2026-10-10T10:31:00Z", side="sell"),                            # other side: new
                 fill("2026-10-10T10:32:00Z"),                                         # after a sell: new
                 fill("2026-10-10T10:33:00Z", kind="liquidation"),                     # other kind: new
                 fill("2026-10-10T10:33:30Z", coin="BTC", price=80000.0),              # other coin: own trade
                 fill("2026-10-10T10:34:00Z")]                                         # after the liquidation: new
        got = B.trades(fills)
        self.assertEqual(len(got), 7)
        self.assertEqual([t["fills"] for t in got if t["coin"] == "SOL"][::-1], [2, 1, 1, 1, 1, 1])

    def test_pnl_unknown_only_when_no_fill_gives_it(self):
        got = B.trades([fill("2026-10-10T10:00:00Z", pnl=None), fill("2026-10-10T10:01:00Z", pnl=None)])
        self.assertIsNone(got[0]["pnl"])
        got = B.trades([fill("2026-10-10T10:00:00Z", pnl=None), fill("2026-10-10T10:01:00Z", pnl=-2.0)])
        self.assertEqual(got[0]["pnl"], -2.0)

    def test_newest_first_capped_and_odd_fills_left_out(self):
        fills = [fill(f"2026-10-{d:02d}T10:00:00Z") for d in range(1, 31)] + \
                [fill(f"2026-09-{d:02d}T10:00:00Z", coin="BTC") for d in range(1, 30)] + \
                [fill("bad time"), fill("2026-10-10T10:00:00Z", coin="b@d"), fill("2026-10-10T10:00:00Z", side="hold"),
                 fill("2026-10-10T10:00:00Z", qty=0), fill("2026-10-10T10:00:00Z", price="NaN"), "not a fill",
                 fill("2026-10-31T10:00:00Z", kind="assignment")]
        got = B.trades(fills)
        self.assertEqual(len(got), B.TRADES_MAX)
        self.assertEqual(got[0]["utc"], "2026-10-31T10:00:00Z")
        self.assertEqual(got[0]["kind"], "other")
        self.assertEqual([t["utc"] for t in got], sorted((t["utc"] for t in got), reverse=True))


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
