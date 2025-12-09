export const fallbackLng = "en";
export const languages = [fallbackLng, "ko", "ja", "zh", "es", "id"] as const;

export const languageNames: Record<(typeof languages)[number], string> = {
  en: "English",
  ko: "한국어",
  ja: "日本語",
  zh: "中文",
  es: "Español",
  id: "Bahasa Indonesia",
};
