"""Unit tests for ML classifier integration."""

import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from trade_safety.ml.classifier import TfidfMLPClassifier, decide_safe_score


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
    """Test TfidfMLPClassifier with mocked model files."""

    @patch("trade_safety.ml.classifier.joblib.load")
    @patch("trade_safety.ml.classifier.torch.load")
    @patch("trade_safety.ml.classifier.Path.exists")
    def test_predict_proba_returns_float(self, mock_exists, mock_torch_load, mock_joblib_load):
        """Test that predict_proba returns scam probability as float."""
        # Mock 설정
        mock_exists.return_value = True

        mock_vectorizer = MagicMock()
        mock_vectorizer.transform.return_value = MagicMock()
        mock_joblib_load.return_value = mock_vectorizer

        mock_torch_load.return_value = {
            "in_dim": 100,
            "state_dict": {}
        }

        # Mock MLP model
        with patch("trade_safety.ml.classifier.MLP") as mock_mlp_class:
            mock_model = MagicMock()
            mock_model.return_value = MagicMock()  # Forward pass
            mock_mlp_class.return_value = mock_model

            # 분류기 생성
            classifier = TfidfMLPClassifier(model_dir=Path("/fake/model"))

            # predict_proba는 float를 반환해야 함
            with patch("trade_safety.ml.classifier.torch.sigmoid") as mock_sigmoid:
                mock_sigmoid.return_value.item.return_value = 0.85

                result = classifier.predict_proba("test scam text")

                self.assertIsInstance(result, float)
                self.assertEqual(result, 0.85)

    @patch("trade_safety.ml.classifier.Path.exists")
    def test_load_raises_error_when_vectorizer_missing(self, mock_exists):
        """Test that load() raises FileNotFoundError when vectorizer is missing."""
        # vectorizer.joblib만 없는 경우
        def exists_side_effect(self):
            return "model.pt" in str(self)

        mock_exists.side_effect = exists_side_effect

        classifier = TfidfMLPClassifier(model_dir=Path("/fake/model"))

        with self.assertRaises(FileNotFoundError) as context:
            classifier.load()

        self.assertIn("Vectorizer not found", str(context.exception))

    @patch("trade_safety.ml.classifier.Path.exists")
    def test_load_raises_error_when_model_missing(self, mock_exists):
        """Test that load() raises FileNotFoundError when model.pt is missing."""
        # model.pt만 없는 경우
        def exists_side_effect(self):
            return "vectorizer.joblib" in str(self)

        mock_exists.side_effect = exists_side_effect

        classifier = TfidfMLPClassifier(model_dir=Path("/fake/model"))

        with self.assertRaises(FileNotFoundError) as context:
            classifier.load()

        self.assertIn("Model not found", str(context.exception))

    @patch("trade_safety.ml.classifier.joblib.load")
    @patch("trade_safety.ml.classifier.torch.load")
    @patch("trade_safety.ml.classifier.Path.exists")
    def test_load_only_once(self, mock_exists, mock_torch_load, mock_joblib_load):
        """Test that load() is idempotent (only loads once)."""
        mock_exists.return_value = True
        mock_joblib_load.return_value = MagicMock()
        mock_torch_load.return_value = {"in_dim": 100, "state_dict": {}}

        with patch("trade_safety.ml.classifier.MLP"):
            classifier = TfidfMLPClassifier(model_dir=Path("/fake/model"))

            # 첫 번째 로드
            classifier.load()
            first_call_count = mock_joblib_load.call_count

            # 두 번째 로드 (실제로는 로드하지 않아야 함)
            classifier.load()
            second_call_count = mock_joblib_load.call_count

            # 로드는 한 번만 수행되어야 함
            self.assertEqual(first_call_count, second_call_count)


if __name__ == "__main__":
    unittest.main()
