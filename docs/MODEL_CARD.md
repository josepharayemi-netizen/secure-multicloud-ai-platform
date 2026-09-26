# Model Card: Transaction Risk Classifier

## Intended use

Demonstrate secure production delivery of a binary risk model. It may support human review in a sandbox but must not be used for real financial decisions.

## Training data

Eight thousand deterministic synthetic records generated from amount, velocity, account age and country-mismatch signals. No personal or customer data is included.

## Limitations

Synthetic performance does not predict production performance. Reason codes are operational indicators, not causal explanations. Real deployment requires representative data, fairness analysis, calibration, privacy review, adversarial testing and human oversight.

## Versioning

The model artifact is paired with version, feature contract, decision threshold, evaluation metrics, training seed and SHA-256 digest.
