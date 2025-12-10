import "../src/styles/globals.css";

import type { Preview, Decorator } from "@storybook/react";
import { I18nextProvider } from "react-i18next";
import { createClientI18nInstance, TRADE_SAFETY_NS } from "../src/i18n";
import { tradeSafetyTranslations } from "../src/i18n/translations";
import { fallbackLng, languages, languageNames } from "../src/i18n/config";

const withI18next: Decorator = (Story, context) => {
  const lang = context.globals.locale as string;

  // Create i18n instance with pre-loaded resources for the selected language
  const i18nInstance = createClientI18nInstance(lang, {
    [lang]: {
      [TRADE_SAFETY_NS]: tradeSafetyTranslations[lang],
    },
  });

  return (
    <I18nextProvider i18n={i18nInstance}>
      <Story {...context} />
    </I18nextProvider>
  );
};

const preview: Preview = {
  globalTypes: {
    locale: {
      name: "Locale",
      description: "Internationalization locale",
      defaultValue: fallbackLng,
      toolbar: {
        icon: "globe",
        items: languages.map((lang) => ({
          value: lang,
          right: lang,
          title: languageNames[lang],
        })),
      },
    },
  },
  parameters: {
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
  },
  decorators: [withI18next],
};

export default preview;
