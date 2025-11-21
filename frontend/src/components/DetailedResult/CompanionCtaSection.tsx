"use client";

import { ChatBubbleOvalLeftEllipsisIcon } from "@heroicons/react/24/solid";
import { motion } from "framer-motion";
import Link from "next/link";
import { useTranslation } from "react-i18next";

export function CompanionCtaSection() {
  const { t, i18n } = useTranslation();
  const lang = i18n.language;

  return (
    <section className="hero min-h-[30vh] rounded-3xl bg-primary text-primary-content">
      <div className="hero-content text-center">
        <div>
          <ChatBubbleOvalLeftEllipsisIcon className="mx-auto mb-6 size-20" />

          <h3 className="mb-4 text-4xl font-bold">
            {t("page.tradeSafety.result.companionCta.title")}
          </h3>

          <p className="mb-8 max-w-2xl text-xl">
            {t("page.tradeSafety.result.companionCta.description")}
          </p>

          <Link href={`/${lang}/companions`}>
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.95 }}
              className="btn btn-lg bg-base-100 text-primary hover:bg-base-200"
            >
              {t("page.tradeSafety.result.companionCta.button")}
            </motion.button>
          </Link>
        </div>
      </div>
    </section>
  );
}
