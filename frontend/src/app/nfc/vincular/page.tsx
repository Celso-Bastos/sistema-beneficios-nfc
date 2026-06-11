"use client";

import { FormEvent, useEffect, useRef, useState } from "react";

import { ClienteSelect } from "@/components/ClienteSelect";
import { FeedbackMessage } from "@/components/FeedbackMessage";
import { FormInput } from "@/components/FormInput";
import { LoadingButton } from "@/components/LoadingButton";
import { ApiRequestError } from "@/services/api";
import { vincularNfcTag } from "@/services/nfcService";

function normalizeUid(value: string): string {
  return value.trim().replace(/\s+/g, "").toUpperCase();
}

export default function VincularNfcPage() {
  const uidInputRef = useRef<HTMLInputElement>(null);
  const [uid, setUid] = useState("");
  const [clienteId, setClienteId] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    uidInputRef.current?.focus();
  }, []);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSubmitting(true);
    setSuccess("");
    setError("");

    try {
      await vincularNfcTag({ uid: normalizeUid(uid), cliente_id: clienteId });
      setUid("");
      setClienteId("");
      setSuccess("Tag vinculada com sucesso.");
      window.setTimeout(() => uidInputRef.current?.focus(), 0);
    } catch (requestError) {
      setError(
        requestError instanceof ApiRequestError
          ? requestError.message
          : "Não foi possível vincular a tag NFC.",
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <section className="form-page">
      <div className="page-heading">
        <p className="eyebrow">NFC</p>
        <h1>Vincular NFC ao cliente</h1>
        <p>Clique no campo UID e aproxime a tag NFC do leitor.</p>
      </div>

      <form className="form-panel" onSubmit={handleSubmit}>
        <FormInput
          ref={uidInputRef}
          label="UID"
          name="uid"
          value={uid}
          required
          className="uid-input"
          onChange={(event) => setUid(normalizeUid(event.target.value))}
        />
        <ClienteSelect value={clienteId} onChange={setClienteId} />

        {success ? <FeedbackMessage type="success" message={success} /> : null}
        {error ? <FeedbackMessage type="error" message={error} /> : null}

        <LoadingButton
          isLoading={isSubmitting}
          type="submit"
          loadingText="Vinculando..."
          disabled={!uid || !clienteId}
        >
          Vincular tag
        </LoadingButton>
      </form>
    </section>
  );
}
