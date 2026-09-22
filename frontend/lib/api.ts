export interface ChatRequestPayload {
  department: string;
  query: string;
  session_id: string;
  user_role?: string;
  permissions?: string[];
  conversation_history?: { role: string; content: string }[];
}

export interface ChatResponsePayload {
  department: string;
  answer: string;
  citations: Record<string, unknown>[];
  proposed_actions: Record<string, unknown>[];
  raw: Record<string, unknown>;
}

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";
const WS_BASE = API_BASE.replace(/^http/, "ws");

export async function sendChat(payload: ChatRequestPayload): Promise<ChatResponsePayload> {
  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    throw new Error(`Chat request failed (${res.status})`);
  }
  return res.json();
}

type StreamHandlers = {
  onToken: (chunk: string) => void;
  onDone: (final: { citations: Record<string, unknown>[]; proposed_actions: Record<string, unknown>[] }) => void;
  onError: (message: string) => void;
};

/**
 * Opens a fresh WebSocket per request (simplest correct approach for a
 * scaffold). For high-traffic production, upgrade to a persisted
 * connection with a session/request id multiplexer.
 */
export function streamChat(payload: ChatRequestPayload, handlers: StreamHandlers): () => void {
  const ws = new WebSocket(`${WS_BASE}/ws/chat`);

  ws.onopen = () => ws.send(JSON.stringify(payload));

  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (msg.type === "token") handlers.onToken(msg.content);
    else if (msg.type === "done") handlers.onDone(msg);
    else if (msg.type === "error") handlers.onError(msg.message);
  };

  ws.onerror = () => handlers.onError("Connection error — check the API is running.");

  return () => ws.close();
}
