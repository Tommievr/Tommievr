# Trading Bot — Main Focus

> FOCUS: Follow One Course Until Successful.

**Goal:** a working bot that generates a small, steady cash flow and compounds on its own. Not a millionaire in a year, just a solid, reliable process.

## Principles
- **Survive first, profit second.** Risk management matters more than the strategy.
- Risk at most 1% of capital per trade; set a daily and a maximum-drawdown stop.
- Never go live without proof: backtest, then paper trade, then tiny live size.
- Log every trade and decision so the bot can be improved with data.
- Never commit API keys. Use a `.env` file (git-ignored).

## Roadmap
1. **Backtest:** pick one simple strategy (e.g. trend following or mean reversion), test on historical data including fees and slippage.
2. **Paper trade:** run it live with fake money for at least 4-8 weeks.
3. **Go live small:** money you can afford to lose, minimal size.
4. **Monitor and improve:** review weekly, change one thing at a time.
5. **Scale slowly:** only add capital after consistent results over months.
6. **Reinvest:** compound profits by rule, not by feeling.

## Suggested structure
```
trading-bot/
  data/        historical data (git-ignored if large)
  strategies/  one file per strategy
  backtest/    backtesting scripts and results
  bot/         live execution, risk manager, logging
  journal.md   weekly review notes
```

## Reality check
Most retail bots lose money after fees. Treat any edge as unproven until it survives out-of-sample tests and paper trading.
