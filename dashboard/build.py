#!/usr/bin/env python3
"""Build Tidebot: the public phone dashboard of the Kraken Futures account (read-only: no Kraken key, no orders).

Reads the read-only account snapshot (positions.json on the branch positions-data of the private repo
Tommievr/tradingbot, written every hour by its ops/positions_snapshot.py) with the read-only token
TRADINGBOT_READ_TOKEN, re-prices the open positions with Kraken's public futures prices (and takes the funding rates
from the same read), passes on each coin's result (from Kraken's account log: P&L, fees and funding, with the funding
also on its own, as on each open position) and the deposits and withdrawals (the page leaves them out of its gain or
loss), and writes site/index.html (the page, its data inline) and site/data.json (the same data, which the
open page re-reads every few minutes). The account value starts at FRESH_START: the value history and money moves
before it are left out, while the results per coin keep everything the snapshot has, losses included. The browser
re-prices the positions every minute from Kraken's public prices and works out the account value and the P&L itself.
The page shows no liquidation figures and no trade list, so neither is passed on.

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
FMT = "%Y-%m-%dT%H:%M:%SZ"
COIN = re.compile(r"[A-Z0-9]{1,12}")
HERE = Path(__file__).resolve().parent
FRESH_START = "2026-10-13T06:54:52Z"    # the account value starts here, right after a deposit (asked for 13 Oct)


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


def read_snapshot():
    if os.environ.get("SNAPSHOT_FILE"):
        return json.loads(Path(os.environ["SNAPSHOT_FILE"]).read_text())
    return json.loads(get(f"https://api.github.com/repos/{REPO}/contents/{SNAPSHOT}?ref={SNAPSHOT_REF}", {
        "Authorization": f"Bearer {os.environ['TRADINGBOT_READ_TOKEN']}",
        "Accept": "application/vnd.github.raw",
    }))


def perp(coin):
    return f"PF_{'XBT' if coin == 'BTC' else coin}USD"


def futures_now(coins):
    """({coin: Kraken's mark price now}, {coin: its funding rate now, per hour as a fraction of the position's value})
    for the coins held; both empty when Kraken is not reachable."""
    if not coins or os.environ.get("NO_NETWORK"):
        return {}, {}
    try:
        tickers = json.loads(get("https://futures.kraken.com/derivatives/api/v3/tickers"))["tickers"]
        by_sym = {str(t.get("symbol", "")).upper(): t for t in tickers}
    except Exception as e:  # the page then starts from the snapshot's prices and rates
        print("kraken tickers failed:", type(e).__name__)
        return {}, {}
    marks, rates = {}, {}
    for c in coins:
        t = by_sym.get(perp(c)) or {}
        mark, rate = num(t.get("markPrice")), num(t.get("fundingRate"))     # the rate in USD per coin per hour
        if mark and mark > 0:
            marks[c] = mark
            if rate is not None:
                rates[c] = rate / mark
    return marks, rates


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
                    "stop": num(p.get("stop")), "tp": num(p.get("tp")), "funding": num(p.get("funding")),
                    "funding_since": utc(p.get("funding_since")), "funding_rate": num(p.get("funding_rate"))})
    out.sort(key=lambda p: (ORDER.index(p["coin"]) if p["coin"] in ORDER else len(ORDER), -p["qty"] * p["mark_snap"]))
    return out


def coins(results):
    """Each coin's result in the account from the snapshot (USD, after fees and funding; None when unknown), the
    funding part of it (None when unknown) and the time of its first booking, in the page's coin order. None when the
    snapshot has no results (unknown, not none)."""
    if not isinstance(results, list):
        return None
    out = [{"coin": r["coin"], "usd": num(r.get("usd")), "funding": num(r.get("funding")), "since": utc(r.get("since"))}
           for r in results if isinstance(r, dict) and COIN.fullmatch(str(r.get("coin", ""))) and utc(r.get("since"))]
    return sorted(out, key=lambda c: (ORDER.index(c["coin"]) if c["coin"] in ORDER else len(ORDER), c["coin"]))


def transfers(snap):
    """Money moved into (+) or out of (-) the account in USD, oldest first (usd None: Kraken gave no rate for it).
    A move worth less than a cent is left out (Kraken values some currencies at $0). None when the snapshot has no
    list: then the page cannot tell a deposit from a gain."""
    moved = snap.get("transfers")
    if not isinstance(moved, list):
        return None
    out = [{"utc": t["utc"], "usd": num(t.get("usd"))} for t in moved if isinstance(t, dict) and utc(t.get("utc"))]
    return sorted((t for t in out if t["usd"] is None or abs(t["usd"]) >= 0.005), key=lambda t: t["utc"])


def history(snap):
    pts = [{"utc": h["utc"], "equity": num(h["equity"])} for h in snap.get("history") or []
           if isinstance(h, dict) and utc(h.get("utc")) and num(h.get("equity")) is not None]
    return sorted(pts, key=lambda h: h["utc"])


def since(start, hist, moved):
    """The value history and money moves from `start` on. The history then begins at `start` with the last value before
    it plus the money moved in or out after that value and up to `start`, so a deposit right at the start is part of
    the starting value, not a gain."""
    before, hist = [h for h in hist if h["utc"] < start], [h for h in hist if h["utc"] >= start]
    if before and not (hist and hist[0]["utc"] == start):
        added = sum(m["usd"] for m in moved or [] if before[-1]["utc"] < m["utc"] <= start and m["usd"] is not None)
        hist.insert(0, {"utc": start, "equity": before[-1]["equity"] + added})
    if moved is not None:
        moved = [m for m in moved if m["utc"] > start]
    return hist, moved


def page_data(snap, marks, now, start=None, rates=None):
    """The page's data; with `start` (a time in FMT) the account value starts afresh there, see since(). `marks` and
    `rates` (Kraken's prices and funding rates now) replace the snapshot's for the coins they have."""
    snap_utc, equity = utc(snap.get("snapshot_utc")), num(snap.get("equity"))
    if not snap_utc or equity is None:
        raise ValueError("the snapshot has no time or account value")
    pos = positions(snap)
    for p in pos:
        p["mark"] = marks.get(p["coin"], p["mark_snap"])
        p["funding_rate"] = (rates or {}).get(p["coin"], p["funding_rate"])
    hist, moved = history(snap), transfers(snap)
    if start:
        hist, moved = since(start, hist, moved)
    return {
        "name": NAME, "built_utc": now.strftime(FMT), "snapshot_utc": snap_utc, "equity_snap": equity,
        "available": num(snap.get("available")), "initial": num(snap.get("initial")),
        "orders_read": snap.get("orders_read") is True,
        "marks_live": bool(marks), "positions": pos, "coins": coins(snap.get("results")), "history": hist,
        "transfers": moved,
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
        doc = page_data(snap, {}, now, FRESH_START)     # fails here on a snapshot without a time or value
    except Exception as e:      # the token, GitHub or the file: only the kind of failure is printed
        print("account snapshot not usable:", type(e).__name__, getattr(e, "code", ""))
        return 3
    marks, rates = futures_now([p["coin"] for p in doc["positions"]])
    doc = page_data(snap, marks, now, FRESH_START, rates)
    write(doc, HERE.parent / "site")
    print(f"built {NAME}: snapshot {doc['snapshot_utc']}, {len(doc['positions'])} position(s), "
          f"{'no' if doc['coins'] is None else len(doc['coins'])} coin result(s), prices "
          f"{'from Kraken now' if marks else 'from the snapshot'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
