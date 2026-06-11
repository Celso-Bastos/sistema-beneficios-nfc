import Link from "next/link";

type NavigationCardProps = {
  title: string;
  description: string;
  href: string;
};

export function NavigationCard({ title, description, href }: NavigationCardProps) {
  return (
    <Link href={href} className="navigation-card">
      <span className="navigation-card-title">{title}</span>
      <span className="navigation-card-description">{description}</span>
    </Link>
  );
}
