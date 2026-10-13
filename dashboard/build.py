#!/usr/bin/env python3
"""Build Tidebot: the public phone dashboard of the Kraken Futures account (read-only: no Kraken key, no orders).

Reads the read-only account snapshot (positions.json on the branch positions-data of the private repo
Tommievr/tradingbot, written every hour by its ops/positions_snapshot.py) with the read-only token
TRADINGBOT_READ_TOKEN, re-prices the open positions with Kraken's public futures prices, groups the account's last
fills into trades, and writes site/index.html (the page, its data inline) and site/data.json (the same data, which
the open page re-reads every few minutes). The browser re-prices the positions every minute from Kraken's public
prices and works out the account value, the P&L and the distance to liquidation itself.

Exit codes: 0 built, 3 no snapshot could be read (nothing written: the workflow keeps the last page up).
Local test: SNAPSHOT_FILE=dashboard/sample/positions.json NO_NETWORK=1 python3 dashboard/build.py
"""
import json
import math
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

NAME = "Tidebot"
REPO = "Tommievr/tradingbot"
SNAPSHOT, SNAPSHOT_REF = "positions.json", "positions-data"
ORDER = ["BTC", "ETH", "SOL", "XRP", "BNB"]     # these first on the page, then the others by size
TRADE_GAP_S = 15 * 60       # fills of one coin, side and kind, each within 15 minutes of the last, are one trade
TRADES_MAX = 40
KINDS = ("taker", "maker", "liquidation", "other")
FMT = "%Y-%m-%dT%H:%M:%SZ"
COIN = re.compile(r"[A-Z0-9]{1,12}")
HERE = Path(__file__).resolve().parent


def get(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": "tidebot-dashboard", **(headers or {})})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def num(x):
    """A finite float, else None (bools are not numbers here)."""
    if isinstance(x, bool):
        return None
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return v if math.isfinite(v) else None


def utc(s):
    """'2026-10-13T06:01:59Z' -> the same string when it is a valid time in that format, else None."""
    try:
        return s if datetime.strptime(s, FMT).strftime(FMT) == s else None
    except (TypeError, ValueError):
        return None


def epoch(s):
    return datetime.strptime(s, FMT).replace(tzinfo=timezone.utc).timestamp()


def stamp(t):
    return datetime.fromtimestamp(t, timezone.utc).strftime(FMT)


def read_snapshot():
    if os.environ.get("SNAPSHOT_FILE"):
        return json.loads(Path(os.environ["SNAPSHOT_FILE"]).read_text())
    return json.loads(get(f"https://api.github.com/repos/{REPO}/contents/{SNAPSHOT}?ref={SNAPSHOT_REF}", {
        "Authorization": f"Bearer {os.environ['TRADINGBOT_READ_TOKEN']}",
        "Accept": "application/vnd.github.raw",
    }))


def perp(coin):
    return f"PF_{'XBT' if coin == 'BTC' else coin}USD"


def futures_marks(coins):
    """{coin: Kraken's mark price now} for the coins held; empty when Kraken is not reachable."""
    if not coins or os.environ.get("NO_NETWORK"):
        return {}
    try:
        tickers = json.loads(get("https://futures.kraken.com/derivatives/api/v3/tickers"))["tickers"]
        by_sym = {str(t.get("symbol", "")).upper(): t for t in tickers}
    except Exception as e:  # the page then starts from the snapshot's prices
        print("kraken tickers failed:", type(e).__name__)
        return {}
    out = {}
    for c in coins:
        mark = num((by_sym.get(perp(c)) or {}).get("markPrice"))
        if mark and mark > 0:
            out[c] = mark
    return out


def positions(snap):
    out = []
    for p in snap.get("positions") or []:
        if not isinstance(p, dict):
            continue
        coin, side = str(p.get("coin", "")), p.get("side")
        qty, entry, mark = num(p.get("qty")), num(p.get("entry")), num(p.get("mark"))
        if not COIN.fullmatch(coin) or side not in ("Long", "Short") or not (
                qty and qty > 0 and entry and entry > 0 and mark and mark > 0):
            continue
        out.append({"coin": coin, "side": side, "qty": qty, "entry": entry, "mark_snap": mark,
                    "stop": num(p.get("stop")), "tp": num(p.get("tp")), "liq_snap": num(p.get("liq")),
                    "funding": num(p.get("funding")), "funding_rate": num(p.get("funding_rate"))})
    out.sort(key=lambda p: (ORDER.index(p["coin"]) if p["coin"] in ORDER else len(ORDER), -p["qty"] * p["mark_snap"]))
    return out


def maintenance(snap, pos, equity):
    """The account's maintenance margin: from the snapshot, or worked back from a position's liquidation price
    (the snapshot puts it where the value would reach the maintenance margin if only that coin moved)."""
    m = num(snap.get("maint"))
    if m is not None:
        return m
    for p in pos:
        if p["liq_snap"]:
            side = 1 if p["side"] == "Long" else -1
            return equity - side * p["qty"] * (p["mark_snap"] - p["liq_snap"])
    return None


def trades(fills):
    """The fills as trades, latest first: one coin's fills of one side and kind, each within TRADE_GAP_S of the last
    and with no other fill of that coin in between, are one trade (one order filled in parts, or a liquidation done
    in steps). None when the snapshot has no fill list (unknown, not "no trades")."""
    if not isinstance(fills, list):
        return None
    clean = []
    for f in fills:
        if not isinstance(f, dict):
            continue
        t, coin, side, kind = utc(f.get("utc")), str(f.get("coin", "")), f.get("side"), f.get("kind")
        qty, px = num(f.get("qty")), num(f.get("price"))
        if t and COIN.fullmatch(coin) and side in ("buy", "sell") and qty and qty > 0 and px and px > 0:
            clean.append((epoch(t), coin, side, kind if kind in KINDS else "other", qty, px, num(f.get("pnl"))))
    clean.sort(key=lambda f: f[0])
    groups, last = [], {}
    for t, coin, side, kind, qty, px, pnl in clean:
        g = last.get(coin)
        if g is None or (g["side"], g["kind"]) != (side, kind) or t - g["t1"] > TRADE_GAP_S:
            g = {"t0": t, "coin": coin, "side": side, "kind": kind, "qty": 0.0, "value": 0.0, "pnl": None, "fills": 0}
            groups.append(g)
            last[coin] = g
        g["t1"] = t
        g["qty"] += qty
        g["value"] += qty * px
        g["fills"] += 1
        if pnl is not None:
            g["pnl"] = (g["pnl"] or 0.0) + pnl
    groups.sort(key=lambda g: g["t1"])                  # the latest activity first on the page
    return [{"utc": stamp(g["t0"]), "end": stamp(g["t1"]) if g["t1"] > g["t0"] else None, "coin": g["coin"],
             "side": g["side"], "kind": g["kind"], "qty": g["qty"], "price": g["value"] / g["qty"],
             "value": g["value"], "pnl": g["pnl"], "fills": g["fills"]} for g in reversed(groups[-TRADES_MAX:])]


def history(snap):
    pts = [{"utc": h["utc"], "equity": num(h["equity"])} for h in snap.get("history") or []
           if isinstance(h, dict) and utc(h.get("utc")) and num(h.get("equity")) is not None]
    return sorted(pts, key=lambda h: h["utc"])


def page_data(snap, marks, now):
    snap_utc, equity = utc(snap.get("snapshot_utc")), num(snap.get("equity"))
    if not snap_utc or equity is None:
        raise ValueError("the snapshot has no time or account value")
    pos = positions(snap)
    for p in pos:
        p["mark"] = marks.get(p["coin"], p["mark_snap"])
    return {
        "name": NAME, "built_utc": now.strftime(FMT), "snapshot_utc": snap_utc, "equity_snap": equity,
        "available": num(snap.get("available")), "initial": num(snap.get("initial")),
        "maint": maintenance(snap, pos, equity), "orders_read": snap.get("orders_read") is True,
        "marks_live": bool(marks), "positions": pos, "trades": trades(snap.get("fills")), "history": history(snap),
    }


def write(doc, out):
    data = json.dumps(doc, separators=(",", ":"), allow_nan=False)
    inline = data.replace("<", "\\u003c")        # nothing in the data can end the script tag it sits in
    out.mkdir(parents=True, exist_ok=True)
    (out / "data.json").write_text(data)
    (out / "index.html").write_text((HERE / "template.html").read_text().replace("__DATA__", inline))


def main():
    now = datetime.now(timezone.utc)
    try:
        snap = read_snapshot()
        doc = page_data(snap, {}, now)          # fails here on a snapshot without a time or value
    except Exception as e:      # the token, GitHub or the file: only the kind of failure is printed
        print("account snapshot not usable:", type(e).__name__, getattr(e, "code", ""))
        return 3
    marks = futures_marks([p["coin"] for p in doc["positions"]])
    doc = page_data(snap, marks, now)
    write(doc, HERE.parent / "site")
    print(f"built {NAME}: snapshot {doc['snapshot_utc']}, {len(doc['positions'])} position(s), "
          f"{'no' if doc['trades'] is None else len(doc['trades'])} trade(s), prices "
          f"{'from Kraken now' if marks else 'from the snapshot'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
