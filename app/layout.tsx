import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "MDfy — Conversor para Markdown",
  description: "Converta documentos, planilhas, e-books, imagens e pacotes para Markdown.",
  other: {
    "codex-preview": "development",
  },
  icons: {
    icon: process.env.GITHUB_PAGES === "true" ? "/MDfy/favicon.svg" : "/favicon.svg",
    shortcut: process.env.GITHUB_PAGES === "true" ? "/MDfy/favicon.svg" : "/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR">
      <body className="antialiased">{children}</body>
    </html>
  );
}
