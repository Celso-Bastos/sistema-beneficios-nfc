import Link from "next/link";

export function AppHeader() {
  return (
    <header className="app-header">
      <Link href="/" className="brand">
        Sistema Benefícios NFC
      </Link>
      <nav className="top-nav" aria-label="Navegação principal">
        <Link href="/clientes">Clientes</Link>
        <Link href="/clientes/novo">Novo cliente</Link>
        <Link href="/nfc">NFC Tags</Link>
        <Link href="/nfc/vincular">Vincular NFC</Link>
        <Link href="/nfc/consultar">Consultar NFC</Link>
      </nav>
    </header>
  );
}
