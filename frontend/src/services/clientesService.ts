import { request } from "./api";
import type { Cliente, ClienteCreate, ClienteListResponse } from "@/types/cliente";

export async function listClientes(ativo?: boolean): Promise<ClienteListResponse> {
  const searchParams = new URLSearchParams();
  if (ativo !== undefined) {
    searchParams.set("ativo", String(ativo));
  }

  const query = searchParams.toString();
  return request<ClienteListResponse>(`/api/clientes${query ? `?${query}` : ""}`);
}

export async function createCliente(payload: ClienteCreate): Promise<Cliente> {
  return request<Cliente>("/api/clientes", {
    method: "POST",
    body: payload,
  });
}
