"""
Trade Safety Service for K-pop Merchandise Trading.

This module provides LLM-based safety analysis for K-pop merchandise trades,
helping international fans overcome language, trust, and information barriers.

The service analyzes trade posts to detect scam signals, explain Korean slang,
assess price fairness, and provide actionable safety recommendations.
"""

from __future__ import annotations

import logging

from langchain_community.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from aioia_core.settings import OpenAIAPISettings
from trade_safety.prompts import TRADE_SAFETY_SYSTEM_PROMPT
from trade_safety.schemas import TradeSafetyAnalysis
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
        system_prompt: str = TRADE_SAFETY_SYSTEM_PROMPT,
    ):
        """
        Initialize TradeSafetyService with LLM configuration.

        Args:
            openai_api: OpenAI API settings (api_key)
            model_settings: Model settings (model name)
            system_prompt: System prompt for trade safety analysis (default: TRADE_SAFETY_SYSTEM_PROMPT)

        Note:
            Temperature is hardcoded to 0.7 for balanced analytical reasoning.
            The default system_prompt is provided by the library, but can be overridden
            with custom prompts (e.g., domain-specific or improved versions).
        """
        logger.debug(
            "Initializing TradeSafetyService with model=%s",
            model_settings.model,
        )

        # Use with_structured_output for schema-enforced responses
        # This uses OpenAI's Structured Outputs (json_schema + strict: true)
        # which guarantees the response adheres to the Pydantic schema
        base_model = ChatOpenAI(
            model=model_settings.model,
            temperature=0.7,  # Hardcoded - balanced for analytical tasks
            api_key=openai_api.api_key,  # type: ignore[arg-type]
        )
        self.chat_model = base_model.with_structured_output(TradeSafetyAnalysis)
        self.system_prompt = system_prompt

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

        # Step 3: Call LLM with structured output
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
            "Trade analysis completed successfully: risk_score=%d, signals=%d, cautions=%d, safe=%d",
            analysis.risk_score,
            len(analysis.risk_signals),
            len(analysis.cautions),
            len(analysis.safe_indicators),
        )

        return analysis

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
