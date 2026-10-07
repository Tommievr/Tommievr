#!/usr/bin/env python3
"""The "Open positions" page (site/index.html): every open position of the Kraken Futures account and the account
value. No name and no bot data on the page. The browser re-prices the positions every minute from Kraken's public
spot prices.

The numbers come from the READ-ONLY snapshot positions.json (every 3 hours) on the positions-data branch of
Tommievr/tradingbot (its positions-snapshot job reads Kraken there with the read-only key, so no Kraken key is ever in
this public repo).
This build reads that file with the read token TRADINGBOT_READ_TOKEN and copies only the fields the page shows.

Local test: SNAPSHOT_FILE=<positions.json> python3 positions.py
"""
import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).parent
SNAPSHOT = "https://api.github.com/repos/Tommievr/tradingbot/contents/positions.json?ref=positions-data"
STALE = timedelta(hours=8)        # the snapshot runs every 3 h and GitHub runs crons late


def get(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": "positions-page", **(headers or {})})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def read_snapshot():
    if os.environ.get("SNAPSHOT_FILE"):
        return json.loads(Path(os.environ["SNAPSHOT_FILE"]).read_text())
    return json.loads(get(SNAPSHOT, {"Authorization": f"Bearer {os.environ['TRADINGBOT_READ_TOKEN']}",
                                     "Accept": "application/vnd.github.raw"}))


def clean(raw):
    """Only the fields the page shows, as numbers and short labels: nothing else in the file reaches the page."""
    pos = [{"coin": str(p["coin"])[:10], "side": "Long" if p["side"] == "Long" else "Short", "qty": float(p["qty"]),
            "entry": float(p["entry"]), "mark": float(p["mark"]), "pnl_usd": float(p["pnl_usd"])}
           for p in raw["positions"]]
    when = datetime.strptime(raw["snapshot_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    return {"equity": float(raw["equity"]), "available": float(raw["available"]), "positions": pos}, when


def build():
    now = datetime.now(timezone.utc)
    empty = {"equity": None, "available": None, "positions": []}
    when = now
    if not (os.environ.get("TRADINGBOT_READ_TOKEN") or os.environ.get("SNAPSHOT_FILE")):
        print("no read token set")
        doc = {**empty, "error": "Account not connected yet."}
    else:
        try:
            doc, when = clean(read_snapshot())
            doc["error"] = "Positions are more than 8 hours old." if now - when > STALE else None
        except urllib.error.HTTPError as e:     # 404: no snapshot written yet
            print("snapshot read failed: HTTP", e.code)
            doc = {**empty, "error": "Account not connected yet." if e.code == 404 else
                   "Positions not readable at the last update."}
        except Exception as e:  # never prints the token or a request: only the error type
            print("snapshot read failed:", type(e).__name__)
            doc = {**empty, "error": "Positions not readable at the last update."}
    doc["updated_utc"] = when.strftime("%Y-%m-%dT%H:%M:%SZ")
    data = json.dumps(doc, separators=(",", ":")).replace("</", "<\\/")
    out = HERE.parent / "site"
    out.mkdir(exist_ok=True)
    (out / "meta.json").write_text(json.dumps({"built_utc": now.strftime("%Y-%m-%dT%H:%M:%SZ")}))
    (out / "index.html").write_text((HERE / "positions.html").read_text().replace("__DATA__", data))
    print(f"built: {len(doc['positions'])} position(s), error {doc['error']}")


if __name__ == "__main__":
    build()
