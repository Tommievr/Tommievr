#!/usr/bin/env python3
"""Build the phone dashboard of the live 5-coin bot (read-only: no Kraken keys, no orders).

Reads the live journal of Tommievr/tradingbot (via the GitHub API with a read-only token in
TRADINGBOT_READ_TOKEN) and the public Kraken Futures tickers, and writes site/index.html.
"""
import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ORDER = ["BTC", "ETH", "SOL", "XRP", "BNB"]
PERP = {"BTC": "PF_XBTUSD", "ETH": "PF_ETHUSD", "SOL": "PF_SOLUSD", "XRP": "PF_XRPUSD", "BNB": "PF_BNBUSD"}
START_EQ = 114.74      # 4 Oct 2026 20:58 UTC go-live
REENTRY_EQ = 114.54    # 4 Oct 2026 21:59 UTC re-entry at 5% risk
TAKER, MAKER = 0.0005, 0.0002   # Kraken Futures base-tier fees, as in tradingbot ruleb_tp2/config.py
JOURNAL = "ruleb_tp2/state_live/5coin/ruleb_tp2_live_journal.jsonl"
HERE = Path(__file__).parent


def get(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": "bot-dashboard", **(headers or {})})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def journal_rows():
    if os.environ.get("JOURNAL_FILE"):
        text = Path(os.environ["JOURNAL_FILE"]).read_text()
    else:
        text = get(f"https://api.github.com/repos/Tommievr/tradingbot/contents/{JOURNAL}?ref=main", {
            "Authorization": f"Bearer {os.environ['TRADINGBOT_READ_TOKEN']}",
            "Accept": "application/vnd.github.raw",
        }).decode()
    return [json.loads(l) for l in text.splitlines() if l.strip()]


def kraken_marks():
    try:
        tickers = json.loads(get("https://futures.kraken.com/derivatives/api/v3/tickers"))["tickers"]
    except Exception as e:  # keep the page building on the last bot marks
        print("kraken tickers failed:", e)
        return {}
    by_sym = {t["symbol"]: t for t in tickers}
    return {c: float(by_sym[p]["markPrice"]) for c, p in PERP.items() if p in by_sym and by_sym[p].get("markPrice")}


def funding_rates(perp):
    """Hourly relative funding (fraction of notional) as [(epoch_s, rel)]; None when unavailable."""
    try:
        rates = json.loads(get(f"https://futures.kraken.com/derivatives/api/v4/historicalfundingrates?symbol={perp}"))["rates"]
        return [(datetime.fromisoformat(r["timestamp"].replace("Z", "+00:00")).timestamp(), float(r["relativeFundingRate"]))
                for r in rates]
    except Exception as e:
        print("funding failed:", perp, e)
        return None


def fees_paid(rows):
    """Trading fees per coin since bot start, estimated from the journal's fills at Kraken's fee rates."""
    fees = {c: 0.0 for c in ORDER}
    flat_runs = {r["run_id"] for r in rows if r["kind"] == "halt"}
    for r in rows:
        p, k = r["payload"], r["kind"]
        if k in ("order_filled", "entry_fallback_filled", "entry_limit_fill", "resting_fill") and p.get("price"):
            rate = MAKER if k == "entry_limit_fill" or p.get("what") == "tp" else TAKER
        elif k == "order_send" and r["run_id"] in flat_runs and p.get("reduce_only"):
            rate = TAKER   # flatten closes: the journal keeps only the order (its IOC limit stands in for the fill)
        else:
            continue
        if p.get("sym") in fees:
            fees[p["sym"]] += rate * float(p.get("qty") or p.get("size")) * float(p["price"])
    return fees


def build():
    rows = journal_rows()
    fees = fees_paid(rows)
    entered = {}
    for r in rows:
        if r["kind"] == "entry_filled":
            entered[r["payload"]["sym"]] = r["ts"]
    runs = [r for r in rows if r["kind"] == "run_summary"]
    last = runs[-1]
    p = last["payload"]
    run_marks = p.get("marks") or {}
    live = kraken_marks()
    marks = {c: live.get(c, run_marks.get(c)) for c in ORDER}

    legs, eq_move = [], 0.0
    for sym in ORDER:
        leg = (p.get("legs") or {}).get(sym)
        mark = marks.get(sym)
        if not leg:
            legs.append({"sym": sym, "open": False, "mark": mark})
            continue
        side, entry, qty = leg["side"], leg["entry"], leg["qty"]
        stop = leg.get("trail") or leg.get("stop")
        if mark and run_marks.get(sym):
            eq_move += (mark - run_marks[sym]) * qty * side
        legs.append({
            "sym": sym, "open": True, "side": "Long" if side > 0 else "Short",
            "entry": entry, "mark": mark, "qty": qty, "stop": stop, "tp": leg.get("tp"),
            "liq": leg.get("liq"), "tp_done": bool(leg.get("tp_done")), "trailing": leg.get("trail") is not None,
            "stop_hit": bool(mark and stop and (mark - stop) * side <= 0),
            "pnl_pct": (mark / entry - 1) * 100 * side if mark else None,
            "pnl_usd": (mark - entry) * qty * side if mark else None, "fees": fees[sym],
        })

    eq = p["equity_usd"] + eq_move if p.get("equity_usd") is not None else None
    notional, funding = 0.0, 0.0
    for l in legs:
        if l["open"] and l["mark"]:
            l["notional"] = l["qty"] * l["mark"]
            l["lev"] = l["notional"] / eq if eq else None
            notional += l["notional"]
            # estimate: longs pay when the rate is positive; current size and price, since this entry
            since = entered.get(l["sym"], 0)
            side = 1 if l["side"] == "Long" else -1
            rates = funding_rates(PERP[l["sym"]])
            l["funding"] = None if rates is None else sum(-side * rel * l["notional"] for ts, rel in rates if ts > since)
            l["funding_rate"] = max(rates)[1] if rates else None  # latest hourly rate, fraction of notional
            funding = None if funding is None or l["funding"] is None else funding + l["funding"]
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    history = [{"utc": r["utc"], "equity": r["payload"].get("equity_usd")} for r in runs[-120:]]
    if eq is not None:
        history.append({"utc": now, "equity": eq})
    doc = {
        "updated_utc": now, "run_utc": last["utc"], "status": p.get("status"), "halted": p.get("halted"),
        "equity": eq, "notional": notional, "lev_total": notional / eq if eq else None, "funding": funding, "fees": sum(fees.values()), "start_eq": START_EQ, "reentry_eq": REENTRY_EQ,
        "vs_start_pct": (eq / START_EQ - 1) * 100 if eq else None,
        "vs_reentry_pct": (eq / REENTRY_EQ - 1) * 100 if eq else None,
        "legs": legs, "history": history,
    }
    data = json.dumps(doc, separators=(",", ":")).replace("</", "<\\/")
    out = HERE.parent / "site"
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text((HERE / "template.html").read_text().replace("__DATA__", data))
    print(f"built: equity {eq}, prices from {'kraken' if live else 'last bot run'}")


if __name__ == "__main__":
    build()
