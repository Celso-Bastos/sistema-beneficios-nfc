"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";

import { FeedbackMessage } from "@/components/FeedbackMessage";
import { FormInput } from "@/components/FormInput";
import { LoadingButton } from "@/components/LoadingButton";
import { ApiRequestError } from "@/services/api";
import { createCliente } from "@/services/clientesService";
import type { ClienteCreate } from "@/types/cliente";

const initialForm: ClienteCreate = {
  nome: "",
  cpf: "",
  telefone: "",
  email: "",
};

function cleanPayload(form: ClienteCreate): ClienteCreate {
  return Object.fromEntries(
    Object.entries(form).filter(([, value]) => value.trim() !== ""),
  ) as ClienteCreate;
}

export default function NovoClientePage() {
  const [form, setForm] = useState<ClienteCreate>(initialForm);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");

  function updateField(field: keyof ClienteCreate, value: string) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSubmitting(true);
    setSuccess("");
    setError("");

    try {
      await createCliente(cleanPayload(form));
      setForm(initialForm);
      setSuccess("Cliente cadastrado com sucesso.");
    } catch (requestError) {
      setError(
        requestError instanceof ApiRequestError
          ? requestError.message
          : "Não foi possível cadastrar o cliente.",
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <section className="form-page">
      <div className="page-heading">
        <p className="eyebrow">Clientes</p>
        <h1>Novo cliente</h1>
      </div>

      <form className="form-panel" onSubmit={handleSubmit}>
        <FormInput
          label="Nome"
          name="nome"
          value={form.nome}
          minLength={2}
          required
          onChange={(event) => updateField("nome", event.target.value)}
        />
        <FormInput
          label="CPF"
          name="cpf"
          value={form.cpf}
          helperText="Use dados fictícios nos testes."
          onChange={(event) => updateField("cpf", event.target.value)}
        />
        <FormInput
          label="Telefone"
          name="telefone"
          value={form.telefone}
          onChange={(event) => updateField("telefone", event.target.value)}
        />
        <FormInput
          label="Email"
          name="email"
          type="email"
          value={form.email}
          onChange={(event) => updateField("email", event.target.value)}
        />

        {success ? <FeedbackMessage type="success" message={success} /> : null}
        {error ? <FeedbackMessage type="error" message={error} /> : null}

        <div className="button-row">
          <LoadingButton isLoading={isSubmitting} type="submit" loadingText="Salvando...">
            Cadastrar cliente
          </LoadingButton>
          <Link href="/clientes" className="button button-secondary">
            Voltar para lista
          </Link>
        </div>
      </form>
    </section>
  );
}
