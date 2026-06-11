export type Cliente = {
  id: string;
  nome: string;
  cpf?: string | null;
  telefone?: string | null;
  email?: string | null;
  ativo: boolean;
  created_at: string;
  updated_at: string;
};

export type ClienteCreate = {
  nome: string;
  cpf?: string;
  telefone?: string;
  email?: string;
};

export type ClienteListResponse = {
  items: Cliente[];
  limit: number;
  offset: number;
  total: number;
};
