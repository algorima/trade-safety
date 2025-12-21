"""TF-IDF + MLP classifier for trade safety analysis."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

try:
    import joblib  # type: ignore
    import torch
    from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore

    from .mlp import MLP
except ImportError:
    # Dependencies not installed - will raise error on load()
    joblib = None  # type: ignore
    torch = None  # type: ignore
    TfidfVectorizer = None  # type: ignore
    MLP = None  # type: ignore


@dataclass
class TfidfMLPClassifier:
    """TF-IDF + PyTorch MLP classifier (Lazy loading + Fail-fast).

    This classifier loads model files (vectorizer.joblib, model.pt) on first
    prediction. If files are missing or corrupted, it raises FileNotFoundError
    immediately (Fail-fast principle for library usage).
    """

    model_dir: Path  # Directory containing vectorizer.joblib, model.pt
    device: str = "cpu"

    _vectorizer: TfidfVectorizer | None = field(default=None, init=False, repr=False)
    _model: MLP | None = field(default=None, init=False, repr=False)

    def load(self) -> None:
        """Load model files (Fail-fast: raises exception on error).

        Raises:
            FileNotFoundError: If vectorizer.joblib or model.pt is missing
            RuntimeError: If required dependencies are not installed
        """
        # TODO: Implement in Phase 2
        raise NotImplementedError("Phase 1 skeleton - implement in Phase 2")

    def predict_proba(self, text: str) -> float:
        """Predict scam probability for given text.

        Args:
            text: Input text to analyze

        Returns:
            float: Scam probability (0.0~1.0, higher = more likely scam)
        """
        # TODO: Implement in Phase 2
        raise NotImplementedError("Phase 1 skeleton - implement in Phase 2")


def decide_safe_score(
    ml_scam_prob: float,
    llm_safe_score: int,
    threshold_high: float,
    threshold_low: float,
) -> int:
    """Conditional ensemble logic based on ML confidence.

    - ML high confidence (scam_prob >= threshold_high): Use ML only
    - ML high confidence (scam_prob <= threshold_low): Use ML only
    - ML uncertain (middle range): Average with LLM

    Args:
        ml_scam_prob: ML scam probability (0.0~1.0)
        llm_safe_score: LLM safe score (0~100)
        threshold_high: High confidence threshold (e.g., 0.85)
        threshold_low: Low confidence threshold (e.g., 0.20)

    Returns:
        int: Final safe score (0~100, higher is safer)
    """
    # TODO: Implement in Phase 2
    raise NotImplementedError("Phase 1 skeleton - implement in Phase 2")
