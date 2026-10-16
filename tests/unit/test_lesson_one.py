from dataclasses import replace
from math import exp
from pathlib import Path

import pytest

from quant_lab.research.lesson_one import build_lesson, experiment_bars, simulate


def test_compounding_and_log_identity():
    lesson = build_lesson(Path(__file__).resolve().parents[2])
    example = lesson["examples"][0]
    assert example["sumSimple"] == pytest.approx(0)
    assert example["compounded"] == pytest.approx(-0.01)
    assert exp(example["sumLog"]) - 1 == pytest.approx(example["compounded"])
    assert lesson["bars"][0]["simple"] is None
    assert lesson["bars"][0]["end"] == "2026-01-02T15:30:00+00:00"


def test_future_prices_cannot_change_earlier_causal_orders():
    bars = experiment_bars()
    changed = bars[:5] + tuple(replace(b, open=200, high=202, low=198, close=201) for b in bars[5:])
    original = simulate(bars, mode="causal", cost_bps=10)["rows"]
    perturbed = simulate(changed, mode="causal", cost_bps=10)["rows"]
    assert original[:5] == perturbed[:5]
    assert original[5]["action"] == perturbed[5]["action"]
    assert all(r["action"] == "Hold" for r in original[:3])


def test_current_close_does_not_change_causal_order_but_changes_biased_order():
    bars = experiment_bars()
    changed = bars[:3] + (replace(bars[3], high=120, close=119),) + bars[4:]
    for mode, equal in [("causal", True), ("biased", False)]:
        a = simulate(bars, mode=mode, cost_bps=0)["rows"][3]["action"]
        b = simulate(changed, mode=mode, cost_bps=0)["rows"][3]["action"]
        assert (a == b) == equal


def test_buy_hold_fee_and_adverse_fill_are_hand_checkable():
    bar = experiment_bars()[0]
    result = simulate((bar,), mode="benchmark", cost_bps=10)
    shares = 1000 / (100 * 1.0005 * 1.0005)
    assert result["finalEquity"] == pytest.approx(shares * 100)
    assert result["totalCost"] == pytest.approx(1000 - shares * 100)
    assert result["maxDrawdown"] == pytest.approx(1 - shares * 100 / 1000)


def test_costs_reduce_equity_and_ledger_reconciles():
    for mode in ("causal", "biased", "benchmark"):
        free = simulate(experiment_bars(), mode=mode, cost_bps=0)
        paid = simulate(experiment_bars(), mode=mode, cost_bps=30)
        assert paid["finalEquity"] < free["finalEquity"]
        assert paid["totalCost"] == pytest.approx(sum(r["cost"] for r in paid["rows"]))
        for row in paid["rows"]:
            assert row["equity"] == pytest.approx(row["cash"] + row["shares"] * row["close"])


@pytest.mark.parametrize("cost", [-1, float("nan"), float("inf"), 101])
def test_invalid_costs_rejected(cost):
    with pytest.raises(ValueError):
        simulate(experiment_bars(), mode="causal", cost_bps=cost)


def test_overlapping_intervals_rejected():
    bars = experiment_bars()
    with pytest.raises(ValueError, match="overlap"):
        simulate((replace(bars[0], duration_seconds=7200), bars[1]), mode="causal", cost_bps=0)
