import { forwardRef } from "react";
import type { InputHTMLAttributes } from "react";

type FormInputProps = InputHTMLAttributes<HTMLInputElement> & {
  label: string;
  helperText?: string;
};

export const FormInput = forwardRef<HTMLInputElement, FormInputProps>(function FormInput(
  { label, helperText, id, ...props },
  ref,
) {
  const inputId = id ?? props.name;

  return (
    <label className="form-field" htmlFor={inputId}>
      <span>{label}</span>
      <input id={inputId} ref={ref} {...props} />
      {helperText ? <small>{helperText}</small> : null}
    </label>
  );
});
