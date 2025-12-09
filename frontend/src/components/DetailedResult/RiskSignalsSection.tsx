"use client";

import { ShieldExclamationIcon } from "@heroicons/react/24/solid";
import { motion } from "framer-motion";
import { useTranslation } from "react-i18next";

import { TRADE_SAFETY_NS } from "../../i18n";
import { RiskSignal } from "../../types";
import { RiskSignalCard } from "../RiskSignalCard";

interface RiskSignalsSectionProps {
  signals: RiskSignal[];
}

export function RiskSignalsSection({ signals }: RiskSignalsSectionProps) {
  const { t } = useTranslation(TRADE_SAFETY_NS);

  if (signals.length === 0) return null;

  return (
    <section>
      <h3 className="mb-6 flex items-center gap-3 text-3xl font-bold">
        <ShieldExclamationIcon className="size-10 text-error" />
        {t("result.riskSignals")}
      </h3>

      <div className="space-y-4">
        {signals.map((signal, idx) => (
          <motion.div
            key={idx}
            initial={{ x: -50, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ delay: idx * 0.1 }}
            whileHover={{ scale: 1.02, x: 10 }}
          >
            <RiskSignalCard signal={signal} variant="error" />
          </motion.div>
        ))}
      </div>
    </section>
  );
}
