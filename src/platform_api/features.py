from dataclasses import asdict, dataclass
import math


@dataclass(frozen=True)
class Transaction:
    transaction_amount: float
    velocity_1h: int
    account_age_days: int
    country_mismatch: bool


FEATURE_NAMES = ["log_amount", "velocity_1h", "new_account", "country_mismatch"]


def validate(transaction: Transaction) -> None:
    if transaction.transaction_amount <= 0 or transaction.transaction_amount > 10_000_000:
        raise ValueError("transaction_amount must be between 0 and 10,000,000")
    if not 0 <= transaction.velocity_1h <= 1000:
        raise ValueError("velocity_1h must be between 0 and 1000")
    if not 0 <= transaction.account_age_days <= 36500:
        raise ValueError("account_age_days must be between 0 and 36500")


def transform(transaction: Transaction) -> list[float]:
    validate(transaction)
    return [
        math.log1p(transaction.transaction_amount),
        float(transaction.velocity_1h),
        float(transaction.account_age_days < 30),
        float(transaction.country_mismatch),
    ]


def lineage(transaction: Transaction) -> dict:
    return {"source": asdict(transaction), "features": dict(zip(FEATURE_NAMES, transform(transaction)))}
