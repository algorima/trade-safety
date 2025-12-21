"""Unit tests for ML classifier integration."""

import shutil
import tempfile
import unittest
from pathlib import Path

import joblib
import torch
from sklearn.feature_extraction.text import TfidfVectorizer

from trade_safety.ml.classifier import TfidfMLPClassifier
from trade_safety.ml.ensemble import decide_safe_score


class TestDecideSafeScore(unittest.TestCase):
    """Test ensemble logic for combining ML and LLM scores."""

    def test_ml_high_confidence_scam(self):
        """Test that high ML scam probability (≥0.85) uses ML score only."""
        ml_scam_prob = 0.90  # High confidence: scam
        llm_safe_score = 70  # LLM thinks it's somewhat safe
        threshold_high = 0.85
        threshold_low = 0.20

        result = decide_safe_score(
            ml_scam_prob, llm_safe_score, threshold_high, threshold_low
        )

        # ML확신: safe_score = 100 - 90 = 10
        self.assertEqual(result, 10)

    def test_ml_high_confidence_legit(self):
        """Test that low ML scam probability (≤0.20) uses ML score only."""
        ml_scam_prob = 0.15  # High confidence: legit
        llm_safe_score = 40  # LLM thinks it's risky
        threshold_high = 0.85
        threshold_low = 0.20

        result = decide_safe_score(
            ml_scam_prob, llm_safe_score, threshold_high, threshold_low
        )

        # ML 확신: safe_score = 100 - 15 = 85
        self.assertEqual(result, 85)

    def test_ml_uncertain_averages_with_llm(self):
        """Test that uncertain ML prediction averages with LLM score."""
        ml_scam_prob = 0.50  # Uncertain (middle range)
        llm_safe_score = 60  # LLM's assessment
        threshold_high = 0.85
        threshold_low = 0.20

        result = decide_safe_score(
            ml_scam_prob, llm_safe_score, threshold_high, threshold_low
        )

        # ML 불확실: (60 + 50) / 2 = 55
        ml_safe_score = 100 - int(0.50 * 100)  # = 50
        expected = int((llm_safe_score + ml_safe_score) / 2)
        self.assertEqual(result, expected)

    def test_ml_at_high_threshold_boundary(self):
        """Test boundary case: ML scam probability exactly at high threshold."""
        ml_scam_prob = 0.85  # Exactly at threshold
        llm_safe_score = 50
        threshold_high = 0.85
        threshold_low = 0.20

        result = decide_safe_score(
            ml_scam_prob, llm_safe_score, threshold_high, threshold_low
        )

        # ≥ threshold_high이므로 ML만 사용
        self.assertEqual(result, 15)

    def test_ml_at_low_threshold_boundary(self):
        """Test boundary case: ML scam probability exactly at low threshold."""
        ml_scam_prob = 0.20  # Exactly at threshold
        llm_safe_score = 50
        threshold_high = 0.85
        threshold_low = 0.20

        result = decide_safe_score(
            ml_scam_prob, llm_safe_score, threshold_high, threshold_low
        )

        # ≤ threshold_low이므로 ML만 사용
        self.assertEqual(result, 80)


class TestTfidfMLPClassifier(unittest.TestCase):
    """Test TfidfMLPClassifier with minimal real model."""

    def setUp(self):
        """Create minimal model files for testing."""
        # Create temporary directory
        self.temp_dir = Path(tempfile.mkdtemp())

        # Create minimal TF-IDF vectorizer
        corpus = [
            "buy cheap product",
            "scam fraud fake",
            "safe genuine authentic",
            "urgent money transfer",
        ]
        self.vectorizer = TfidfVectorizer(max_features=20)
        self.vectorizer.fit(corpus)

        # Save vectorizer
        vec_path = self.temp_dir / "vectorizer.joblib"
        joblib.dump(self.vectorizer, vec_path)

        # Create minimal MLP model using public factory method
        in_dim = len(self.vectorizer.get_feature_names_out())
        hidden_dim = 8
        torch.manual_seed(42)
        self.model = TfidfMLPClassifier.create_mlp(in_dim, hidden_dim)

        # Initialize with small random weights for reproducibility
        for param in self.model.parameters():
            param.data = torch.randn_like(param.data) * 0.01

        # Save model with hidden dimension
        model_path = self.temp_dir / "model.pt"
        torch.save(
            {
                "in_dim": in_dim,
                "hidden": hidden_dim,
                "state_dict": self.model.state_dict(),
            },
            model_path,
        )

    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.temp_dir)

    def test_predict_proba_returns_float(self):
        """Test that predict_proba returns scam probability as float."""
        classifier = TfidfMLPClassifier(model_dir=self.temp_dir)

        result = classifier.predict_proba("urgent money transfer scam")

        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)

    def test_predict_proba_consistent_results(self):
        """Test that predict_proba returns consistent results for same input."""
        classifier = TfidfMLPClassifier(model_dir=self.temp_dir)

        result1 = classifier.predict_proba("scam fraud")
        result2 = classifier.predict_proba("scam fraud")

        self.assertEqual(result1, result2)

    def test_load_raises_error_when_vectorizer_missing(self):
        """Test that load() raises FileNotFoundError when vectorizer is missing."""
        # Remove vectorizer file
        vec_path = self.temp_dir / "vectorizer.joblib"
        vec_path.unlink()

        classifier = TfidfMLPClassifier(model_dir=self.temp_dir)

        with self.assertRaises(FileNotFoundError) as context:
            classifier.load()

        self.assertIn("Vectorizer not found", str(context.exception))

    def test_load_raises_error_when_model_missing(self):
        """Test that load() raises FileNotFoundError when model.pt is missing."""
        # Remove model file
        model_path = self.temp_dir / "model.pt"
        model_path.unlink()

        classifier = TfidfMLPClassifier(model_dir=self.temp_dir)

        with self.assertRaises(FileNotFoundError) as context:
            classifier.load()

        self.assertIn("Model not found", str(context.exception))

    def test_load_only_once(self):
        """Test that load() is idempotent (only loads once)."""
        classifier = TfidfMLPClassifier(model_dir=self.temp_dir)

        # First load
        classifier.load()
        first_model = classifier._model

        # Second load (should not reload)
        classifier.load()
        second_model = classifier._model

        # Same model instance
        self.assertIs(first_model, second_model)

    def test_multiple_predictions(self):
        """Test that classifier can handle multiple predictions."""
        classifier = TfidfMLPClassifier(model_dir=self.temp_dir)

        texts = [
            "scam fraud fake",
            "safe genuine product",
            "urgent money transfer",
            "buy cheap",
        ]

        results = [classifier.predict_proba(text) for text in texts]

        # All results should be valid probabilities
        for result in results:
            self.assertIsInstance(result, float)
            self.assertGreaterEqual(result, 0.0)
            self.assertLessEqual(result, 1.0)


if __name__ == "__main__":
    unittest.main()
