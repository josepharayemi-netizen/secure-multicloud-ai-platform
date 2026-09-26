import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from .features import Transaction, validate


@dataclass(frozen=True)
class TransactionEvent:
    event_id: str
    occurred_at: str
    transaction: Transaction
    schema_version: str = "1.0"

    def validate(self) -> None:
        validate(self.transaction)
        datetime.fromisoformat(self.occurred_at.replace("Z", "+00:00"))
        if not self.event_id.strip():
            raise ValueError("event_id is required")


def create_event(event_id: str, transaction: Transaction) -> TransactionEvent:
    return TransactionEvent(
        event_id=event_id,
        occurred_at=datetime.now(timezone.utc).isoformat(),
        transaction=transaction,
    )


def write_validated_batch(events: Iterable[TransactionEvent], output: Path) -> dict:
    """Validate, deduplicate and persist an immutable JSONL micro-batch plus lineage manifest."""
    records: dict[str, dict] = {}
    for event in events:
        event.validate()
        records[event.event_id] = asdict(event)

    output.parent.mkdir(parents=True, exist_ok=True)
    payload = "".join(json.dumps(records[key], sort_keys=True) + "\n" for key in sorted(records))
    output.write_text(payload, encoding="utf-8")
    return {
        "schema_version": "1.0",
        "record_count": len(records),
        "sha256": hashlib.sha256(payload.encode()).hexdigest(),
        "output": str(output),
    }
