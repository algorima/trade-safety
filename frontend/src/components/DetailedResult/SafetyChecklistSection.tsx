"use client";

import { ClipboardDocumentCheckIcon } from "@heroicons/react/24/solid";
import { motion } from "framer-motion";
import { useTranslation } from "react-i18next";

import { TRADE_SAFETY_NS } from "../../i18n";

interface SafetyChecklistSectionProps {
  items: string[];
}

export function SafetyChecklistSection({ items }: SafetyChecklistSectionProps) {
  const { t } = useTranslation(TRADE_SAFETY_NS);

  if (items.length === 0) return null;

  return (
    <section>
      <h3 className="mb-6 flex items-center gap-3 text-3xl font-bold">
        <ClipboardDocumentCheckIcon className="size-10 text-primary" />
        {t("result.safetyChecklist")}
      </h3>

      <div className="card border-2 border-primary/30 bg-base-200">
        <div className="card-body">
          <p className="mb-6 text-lg text-neutral-content">
            {t("result.checklistDescription")}
          </p>

          <div className="space-y-3">
            {items.map((item, idx) => (
              <motion.label
                key={idx}
                initial={{ x: -20, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ delay: idx * 0.08 }}
                className="flex cursor-pointer items-start gap-3 rounded-lg p-3 hover:bg-base-100/30"
              >
                <input
                  type="checkbox"
                  className="checkbox-primary checkbox mt-1"
                />
                <span className="text-lg">{item}</span>
              </motion.label>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
