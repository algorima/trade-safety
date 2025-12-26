"""Integration tests for Trade Safety Analysis service."""

from __future__ import annotations

import asyncio
import os
import unittest
from decimal import Decimal

from aioia_core.settings import OpenAIAPISettings

from trade_safety.preview_service import PreviewService
from trade_safety.schemas import Platform
from trade_safety.service import TradeSafetyService
from trade_safety.settings import (
    RedditAPISettings,
    TradeSafetyModelSettings,
    TwitterAPISettings,
)


class TestTradeSafetyAnalysis(unittest.TestCase):
    """
    통합 테스트: Trade Safety Service의 LLM 응답 검증

    이 테스트는 TradeSafetyService가 실제 LLM을 사용하여
    거래 안전성을 분석하고, 올바른 형식의 응답을 반환하는지 검증합니다.

    환경 변수:
        OPENAI_API_KEY: OpenAI API key (필수)
        TWITTER_BEARER_TOKEN: Twitter API Bearer Token (선택, URL 분석용)
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
        twitter_api = TwitterAPISettings()  # Auto-load from environment
        reddit_api = RedditAPISettings()  # Auto-load from environment

        self.service = TradeSafetyService(
            openai_api=openai_api,
            model_settings=model_settings,
            twitter_api=twitter_api,
            reddit_api=reddit_api,
        )

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

        # Safe score가 설정되어야 함
        self.assertIsNotNone(analysis.safe_score, "안전 점수가 설정되어야 합니다")
        self.assertGreaterEqual(
            analysis.safe_score, 0, "안전 점수는 0 이상이어야 합니다"
        )
        self.assertLessEqual(
            analysis.safe_score, 100, "안전 점수는 100 이하여야 합니다"
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

    def test_analyze_trade_with_twitter_url(self) -> None:
        """
        Twitter/X URL을 입력받아 트윗 내용을 추출하고 분석해야 함

        시나리오:
        - 입력: Twitter/X URL (실제 존재하는 트윗)
        - 기대 결과: URL에서 트윗 내용을 추출하여 분석 수행

        Note:
        - 이 테스트는 실제 Twitter API를 호출합니다
        - Twitter API Bearer Token이 필요합니다 (TWITTER_BEARER_TOKEN 환경변수)
        - 네트워크 연결이 필요합니다
        """
        # Given: 실제 Twitter URL
        # 예시: K-pop 관련 티켓/굿즈 양도 트윗
        twitter_url = "https://x.com/mkticket7/status/2000111727493718384"

        # When: Twitter URL로 거래 분석 수행
        try:
            analysis = asyncio.run(
                self.service.analyze_trade(
                    input_text=twitter_url,
                )
            )

            # Then: 분석 결과 검증
            self.assertIsNotNone(analysis, "분석 결과가 반환되어야 합니다")
            assert analysis is not None  # Type narrowing for mypy

            # 기본 필드들이 존재해야 함
            self.assertIsNotNone(analysis.safe_score, "안전 점수가 반환되어야 합니다")
            self.assertGreaterEqual(
                analysis.safe_score, 0, "안전 점수는 0 이상이어야 합니다"
            )
            self.assertLessEqual(
                analysis.safe_score, 100, "안전 점수는 100 이하여야 합니다"
            )

            # 안전 체크리스트가 제공되어야 함
            self.assertIsNotNone(
                analysis.safety_checklist, "안전 체크리스트가 포함되어야 합니다"
            )
            self.assertGreater(
                len(analysis.safety_checklist),
                0,
                "안전 체크리스트에 최소 1개 이상의 항목이 있어야 합니다",
            )

            # 번역 또는 뉘앙스 설명이 제공되어야 함
            has_translation = (
                analysis.translation is not None
                and len(analysis.translation.strip()) > 0
            )
            has_nuance = (
                analysis.nuance_explanation is not None
                and len(analysis.nuance_explanation.strip()) > 0
            )
            self.assertTrue(
                has_translation or has_nuance,
                "Twitter 콘텐츠에 대한 번역 또는 뉘앙스 설명이 제공되어야 합니다",
            )

            print("\n✅ Twitter URL 분석 성공")
            print(f"   Safe Score: {analysis.safe_score}/100")
            print(f"   Risk Signals: {len(analysis.risk_signals)}개")
            print(f"   Cautions: {len(analysis.cautions)}개")
            print(f"   Safe Indicators: {len(analysis.safe_indicators)}개")

        except ValueError as e:
            # Twitter API 접근 불가 또는 네트워크 에러인 경우 테스트 스킵
            if "Twitter Bearer Token" in str(e) or "Failed to fetch tweet" in str(e):
                self.skipTest(f"Twitter API 사용 불가: {e}")
            else:
                raise

    def test_analyze_trade_with_reddit_url(self) -> None:
        """
        Reddit URL을 입력받아 포스트 내용을 추출하고 분석해야 함

        시나리오:
        - 입력: Reddit URL (실제 존재하는 포스트)
        - 기대 결과: URL에서 포스트 내용을 추출하여 분석 수행

        Note:
        - 이 테스트는 실제 Reddit OAuth API를 호출합니다
        - Reddit API 자격 증명이 필요합니다 (REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET 환경변수)
        - 네트워크 연결이 필요합니다
        """
        # Given: 실제 Reddit URL (r/kpopforsale 거래 포스트)
        reddit_url = "https://www.reddit.com/r/kpopforsale/comments/1ptmrbl/wtsusa_selling_my_entire_kpop_album_collection/"

        # When: Reddit URL로 거래 분석 수행
        try:
            analysis = asyncio.run(
                self.service.analyze_trade(
                    input_text=reddit_url,
                )
            )

            # Then: 분석 결과 검증
            self.assertIsNotNone(analysis, "분석 결과가 반환되어야 합니다")
            assert analysis is not None  # Type narrowing for mypy

            # 기본 필드들이 존재해야 함
            self.assertIsNotNone(analysis.safe_score, "안전 점수가 반환되어야 합니다")
            self.assertGreaterEqual(
                analysis.safe_score, 0, "안전 점수는 0 이상이어야 합니다"
            )
            self.assertLessEqual(
                analysis.safe_score, 100, "안전 점수는 100 이하여야 합니다"
            )

            # 안전 체크리스트가 제공되어야 함
            self.assertIsNotNone(
                analysis.safety_checklist, "안전 체크리스트가 포함되어야 합니다"
            )
            self.assertGreater(
                len(analysis.safety_checklist),
                0,
                "안전 체크리스트에 최소 1개 이상의 항목이 있어야 합니다",
            )

            # 번역 또는 뉘앙스 설명이 제공되어야 함
            has_translation = (
                analysis.translation is not None
                and len(analysis.translation.strip()) > 0
            )
            has_nuance = (
                analysis.nuance_explanation is not None
                and len(analysis.nuance_explanation.strip()) > 0
            )
            self.assertTrue(
                has_translation or has_nuance,
                "Reddit 콘텐츠에 대한 번역 또는 뉘앙스 설명이 제공되어야 합니다",
            )

            print("\n✅ Reddit URL 분석 성공")
            print(f"   Safe Score: {analysis.safe_score}/100")
            print(f"   Risk Signals: {len(analysis.risk_signals)}개")
            print(f"   Cautions: {len(analysis.cautions)}개")
            print(f"   Safe Indicators: {len(analysis.safe_indicators)}개")

        except ValueError as e:
            # Reddit API 접근 불가 또는 네트워크 에러인 경우 테스트 스킵
            if "Reddit API credentials" in str(e) or "Failed to fetch" in str(e):
                self.skipTest(f"Reddit API 사용 불가: {e}")
            else:
                raise


class TestOutputLanguageCompliance(unittest.TestCase):
    """
    통합 테스트: LLM이 output_language 파라미터에 맞는 언어로 응답하는지 검증

    이 테스트는 각 지원 언어로 요청했을 때 LLM 응답이
    해당 언어로 출력되는지 Unicode 범위 확인 방식으로 검증합니다.

    환경 변수:
        OPENAI_API_KEY: OpenAI API key (필수)
    """

    def setUp(self) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is required for integration tests."
            )

        openai_api = OpenAIAPISettings(api_key=api_key)
        model_settings = TradeSafetyModelSettings()

        self.service = TradeSafetyService(openai_api, model_settings)

        # 테스트용 거래 글
        self.test_input = """
        [WTS][Canada] Signed Albums (I-dle, Everglow, Cherry Bullet) + OMG Banhana,
        Located in Canada, prices in CAD. Shipping extra. Will ship worldwide,
         only using trackable options. 
        GFriend album in picture is already sold. All inclusions includes PCs.
        Izone Heart*Iz Signed Wonyoung (Mwave - has 3 PCs, don't remember if hey came with the album, 
        see photo) - $90"
        """

    def _detect_language(self, text: str) -> str | None:
        """
        텍스트의 언어를 Unicode 범위로 감지합니다.
        langdetect 대신 Unicode 체크를 사용하여 더 robust하게 동작합니다.
        """
        if not text or len(text.strip()) < 5:
            return None

        sample = text.strip()[:200]

        # 각 언어의 문자 수 카운트 (float: 일본어 한자 가중치 때문)
        counts: dict[str, float] = {
            "ko": 0.0,  # 한글: AC00-D7AF (가-힣), 1100-11FF (자모)
            "ja": 0.0,  # 일본어: 3040-309F (히라가나), 30A0-30FF (가타카나)
            "zh": 0.0,  # 중국어: 4E00-9FFF (CJK 한자)
            "th": 0.0,  # 태국어: 0E00-0E7F
            "vi": 0.0,  # 베트남어: 라틴 + 성조 부호 (1EA0-1EF9)
            "en": 0.0,  # 영어/라틴: 0041-007A
        }

        for char in sample:
            code = ord(char)
            if 0xAC00 <= code <= 0xD7AF or 0x1100 <= code <= 0x11FF:
                counts["ko"] += 1
            elif 0x3040 <= code <= 0x309F or 0x30A0 <= code <= 0x30FF:
                counts["ja"] += 1
            elif 0x4E00 <= code <= 0x9FFF:
                counts["zh"] += 1
                counts["ja"] += 0.5  # 일본어도 한자 사용
            elif 0x0E00 <= code <= 0x0E7F:
                counts["th"] += 1
            elif 0x1EA0 <= code <= 0x1EF9 or 0x0100 <= code <= 0x017F:
                counts["vi"] += 1
            elif 0x0041 <= code <= 0x007A:
                counts["en"] += 1

        # 가장 많은 언어 반환
        if max(counts.values()) == 0:
            # 라틴 문자 기반 언어 (ES, ID, TL 등)는 영어로 분류됨
            return "en"

        detected = max(counts, key=lambda k: counts[k])
        return detected

    def _is_language_match(self, detected: str | None, expected: str) -> bool:
        """
        감지된 언어가 예상 언어와 일치하는지 확인합니다.

        Unicode 기반 감지 결과와 시스템 언어 코드 매핑:
        - 라틴 문자 기반 언어 (EN, ES, ID, TL, VI)는 모두 'en'으로 감지될 수 있음
        """
        if detected is None:
            return False

        mapping = {
            "EN": ["en"],
            "KO": ["ko"],
            "JA": ["ja", "zh"],  # 일본어는 한자도 사용
            "ZH": ["zh"],
            "TH": ["th"],
            "VI": ["vi", "en"],  # 베트남어는 라틴 기반이라 en으로 감지될 수 있음
            "ES": ["en"],  # 라틴 문자 기반
            "ID": ["en"],  # 라틴 문자 기반
            "TL": ["en"],  # 라틴 문자 기반
        }

        expected_codes = mapping.get(expected.upper(), [expected.lower()])
        return detected.lower() in expected_codes

    # 언어 일치 비율 임계값 (80% 이상이면 통과)
    LANGUAGE_MATCH_THRESHOLD = 0.80

    def _get_all_text_fields_to_check(self, analysis) -> list[tuple[str, str | None]]:
        """
        프롬프트 로직에 따라 언어 검증이 필요한 모든 텍스트 필드를 수집합니다.

        프롬프트에서 명시한 검증 대상:
        - translation, nuance_explanation, ai_summary
        - risk_signals의 title, description, what_to_do
        - cautions의 title, description, what_to_do
        - safe_indicators의 title, description, what_to_do
        - price_analysis.price_assessment, price_analysis.warnings
        - safety_checklist
        - recommendation, emotional_support
        """
        fields: list[tuple[str, str | None]] = []

        # 기본 필드들
        fields.append(("recommendation", analysis.recommendation))
        fields.append(("emotional_support", analysis.emotional_support))
        fields.append(("ai_summary", analysis.ai_summary))
        fields.append(("nuance_explanation", analysis.nuance_explanation))

        # risk_signals 내부 필드들
        for i, signal in enumerate(analysis.risk_signals):
            fields.append((f"risk_signals[{i}].title", signal.title))
            fields.append((f"risk_signals[{i}].description", signal.description))
            fields.append((f"risk_signals[{i}].what_to_do", signal.what_to_do))

        # cautions 내부 필드들
        for i, caution in enumerate(analysis.cautions):
            fields.append((f"cautions[{i}].title", caution.title))
            fields.append((f"cautions[{i}].description", caution.description))
            fields.append((f"cautions[{i}].what_to_do", caution.what_to_do))

        # safe_indicators 내부 필드들
        for i, indicator in enumerate(analysis.safe_indicators):
            fields.append((f"safe_indicators[{i}].title", indicator.title))
            fields.append((f"safe_indicators[{i}].description", indicator.description))
            fields.append((f"safe_indicators[{i}].what_to_do", indicator.what_to_do))

        # price_analysis 필드들
        if analysis.price_analysis:
            fields.append(
                (
                    "price_analysis.price_assessment",
                    analysis.price_analysis.price_assessment,
                )
            )
            if analysis.price_analysis.warnings:
                for i, warning in enumerate(analysis.price_analysis.warnings):
                    fields.append((f"price_analysis.warnings[{i}]", warning))

        # safety_checklist
        for i, item in enumerate(analysis.safety_checklist):
            fields.append((f"safety_checklist[{i}]", item))

        return fields

    def _check_language_compliance_ratio(
        self, analysis, expected_lang: str
    ) -> tuple[float, int, int, list[str]]:
        """
        언어 일치 비율을 계산합니다.

        Returns:
            (match_ratio, matched_count, total_count, failed_fields)
        """
        fields_to_check = self._get_all_text_fields_to_check(analysis)
        matched_count = 0
        total_count = 0
        failed_fields = []

        for field_name, field_value in fields_to_check:
            if field_value and len(str(field_value).strip()) > 20:
                total_count += 1
                detected = self._detect_language(str(field_value))
                if self._is_language_match(detected, expected_lang):
                    matched_count += 1
                else:
                    failed_fields.append(f"{field_name}: detected={detected}")

        match_ratio = matched_count / total_count if total_count > 0 else 1.0
        return match_ratio, matched_count, total_count, failed_fields

    def test_output_language_english(self) -> None:
        """
        output_language='EN'으로 요청 시 영어로 응답해야 함

        비율 기반 검증: 80% 이상의 필드가 영어로 작성되면 통과
        """
        # When
        analysis = asyncio.run(
            self.service.analyze_trade(
                input_text=self.test_input,
                output_language="EN",
            )
        )

        # Then: 80% 이상의 필드가 영어로 작성되어야 함
        ratio, matched, total, failed = self._check_language_compliance_ratio(
            analysis, "EN"
        )

        self.assertGreaterEqual(
            ratio,
            self.LANGUAGE_MATCH_THRESHOLD,
            f"영어 응답 비율이 {self.LANGUAGE_MATCH_THRESHOLD*100}% 미만입니다. "
            f"실제: {ratio*100:.1f}% ({matched}/{total})\n"
            f"실패 필드: {failed}",
        )

    def test_output_language_korean(self) -> None:
        """
        output_language='KO'로 요청 시 한국어로 응답해야 함

        비율 기반 검증: 80% 이상의 필드가 한국어로 작성되면 통과
        """
        # When
        analysis = asyncio.run(
            self.service.analyze_trade(
                input_text=self.test_input,
                output_language="KO",
            )
        )

        # Then: 80% 이상의 필드가 한국어로 작성되어야 함
        ratio, matched, total, failed = self._check_language_compliance_ratio(
            analysis, "KO"
        )

        self.assertGreaterEqual(
            ratio,
            self.LANGUAGE_MATCH_THRESHOLD,
            f"한국어 응답 비율이 {self.LANGUAGE_MATCH_THRESHOLD*100}% 미만입니다. "
            f"실제: {ratio*100:.1f}% ({matched}/{total})\n"
            f"실패 필드: {failed}",
        )

    def test_output_language_japanese(self) -> None:
        """
        output_language='JA'로 요청 시 일본어로 응답해야 함

        비율 기반 검증: 80% 이상의 필드가 일본어로 작성되면 통과
        """
        # When
        analysis = asyncio.run(
            self.service.analyze_trade(
                input_text=self.test_input,
                output_language="JA",
            )
        )

        # Then: 80% 이상의 필드가 일본어로 작성되어야 함
        ratio, matched, total, failed = self._check_language_compliance_ratio(
            analysis, "JA"
        )

        self.assertGreaterEqual(
            ratio,
            self.LANGUAGE_MATCH_THRESHOLD,
            f"일본어 응답 비율이 {self.LANGUAGE_MATCH_THRESHOLD*100}% 미만입니다. "
            f"실제: {ratio*100:.1f}% ({matched}/{total})\n"
            f"실패 필드: {failed}",
        )

    def test_output_language_chinese(self) -> None:
        """
        output_language='ZH'로 요청 시 중국어로 응답해야 함

        비율 기반 검증: 80% 이상의 필드가 중국어로 작성되면 통과
        """
        # When
        analysis = asyncio.run(
            self.service.analyze_trade(
                input_text=self.test_input,
                output_language="ZH",
            )
        )

        # Then: 80% 이상의 필드가 중국어로 작성되어야 함
        ratio, matched, total, failed = self._check_language_compliance_ratio(
            analysis, "ZH"
        )

        self.assertGreaterEqual(
            ratio,
            self.LANGUAGE_MATCH_THRESHOLD,
            f"중국어 응답 비율이 {self.LANGUAGE_MATCH_THRESHOLD*100}% 미만입니다. "
            f"실제: {ratio*100:.1f}% ({matched}/{total})\n"
            f"실패 필드: {failed}",
        )

    def test_output_language_spanish(self) -> None:
        """
        output_language='ES'로 요청 시 스페인어로 응답해야 함

        비율 기반 검증: 80% 이상의 필드가 스페인어로 작성되면 통과
        """
        # When
        analysis = asyncio.run(
            self.service.analyze_trade(
                input_text=self.test_input,
                output_language="ES",
            )
        )

        # Then: 80% 이상의 필드가 스페인어로 작성되어야 함
        ratio, matched, total, failed = self._check_language_compliance_ratio(
            analysis, "ES"
        )

        self.assertGreaterEqual(
            ratio,
            self.LANGUAGE_MATCH_THRESHOLD,
            f"스페인어 응답 비율이 {self.LANGUAGE_MATCH_THRESHOLD*100}% 미만입니다. "
            f"실제: {ratio*100:.1f}% ({matched}/{total})\n"
            f"실패 필드: {failed}",
        )

    def test_output_language_thai(self) -> None:
        """
        output_language='TH'로 요청 시 태국어로 응답해야 함

        비율 기반 검증: 80% 이상의 필드가 태국어로 작성되면 통과
        """
        # When
        analysis = asyncio.run(
            self.service.analyze_trade(
                input_text=self.test_input,
                output_language="TH",
            )
        )

        # Then: 80% 이상의 필드가 태국어로 작성되어야 함
        ratio, matched, total, failed = self._check_language_compliance_ratio(
            analysis, "TH"
        )

        self.assertGreaterEqual(
            ratio,
            self.LANGUAGE_MATCH_THRESHOLD,
            f"태국어 응답 비율이 {self.LANGUAGE_MATCH_THRESHOLD*100}% 미만입니다. "
            f"실제: {ratio*100:.1f}% ({matched}/{total})\n"
            f"실패 필드: {failed}",
        )

    def test_output_language_vietnamese(self) -> None:
        """
        output_language='VI'로 요청 시 베트남어로 응답해야 함

        비율 기반 검증: 80% 이상의 필드가 베트남어로 작성되면 통과
        """
        # When
        analysis = asyncio.run(
            self.service.analyze_trade(
                input_text=self.test_input,
                output_language="VI",
            )
        )

        # Then: 80% 이상의 필드가 베트남어로 작성되어야 함
        ratio, matched, total, failed = self._check_language_compliance_ratio(
            analysis, "VI"
        )

        self.assertGreaterEqual(
            ratio,
            self.LANGUAGE_MATCH_THRESHOLD,
            f"베트남어 응답 비율이 {self.LANGUAGE_MATCH_THRESHOLD*100}% 미만입니다. "
            f"실제: {ratio*100:.1f}% ({matched}/{total})\n"
            f"실패 필드: {failed}",
        )

    def test_output_language_indonesian(self) -> None:
        """
        output_language='ID'로 요청 시 인도네시아어로 응답해야 함

        비율 기반 검증: 80% 이상의 필드가 인도네시아어로 작성되면 통과
        """
        # When
        analysis = asyncio.run(
            self.service.analyze_trade(
                input_text=self.test_input,
                output_language="ID",
            )
        )

        # Then: 80% 이상의 필드가 인도네시아어로 작성되어야 함
        ratio, matched, total, failed = self._check_language_compliance_ratio(
            analysis, "ID"
        )

        self.assertGreaterEqual(
            ratio,
            self.LANGUAGE_MATCH_THRESHOLD,
            f"인도네시아어 응답 비율이 {self.LANGUAGE_MATCH_THRESHOLD*100}% 미만입니다. "
            f"실제: {ratio*100:.1f}% ({matched}/{total})\n"
            f"실패 필드: {failed}",
        )

    def test_output_language_tagalog(self) -> None:
        """
        output_language='TL'로 요청 시 타갈로그어로 응답해야 함

        비율 기반 검증: 80% 이상의 필드가 타갈로그어로 작성되면 통과
        """
        # When
        analysis = asyncio.run(
            self.service.analyze_trade(
                input_text=self.test_input,
                output_language="TL",
            )
        )

        # Then: 80% 이상의 필드가 타갈로그어로 작성되어야 함
        ratio, matched, total, failed = self._check_language_compliance_ratio(
            analysis, "TL"
        )

        self.assertGreaterEqual(
            ratio,
            self.LANGUAGE_MATCH_THRESHOLD,
            f"타갈로그어 응답 비율이 {self.LANGUAGE_MATCH_THRESHOLD*100}% 미만입니다. "
            f"실제: {ratio*100:.1f}% ({matched}/{total})\n"
            f"실패 필드: {failed}",
        )


class TestPreviewService(unittest.TestCase):
    """
    통합 테스트: PreviewService의 Twitter URL 메타데이터 추출 검증

    이 테스트는 PreviewService가 실제 Twitter API를 사용하여
    포스트 메타데이터를 추출하고, 올바른 형식의 응답을 반환하는지 검증합니다.

    환경 변수:
        TWITTER_BEARER_TOKEN: Twitter API Bearer Token (필수)
    """

    def setUp(self) -> None:
        # PreviewService will auto-create TwitterService with environment settings
        self.service = PreviewService()

    def test_preview_twitter_url_integration(self) -> None:
        """
        Twitter/X URL을 입력받아 포스트 메타데이터를 추출해야 함

        시나리오:
        - 입력: Twitter/X URL (실제 존재하는 트윗)
        - 기대 결과: 작성자, 텍스트, 이미지, 생성일 등 메타데이터 추출

        Note:
        - 이 테스트는 실제 Twitter API를 호출합니다
        - Twitter API Bearer Token이 필요합니다 (TWITTER_BEARER_TOKEN 환경변수)
        - 네트워크 연결이 필요합니다
        """
        # Given: 실제 Twitter URL
        twitter_url = "https://x.com/jenniestbalipin/status/1990666828457390345"

        # When: Twitter URL로 메타데이터 추출
        try:
            preview = self.service.preview(twitter_url)

            # Then: 메타데이터 검증
            self.assertIsNotNone(preview, "메타데이터가 반환되어야 합니다")

            # Platform 검증
            self.assertEqual(
                preview.platform, Platform.TWITTER, "플랫폼은 TWITTER여야 합니다"
            )

            # Author 검증
            self.assertIsNotNone(preview.author, "작성자가 반환되어야 합니다")
            self.assertGreater(
                len(preview.author), 0, "작성자는 빈 문자열이 아니어야 합니다"
            )

            # Text 검증
            self.assertIsNotNone(preview.text, "텍스트가 반환되어야 합니다")
            self.assertGreater(
                len(preview.text), 0, "텍스트는 빈 문자열이 아니어야 합니다"
            )

            # Text preview 검증 (200자 제한)
            self.assertIsNotNone(
                preview.text_preview, "텍스트 미리보기가 반환되어야 합니다"
            )
            self.assertLessEqual(
                len(preview.text_preview),
                200,
                "텍스트 미리보기는 200자 이하여야 합니다",
            )

            # Images 검증 (리스트여야 함, 비어있을 수 있음)
            self.assertIsInstance(preview.images, list, "이미지는 리스트여야 합니다")

            # Created_at 검증 (있을 수도 없을 수도 있음)
            if preview.created_at:
                self.assertIsNotNone(
                    preview.created_at, "생성일이 제공된 경우 None이 아니어야 합니다"
                )

            print("\n✅ Twitter URL 메타데이터 추출 성공")
            print(f"   Platform: {preview.platform}")
            print(f"   Author: {preview.author}")
            print(f"   Text length: {len(preview.text)} chars")
            print(f"   Text preview length: {len(preview.text_preview)} chars")
            print(f"   Images: {len(preview.images)}개")
            print(f"   Created at: {preview.created_at}")

        except ValueError as e:
            # Twitter API 접근 불가 또는 네트워크 에러인 경우 테스트 스킵
            if "Twitter Bearer Token" in str(e) or "Failed to fetch tweet" in str(e):
                self.skipTest(f"Twitter API 사용 불가: {e}")
            else:
                raise

    def test_preview_unsupported_url(self) -> None:
        """
        지원하지 않는 URL 입력 시 ValueError를 발생시켜야 함

        시나리오:
        - 입력: 지원하지 않는 플랫폼의 URL
        - 기대 결과: ValueError 발생
        """
        # Given: 지원하지 않는 URL
        unsupported_url = "https://www.instagram.com/p/ABC123/"

        # When & Then: ValueError 발생해야 함
        with self.assertRaises(ValueError) as context:
            self.service.preview(unsupported_url)

        self.assertIn(
            "Unsupported URL",
            str(context.exception),
            "에러 메시지에 'Unsupported URL'이 포함되어야 합니다",
        )


if __name__ == "__main__":
    unittest.main()
