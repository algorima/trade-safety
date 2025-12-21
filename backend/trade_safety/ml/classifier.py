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
        if self._model is not None:
            return  # Already loaded

        if joblib is None or torch is None:
            raise RuntimeError(
                "ML dependencies not installed. "
                "Install torch and scikit-learn to use ML classifier."
            )

        vec_path = self.model_dir / "vectorizer.joblib"
        model_path = self.model_dir / "model.pt"

        # Fail-fast: File existence check
        if not vec_path.exists():
            raise FileNotFoundError(f"Vectorizer not found: {vec_path}")
        if not model_path.exists():
            raise FileNotFoundError(f"Model not found: {model_path}")

        # Load vectorizer and model
        self._vectorizer = joblib.load(vec_path)
        payload = torch.load(model_path, map_location="cpu")
        self._model = MLP(in_dim=payload["in_dim"])
        self._model.load_state_dict(payload["state_dict"])
        self._model.to(self.device)
        self._model.eval()

    @torch.inference_mode()
    def predict_proba(self, text: str) -> float:
        """Predict scam probability for given text.

        Args:
            text: Input text to analyze

        Returns:
            float: Scam probability (0.0~1.0, higher = more likely scam)
        """
        self.load()
        assert self._model is not None and self._vectorizer is not None

        # Transform text to TF-IDF features
        X = self._vectorizer.transform([text])
        x = torch.from_numpy(X.toarray()).float().to(self.device)

        # Get model prediction
        logit = self._model(x)
        prob = torch.sigmoid(logit).item()
        return float(prob)


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
    ml_safe_score = 100 - int(ml_scam_prob * 100)

    # ML is confident it's a scam
    if ml_scam_prob >= threshold_high:
        return ml_safe_score

    # ML is confident it's legit
    if ml_scam_prob <= threshold_low:
        return ml_safe_score

    # ML is uncertain → Average with LLM
    return int((llm_safe_score + ml_safe_score) / 2)
