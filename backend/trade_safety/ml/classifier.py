"""TF-IDF + MLP classifier for trade safety analysis."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import joblib
import torch
from sklearn.feature_extraction.text import TfidfVectorizer


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
    _model: torch.nn.Module | None = field(default=None, init=False, repr=False)

    def load(self) -> None:
        """Load model files (Fail-fast: raises exception on error).

        Raises:
            FileNotFoundError: If vectorizer.joblib or model.pt is missing
        """
        if self._model is not None:
            return  # Already loaded

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

        # Create 2-layer MLP and load weights
        in_dim = payload["in_dim"]
        hidden = payload.get("hidden", 256)
        self._model = torch.nn.Sequential(
            torch.nn.Linear(in_dim, hidden),
            torch.nn.ReLU(),
            torch.nn.Dropout(0.2),
            torch.nn.Linear(hidden, 1),
        )
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

        # Get model prediction (Sequential returns (batch, 1), squeeze to (batch,))
        logit = self._model(x).squeeze(-1)
        prob = torch.sigmoid(logit).item()
        return float(prob)
