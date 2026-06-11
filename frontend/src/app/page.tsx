import { NavigationCard } from "@/components/NavigationCard";

const navigationItems = [
  {
    title: "Clientes",
    description: "Consultar clientes cadastrados no MVP.",
    href: "/clientes",
  },
  {
    title: "Novo Cliente",
    description: "Cadastrar um cliente para vínculo NFC.",
    href: "/clientes/novo",
  },
  {
    title: "NFC Tags",
    description: "Listar tags NFC já cadastradas.",
    href: "/nfc",
  },
  {
    title: "Vincular NFC",
    description: "Associar UID de tag a um cliente ativo.",
    href: "/nfc/vincular",
  },
  {
    title: "Consultar NFC",
    description: "Ler UID digitado pelo leitor e localizar cliente.",
    href: "/nfc/consultar",
  },
];

export default function HomePage() {
  return (
    <section className="stack">
      <div className="page-heading">
        <p className="eyebrow">MVP web</p>
        <h1>Sistema Benefícios NFC</h1>
        <p>
          Identifique clientes a partir do UID digitado pelo leitor NFC em um
          campo de texto comum.
        </p>
      </div>

      <div className="navigation-grid">
        {navigationItems.map((item) => (
          <NavigationCard key={item.href} {...item} />
        ))}
      </div>
    </section>
  );
}
