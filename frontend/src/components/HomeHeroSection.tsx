import { clsx } from "clsx";
import { useTranslation } from "react-i18next";
import { FaReddit, FaXTwitter } from "react-icons/fa6";

import { TRADE_SAFETY_NS } from "@/i18n";

export interface HomeHeroSectionProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  isLoading: boolean;
  error: string | null;
}

export function HomeHeroSection({
  value,
  onChange,
  onSubmit,
  isLoading,
  error,
}: HomeHeroSectionProps) {
  const { t } = useTranslation(TRADE_SAFETY_NS);

  const buttonContent = isLoading ? (
    <span className="loading loading-spinner loading-sm" />
  ) : (
    t("hero.checkSafety")
  );

  const isButtonDisabled = isLoading || !value.trim();

  return (
    <div className="flex w-full flex-col items-center justify-center">
      <div className="w-full lg:max-w-[720px]">
        <h1 className="mb-2 text-left text-3xl font-bold text-base-content sm:mb-8 sm:text-center sm:text-4xl md:mb-8">
          {t("hero.title")}
        </h1>
        <p className="mb-4 text-left text-sm text-base-content/70 sm:mb-8 sm:text-center sm:text-base md:mb-16">
          {t("hero.subtitle")}
        </p>

        <div className={clsx("mb-4", !error && "sm:mb-8 md:mb-12")}>
          <div className="relative hidden lg:block">
            <input
              type="text"
              className="input input-bordered h-[72px] w-full pr-36 text-sm placeholder:text-base-300 focus:outline-none"
              placeholder={t("hero.placeholder")}
              aria-label={t("hero.placeholder")}
              value={value}
              onChange={(e) => onChange(e.target.value)}
              disabled={isLoading}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !isButtonDisabled) {
                  onSubmit();
                }
              }}
            />
            <button
              className="btn btn-neutral absolute right-2 top-1/2 h-[56px] min-h-0 -translate-y-1/2 !animate-none px-6 font-bold text-neutral-content"
              onClick={onSubmit}
              disabled={isButtonDisabled}
            >
              {buttonContent}
            </button>
          </div>

          <div className="block lg:hidden">
            <div className="relative h-[400px] w-full overflow-hidden rounded-xl border border-base-300 bg-base-100">
              {!value && (
                <div
                  className="pointer-events-none absolute inset-0 overflow-hidden p-5 pb-24 text-base text-base-300"
                  aria-hidden="true"
                >
                  <div className="whitespace-pre-line leading-relaxed">
                    <p className="mb-4 text-base-300">
                      {t("hero.placeholder")}
                    </p>
                    {t("hero.placeholderExample")}
                  </div>
                </div>
              )}

              <div className="absolute inset-0 overflow-hidden pb-24">
                <textarea
                  className="textarea size-full resize-none overflow-auto bg-transparent p-4 leading-6 text-base-content focus:outline-none"
                  value={value}
                  aria-label={t("hero.placeholder")}
                  onChange={(e) => onChange(e.target.value)}
                  disabled={isLoading}
                  placeholder=""
                />
              </div>

              <div className="absolute inset-x-4 bottom-4 z-10">
                <button
                  className="btn btn-neutral h-16 w-full text-base font-medium text-neutral-content"
                  onClick={onSubmit}
                  disabled={isButtonDisabled}
                >
                  {buttonContent}
                </button>
              </div>
            </div>
          </div>
        </div>

        {error && (
          <div className="alert alert-error mb-6 flex items-center gap-2 text-sm">
            <span>{error}</span>
          </div>
        )}

        <p className="mb-4 text-left text-xs text-base-content/60 sm:mb-8 sm:text-center md:mb-12">
          {t("hero.disclaimer")}
        </p>

        <div className="flex items-center justify-start gap-6 sm:justify-center">
          <a
            href="https://x.com"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="X"
          >
            <FaXTwitter className="size-6 text-base-content transition-colors hover:text-base-content/70" />
          </a>
          <a
            href="https://reddit.com"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="Reddit"
          >
            <FaReddit className="size-6 text-base-content transition-colors hover:text-base-content/70" />
          </a>
        </div>
      </div>
    </div>
  );
}
