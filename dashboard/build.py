#!/usr/bin/env python3
"""Build the phone dashboard of the live 5-coin bot (read-only: no Kraken keys, no orders).

Reads the live journal of Tommievr/tradingbot (via the GitHub API with a read-only token in
TRADINGBOT_READ_TOKEN) and the public Kraken Futures tickers, and writes site/index.html.
"""
import json
import os
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ORDER = ["BTC", "ETH", "SOL", "XRP", "BNB"]
PERP = {"BTC": "PF_XBTUSD", "ETH": "PF_ETHUSD", "SOL": "PF_SOLUSD", "XRP": "PF_XRPUSD", "BNB": "PF_BNBUSD"}
START_EQ = 95.19       # 7 Oct 2026 restart at 5% risk per coin (Tommie): the page counts from here
RESTART_UTC = "2026-10-07T20:05:00Z"   # journal rows before this belong to the first run (4-7 Oct), not shown
TAKER, MAKER = 0.0005, 0.0002   # Kraken Futures base-tier fees, as in tradingbot ruleb_tp2/config.py
JOURNAL = "ruleb_tp2/state_live/5coin/ruleb_tp2_live_journal.jsonl"
STATE = "ruleb_tp2/state_live/5coin/ruleb_tp2_live_state.json"
HERE = Path(__file__).parent


def get(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": "bot-dashboard", **(headers or {})})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def repo_file(path, env):
    if os.environ.get(env):
        return Path(os.environ[env]).read_text()
    return get(f"https://api.github.com/repos/Tommievr/tradingbot/contents/{path}?ref=main", {
        "Authorization": f"Bearer {os.environ['TRADINGBOT_READ_TOKEN']}",
        "Accept": "application/vnd.github.raw",
    }).decode()


def journal_rows():
    rows = [json.loads(l) for l in repo_file(JOURNAL, "JOURNAL_FILE").splitlines() if l.strip()]
    return [r for r in rows if r["utc"] >= RESTART_UTC]


def halted_flat(rows, last):
    """(reason, equity) when the bot was HALTED and flattened after its last run summary (the kill switch writes
    no run summary), else None. The equity is the book's cash after the flatten (= the Kraken equity it read)."""
    after = rows[rows.index(last) + 1:]
    halt = next((r for r in reversed(after) if r["kind"] == "halt"), None)
    flat = any(r["kind"] == "flatten_done" and not r["payload"].get("left") for r in after)
    if halt is None or not flat:
        return None
    try:
        eq = float(json.loads(repo_file(STATE, "STATE_FILE"))["engine"]["cash"])
    except Exception as e:  # keep building on the journal alone
        print("state read failed:", e)
        eq = None
    return halt["payload"].get("reason") or "halted", eq, halt["utc"]


def kraken_marks():
    try:
        tickers = json.loads(get("https://futures.kraken.com/derivatives/api/v3/tickers"))["tickers"]
    except Exception as e:  # keep the page building on the last bot marks
        print("kraken tickers failed:", e)
        return {}
    by_sym = {t["symbol"]: t for t in tickers}
    return {c: float(by_sym[p]["markPrice"]) for c, p in PERP.items() if p in by_sym and by_sym[p].get("markPrice")}


def funding_rates(perp):
    """Kraken's hourly funding as [(hour start epoch_s, USD per contract per hour, fraction of notional)], oldest
    first; None when unavailable."""
    try:
        rates = json.loads(get(f"https://futures.kraken.com/derivatives/api/v4/historicalfundingrates?symbol={perp}"))["rates"]
        return sorted((datetime.fromisoformat(r["timestamp"].replace("Z", "+00:00")).timestamp(), float(r["fundingRate"]),
                       float(r["relativeFundingRate"])) for r in rates)
    except Exception as e:
        print("funding failed:", perp, e)
        return None


def funding_paid(rates, side, qty, t0, t1):
    """Funding over [t0, t1] (+ received, - paid; > 0 rate = longs pay): each hour's rate accrues for the part of
    that hour held, x the size (as Kraken accrues it)."""
    total = 0.0
    for ts, rate, _ in rates:
        held = min(ts + 3600, t1) - max(ts, t0)
        if held > 0:
            total -= side * qty * rate * held / 3600
    return total


def fees_paid(rows):
    """Trading fees per coin since the restart, estimated from the journal's fills at Kraken's fee rates."""
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
    stopped = halted_flat(rows, last)
    if stopped:      # flattened by the kill switch: no legs, the equity after the flatten, the halt's time
        reason, eq_after, halt_utc = stopped
        p = {**p, "legs": {}, "status": "halted", "halted": reason,
             "equity_usd": eq_after if eq_after is not None else p.get("equity_usd")}
        last = {**last, "utc": halt_utc, "payload": p}
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
            # estimate: longs pay when the rate is positive; the current size, since this entry
            since = entered.get(l["sym"], 0)
            side = 1 if l["side"] == "Long" else -1
            rates = funding_rates(PERP[l["sym"]])
            l["funding"] = None if rates is None else funding_paid(rates, side, l["qty"], since, time.time())
            l["funding_rate"] = rates[-1][2] if rates else None  # latest hourly rate, fraction of notional
            funding = None if funding is None or l["funding"] is None else funding + l["funding"]
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    history = [{"utc": r["utc"], "equity": r["payload"].get("equity_usd")} for r in runs[-120:]]
    if eq is not None:
        history.append({"utc": now, "equity": eq})
    doc = {
        "updated_utc": now, "run_utc": last["utc"], "status": p.get("status"), "halted": p.get("halted"),
        "equity": eq, "notional": notional, "lev_total": notional / eq if eq else None, "funding": funding,
        "fees": sum(fees.values()), "start_eq": START_EQ, "vs_start_pct": (eq / START_EQ - 1) * 100 if eq else None,
        "legs": legs, "history": history,
    }
    data = json.dumps(doc, separators=(",", ":")).replace("</", "<\\/")
    out = HERE.parent / "site"
    out.mkdir(exist_ok=True)
    (out / "meta.json").write_text(json.dumps({"built_utc": now, "journal_sha": os.environ.get("JOURNAL_SHA", "")}))
    (out / "index.html").write_text((HERE / "template.html").read_text().replace("__DATA__", data))
    print(f"built: equity {eq}, prices from {'kraken' if live else 'last bot run'}")


if __name__ == "__main__":
    build()
