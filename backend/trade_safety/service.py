"""
Trade Safety Service for K-pop Merchandise Trading.

This module provides LLM-based safety analysis for K-pop merchandise trades,
helping international fans overcome language, trust, and information barriers.

The service analyzes trade posts to detect scam signals, explain Korean slang,
assess price fairness, and provide actionable safety recommendations.
"""

from __future__ import annotations

import json
import logging

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import ValidationError

from aioia_core.settings import OpenAIAPISettings

from trade_safety.prompts import TRADE_SAFETY_SYSTEM_PROMPT
from trade_safety.schemas import (
    PriceAnalysis,
    RiskCategory,
    RiskSeverity,
    RiskSignal,
    TradeSafetyAnalysis,
)
from trade_safety.settings import TradeSafetyModelSettings

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
        >>> service = TradeSafetyService(openai_api, model_settings)
        >>> analysis = await service.analyze_trade(
        ...     input_text="급처분 공구 실패해서 양도해요"
        ... )
        >>> print(analysis.risk_score)
        35
    """

    def __init__(
        self,
        openai_api: OpenAIAPISettings,
        model_settings: TradeSafetyModelSettings,
    ):
        """
        Initialize TradeSafetyService with LLM configuration.

        Args:
            openai_api: OpenAI API settings (api_key)
            model_settings: Model settings (model name)

        Note:
            Temperature is hardcoded to 0.7 for balanced analytical reasoning.
        """
        logger.debug(
            "Initializing TradeSafetyService with model=%s",
            model_settings.model,
        )

        self.chat_model = ChatOpenAI(
            model=model_settings.model,
            temperature=0.7,  # Hardcoded - balanced for analytical tasks
            api_key=openai_api.api_key,
            model_kwargs={
                "response_format": {"type": "json_object"}
            },  # Force JSON response
        )
        self.system_prompt = TRADE_SAFETY_SYSTEM_PROMPT

    # ==========================================
    # Main Analysis Method
    # ==========================================

    async def analyze_trade(
        self,
        input_text: str,
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

        Returns:
            TradeSafetyAnalysis: Complete analysis including:
                - Translation and nuance explanation
                - Risk signals, cautions, and safe indicators
                - Price analysis (extracted from input text)
                - Safety checklist
                - Risk score (0-100)
                - Recommendation and emotional support

        Raises:
            ValueError: If input validation fails
            Exception: If LLM generation fails unexpectedly

        Example:
            >>> analysis = await service.analyze_trade(
            ...     "급처분 ㅠㅠ 공구 실패해서 양도해요"
            ... )
            >>> print(f"Risk: {analysis.risk_score}/100")
            Risk: 35/100
        """
        # Step 1: Validate input
        self._validate_input(input_text)

        logger.info(
            "Starting trade analysis: text_length=%d",
            len(input_text),
        )

        # Step 2: Build prompts
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(input_text)

        response_text: str | None = None  # Initialize for error handling
        try:
            # Step 3: Call LLM
            logger.debug("Calling LLM for trade analysis (%d chars)", len(user_prompt))
            response = await self.chat_model.agenerate(
                [
                    [
                        SystemMessage(content=system_prompt),
                        HumanMessage(content=user_prompt),
                    ]
                ]
            )

            # Step 4: Extract and parse response
            response_text = response.generations[0][0].text
            logger.debug("LLM response received (%d chars)", len(response_text))

            analysis = self._parse_llm_response(response_text)

            logger.info(
                "Trade analysis completed successfully: risk_score=%d, signals=%d, cautions=%d, safe=%d",
                analysis.risk_score,
                len(analysis.risk_signals),
                len(analysis.cautions),
                len(analysis.safe_indicators),
            )

            return analysis

        except (KeyError, TypeError, ValueError, ValidationError) as e:
            # ValueError includes json.JSONDecodeError
            # ValidationError handles Pydantic validation failures
            response_preview = "N/A"
            if response_text is not None:
                response_preview = response_text[:200]
            logger.error(
                "Failed to parse LLM response: %s (response preview: %s...)",
                e,
                response_preview,
                exc_info=True,
            )
            # Return fallback analysis for expected parsing errors
            return self._create_fallback_analysis()

        except Exception as e:
            logger.error(
                "Trade analysis failed unexpectedly: %s",
                e,
                exc_info=True,
            )
            raise

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
    ) -> str:
        """
        Build user prompt with trade post content.

        Args:
            input_text: Trade post text/URL

        Returns:
            The input text to be analyzed
        """
        logger.debug(
            "Built user prompt: text_length=%d",
            len(input_text),
        )

        return input_text

    # ==========================================
    # Response Parsing Methods
    # ==========================================

    def _parse_llm_response(self, response_text: str) -> TradeSafetyAnalysis:
        """
        Parse LLM response text into structured TradeSafetyAnalysis object.

        Handles:
        - Extracting JSON from markdown code blocks
        - Converting JSON dict to Pydantic models
        - Building nested objects (RiskSignal, PriceAnalysis)

        Args:
            response_text: Raw LLM response (may include markdown formatting)

        Returns:
            Structured analysis object

        Raises:
            json.JSONDecodeError: If response is not valid JSON
            KeyError: If response missing required fields (risk_score, etc.)
            ValidationError: If Pydantic validation fails
        """
        logger.debug("Parsing LLM response (%d chars)", len(response_text))

        # Extract JSON from response (LLM might wrap it in markdown code blocks)
        cleaned_text = self._extract_json_from_markdown(response_text)

        # Parse JSON
        try:
            data = json.loads(cleaned_text)
            logger.debug("JSON parsed successfully, converting to Pydantic models")
        except json.JSONDecodeError as e:
            logger.error(
                "JSON parsing failed: %s (cleaned text preview: %s...)",
                e,
                cleaned_text[:200],
            )
            raise

        # Convert nested objects to Pydantic models
        # (Pydantic doesn't auto-convert nested dicts, so we handle them explicitly)
        data["risk_signals"] = [
            RiskSignal(**signal) for signal in data.get("risk_signals", [])
        ]
        data["cautions"] = [
            RiskSignal(**caution) for caution in data.get("cautions", [])
        ]
        data["safe_indicators"] = [
            RiskSignal(**indicator) for indicator in data.get("safe_indicators", [])
        ]

        if data.get("price_analysis"):
            data["price_analysis"] = PriceAnalysis(**data["price_analysis"])

        # Use Pydantic's direct initialization for validation and type checking
        analysis = TradeSafetyAnalysis(**data)

        logger.debug(
            "Response parsed successfully: risk_score=%d, total_signals=%d",
            analysis.risk_score,
            len(analysis.risk_signals)
            + len(analysis.cautions)
            + len(analysis.safe_indicators),
        )

        return analysis

    def _extract_json_from_markdown(self, text: str) -> str:
        """
        Extract JSON content from markdown code blocks.

        LLMs often wrap JSON in ```json ... ``` or ``` ... ``` blocks.
        This method strips those wrappers to get clean JSON.

        Args:
            text: Raw text that may contain markdown formatting

        Returns:
            Cleaned text with markdown removed
        """
        text = text.strip()

        # Remove ```json prefix
        if text.startswith("```json"):
            text = text[7:]

        # Remove ``` prefix/suffix
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]

        return text.strip()

    # ==========================================
    # Fallback and Error Handling
    # ==========================================

    def _create_fallback_analysis(self) -> TradeSafetyAnalysis:
        """
        Create fallback analysis when LLM fails or returns invalid response.

        Returns a safe, neutral analysis that:
        - Indicates the system error to user
        - Provides generic safety checklist
        - Sets neutral risk score (50/100)
        - Encourages caution without false information

        Returns:
            Basic fallback analysis with neutral risk assessment

        Note:
            This is a last-resort fallback. Ideally, LLM should always succeed.
            Monitor fallback usage rate to detect LLM issues.
        """
        logger.warning("Creating fallback analysis due to LLM failure")

        return TradeSafetyAnalysis(
            translation=None,
            nuance_explanation=None,
            risk_signals=[
                RiskSignal(
                    category=RiskCategory.CONTENT,
                    severity=RiskSeverity.MEDIUM,
                    title="Unable to complete full analysis",
                    description="The automatic analysis system encountered an error. Please proceed with extra caution.",
                    what_to_do="Manually verify all details with the seller and check community reviews.",
                )
            ],
            cautions=[],
            safe_indicators=[],
            price_analysis=None,
            safety_checklist=[
                "Request detailed authentication photos with today's date",
                "Propose safe payment method (PayPal Goods & Services)",
                "Search for seller reviews in K-pop communities",
                "Take your time - don't rush due to FOMO",
            ],
            risk_score=50,  # Neutral score when we can't analyze
            recommendation="We couldn't complete the full safety analysis. Please be extra careful and verify all details before proceeding with this trade.",
            emotional_support="It's okay to be cautious. If you're unsure, it's better to wait for another opportunity. Your safety is more important than any item.",
        )

    # ==========================================
    # Input Validation
    # ==========================================

    def _validate_input(self, input_text: str) -> None:
        """
        Validate input parameters before analysis.

        Args:
            input_text: Trade post text

        Raises:
            ValueError: If input validation fails
        """
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
