"use client";

import { useState, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Send } from "lucide-react";
import { MessageBubble, type ChatMessage } from "./MessageBubble";
import { SourcesPanel } from "./SourcesPanel";
import { streamChat } from "@/lib/api";
import type { DepartmentMeta } from "@/lib/departments";

function newId() {
  return Math.random().toString(36).slice(2);
}

export function ChatWindow({ dept, sessionId }: { dept: DepartmentMeta; sessionId: string }) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [citations, setCitations] = useState<Record<string, unknown>[]>([]);
  const [proposedActions, setProposedActions] = useState<Record<string, unknown>[]>([]);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const closeRef = useRef<(() => void) | null>(null);

  function send(query: string) {
    if (!query.trim() || busy) return;
    setErrorMsg(null);
    setInput("");

    const userMsg: ChatMessage = { id: newId(), role: "user", content: query };
    const assistantId = newId();
    setMessages((prev) => [
      ...prev,
      userMsg,
      { id: assistantId, role: "assistant", content: "", streaming: true },
    ]);
    setBusy(true);

    const history = messages.map((m) => ({ role: m.role, content: m.content }));

    closeRef.current = streamChat(
      {
        department: dept.slug,
        query,
        session_id: sessionId,
        conversation_history: history,
      },
      {
        onToken: (chunk) => {
          setMessages((prev) =>
            prev.map((m) => (m.id === assistantId ? { ...m, content: m.content + chunk } : m))
          );
        },
        onDone: (final) => {
          setMessages((prev) =>
            prev.map((m) => (m.id === assistantId ? { ...m, streaming: false } : m))
          );
          setCitations(final.citations ?? []);
          setProposedActions(final.proposed_actions ?? []);
          setBusy(false);
        },
        onError: (message) => {
          setErrorMsg(message);
          setMessages((prev) =>
            prev.map((m) =>
              m.id === assistantId ? { ...m, streaming: false, content: m.content || "" } : m
            )
          );
          setBusy(false);
        },
      }
    );
  }

  return (
    <div className="flex flex-col gap-6 lg:flex-row">
      <div className="flex min-h-[60vh] flex-1 flex-col panel p-5">
        <div className="flex-1 space-y-4 overflow-y-auto">
          {messages.length === 0 ? (
            <div className="flex h-full flex-col items-start justify-center gap-3 py-12">
              <p className="text-sm text-muted">Try asking:</p>
              <div className="flex flex-wrap gap-2">
                {dept.prompts.map((p) => (
                  <button
                    key={p}
                    onClick={() => send(p)}
                    className="rounded-card border border-border px-3 py-2 text-left text-xs text-muted transition-colors hover:border-accent-teal/60 hover:text-ink"
                  >
                    {p}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <AnimatePresence initial={false}>
              {messages.map((m) => (
                <MessageBubble key={m.id} message={m} />
              ))}
            </AnimatePresence>
          )}

          {errorMsg && (
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="rounded-card border border-status-bad/40 bg-status-bad/5 p-3 text-xs text-status-bad"
            >
              {errorMsg}
            </motion.p>
          )}
        </div>

        <form
          onSubmit={(e) => {
            e.preventDefault();
            send(input);
          }}
          className="mt-4 flex items-center gap-2 border-t border-border pt-4"
        >
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={`Ask ${dept.name}...`}
            className="flex-1 rounded-card border border-border bg-base px-4 py-2.5 text-sm text-ink placeholder:text-muted focus:border-accent-teal/60"
            disabled={busy}
          />
          <button
            type="submit"
            disabled={busy || !input.trim()}
            className="flex h-10 w-10 items-center justify-center rounded-card bg-accent-teal text-base transition-opacity disabled:opacity-40"
            aria-label="Send"
          >
            <Send size={16} />
          </button>
        </form>
      </div>

      <SourcesPanel citations={citations} proposedActions={proposedActions} />
    </div>
  );
}
