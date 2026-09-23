import { useCallback, useState } from 'react';
import { callAgent, AgentApiError } from '../lib/api';
import { mockAgentCall } from '../lib/mockAgent';

const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true';

// Conversation history keyed by department slug, so switching departments
// (department isolation, per the real system's requirement) never bleeds
// context between agents. Held at module scope so it survives navigation
// within the session without needing a global store.
const store = {};

function ensure(slug) {
  if (!store[slug]) store[slug] = [];
  return store[slug];
}

export function useChat(departmentSlug) {
  const [messages, setMessages] = useState(() => [...ensure(departmentSlug)]);
  const [isThinking, setIsThinking] = useState(false);

  const send = useCallback(
    async (text) => {
      if (!text.trim()) return;
      const userMsg = { id: crypto.randomUUID(), role: 'user', text };
      const historyBefore = ensure(departmentSlug);
      const next = [...historyBefore, userMsg];
      store[departmentSlug] = next;
      setMessages(next);
      setIsThinking(true);

      try {
        const call = USE_MOCK ? mockAgentCall : callAgent;
        const response = await call({
          department: departmentSlug,
          message: text,
          history: historyBefore,
        });

        const assistantMsg = {
          id: crypto.randomUUID(),
          role: 'assistant',
          text: response.answer,
          status: response.status,
          sources: response.sources ?? [],
          actions: response.actions ?? [],
        };
        const withReply = [...store[departmentSlug], assistantMsg];
        store[departmentSlug] = withReply;
        setMessages(withReply);
      } catch (err) {
        const errorMsg = {
          id: crypto.randomUUID(),
          role: 'assistant',
          text:
            err instanceof AgentApiError
              ? err.message
              : 'Something went wrong reaching the assistant. Please try again.',
          status: 'error',
          sources: [],
          actions: [],
        };
        const withError = [...store[departmentSlug], errorMsg];
        store[departmentSlug] = withError;
        setMessages(withError);
      } finally {
        setIsThinking(false);
      }
    },
    [departmentSlug]
  );

  const reset = useCallback(() => {
    store[departmentSlug] = [];
    setMessages([]);
  }, [departmentSlug]);

  return { messages, isThinking, send, reset };
}
