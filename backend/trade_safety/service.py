"""
Trade Safety Service for K-pop Merchandise Trading.

This module provides LLM-based safety analysis for K-pop merchandise trades,
helping international fans overcome language, trust, and information barriers.

The service analyzes trade posts to detect scam signals, explain Korean slang,
assess price fairness, and provide actionable safety recommendations.
"""

from __future__ import annotations

import logging
from urllib.parse import urlparse

from aioia_core.settings import OpenAIAPISettings
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from trade_safety.ml.classifier import TfidfMLPClassifier
from trade_safety.prompts import TRADE_SAFETY_SYSTEM_PROMPT
from trade_safety.reddit_extract_text_service import RedditService
from trade_safety.schemas import TradeSafetyAnalysis
from trade_safety.settings import (
    ALLOWED_LANGUAGES,
    TradeSafetyModelSettings,
    TwitterAPISettings,
)
from trade_safety.twitter_extract_text_service import TwitterService

logger = logging.getLogger(__name__)


# ==============================================================================
# Trade Safety Analysis Service
# ==============================================================================


class TradeSafetyService:
    """
    Service for analyzing K-pop merchandise trade safety using LLM.

    This service helps international K-pop fans (especially young fans) who face:
    1. Language Barrier: Korean slang, abbreviations, nuances
    2. Trust Issues: Unable to verify sellers, authentication photos
    3. Information Gap: Don't know market prices, can't spot fakes
    4. No Protection: No refunds, FOMO-driven impulse buys

    The service provides:
    - Translation and nuance explanation of Korean trade posts
    - Scam signal detection (risk signals, cautions, safe indicators)
    - Price fairness analysis with market reference
    - Actionable safety checklist
    - Empathetic guidance to reduce FOMO and anxiety

    Example:
        >>> from aioia_core.settings import OpenAIAPISettings
        >>> from trade_safety.settings import TradeSafetyModelSettings
        >>>
        >>> openai_api = OpenAIAPISettings(api_key="sk-...")
        >>> model_settings = TradeSafetyModelSettings()
        >>> service = TradeSafetyService(
        ...     openai_api=openai_api,
        ...     model_settings=model_settings,
        ... )
        >>> analysis = await service.analyze_trade(
        ...     input_text="급처분 공구 실패해서 양도해요"
        ... )
        >>> print(analysis.safe_score)
        75
    """

    def __init__(
        self,
        openai_api: OpenAIAPISettings,
        model_settings: TradeSafetyModelSettings,
        twitter_api: TwitterAPISettings | None = None,
        system_prompt: str = TRADE_SAFETY_SYSTEM_PROMPT,
    ):
        """
        Initialize TradeSafetyService with LLM and optional ML configuration.

        Args:
            openai_api: OpenAI API settings (api_key)
            model_settings: Model settings (model name, ML config)
            twitter_api: Twitter API settings (bearer_token). If not provided, will try
                         TWITTER_BEARER_TOKEN env var via TwitterAPISettings().
            system_prompt: System prompt for trade safety analysis (default: TRADE_SAFETY_SYSTEM_PROMPT)

        Note:
            Temperature is hardcoded to 0.7 for balanced analytical reasoning.
            The default system_prompt is provided by the library, but can be overridden
            with custom prompts (e.g., domain-specific or improved versions).

            If ML is enabled (model_settings.ml_enabled), the ML classifier will be
            loaded on first prediction (lazy loading). Missing model files will raise
            FileNotFoundError immediately (Fail-fast principle).
        """
        logger.debug(
            "Initializing TradeSafetyService with model=%s, ml_enabled=%s",
            model_settings.model,
            model_settings.ml_enabled,
        )

        # Use with_structured_output for schema-enforced responses
        # This uses OpenAI's Structured Outputs (json_schema + strict: true)
        # which guarantees the response adheres to the Pydantic schema
        base_model = ChatOpenAI(
            model=model_settings.model,
            temperature=0.7,  # Hardcoded - balanced for analytical tasks
            api_key=openai_api.api_key,  # type: ignore[arg-type]
            max_retries=3,
        )
        self.chat_model = base_model.with_structured_output(
            TradeSafetyAnalysis,
            strict=True,  # Enforce enum constraints and schema validation
        )
        self.system_prompt = system_prompt
        self.twitter_service = TwitterService(twitter_api=twitter_api)
        self.reddit_service = RedditService()

        # ML classifier (lazy loading)
        self.model_settings = model_settings
        self.ml_classifier: TfidfMLPClassifier | None = None
        if model_settings.ml_enabled and model_settings.ml_model_dir:
            self.ml_classifier = TfidfMLPClassifier(
                model_dir=model_settings.ml_model_dir
            )
            logger.debug(
                "ML classifier initialized (lazy loading): %s",
                model_settings.ml_model_dir,
            )

    # ==========================================
    # Main Analysis Method
    # ==========================================

    async def analyze_trade(
        self,
        input_text: str,
        output_language: str = "en",
    ) -> TradeSafetyAnalysis:
        """
        Analyze a trade post for safety issues using LLM.

        This method orchestrates the complete analysis workflow:
        1. Validate input parameters
        2. Build system and user prompts
        3. Call LLM for analysis
        4. Parse and structure the response
        5. Handle errors with fallback analysis

        Args:
            input_text: Trade post text or URL to analyze
            output_language: Language for analysis results (default: "en")

        Returns:
            TradeSafetyAnalysis: Complete analysis including:
                - Translation and nuance explanation
                - Risk signals, cautions, and safe indicators
                - Price analysis (extracted from input text)
                - Safety checklist
                - Safety score (0-100, higher is safer)
                - Recommendation and emotional support

        Raises:
            ValueError: If input validation fails
            Exception: If LLM generation fails unexpectedly

        Example:
            >>> analysis = await service.analyze_trade(
            ...     "급처분 ㅠㅠ 공구 실패해서 양도해요"
            ... )
            >>> print(f"Safety: {analysis.safe_score}/100")
            Safety: 75/100
        """
        # Step 1: Validate input
        self._validate_input(input_text, output_language)

        # Step 2: Validate URL
        is_url = self._is_url(input_text)
        if is_url:
            logger.info("URL detected, fetching content from: %s", input_text[:100])
            content = self._fetch_url_content(input_text)
            logger.info("Fetched content length: %d chars", len(content))
        else:
            logger.info("Text input detected, using as-is")
            content = input_text

        logger.info(
            "Starting trade analysis: text_length=%d",
            len(content),
        )

        # Step 3: Build prompts
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(content, output_language)

        # Step 4: Call LLM with structured output
        # with_structured_output uses OpenAI's Structured Outputs feature,
        # which guarantees the response adheres to the TradeSafetyAnalysis schema
        logger.debug("Calling LLM for trade analysis (%d chars)", len(user_prompt))
        analysis = await self.chat_model.ainvoke(
            [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt),
            ]
        )

        # Type narrowing: with_structured_output returns TradeSafetyAnalysis
        if not isinstance(analysis, TradeSafetyAnalysis):
            raise TypeError(
                f"Unexpected response type: {type(analysis)} (expected TradeSafetyAnalysis)"
            )

        logger.info(
            "Trade analysis completed successfully: safe_score=%d, signals=%d, cautions=%d, safe=%d",
            analysis.safe_score,
            len(analysis.risk_signals),
            len(analysis.cautions),
            len(analysis.safe_indicators),
        )

        # Step 5: Apply ML ensemble if enabled
        final_analysis = self._apply_ensemble(analysis, content)

        return final_analysis

    # ==========================================
    # Prompt Building Methods
    # ==========================================

    def _build_system_prompt(self) -> str:
        """
        Build system prompt instructing LLM how to analyze trades.

        The prompt defines:
        - Role: K-pop merchandise trading safety expert
        - Target audience: International fans with barriers
        - Analysis steps: Translation, scam detection, price analysis, checklist
        - Output format: Structured JSON
        - Guidelines: Empathetic, empowering, non-judgmental

        Returns:
            Complete system prompt for LLM (from prompts.py)
        """
        return self.system_prompt

    def _build_user_prompt(
        self,
        input_text: str,
        output_language: str,
    ) -> str:
        """
        Build user prompt with trade post content.

        Args:
            input_text: Trade post text/URL
            output_language: Language for analysis results

        Returns:
            The input text to be analyzed
        """
        prompt = f"""output_language: {output_language}
                IMPORTANT: Write ALL field values (translation, nuance_explanation, titles, descriptions, recommendations, emotional_support) in {output_language}. Do NOT mix languages.
                Trade post to analyze: {input_text}"""

        logger.debug(
            "Built user prompt: text_length=%d",
            len(prompt),
        )

        return prompt

    # ==========================================
    # Input Validation
    # ==========================================

    def _validate_input(self, input_text: str, output_language: str) -> None:
        """
        Validate input parameters before analysis.

        Args:
            input_text: Trade post text
            output_language: Language code for analysis results

        Raises:
            ValueError: If input validation fails
        """
        if output_language.upper() not in ALLOWED_LANGUAGES:
            error_msg = f"Invalid output_language: {output_language} (allowed: {ALLOWED_LANGUAGES})"
            logger.error("Validation failed: %s", error_msg)
            raise ValueError(error_msg)

        if not input_text or not input_text.strip():
            error_msg = "input_text cannot be empty"
            logger.error("Validation failed: %s", error_msg)
            raise ValueError(error_msg)

        if len(input_text) > 10000:  # Reasonable limit for trade posts
            error_msg = f"input_text too long: {len(input_text)} chars (max 10000)"
            logger.error("Validation failed: %s", error_msg)
            raise ValueError(error_msg)

        logger.debug(
            "Input validation passed: text_length=%d",
            len(input_text),
        )

    def _is_url(self, input_text: str) -> bool:
        """
        Validate input text is URL?

        Args:
            input_text: Trade Post text

        Returns:

        """
        text = input_text.strip()

        # use to urlparse
        parsed = urlparse(text)

        if parsed.scheme in {"http", "https"} and parsed.netloc:
            logger.debug("URL detected: %s", text[:100])
            return True

        logger.debug("Not a URL, treating as text")
        return False

    def _fetch_url_content(self, url: str) -> str:
        """
        Fetch content from URL.

        Args:
            url: URL to fetch content from

        Returns:
            str: Text content from the URL

        Raises:
            ValueError: If URL fetch fails or returns error status
        """

        # X(트위터) URL인지 먼저 판별
        if TwitterService.is_twitter_url(url):
            logger.info("Detected Twitter/X URL, using TwitterService")
            return self.twitter_service.fetch_tweet_content(url)

        if RedditService.is_reddit_url(url):
            logger.info("Detected Reddit URL, using RedditService")
            return self.reddit_service.fetch_post_content(url)

        logger.warning("Unsupported URL type: %s", url)
        raise ValueError(
            "Unsupported URL. Currently only Twitter/X and Reddit URLs are supported."
            "Please paste the text content directly instead of the URL."
        )

    def _apply_ensemble(
        self, llm_analysis: TradeSafetyAnalysis, content: str
    ) -> TradeSafetyAnalysis:
        """
        Apply ML ensemble if enabled, otherwise return LLM analysis as-is.

        Args:
            llm_analysis: Analysis from LLM
            content: Original trade post content

        Returns:
            TradeSafetyAnalysis: Analysis with ensemble-adjusted safe_score
        """
        if not self.ml_classifier:
            logger.debug("ML disabled, using LLM-only analysis")
            return llm_analysis

        logger.debug("ML enabled, applying ensemble logic")

        # Get ML prediction
        ml_scam_prob = self.ml_classifier.predict_proba(content)
        logger.info(
            "ML prediction: scam_prob=%.2f, LLM safe_score=%d",
            ml_scam_prob,
            llm_analysis.safe_score,
        )

        # Apply conditional ensemble
        final_safe_score = self._decide_safe_score(
            ml_scam_prob,
            llm_analysis.safe_score,
            self.model_settings.ml_threshold_high,
            self.model_settings.ml_threshold_low,
        )

        logger.info(
            "Ensemble applied: LLM=%d, ML_safe=%d, final=%d",
            llm_analysis.safe_score,
            100 - int(ml_scam_prob * 100),
            final_safe_score,
        )

        # Return new analysis with updated safe_score
        return TradeSafetyAnalysis(
            **{
                **llm_analysis.model_dump(),
                "safe_score": final_safe_score,
            }
        )

    @staticmethod
    def _decide_safe_score(
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
