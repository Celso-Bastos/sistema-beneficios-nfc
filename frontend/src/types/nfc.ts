export type NfcTag = {
  id: string;
  uid: string;
  cliente_id?: string | null;
  status: "ativa" | "inativa" | string;
  created_at?: string;
  updated_at?: string;
};

export type NfcTagListResponse = {
  items: NfcTag[];
  limit: number;
  offset: number;
  total: number;
};

export type NfcLookupCliente = {
  id: string;
  nome: string;
  telefone?: string | null;
};

export type NfcLookupResponse = {
  uid: string;
  cliente: NfcLookupCliente;
};

export type VincularNfcPayload = {
  uid: string;
  cliente_id: string;
};
