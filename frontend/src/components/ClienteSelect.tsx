"use client";

import { useEffect, useState } from "react";

import { listClientes } from "@/services/clientesService";
import type { Cliente } from "@/types/cliente";

type ClienteSelectProps = {
  value: string;
  onChange: (value: string) => void;
};

export function ClienteSelect({ value, onChange }: ClienteSelectProps) {
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let isMounted = true;

    async function loadClientes() {
      try {
        setIsLoading(true);
        const response = await listClientes(true);
        if (isMounted) {
          setClientes(response.items);
          setError("");
        }
      } catch {
        if (isMounted) {
          setError("Não foi possível carregar os clientes.");
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
    <label className="form-field" htmlFor="cliente_id">
      <span>Cliente</span>
      <select
        id="cliente_id"
        name="cliente_id"
        value={value}
        onChange={(event) => onChange(event.target.value)}
        disabled={isLoading}
        required
      >
        <option value="">{isLoading ? "Carregando clientes..." : "Selecione um cliente"}</option>
        {clientes.map((cliente) => (
          <option key={cliente.id} value={cliente.id}>
            {cliente.nome}
          </option>
        ))}
      </select>
      {error ? <small className="field-error">{error}</small> : null}
    </label>
  );
}
