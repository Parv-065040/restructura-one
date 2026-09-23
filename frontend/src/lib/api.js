// Talks to api/main.py in the backend repo (FastAPI wrapper around
// AgentOrchestrator). Returns the response shaped exactly like the
// backend's AgentResponse contract — department, answer, status, sources,
// actions, metadata — so components render the real thing directly with
// no translation layer in between.

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export class AgentApiError extends Error {}

/**
 * @param {{department: string, message: string, history: {role: string, text: string}[]}} args
 */
export async function callAgent({ department, message, history }) {
  let res;
  try {
    res = await fetch(`${API_BASE}/api/departments/${department}/ask`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message,
        // The frontend stores messages as {role, text}; the backend's
        // conversation history helper expects {role, content}.
        history: history.map((m) => ({ role: m.role, content: m.text })),
      }),
    });
  } catch {
    throw new AgentApiError(
      `Can't reach the assistant API at ${API_BASE}. Is the backend running (uvicorn api.main:app)?`
    );
  }

  if (!res.ok) {
    let detail = `Request failed (${res.status}).`;
    try {
      const body = await res.json();
      if (body?.detail) detail = body.detail;
    } catch {
      // response wasn't JSON — keep the generic message
    }
    throw new AgentApiError(detail);
  }

  return res.json();
}
