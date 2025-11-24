"use client";

import { ExclamationTriangleIcon } from "@heroicons/react/24/solid";
import { motion } from "framer-motion";
import { useTranslation } from "react-i18next";

import { RiskSignal } from "../../types";
import { RiskSignalCard } from "../RiskSignalCard";

interface CautionsSectionProps {
  cautions: RiskSignal[];
}

export function CautionsSection({ cautions }: CautionsSectionProps) {
  const { t } = useTranslation();

  if (cautions.length === 0) return null;

  return (
    <section>
      <h3 className="mb-6 flex items-center gap-3 text-3xl font-bold">
        <ExclamationTriangleIcon className="size-10 text-warning" />
        {t("page.tradeSafety.result.cautions")}
      </h3>

      <div className="space-y-4">
        {cautions.map((caution, idx) => (
          <motion.div
            key={idx}
            initial={{ x: -50, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ delay: idx * 0.1 }}
            whileHover={{ scale: 1.02, x: 10 }}
          >
            <RiskSignalCard signal={caution} variant="warning" />
          </motion.div>
        ))}
      </div>
    </section>
  );
}
