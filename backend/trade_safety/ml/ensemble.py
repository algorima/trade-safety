"""Ensemble logic for combining ML and LLM predictions."""


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

    Examples:
        >>> decide_safe_score(0.90, 70, 0.85, 0.20)  # ML confident: scam
        10
        >>> decide_safe_score(0.15, 40, 0.85, 0.20)  # ML confident: legit
        85
        >>> decide_safe_score(0.50, 60, 0.85, 0.20)  # ML uncertain
        55
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
