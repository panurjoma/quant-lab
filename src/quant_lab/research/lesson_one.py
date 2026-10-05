"""Deterministic Lesson 1 calculations and the versioned offline Learn contract.

Run with PYTHONPATH=src: python -m quant_lab.research.lesson_one
The browser presents this generated contract; it contains no trading rules.
"""
from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timedelta, timezone
from math import exp, isfinite
from pathlib import Path

import pandas as pd

from quant_lab.domain import Bar, validate_bars
from quant_lab.research.returns import log_returns, simple_returns


def load_bars(path: Path) -> tuple[Bar, ...]:
    with path.open(encoding="utf-8") as source:
        bars = tuple(Bar(
            instrument_id=row["instrument_id"],
            timestamp=datetime.fromisoformat(row["timestamp"]),
            duration_seconds=int(row["duration_seconds"]),
            **{key: float(row[key]) for key in ("open", "high", "low", "close", "volume")},
        ) for row in csv.DictReader(source))
    return validate_bars(bars)


def experiment_bars() -> tuple[Bar, ...]:
    """Invented consecutive hourly intervals, not an exchange-session model."""
    closes = [100, 103, 106, 102, 98, 101, 105, 109, 104, 100, 103, 107]
    opens = [100, 101, 104, 105, 101, 99, 102, 106, 108, 103, 101, 104]
    start = datetime(2026, 1, 3, tzinfo=timezone.utc)
    return tuple(Bar("DEMO.SYNTH", start + timedelta(hours=i), 3600,
                     float(op), float(max(op, close) + 1), float(min(op, close) - 1),
                     float(close), 1000.0) for i, (op, close) in enumerate(zip(opens, closes)))


def simulate(bars: tuple[Bar, ...], *, mode: str, cost_bps: float, window: int = 3) -> dict:
    """One-asset teaching ledger. Targets are all-cash or all-stock.

    causal: previous completed close > trailing mean of completed closes.
    biased: current close > current open, deliberately uses the future.
    benchmark: buy at first open and hold. Costs split equally into an
    adverse fill adjustment and a fee on traded fill notional. Final shares
    are marked to close, not liquidated. No volume/latency/impact model.
    """
    validate_bars(bars)
    if not bars or len({bar.instrument_id for bar in bars}) != 1:
        raise ValueError("one non-empty instrument series is required")
    if any(a.end_timestamp > b.timestamp for a, b in zip(bars, bars[1:])):
        raise ValueError("bar intervals must not overlap")
    if mode not in {"causal", "biased", "benchmark"}:
        raise ValueError("unknown mode")
    if not isinstance(window, int) or window < 2:
        raise ValueError("window must be an integer of at least two")
    if not isfinite(cost_bps) or not 0 <= cost_bps <= 100:
        raise ValueError("cost_bps must be finite and between 0 and 100")
    fee = slippage = cost_bps / 20000
    cash, shares, peak, max_drawdown, total_cost = 1000.0, 0.0, 1000.0, 0.0, 0.0
    rows, trades = [], 0
    for i, bar in enumerate(bars):
        history = bars[max(0, i - window):i]
        mean = sum(b.close for b in history) / window if len(history) == window else None
        target = (True if mode == "benchmark" else bar.close > bar.open if mode == "biased"
                  else mean is not None and history[-1].close > mean)
        action, fill, cost = "Hold", None, 0.0
        if target and shares == 0:
            fill = bar.open * (1 + slippage)
            shares = cash / (fill * (1 + fee))
            cost = shares * (fill - bar.open) + shares * fill * fee
            cash, action = 0.0, "Buy"
        elif not target and shares > 0:
            fill = bar.open * (1 - slippage)
            cost = shares * (bar.open - fill) + shares * fill * fee
            cash, shares, action = shares * fill * (1 - fee), 0.0, "Sell"
        if action != "Hold":
            trades += 1
        total_cost += cost
        equity = cash + shares * bar.close
        peak = max(peak, equity)
        max_drawdown = max(max_drawdown, 1 - equity / peak)
        rows.append({"step": i + 1, "time": bar.timestamp.strftime("%H:%M"),
                     "open": bar.open, "close": bar.close, "mean": mean,
                     "signalTime": history[-1].end_timestamp.isoformat() if history else None,
                     "action": action, "fill": fill, "cost": cost,
                     "equity": equity, "cash": cash, "shares": shares})
    return {"mode": mode, "costBps": cost_bps, "window": window, "rows": rows,
            "totalReturn": equity / 1000 - 1, "maxDrawdown": max_drawdown,
            "trades": trades, "totalCost": total_cost, "finalEquity": equity}


def build_lesson(root: Path) -> dict:
    bars = load_bars(root / "data/lesson-01/sample_bars.csv")
    prices = pd.Series([bar.close for bar in bars])
    simple, logs = simple_returns(prices), log_returns(prices)
    records = [{"start": b.timestamp.isoformat(), "end": b.end_timestamp.isoformat(),
                "time": b.end_timestamp.strftime("%H:%M"), "open": b.open, "high": b.high,
                "low": b.low, "close": b.close, "volume": b.volume,
                "simple": None if i == 0 else float(simple.iloc[i]),
                "log": None if i == 0 else float(logs.iloc[i])} for i, b in enumerate(bars)]
    examples = []
    for name, values in [("Round trip", [100.0, 110.0, 99.0]),
                         ("Recovery", [100.0, 80.0, 100.0]),
                         ("Steady growth", [100.0, 105.0, 110.25])]:
        series = pd.Series(values)
        returns, log_values = simple_returns(series).iloc[1:], log_returns(series).iloc[1:]
        examples.append({"name": name, "prices": values, "simple": returns.tolist(),
                         "log": log_values.tolist(), "sumSimple": float(returns.sum()),
                         "compounded": float((1 + returns).prod() - 1),
                         "sumLog": float(log_values.sum()), "fromLog": exp(float(log_values.sum())) - 1})
    fixture = experiment_bars()
    return {"schemaVersion": 1, "lessonId": "market-data-returns-v1",
            "provenance": {"source": "Deterministic synthetic fixtures", "timezone": "UTC",
                           "instrument": "QLAB.XNAS", "pricePolicy": "Unadjusted synthetic prices; no corporate actions",
                           "availability": "At interval end; zero publication delay assumed for this lesson"},
            "bars": records, "examples": examples,
            "experiments": [{"costBps": cost, "runs": {mode: simulate(fixture, mode=mode, cost_bps=cost)
                             for mode in ("causal", "biased", "benchmark")}} for cost in (0, 10, 30)]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if the checked-in lesson contract is stale")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[3]
    target = root / "frontend/src/lesson-one.generated.json"
    content = json.dumps(build_lesson(root), indent=2, allow_nan=False) + "\n"
    if args.check:
        if not target.exists() or target.read_text(encoding="utf-8") != content:
            raise SystemExit("Lesson contract is stale. Run python -m quant_lab.research.lesson_one")
    else:
        target.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
