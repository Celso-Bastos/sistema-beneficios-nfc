"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { FeedbackMessage } from "@/components/FeedbackMessage";
import { listClientes } from "@/services/clientesService";
import type { Cliente } from "@/types/cliente";

export default function ClientesPage() {
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let isMounted = true;

    async function loadClientes() {
      try {
        setIsLoading(true);
        const response = await listClientes();
        if (isMounted) {
          setClientes(response.items);
          setError("");
        }
      } catch {
        if (isMounted) {
          setError("Não foi possível carregar a lista de clientes.");
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    loadClientes();

    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <section className="stack">
      <div className="page-heading row-between">
        <div>
          <p className="eyebrow">Clientes</p>
          <h1>Clientes cadastrados</h1>
        </div>
        <Link href="/clientes/novo" className="button button-primary">
          Novo cliente
        </Link>
      </div>

      {isLoading ? <FeedbackMessage type="info" message="Carregando clientes..." /> : null}
      {error ? <FeedbackMessage type="error" message={error} /> : null}

      {!isLoading && !error && clientes.length === 0 ? (
        <div className="empty-state">Nenhum cliente cadastrado ainda.</div>
      ) : null}

      {clientes.length > 0 ? (
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Nome</th>
                <th>Telefone</th>
                <th>Email</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {clientes.map((cliente) => (
                <tr key={cliente.id}>
                  <td>{cliente.nome}</td>
                  <td>{cliente.telefone || "-"}</td>
                  <td>{cliente.email || "-"}</td>
                  <td>
                    <span className={`status-pill ${cliente.ativo ? "is-active" : "is-inactive"}`}>
                      {cliente.ativo ? "Ativo" : "Inativo"}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : null}
    </section>
  );
}
