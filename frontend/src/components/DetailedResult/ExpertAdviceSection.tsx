"use client";

import { UserIcon } from "@heroicons/react/24/solid";
import { motion } from "framer-motion";
import { useTranslation } from "react-i18next";

interface ExpertAdviceSectionProps {
  advice: string;
}

export function ExpertAdviceSection({ advice }: ExpertAdviceSectionProps) {
  const { t } = useTranslation();

  return (
    <motion.section
      whileHover={{ scale: 1.02 }}
      className="card bg-secondary text-secondary-content shadow-xl"
    >
      <div className="card-body">
        <div className="mb-6 flex items-center gap-4">
          <div className="avatar placeholder">
            <div className="w-16 rounded-full bg-primary text-primary-content">
              <UserIcon className="size-8" />
            </div>
          </div>
          <div>
            <h3 className="text-2xl font-bold">
              {t("page.tradeSafety.result.expertAdvice")}
            </h3>
            <p className="opacity-80">
              {t("page.tradeSafety.result.expertName")}
            </p>
          </div>
        </div>

        <div className="prose max-w-none">
          <p className="whitespace-pre-wrap text-lg">{advice}</p>
        </div>
      </div>
    </motion.section>
  );
}
