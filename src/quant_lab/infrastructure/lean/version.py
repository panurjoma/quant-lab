"""Immutable identity of the LEAN engine used by Quant Lab."""

from dataclasses import dataclass


@dataclass(frozen=True)
class LeanPin:
    repository: str
    commit: str
    captured_date: str
    license: str

    @property
    def source_url(self) -> str:
        return f"{self.repository}/tree/{self.commit}"


LEAN_PIN = LeanPin(
    repository="https://github.com/QuantConnect/Lean",
    commit="80e7843f645673bcbeaab963049f76f20f6785e1",
    captured_date="2026-10-06",
    license="Apache-2.0",
)
