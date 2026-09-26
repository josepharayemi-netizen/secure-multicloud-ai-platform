from pathlib import Path
from tempfile import TemporaryDirectory
import pytest
from src.platform_api.events import TransactionEvent, write_validated_batch
from src.platform_api.features import Transaction, transform
from src.platform_api.service import RiskService
from src.platform_api.train import train


def risky():
    return Transaction(8500, 9, 3, True)


def test_training_is_reproducible():
    with TemporaryDirectory() as first, TemporaryDirectory() as second:
        a = train(Path(first))
        b = train(Path(second))
        assert a["metrics"] == b["metrics"]
        assert a["sha256"] == b["sha256"]


def test_prediction_contract():
    with TemporaryDirectory() as directory:
        service = RiskService(Path(directory))
        result = service.predict(risky())
        assert result["model_version"] == "2.0.0"
        assert 0 <= result["risk_probability"] <= 1
        assert "COUNTRY_MISMATCH" in result["reason_codes"]


def test_invalid_feature_rejected():
    with pytest.raises(ValueError):
        transform(Transaction(-1, 1, 20, False))


def test_batch_pipeline_is_idempotent(tmp_path):
    transaction = Transaction(100.0, 2, 400, False)
    event = TransactionEvent("event-1", "2026-01-01T00:00:00Z", transaction)
    manifest = write_validated_batch([event, event], tmp_path / "silver" / "batch.jsonl")
    assert manifest["record_count"] == 1
    assert len(manifest["sha256"]) == 64
