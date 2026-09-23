import { useEffect, useRef } from 'react';
import { useParams, Navigate } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import ChatHeader from '../components/ChatHeader';
import MessageBubble from '../components/MessageBubble';
import ThinkingIndicator from '../components/ThinkingIndicator';
import SuggestedPrompts from '../components/SuggestedPrompts';
import Composer from '../components/Composer';
import { getDepartment } from '../data/departments';
import { useChat } from '../hooks/useChat';

export default function Chat() {
  const { department: slug } = useParams();
  const department = getDepartment(slug);
  const { messages, isThinking, send, reset } = useChat(slug ?? 'finance');
  const scrollRef = useRef(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' });
  }, [messages, isThinking]);

  if (!department) return <Navigate to="/chat/finance" replace />;

  const Icon = department.icon;

  return (
    <div className="flex h-[100dvh] flex-col md:flex-row">
      <Sidebar activeSlug={department.slug} />

      <div className="flex min-w-0 flex-1 flex-col">
        <ChatHeader department={department} onReset={reset} />

        <div ref={scrollRef} className="flex-1 overflow-y-auto px-4 py-6 sm:px-6">
          <div className="mx-auto flex max-w-[760px] flex-col gap-4">
            {messages.length === 0 && (
              <div className="animate-fade-up rounded-2xl border border-white/8 bg-base-800/30 p-6">
                <span className="grid h-11 w-11 place-items-center rounded-xl border border-white/10 bg-base-900/60">
                  <Icon size={20} weight="duotone" className="text-current-400" />
                </span>
                <h2 className="mt-4 text-base font-semibold text-ink-100">{department.description}</h2>
                <p className="mt-3 text-[13px] font-medium uppercase tracking-wide text-ink-400">Try asking</p>
                <div className="mt-2.5">
                  <SuggestedPrompts prompts={department.prompts} onPick={send} />
                </div>
              </div>
            )}

            {messages.map((m) => (
              <MessageBubble key={m.id} message={m} />
            ))}

            {isThinking && <ThinkingIndicator label={`One is checking the ${department.short} knowledge base`} />}
          </div>
        </div>

        <Composer onSend={send} disabled={isThinking} departmentName={department.name} />
      </div>
    </div>
  );
}
