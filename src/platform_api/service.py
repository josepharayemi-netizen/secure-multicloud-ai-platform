from pathlib import Path
import json
import joblib
from .features import Transaction, transform


class RiskService:
    def __init__(self, model_dir: Path = Path("models")):
        if not (model_dir / "risk_model.joblib").exists():
            from .train import train
            train(model_dir)
        self.model = joblib.load(model_dir / "risk_model.joblib")
        self.metadata = json.loads((model_dir / "metadata.json").read_text())

    def predict(self, transaction: Transaction) -> dict:
        probability = float(self.model.predict_proba([transform(transaction)])[0][1])
        threshold = float(self.metadata["decision_threshold"])
        reasons = []
        if transaction.transaction_amount >= 5000:
            reasons.append("HIGH_AMOUNT")
        if transaction.velocity_1h >= 6:
            reasons.append("HIGH_VELOCITY")
        if transaction.account_age_days < 30:
            reasons.append("NEW_ACCOUNT")
        if transaction.country_mismatch:
            reasons.append("COUNTRY_MISMATCH")
        return {
            "model_version": self.metadata["model_version"],
            "risk_probability": round(probability, 4),
            "decision": "REVIEW" if probability >= threshold else "APPROVE",
            "reason_codes": reasons or ["NO_MAJOR_RULE_TRIGGER"],
        }
