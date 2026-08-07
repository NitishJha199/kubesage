import axios from "axios";
import type { Diagnosis } from "../types/diagnosis";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export async function getDiagnosis(): Promise<Diagnosis[]> {
  const response = await api.get<Diagnosis[]>("/diagnose");
  return response.data;
}
