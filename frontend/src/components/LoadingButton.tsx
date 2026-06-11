import type { ButtonHTMLAttributes, ReactNode } from "react";

type LoadingButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  isLoading: boolean;
  children: ReactNode;
  loadingText?: string;
};

export function LoadingButton({
  isLoading,
  children,
  loadingText = "Processando...",
  disabled,
  ...props
}: LoadingButtonProps) {
  return (
    <button className="button button-primary" disabled={disabled || isLoading} {...props}>
      {isLoading ? loadingText : children}
    </button>
  );
}
