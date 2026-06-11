import type { Metadata } from "next";

import { AppHeader } from "@/components/AppHeader";
import "@/styles/globals.css";

export const metadata: Metadata = {
  title: "Sistema Benefícios NFC",
  description: "MVP web para identificação de clientes por NFC.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR">
      <body>
        <AppHeader />
        <main className="page-shell">{children}</main>
      </body>
    </html>
  );
}
