from datetime import datetime, timezone

import pytest

from quant_lab.domain import AssetClass, Bar, Instrument, validate_bars


def bar(hour: int, **overrides) -> Bar:
    values = dict(instrument_id="AAPL.XNAS", timestamp=datetime(2026, 1, 2, hour, tzinfo=timezone.utc),
                  open=100.0, high=102.0, low=99.0, close=101.0, volume=1000.0)
    values.update(overrides)
    return Bar(**values)


def test_instrument_requires_canonical_identity() -> None:
    instrument = Instrument("AAPL.XNAS", "AAPL", AssetClass.EQUITY, "USD", "XNAS")
    assert instrument.instrument_id == "AAPL.XNAS"


def test_bar_requires_timezone() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        bar(10, timestamp=datetime(2026, 1, 2, 10))


def test_bar_rejects_inconsistent_ohlc() -> None:
    with pytest.raises(ValueError, match="inconsistent"):
        bar(10, high=100.5, close=101.0)


def test_bar_rejects_negative_volume() -> None:
    with pytest.raises(ValueError, match="volume"):
        bar(10, volume=-1)


def test_series_rejects_duplicates() -> None:
    b = bar(10)
    with pytest.raises(ValueError, match="duplicate"):
        validate_bars([b, b])


def test_series_rejects_out_of_order_bars() -> None:
    with pytest.raises(ValueError, match="chronological"):
        validate_bars([bar(11), bar(10)])
