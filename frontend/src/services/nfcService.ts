import { request } from "./api";
import type { NfcLookupResponse, NfcTagListResponse, VincularNfcPayload } from "@/types/nfc";

export async function listNfcTags(): Promise<NfcTagListResponse> {
  return request<NfcTagListResponse>("/api/nfc-tags");
}

export async function vincularNfcTag(payload: VincularNfcPayload): Promise<{ message: string }> {
  return request<{ message: string }>("/api/nfc-tags/vincular", {
    method: "POST",
    body: payload,
  });
}

export async function lookupNfcTag(uid: string): Promise<NfcLookupResponse> {
  return request<NfcLookupResponse>(`/api/nfc-tags/lookup/${encodeURIComponent(uid)}`);
}
