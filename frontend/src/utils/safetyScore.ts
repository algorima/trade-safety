import { SAFETY_SCORE_THRESHOLDS, SafetyLevel } from "@/types";

export const getSafetyLevel = (safetyScore: number): SafetyLevel => {
  if (safetyScore >= SAFETY_SCORE_THRESHOLDS.safe) return "safe";
  if (safetyScore >= SAFETY_SCORE_THRESHOLDS.caution) return "caution";
  return "danger";
};
