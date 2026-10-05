from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from math import isfinite
from typing import Iterable


class AssetClass(StrEnum):
    EQUITY = "equity"
    ETF = "etf"
    FX = "fx"
    FUTURE = "future"
    CRYPTO = "crypto"
    OTHER = "other"


@dataclass(frozen=True, slots=True)
class Instrument:
    instrument_id: str
    symbol: str
    asset_class: AssetClass
    currency: str
    venue: str | None = None

    def __post_init__(self) -> None:
        if not self.instrument_id.strip() or not self.symbol.strip():
            raise ValueError("instrument_id and symbol must be non-empty")
        if len(self.currency) != 3:
            raise ValueError("currency must be a three-letter code")


@dataclass(frozen=True, slots=True)
class Bar:
    instrument_id: str
    timestamp: datetime
    duration_seconds: int
    open: float
    high: float
    low: float
    close: float
    volume: float

    def __post_init__(self) -> None:
        if self.timestamp.tzinfo is None or self.timestamp.utcoffset() is None:
            raise ValueError("bar timestamp must be timezone-aware")
        if self.duration_seconds <= 0:
            raise ValueError("bar duration must be positive")
        values = (self.open, self.high, self.low, self.close, self.volume)
        if not all(isfinite(v) for v in values):
            raise ValueError("bar values must be finite")
        if min(self.open, self.high, self.low, self.close) <= 0:
            raise ValueError("prices must be positive")
        if self.volume < 0:
            raise ValueError("volume cannot be negative")
        if self.high < max(self.open, self.close) or self.low > min(self.open, self.close):
            raise ValueError("OHLC values are inconsistent")
        if self.high < self.low:
            raise ValueError("high cannot be below low")


    @property
    def end_timestamp(self) -> datetime:
        """Exclusive end of the interval summarized by this bar."""
        from datetime import timedelta
        return self.timestamp + timedelta(seconds=self.duration_seconds)


def validate_bars(bars: Iterable[Bar]) -> tuple[Bar, ...]:
    result = tuple(bars)
    seen: set[tuple[str, datetime]] = set()
    previous: dict[str, datetime] = {}
    for bar in result:
        key = (bar.instrument_id, bar.timestamp)
        if key in seen:
            raise ValueError(f"duplicate bar: {key}")
        seen.add(key)
        if bar.instrument_id in previous and bar.timestamp <= previous[bar.instrument_id]:
            raise ValueError(f"bars for {bar.instrument_id} must be strictly chronological")
        previous[bar.instrument_id] = bar.timestamp
    return result
