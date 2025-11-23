"use client";

import { CheckCircleIcon } from "@heroicons/react/24/solid";
import { motion } from "framer-motion";
import { useTranslation } from "react-i18next";

import { RiskSignal } from "@/types";

import { RiskSignalCard } from "../RiskSignalCard";

interface SafeIndicatorsSectionProps {
  indicators: RiskSignal[];
}

export function SafeIndicatorsSection({
  indicators,
}: SafeIndicatorsSectionProps) {
  const { t } = useTranslation();

  if (indicators.length === 0) return null;

  return (
    <section>
      <h3 className="mb-6 flex items-center gap-3 text-3xl font-bold">
        <CheckCircleIcon className="size-10 text-success" />
        {t("page.tradeSafety.result.safeIndicators")}
      </h3>

      <div className="space-y-4">
        {indicators.map((indicator, idx) => (
          <motion.div
            key={idx}
            initial={{ x: -50, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ delay: idx * 0.1 }}
            whileHover={{ scale: 1.02, x: 10 }}
          >
            <RiskSignalCard signal={indicator} variant="success" />
          </motion.div>
        ))}
      </div>
    </section>
  );
}
