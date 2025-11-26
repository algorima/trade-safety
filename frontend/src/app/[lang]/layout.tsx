import { notFound } from "next/navigation";

import { getServerTranslationResources } from "@/i18n";
import { languages } from "@/i18n/config";
import { I18nProvider } from "@/providers/I18nProvider";

// eslint-disable-next-line @typescript-eslint/require-await
export async function generateStaticParams() {
  return languages.map((lang) => ({ lang }));
}

interface LangLayoutProps {
  children: React.ReactNode;
  params: { lang: string };
}

export default async function LangLayout({
  children,
  params,
}: LangLayoutProps) {
  const { lang } = params;
  if (!languages.includes(lang)) {
    notFound();
  }

  // 서버에서 번역 리소스를 미리 로드
  const { resources } = await getServerTranslationResources(lang);

  return (
    <html lang={lang}>
      <body>
        <I18nProvider lang={lang} resources={resources}>
          {children}
        </I18nProvider>
      </body>
    </html>
  );
}
