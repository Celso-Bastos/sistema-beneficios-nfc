"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { FeedbackMessage } from "@/components/FeedbackMessage";
import { listNfcTags } from "@/services/nfcService";
import type { NfcTag } from "@/types/nfc";

export default function NfcPage() {
  const [tags, setTags] = useState<NfcTag[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let isMounted = true;

    async function loadTags() {
      try {
        setIsLoading(true);
        const response = await listNfcTags();
        if (isMounted) {
          setTags(response.items);
          setError("");
        }
      } catch {
        if (isMounted) {
          setError("Não foi possível carregar as tags NFC.");
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    loadTags();

    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <section className="stack">
      <div className="page-heading row-between">
        <div>
          <p className="eyebrow">NFC</p>
          <h1>NFC Tags</h1>
        </div>
        <div className="button-row">
          <Link href="/nfc/vincular" className="button button-primary">
            Vincular NFC
          </Link>
          <Link href="/nfc/consultar" className="button button-secondary">
            Consultar NFC
          </Link>
        </div>
      </div>

      {isLoading ? <FeedbackMessage type="info" message="Carregando tags NFC..." /> : null}
      {error ? <FeedbackMessage type="error" message={error} /> : null}

      {!isLoading && !error && tags.length === 0 ? (
        <div className="empty-state">Nenhuma tag NFC cadastrada ainda.</div>
      ) : null}

      {tags.length > 0 ? (
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>UID</th>
                <th>Status</th>
                <th>Cliente vinculado</th>
              </tr>
            </thead>
            <tbody>
              {tags.map((tag) => (
                <tr key={tag.id}>
                  <td className="mono">{tag.uid}</td>
                  <td>
                    <span className={`status-pill ${tag.status === "ativa" ? "is-active" : "is-inactive"}`}>
                      {tag.status}
                    </span>
                  </td>
                  <td>{tag.cliente_id ? "Sim" : "Não"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : null}
    </section>
  );
}
