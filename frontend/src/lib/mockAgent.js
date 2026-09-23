// Used only when VITE_USE_MOCK=true (see .env.example) — for working on
// the frontend without the Python backend running. Shaped identically to
// the real backend's AgentResponse (core/schemas/agent_contracts.py):
// department, answer, status, sources[], actions[], metadata. Because the
// shape matches exactly, src/lib/api.js is the only file that changes
// when switching between mock and real.

const SOURCE_POOL = {
  finance: ['q3_cost_review.md', 'capex_plan_fy26.md', 'vendor_contracts_summary.md'],
  risk_restructuring: ['covenant_schedule.md', 'restructuring_playbook.md', 'supplier_risk_matrix.md'],
  sales: ['pipeline_snapshot_q3.md', 'account_health_scores.md', 'retention_playbook.md'],
  it: ['systems_inventory.md', 'integration_runbook.md', 'vendor_risk_register.md'],
  hr: ['workforce_plan_fy26.md', 'attrition_report.md', 'change_comms_templates.md'],
  marketing: ['positioning_brief.md', 'segment_research.md', 'press_guidelines.md'],
  legal_compliance: ['disclosure_requirements.md', 'compliance_tracker.md', 'contract_terms_master.md'],
  customer_support: ['support_macros.md', 'escalation_log.md', 'service_continuity_plan.md'],
};

function pick(arr, n) {
  const copy = [...arr];
  const out = [];
  while (out.length < n && copy.length) {
    out.push(copy.splice(Math.floor(Math.random() * copy.length), 1)[0]);
  }
  return out;
}

export async function mockAgentCall({ department, message }) {
  await new Promise((r) => setTimeout(r, 900 + Math.random() * 700));

  const files = SOURCE_POOL[department] ?? SOURCE_POOL.finance;
  const sources = pick(files, Math.min(2, files.length)).map((file, i) => ({
    source_id: file.replace('.md', ''),
    document_name: file,
    excerpt:
      'Retrieved passage relevant to this query would appear here, pulled from the department-scoped knowledge base.',
    chunk_id: `${file.replace('.md', '')}-${i}`,
    relevance_score: 0.6 + Math.random() * 0.35,
  }));

  const actions =
    Math.random() > 0.5
      ? [
          {
            action_id: crypto.randomUUID(),
            action_type: 'review',
            description: 'A concrete, reviewable action derived from the answer above.',
            requires_approval: true,
            status: 'proposed',
            parameters: {},
          },
        ]
      : [];

  return {
    department,
    answer: `Based on the ${department.replace('_', ' ')} knowledge base, here is a grounded response to: "${message}". In production this streams from the shared Groq gateway (openai/gpt-oss-120b) with retrieval-augmented context from this department's synthetic knowledge base.`,
    status: 'success',
    sources,
    actions,
    metadata: {},
  };
}
