"""The week review page (site/review.html) of the live 5-coin bot: account, per coin, what happened, live vs the
paper books, backtest context. Read-only; built by build.py from the same journal, as of the last bot run."""
import json
import os
from datetime import datetime, timezone
from html import escape
from pathlib import Path

HERE = Path(__file__).parent
FLOOR_FRACTION = 0.5
# the paper books of the same rule (Tommievr/tradingbot), each with its own start
PAPERS = [
    ("Paper: same rule, 1% risk", "1%", "ruleb_tp2/state_5coin/ruleb_tp2_journal.jsonl"),
    ("Paper: 1% risk, smart limit entry", "1%", "ruleb_tp2/state_5coin_limit/ruleb_tp2_journal.jsonl"),
    ("Paper: 1-day limit entry (0.25 x ATR)", "1%", "limit_paper/state/journal.jsonl"),
]
# Backtest of the live settings (5% risk per coin, ruleb_tp2.sim_n with config_5coin and risk 0.05, Kraken-like
# costs), one start per year, run on 7 Oct 2026. Static context: the backtest does not change week to week.
BACKTEST = [
    ("Start 1 Jan 2021", "up to +242%, then down to the 50% floor: stopped 22 Dec 2021 at +72%"),
    ("Start 3 Jan 2022", "up to +129%, then down to the floor: stopped 8 Nov 2022 at +15%"),
    ("Start 2 Jan 2023", "never above the start: stopped at the floor on 17 Aug 2023 at -50%"),
    ("Start 1 Jan 2024", "up to +82%, then down to the floor: stopped 14 Jul 2024 at -9%"),
    ("Start 1 Jan 2025", "up to +32%, then down to the floor: stopped 27 Jun 2025 at -34%"),
]
BACKTEST_WEEKS = "Any 7 days while it ran (until each stop): median -0.4%; 1 in 4 below -5.3%, 1 in 4 above " \
                 "+3.7%; 1 in 10 below -10.8%, 1 in 10 above +13.0%."


def _eq(p):
    v = p.get("equity_usd", p.get("equity"))
    return float(v) if isinstance(v, (int, float)) else None


def paper_change(rows, live_start):
    """(start label, % change) of a paper book: from its last equity at or before the live start (else its own
    first record) to its last record. None when the journal has no equity yet."""
    pts = [(r["utc"], _eq(r["payload"])) for r in rows if isinstance(r.get("payload"), dict)]
    pts = [(t, e) for t, e in pts if e]
    if not pts:
        return None
    before = [x for x in pts if x[0] <= live_start]
    base = before[-1] if before else pts[0]
    since = "the live start" if before else datetime.fromisoformat(base[0].replace("Z", "+00:00")).strftime("%-d %b")
    return since, (pts[-1][1] / base[1] - 1) * 100, pts[-1][0]


def _pct(v, d=2):
    return "–" if v is None else f"{v:+.{d}f}%"


def _usd(v):
    return "–" if v is None else ("+$" if v >= 0 else "−$") + f"{abs(v):.2f}"


def _cls(v):
    return "" if v is None else ("up" if v >= 0 else "down")


def _hm(utc):
    return datetime.fromisoformat(utc.replace("Z", "+00:00")).strftime("%a %-d %b %H:%M UTC")


def build_review(rows, doc, papers, out: Path, start_utc: str):
    runs = [r for r in rows if r["kind"] == "run_summary" and _eq(r["payload"])]
    eqs = [_eq(r["payload"]) for r in runs]
    start_eq, now_eq = doc["start_eq"], eqs[-1] if eqs else None
    peak, maxdd = start_eq, 0.0
    for e in eqs:
        peak = max(peak, e)
        maxdd = min(maxdd, (e / peak - 1) * 100)
    floor = FLOOR_FRACTION * peak
    last_run = runs[-1]["utc"] if runs else doc["run_utc"]
    days = (datetime.fromisoformat(last_run.replace("Z", "+00:00"))
            - datetime.fromisoformat(start_utc.replace("Z", "+00:00"))).total_seconds() / 86400
    kinds = [r["kind"] for r in rows]
    fills = [r["payload"].get("what") for r in rows if r["kind"] == "resting_fill"]
    gaps = 0
    ts = [datetime.fromisoformat(r["utc"].replace("Z", "+00:00")) for r in runs]
    for a, b in zip(ts, ts[1:]):
        gaps += (b - a).total_seconds() > 13 * 3600
    events = [
        ("Bot runs", len(runs)), ("Gaps over 13 h between runs", gaps),
        ("Entries filled", kinds.count("entry_filled")), ("Take-profit (TP1) fills", fills.count("tp")),
        ("Stop fills", fills.count("stop")), ("Daily loss guard / floor at a 12:20 run", kinds.count("account_guard")),
        ("Kraken errors that paused a run", kinds.count("exchange_error")), ("HALTs", kinds.count("halt")),
    ]
    tiles = [
        ("Equity at the last run", f"${now_eq:.2f}" if now_eq else "–",
         f"{_usd(now_eq - start_eq if now_eq else None)} ({_pct((now_eq / start_eq - 1) * 100 if now_eq else None)})",
         _cls(now_eq - start_eq if now_eq else None)),
        ("Bot start", f"${start_eq:.2f}", f"{days:.1f} days live", ""),
        ("Peak", f"${peak:.2f}", f"max drawdown {_pct(maxdd, 1)}", "down" if maxdd < 0 else ""),
        ("50% floor", f"${floor:.2f}",
         f"{(now_eq - floor) / now_eq * 100:.0f}% away" if now_eq else "–", ""),
    ]
    coin_rows = []
    for l in doc["legs"]:
        if not l["open"]:
            coin_rows.append(f"<tr><td><b>{escape(l['sym'])}</b></td><td colspan=6 class=muted>no position</td></tr>")
            continue
        status = "TP1 hit, trailing" if l["tp_done"] else ("past stop" if l["stop_hit"] else "open")
        coin_rows.append(
            f"<tr><td><b>{escape(l['sym'])}</b></td><td>{l['side']}</td><td class=num>{l['entry']:,.4g}</td>"
            f"<td class=num>{l['mark']:,.4g}</td><td class='num {_cls(l['pnl_pct'])}'>{_pct(l['pnl_pct'])}</td>"
            f"<td class='num {_cls(l['pnl_usd'])}'>{_usd(l['pnl_usd'])}</td><td>{status}</td></tr>")
    paper_rows = [f"<tr><td>Live bot (real money)</td><td>5%</td><td>the live start</td>"
                  f"<td class='num {_cls(now_eq - start_eq if now_eq else None)}'>"
                  f"{_pct((now_eq / start_eq - 1) * 100 if now_eq else None)}</td></tr>"]
    for name, risk, res in papers:
        if res is None:
            paper_rows.append(f"<tr><td>{escape(name)}</td><td>{risk}</td><td colspan=2 class=muted>no data yet</td></tr>")
        else:
            since, ch, _ = res
            paper_rows.append(f"<tr><td>{escape(name)}</td><td>{risk}</td><td>{escape(since)}</td>"
                              f"<td class='num {_cls(ch)}'>{_pct(ch)}</td></tr>")
    body = f"""
<header><h1>Week review · 5-coin bot</h1><a href="./">← dashboard</a></header>
<p class=muted>As of the last bot run, {_hm(last_run)}. Live since {_hm(start_utc)}. Built {_hm(doc['updated_utc'])}.</p>
<section class=tiles>{''.join(f'<div class=tile><span>{escape(a)}</span><b class=num>{b}</b><small class="{d}">{escape(c)}</small></div>' for a, b, c, d in tiles)}</section>
<h2>Per coin (as of the last run)</h2>
<div class=scroll><table><tr><th>Coin</th><th>Side</th><th>Entry</th><th>Last</th><th>Move</th><th>P&amp;L</th><th>Status</th></tr>{''.join(coin_rows)}</table></div>
<p class=muted>Trading fees so far {_usd(-doc['fees'])}; funding (estimate) {_usd(doc['funding'])}. Both are already inside the equity.</p>
<h2>What happened</h2>
<table>{''.join(f'<tr><td>{escape(k)}</td><td class=num>{v}</td></tr>' for k, v in events)}</table>
<h2>Live vs paper</h2>
<table><tr><th>Book</th><th>Risk per coin</th><th>Since</th><th>Change</th></tr>{''.join(paper_rows)}</table>
<p class=muted>The paper books trade the same rule on Kraken's public prices. At 1% risk their moves are roughly a fifth of the live bot's. A big gap in direction (not in size) between live and paper is worth a look.</p>
<h2>Backtest context (live settings, 5% per coin)</h2>
<table>{''.join(f'<tr><td>{escape(a)}</td><td>{escape(b)}</td></tr>' for a, b in BACKTEST)}</table>
<p class=muted>{escape(BACKTEST_WEEKS)} One week of live trading says little on its own; these ranges show what a normal week looked like in the backtest.</p>
"""
    out.mkdir(exist_ok=True)
    (out / "review.html").write_text((HERE / "review_template.html").read_text().replace("__BODY__", body))
