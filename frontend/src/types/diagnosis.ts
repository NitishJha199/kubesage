export interface AIExplanation {
  summary: string;

  root_cause: string;

  impact: string;

  verification_steps: string[];

  kubectl_commands: string[];

  prevention: string;
}

export interface Diagnosis {
  resource_type: string;

  resource_name: string;

  namespace: string;

  diagnosis: string;

  severity: string;

  confidence: number;

  evidence: string[];

  recommendation: string;

  ai: AIExplanation;
}
