"""Integration tests for Trade Safety Analysis service."""

from __future__ import annotations

import asyncio
import os
import unittest
from decimal import Decimal

from aioia_core.settings import OpenAIAPISettings

from trade_safety.service import TradeSafetyService
from trade_safety.settings import TradeSafetyModelSettings


class TestTradeSafetyAnalysis(unittest.TestCase):
    """
    통합 테스트: Trade Safety Service의 LLM 응답 검증

    이 테스트는 TradeSafetyService가 실제 LLM을 사용하여
    거래 안전성을 분석하고, 올바른 형식의 응답을 반환하는지 검증합니다.

    환경 변수:
        OPENAI_API_KEY: OpenAI API key (필수)
    """

    def setUp(self) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is required for integration tests. "
                "Set it in backend/.envrc or export it before running tests."
            )

        openai_api = OpenAIAPISettings(api_key=api_key)
        model_settings = TradeSafetyModelSettings()

        self.service = TradeSafetyService(openai_api, model_settings)

    def test_analyze_trade_with_price_info(self) -> None:
        """
        가격 정보가 있는 경우 offered_price를 Decimal로 반환해야 함

        시나리오:
        - 거래 글: 한국어로 작성된 포토카드 거래 글
        - 가격: 15,000원
        - 기대 결과: offered_price가 Decimal 타입으로 반환됨
        """
        # Given: 가격 정보가 포함된 거래 글
        input_text = """
        [급처] 르세라핌 카즈하 포카 팝니다
        15,000원에 판매합니다
        직거래 가능, 택배 가능
        연락 주세요!
        """

        # When: 거래 분석 수행
        analysis = asyncio.run(
            self.service.analyze_trade(
                input_text=input_text,
            )
        )

        # Then: 응답 검증
        self.assertIsNotNone(analysis, "분석 결과가 반환되어야 합니다")
        assert analysis is not None  # Type narrowing for mypy
        self.assertIsNotNone(analysis.price_analysis, "가격 분석이 포함되어야 합니다")
        assert analysis.price_analysis is not None  # Type narrowing for mypy

        # PriceAnalysis의 offered_price가 Decimal이어야 함 (가격 정보 제공됨)
        offered_price = analysis.price_analysis.offered_price
        self.assertIsInstance(
            offered_price,
            Decimal,
            f"가격 정보가 있으므로 offered_price는 Decimal이어야 하지만, {type(offered_price)}가 반환되었습니다",
        )

        # 가격 평가가 제공되어야 함
        self.assertIsNotNone(
            analysis.price_analysis.price_assessment,
            "가격 평가(price_assessment)가 제공되어야 합니다",
        )

    def test_analyze_trade_without_price_info(self) -> None:
        """
        가격 정보가 없는 경우 offered_price가 None으로 반환되어야 함

        시나리오:
        - 거래 글: 가격 미기재 포토카드 거래 글
        - 기대 결과: offered_price가 None으로 반환됨
        """
        # Given: 가격 정보가 없는 거래 글
        input_text = """
        NCT 재현 포카 양도합니다
        DM으로 가격 문의 주세요
        """

        # When: 거래 분석 수행
        analysis = asyncio.run(
            self.service.analyze_trade(
                input_text=input_text,
            )
        )

        # Then: 응답 검증
        self.assertIsNotNone(analysis, "분석 결과가 반환되어야 합니다")
        assert analysis is not None  # Type narrowing for mypy
        self.assertIsNotNone(analysis.price_analysis, "가격 분석이 포함되어야 합니다")
        assert analysis.price_analysis is not None  # Type narrowing for mypy

        # offered_price가 None이어야 함
        self.assertIsNone(
            analysis.price_analysis.offered_price,
            "가격 정보가 없으면 offered_price는 None이어야 합니다",
        )

    def test_analyze_trade_with_scam_signals(self) -> None:
        """
        사기 신호가 있는 거래 글을 분석하여 위험 신호를 감지해야 함

        시나리오:
        - 거래 글: 의심스러운 요소가 포함된 거래 글
        - 기대 결과: risk_signals에 위험 신호가 포함됨
        """
        # Given: 사기 신호가 있는 거래 글
        input_text = """
        [급처] BTS 포카 5천원에 팝니다!
        선입금만 받습니다. 계좌이체 필수
        빨리 연락주세요 몇 개 안남았어요
        """

        # When: 거래 분석 수행
        analysis = asyncio.run(
            self.service.analyze_trade(
                input_text=input_text,
            )
        )

        # Then: 위험 신호 또는 주의사항이 감지되어야 함
        self.assertIsNotNone(analysis, "분석 결과가 반환되어야 합니다")

        total_warnings = len(analysis.risk_signals) + len(analysis.cautions)
        self.assertGreater(
            total_warnings,
            0,
            "사기 신호가 있는 거래 글에서는 위험 신호 또는 주의사항이 감지되어야 합니다",
        )

        # Risk score가 설정되어야 함
        self.assertIsNotNone(analysis.risk_score, "위험 점수가 설정되어야 합니다")
        self.assertGreaterEqual(
            analysis.risk_score, 0, "위험 점수는 0 이상이어야 합니다"
        )
        self.assertLessEqual(
            analysis.risk_score, 100, "위험 점수는 100 이하여야 합니다"
        )

    def test_analyze_trade_returns_safety_checklist(self) -> None:
        """
        모든 거래 분석에 안전 체크리스트가 포함되어야 함

        시나리오:
        - 거래 글: 일반적인 거래 글
        - 기대 결과: safety_checklist에 항목이 포함됨
        """
        # Given: 일반 거래 글
        input_text = """
        에스파 카리나 포카 판매합니다
        가격: 20,000원
        안전거래 원합니다
        """

        # When: 거래 분석 수행
        analysis = asyncio.run(
            self.service.analyze_trade(
                input_text=input_text,
            )
        )

        # Then: 안전 체크리스트가 제공되어야 함
        self.assertIsNotNone(analysis, "분석 결과가 반환되어야 합니다")
        self.assertIsNotNone(
            analysis.safety_checklist, "안전 체크리스트가 포함되어야 합니다"
        )
        self.assertGreater(
            len(analysis.safety_checklist),
            0,
            "안전 체크리스트에 최소 1개 이상의 항목이 있어야 합니다",
        )

    def test_analyze_trade_handles_korean_slang(self) -> None:
        """
        한국어 은어/슬랭이 포함된 거래 글을 분석하여 번역과 설명을 제공해야 함

        시나리오:
        - 거래 글: 한국어 은어가 포함된 거래 글
        - 기대 결과: translation과 nuance_explanation이 제공됨
        """
        # Given: 한국어 은어가 포함된 거래 글
        input_text = """
        [급처분] 스키즈 필릭스 포카 무탈
        공구 실패로 급처합니다
        """

        # When: 거래 분석 수행
        analysis = asyncio.run(
            self.service.analyze_trade(
                input_text=input_text,
            )
        )

        # Then: 번역 또는 뉘앙스 설명이 제공되어야 함
        self.assertIsNotNone(analysis, "분석 결과가 반환되어야 합니다")

        # translation 또는 nuance_explanation 중 하나는 제공되어야 함
        has_translation = (
            analysis.translation is not None and len(analysis.translation.strip()) > 0
        )
        has_nuance = (
            analysis.nuance_explanation is not None
            and len(analysis.nuance_explanation.strip()) > 0
        )

        self.assertTrue(
            has_translation or has_nuance,
            "한국어 은어가 포함된 경우 번역 또는 뉘앙스 설명이 제공되어야 합니다",
        )

    def test_analyze_trade_with_krw_price_returns_currency_code(self) -> None:
        """
        한국 원화(KRW) 가격이 있는 경우 currency 필드에 'KRW'가 반환되어야 함

        시나리오:
        - 거래 글: 한국 원화로 가격이 표시된 거래 글
        - 기대 결과: price_analysis.currency가 'KRW'로 반환됨
        """
        # Given: 한국 원화로 가격이 표시된 거래 글
        input_text = """
        [판매] 뉴진스 하니 포카 팝니다
        가격: 15,000원
        안전거래 원합니다
        """

        # When: 거래 분석 수행
        analysis = asyncio.run(
            self.service.analyze_trade(
                input_text=input_text,
            )
        )

        # Then: 응답 검증
        self.assertIsNotNone(analysis, "분석 결과가 반환되어야 합니다")
        assert analysis is not None  # Type narrowing for mypy
        self.assertIsNotNone(analysis.price_analysis, "가격 분석이 포함되어야 합니다")
        assert analysis.price_analysis is not None  # Type narrowing for mypy

        # currency 필드가 'KRW'이어야 함
        self.assertEqual(
            analysis.price_analysis.currency,
            "KRW",
            "한국 원화 가격의 경우 currency는 'KRW'이어야 합니다",
        )

        # offered_price도 함께 검증
        self.assertIsNotNone(
            analysis.price_analysis.offered_price,
            "가격 정보가 제공되었으므로 offered_price가 있어야 합니다",
        )

    def test_analyze_trade_with_usd_price_returns_currency_code(self) -> None:
        """
        미국 달러(USD) 가격이 있는 경우 currency 필드에 'USD'가 반환되어야 함

        시나리오:
        - 거래 글: 미국 달러로 가격이 표시된 거래 글
        - 기대 결과: price_analysis.currency가 'USD'로 반환됨
        """
        # Given: 미국 달러로 가격이 표시된 거래 글
        input_text = """
        [WTS] NewJeans Hanni photocard
        Price: $25 USD
        Safe payment only
        """

        # When: 거래 분석 수행
        analysis = asyncio.run(
            self.service.analyze_trade(
                input_text=input_text,
            )
        )

        # Then: 응답 검증
        self.assertIsNotNone(analysis, "분석 결과가 반환되어야 합니다")
        assert analysis is not None  # Type narrowing for mypy
        self.assertIsNotNone(analysis.price_analysis, "가격 분석이 포함되어야 합니다")
        assert analysis.price_analysis is not None  # Type narrowing for mypy

        # currency 필드가 'USD'이어야 함
        self.assertEqual(
            analysis.price_analysis.currency,
            "USD",
            "미국 달러 가격의 경우 currency는 'USD'이어야 합니다",
        )

        # offered_price도 함께 검증
        self.assertIsNotNone(
            analysis.price_analysis.offered_price,
            "가격 정보가 제공되었으므로 offered_price가 있어야 합니다",
        )


if __name__ == "__main__":
    unittest.main()
