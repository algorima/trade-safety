"use client";

import { ChatBubbleOvalLeftEllipsisIcon } from "@heroicons/react/24/solid";
import { motion } from "framer-motion";
import Link from "next/link";
import { useTranslation } from "react-i18next";

import { TRADE_SAFETY_NS } from "../../i18n";

export function CompanionCtaSection() {
  const { t, i18n } = useTranslation(TRADE_SAFETY_NS);
  const lang = i18n.language;

  return (
    <section className="hero min-h-[30vh] rounded-3xl bg-primary text-primary-content">
      <div className="hero-content text-center">
        <div>
          <ChatBubbleOvalLeftEllipsisIcon className="mx-auto mb-6 size-20" />

          <h3 className="mb-4 text-4xl font-bold">
            {t("result.companionCta.title")}
          </h3>

          <p className="mb-8 max-w-2xl text-xl">
            {t("result.companionCta.description")}
          </p>

          <Link href={`/${lang}/companions`}>
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.95 }}
              className="btn btn-lg bg-base-100 text-primary hover:bg-base-200"
            >
              {t("result.companionCta.button")}
            </motion.button>
          </Link>
        </div>
      </div>
    </section>
  );
}
