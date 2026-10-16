import json
from pathlib import Path

from quant_lab.infrastructure.lean import LEAN_PIN


def test_lean_pin_is_immutable_and_matches_lock_file() -> None:
    root = Path(__file__).parents[2]
    lock = json.loads((root / "integrations/lean/lean.lock.json").read_text())

    assert len(LEAN_PIN.commit) == 40
    assert all(character in "0123456789abcdef" for character in LEAN_PIN.commit)
    assert LEAN_PIN.commit == lock["commit"]
    assert LEAN_PIN.repository == lock["upstream"]
    assert LEAN_PIN.captured_date == lock["captured_date"]
    assert LEAN_PIN.license == lock["license"]
    assert LEAN_PIN.source_url.endswith(LEAN_PIN.commit)
