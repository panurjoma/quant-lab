from __future__ import annotations

from datetime import datetime
from typing import Protocol

from quant_lab.domain import Bar, Instrument


class HistoricalDataProvider(Protocol):
    """Vendor-neutral historical-data capability.

    Future IBKR and QuantConnect adapters translate vendor objects into these
    canonical Quant Lab models at the infrastructure boundary.
    """

    def get_bars(
        self,
        instrument: Instrument,
        *,
        start: datetime,
        end: datetime,
        timeframe: str,
    ) -> tuple[Bar, ...]: ...
