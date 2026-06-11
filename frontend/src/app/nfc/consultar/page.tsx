"use client";

import { useEffect, useRef, useState } from "react";

import { FeedbackMessage } from "@/components/FeedbackMessage";
import { FormInput } from "@/components/FormInput";
import { LoadingButton } from "@/components/LoadingButton";
import { ApiRequestError } from "@/services/api";
import { lookupNfcTag } from "@/services/nfcService";
import type { NfcLookupResponse } from "@/types/nfc";

function normalizeUid(value: string): string {
  return value.trim().replace(/\s+/g, "").toUpperCase();
}

export default function ConsultarNfcPage() {
  const uidInputRef = useRef<HTMLInputElement>(null);
  const [uid, setUid] = useState("");
  const [result, setResult] = useState<NfcLookupResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    uidInputRef.current?.focus();
  }, []);

  useEffect(() => {
    if (!uid) {
      return;
    }

    const timeoutId = window.setTimeout(() => {
      handleLookup(uid);
    }, 450);

    return () => window.clearTimeout(timeoutId);
  }, [uid]);

  async function handleLookup(nextUid = uid) {
    const normalizedUid = normalizeUid(nextUid);
    if (!normalizedUid) {
      return;
    }

    setIsLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await lookupNfcTag(normalizedUid);
      setResult(response);
    } catch (requestError) {
      setError(
        requestError instanceof ApiRequestError
          ? requestError.message
          : "Não foi possível consultar a tag NFC.",
      );
    } finally {
      setIsLoading(false);
    }
  }

  function clearLookup() {
    setUid("");
    setResult(null);
    setError("");
    window.setTimeout(() => uidInputRef.current?.focus(), 0);
  }

  return (
    <section className="lookup-page">
      <div className="page-heading">
        <p className="eyebrow">Consulta NFC</p>
        <h1>Aproxime a tag NFC do leitor</h1>
        <p>O UID digitado pelo leitor será consultado automaticamente.</p>
      </div>

      <div className="lookup-panel">
        <FormInput
          ref={uidInputRef}
          label="UID da tag"
          name="uid"
          value={uid}
          className="uid-input uid-input-large"
          autoComplete="off"
          onChange={(event) => setUid(normalizeUid(event.target.value))}
        />

        <div className="button-row">
          <LoadingButton
            isLoading={isLoading}
            type="button"
            loadingText="Consultando..."
            disabled={!uid}
            onClick={() => handleLookup()}
          >
            Consultar
          </LoadingButton>
          <button className="button button-secondary" type="button" onClick={clearLookup}>
            Limpar e ler outra tag
          </button>
        </div>

        {isLoading ? <FeedbackMessage type="info" message="Consultando tag NFC..." /> : null}
        {error ? <FeedbackMessage type="error" message={error} /> : null}

        {result ? (
          <div className="result-card">
            <span className="status-pill is-active">Encontrado</span>
            <dl>
              <div>
                <dt>UID</dt>
                <dd className="mono">{result.uid}</dd>
              </div>
              <div>
                <dt>Cliente</dt>
                <dd>{result.cliente.nome}</dd>
              </div>
              <div>
                <dt>Telefone</dt>
                <dd>{result.cliente.telefone || "-"}</dd>
              </div>
            </dl>
          </div>
        ) : null}
      </div>
    </section>
  );
}
