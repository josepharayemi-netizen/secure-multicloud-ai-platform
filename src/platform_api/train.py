from pathlib import Path
import hashlib
import json
import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split

MODEL_DIR = Path("models")


def dataset(rows: int = 8000, seed: int = 42):
    rng = np.random.default_rng(seed)
    log_amount = rng.normal(6.5, 1.6, rows)
    velocity = rng.poisson(2.4, rows)
    new_account = rng.binomial(1, 0.18, rows)
    mismatch = rng.binomial(1, 0.10, rows)
    x = np.column_stack([log_amount, velocity, new_account, mismatch])
    logit = -8.4 + 0.62 * log_amount + 0.38 * velocity + 1.1 * new_account + 2.0 * mismatch
    probability = 1 / (1 + np.exp(-logit))
    y = rng.binomial(1, probability)
    return x, y


def train(output_dir: Path = MODEL_DIR) -> dict:
    x, y = dataset()
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=42, stratify=y
    )
    model = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)
    model.fit(x_train, y_train)
    probability = model.predict_proba(x_test)[:, 1]
    prediction = (probability >= 0.70).astype(int)
    metrics = {
        "roc_auc": round(float(roc_auc_score(y_test, probability)), 4),
        "precision_at_070": round(float(precision_score(y_test, prediction)), 4),
        "recall_at_070": round(float(recall_score(y_test, prediction)), 4),
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    model_path = output_dir / "risk_model.joblib"
    joblib.dump(model, model_path)
    digest = hashlib.sha256(model_path.read_bytes()).hexdigest()
    metadata = {
        "model_name": "transaction-risk-classifier",
        "model_version": "2.0.0",
        "decision_threshold": 0.70,
        "features": ["log_amount", "velocity_1h", "new_account", "country_mismatch"],
        "metrics": metrics,
        "sha256": digest,
        "training_seed": 42,
    }
    (output_dir / "metadata.json").write_text(json.dumps(metadata, indent=2))
    print(json.dumps(metadata, indent=2))
    return metadata


if __name__ == "__main__":
    train()
