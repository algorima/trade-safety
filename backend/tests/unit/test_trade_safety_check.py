"""Unit tests for trade safety check models."""

import unittest
from decimal import Decimal

from pydantic import ValidationError

from trade_safety.schemas import PriceAnalysis


class TestPriceAnalysis(unittest.TestCase):
    """Test PriceAnalysis model, especially offered_price validation."""

    def test_offered_price_with_valid_decimal(self):
        """Test that valid decimal values are accepted."""
        price_analysis = PriceAnalysis(
            market_price_range="$10-15 USD",
            offered_price=Decimal("12.50"),
            currency=None,
            price_assessment="Fair price",
            warnings=[],
        )
        self.assertEqual(price_analysis.offered_price, Decimal("12.50"))

    def test_offered_price_with_none(self):
        """Test that None is accepted for offered_price."""
        price_analysis = PriceAnalysis(
            market_price_range="$10-15 USD",
            offered_price=None,
            currency=None,
            price_assessment="Price not provided",
            warnings=[],
        )
        self.assertIsNone(price_analysis.offered_price)

    def test_offered_price_with_na_string(self):
        """Test that 'N/A' string is converted to None."""
        price_analysis = PriceAnalysis(
            market_price_range="$10-15 USD",
            offered_price="N/A",  # type: ignore[arg-type]
            currency=None,
            price_assessment="Price not available",
            warnings=[],
        )
        self.assertIsNone(price_analysis.offered_price)

    def test_offered_price_with_lowercase_na(self):
        """Test that 'n/a' (lowercase) is converted to None."""
        price_analysis = PriceAnalysis(
            market_price_range="$10-15 USD",
            offered_price="n/a",  # type: ignore[arg-type]
            currency=None,
            price_assessment="Price not available",
            warnings=[],
        )
        self.assertIsNone(price_analysis.offered_price)

    def test_offered_price_with_empty_string(self):
        """Test that empty string is converted to None."""
        price_analysis = PriceAnalysis(
            market_price_range="$10-15 USD",
            offered_price="",  # type: ignore[arg-type]
            currency=None,
            price_assessment="Price not provided",
            warnings=[],
        )
        self.assertIsNone(price_analysis.offered_price)

    def test_offered_price_with_whitespace_na(self):
        """Test that ' N/A ' (with whitespace) is converted to None."""
        price_analysis = PriceAnalysis(
            market_price_range="$10-15 USD",
            offered_price=" N/A ",  # type: ignore[arg-type]
            currency=None,
            price_assessment="Price not available",
            warnings=[],
        )
        self.assertIsNone(price_analysis.offered_price)

    def test_offered_price_with_numeric_string(self):
        """Test that numeric string is converted to Decimal."""
        price_analysis = PriceAnalysis(
            market_price_range="$10-15 USD",
            offered_price="15.99",  # type: ignore[arg-type]
            currency=None,
            price_assessment="Fair price",
            warnings=[],
        )
        self.assertEqual(price_analysis.offered_price, Decimal("15.99"))

    def test_offered_price_with_integer(self):
        """Test that integer is converted to Decimal."""
        price_analysis = PriceAnalysis(
            market_price_range="$10-15 USD",
            offered_price=20,  # type: ignore[arg-type]
            currency=None,
            price_assessment="Fair price",
            warnings=[],
        )
        self.assertEqual(price_analysis.offered_price, Decimal("20"))

    def test_offered_price_with_float(self):
        """Test that float is converted to Decimal."""
        price_analysis = PriceAnalysis(
            market_price_range="$10-15 USD",
            offered_price=12.5,  # type: ignore[arg-type]
            currency=None,
            price_assessment="Fair price",
            warnings=[],
        )
        self.assertEqual(price_analysis.offered_price, Decimal("12.5"))

    def test_offered_price_with_invalid_string(self):
        """Test that invalid string raises ValidationError."""
        with self.assertRaises(ValidationError) as context:
            PriceAnalysis(
                market_price_range="$10-15 USD",
                offered_price="invalid",  # type: ignore[arg-type]
                currency=None,
                price_assessment="Fair price",
                warnings=[],
            )

        error = context.exception
        self.assertEqual(len(error.errors()), 1)
        self.assertEqual(error.errors()[0]["type"], "decimal_parsing")
        self.assertEqual(error.errors()[0]["loc"], ("offered_price",))


if __name__ == "__main__":
    unittest.main()
