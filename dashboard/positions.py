#!/usr/bin/env python3
"""The "Open positions" page (site/index.html): every open position of the Kraken Futures account and the account
value, read with a READ-ONLY key (repository secrets KRAKEN_READ_KEY / KRAKEN_READ_SECRET). No name and no bot data
on the page. The browser re-prices the positions every minute from Kraken's public spot prices.

Local test without a key: POSITIONS_FILE=<openpositions json> ACCOUNTS_FILE=<accounts json> python3 positions.py
"""
import base64
import hashlib
import hmac
import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).parent
FUTURES = "https://futures.kraken.com"


def get(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": "positions-page", **(headers or {})})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def read_private(path, local_env):
    """GET a private Kraken Futures endpoint with the read-only key. No nonce (optional on Kraken Futures), so it
    never clashes with another client of the same account."""
    if os.environ.get(local_env):
        return json.loads(Path(os.environ[local_env]).read_text())
    key, secret = os.environ["KRAKEN_READ_KEY"], os.environ["KRAKEN_READ_SECRET"]
    digest = hashlib.sha256(path.removeprefix("/derivatives").encode()).digest()
    authent = base64.b64encode(hmac.new(base64.b64decode(secret), digest, hashlib.sha512).digest()).decode()
    return json.loads(get(FUTURES + path, {"APIKey": key, "Authent": authent}))


def marks():
    try:
        tickers = json.loads(get(FUTURES + "/derivatives/api/v3/tickers"))["tickers"]
        return {t["symbol"].upper(): float(t["markPrice"]) for t in tickers if t.get("markPrice")}
    except Exception as e:
        print("tickers failed:", type(e).__name__)
        return {}


def coin_of(symbol):
    """PF_XBTUSD -> BTC, PF_SOLUSD -> SOL."""
    c = symbol.upper().removeprefix("PF_").removeprefix("PI_").removesuffix("USD")
    return {"XBT": "BTC"}.get(c, c)


def snapshot():
    pos = read_private("/derivatives/api/v3/openpositions", "POSITIONS_FILE")["openPositions"]
    flex = read_private("/derivatives/api/v3/accounts", "ACCOUNTS_FILE")["accounts"]["flex"]
    m = marks()
    out = []
    for p in pos:
        sym, qty, entry = p["symbol"].upper(), float(p["size"]), float(p["price"])
        side = 1 if p.get("side") == "long" else -1
        mark = m.get(sym)
        if mark:
            upnl = side * qty * (mark - entry)
        else:                   # no public mark: Kraken's own unrealized P&L gives the price
            upnl = float(p.get("unrealizedPnl") or 0.0)
            mark = entry + upnl / (side * qty) if qty else entry
        out.append({"coin": coin_of(sym), "side": "Long" if side > 0 else "Short", "qty": qty, "entry": entry,
                    "mark": mark, "pnl_usd": upnl})
    return {"equity": float(flex["portfolioValue"]), "available": float(flex.get("availableMargin") or 0.0),
            "positions": out, "error": None}


def build():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    keyed = os.environ.get("KRAKEN_READ_KEY") and os.environ.get("KRAKEN_READ_SECRET")
    if not (keyed or os.environ.get("POSITIONS_FILE")):
        print("no read key set")
        doc = {"equity": None, "available": None, "positions": [], "error": "Account not connected yet."}
    else:
        try:
            doc = snapshot()
        except Exception as e:  # never prints the key or a request: only the error type
            print("account read failed:", type(e).__name__)
            doc = {"equity": None, "available": None, "positions": [], "error": "Account not readable at the last update."}
    doc["updated_utc"] = now
    data = json.dumps(doc, separators=(",", ":")).replace("</", "<\\/")
    out = HERE.parent / "site"
    out.mkdir(exist_ok=True)
    (out / "meta.json").write_text(json.dumps({"built_utc": now}))
    (out / "index.html").write_text((HERE / "positions.html").read_text().replace("__DATA__", data))
    print(f"built: {len(doc['positions'])} position(s), error {doc['error']}")


if __name__ == "__main__":
    build()
