export type DepartmentSlug =
  | "risk_restructuring"
  | "finance"
  | "sales"
  | "it"
  | "hr"
  | "marketing"
  | "legal_compliance"
  | "customer_support";

export interface DepartmentMeta {
  slug: DepartmentSlug;
  name: string;
  focus: string;
  prompts: string[];
}

// NOTE: slugs must match core.schemas.agent_contracts.Department values
// exactly — verify against the real enum before wiring this to the API.
export const DEPARTMENTS: DepartmentMeta[] = [
  {
    slug: "risk_restructuring",
    name: "Risk & Restructuring",
    focus: "Risk cases and restructuring decision support",
    prompts: [
      "Summarize the key risk factors in the current portfolio",
      "What restructuring options exist for a distressed account?",
    ],
  },
  {
    slug: "finance",
    name: "Finance",
    focus: "Financial analysis and finance knowledge",
    prompts: [
      "Walk me through this quarter's margin trend",
      "What's driving the variance against forecast?",
    ],
  },
  {
    slug: "sales",
    name: "Sales",
    focus: "Sales processes and sales knowledge",
    prompts: [
      "What's the standard discount approval process?",
      "Summarize best practices for enterprise deal negotiation",
    ],
  },
  {
    slug: "it",
    name: "IT",
    focus: "IT support and technology knowledge",
    prompts: [
      "What's the process for requesting new software access?",
      "Summarize our incident escalation policy",
    ],
  },
  {
    slug: "hr",
    name: "Human Resources",
    focus: "Human-resources policies and processes",
    prompts: [
      "What's our policy on parental leave?",
      "Summarize the performance review cycle",
    ],
  },
  {
    slug: "marketing",
    name: "Marketing",
    focus: "Marketing strategy and execution knowledge",
    prompts: [
      "Summarize our current brand positioning",
      "What channels have performed best this quarter?",
    ],
  },
  {
    slug: "legal_compliance",
    name: "Legal & Compliance",
    focus: "Compliance guidance and policy knowledge",
    prompts: [
      "What's our data retention policy?",
      "Summarize the vendor contract review process",
    ],
  },
  {
    slug: "customer_support",
    name: "Customer Support",
    focus: "Customer-service knowledge and response support",
    prompts: [
      "What's the standard refund policy?",
      "Summarize our SLA tiers",
    ],
  },
];

export function getDepartment(slug: string): DepartmentMeta | undefined {
  return DEPARTMENTS.find((d) => d.slug === slug);
}
