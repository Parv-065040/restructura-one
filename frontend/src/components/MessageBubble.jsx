import { motion } from 'framer-motion';
import { WarningCircle } from '@phosphor-icons/react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

import CitationChip from './CitationChip';
import ProposedActionCard from './ProposedActionCard';

const NON_SUCCESS_LABEL = {
  needs_clarification: 'Needs clarification',
  insufficient_evidence: 'Insufficient evidence in the knowledge base',
  error: 'Something went wrong',
};

const markdownComponents = {
  h1: ({ children }) => (
    <h1 className="mb-3 mt-4 text-xl font-semibold text-ink-100">
      {children}
    </h1>
  ),
  h2: ({ children }) => (
    <h2 className="mb-2 mt-4 text-lg font-semibold text-ink-100">
      {children}
    </h2>
  ),
  h3: ({ children }) => (
    <h3 className="mb-2 mt-3 text-base font-semibold text-ink-100">
      {children}
    </h3>
  ),
  p: ({ children }) => (
    <p className="mb-3 last:mb-0">
      {children}
    </p>
  ),
  strong: ({ children }) => (
    <strong className="font-semibold text-ink-50">
      {children}
    </strong>
  ),
  ul: ({ children }) => (
    <ul className="mb-3 list-disc space-y-1 pl-5 last:mb-0">
      {children}
    </ul>
  ),
  ol: ({ children }) => (
    <ol className="mb-3 list-decimal space-y-1 pl-5 last:mb-0">
      {children}
    </ol>
  ),
  li: ({ children }) => (
    <li className="pl-1">{children}</li>
  ),
  blockquote: ({ children }) => (
    <blockquote className="my-3 border-l-2 border-signal-500/60 pl-3 text-ink-300">
      {children}
    </blockquote>
  ),
  table: ({ children }) => (
    <div className="my-3 overflow-x-auto rounded-lg border border-white/10">
      <table className="w-full border-collapse text-left text-[13px]">
        {children}
      </table>
    </div>
  ),
  thead: ({ children }) => (
    <thead className="bg-white/5 text-ink-100">
      {children}
    </thead>
  ),
  th: ({ children }) => (
    <th className="border-b border-white/10 px-3 py-2 font-semibold">
      {children}
    </th>
  ),
  td: ({ children }) => (
    <td className="border-b border-white/5 px-3 py-2 align-top">
      {children}
    </td>
  ),
  a: ({ children, href }) => (
    <a
      href={href}
      target="_blank"
      rel="noreferrer"
      className="text-signal-400 underline underline-offset-2"
    >
      {children}
    </a>
  ),
  code: ({ children, className }) => (
    <code
      className={`rounded bg-white/5 px-1 py-0.5 text-[0.9em] ${className ?? ''}`}
    >
      {children}
    </code>
  ),
  hr: () => <hr className="my-4 border-white/10" />,
};

export default function MessageBubble({ message }) {
  const isUser = message.role === 'user';

  const statusLabel =
    !isUser && message.status && message.status !== 'success'
      ? NON_SUCCESS_LABEL[message.status]
      : null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35, ease: [0.23, 1, 0.32, 1] }}
      className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}
    >
      <div className={`max-w-[min(640px,85%)] ${isUser ? '' : 'w-full'}`}>
        {statusLabel && (
          <div className="mb-1.5 flex items-center gap-1.5 text-[11px] font-medium text-amber-400">
            <WarningCircle size={12} weight="bold" />
            {statusLabel}
          </div>
        )}

        <div
          className={
            isUser
              ? 'rounded-2xl rounded-br-md bg-signal-500 px-4 py-2.5 text-[14.5px] leading-relaxed text-white'
              : 'rounded-2xl rounded-bl-md border border-white/8 bg-base-800/60 px-4 py-3 text-[14.5px] leading-relaxed text-ink-100'
          }
        >
          {isUser ? (
            message.text
          ) : (
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              components={markdownComponents}
            >
              {message.text ?? ''}
            </ReactMarkdown>
          )}
        </div>

        {!isUser && message.sources?.length > 0 && (
          <div className="mt-2.5 space-y-1.5">
            <p className="px-1 text-[11px] font-medium uppercase tracking-wide text-ink-400">
              Sources
            </p>

            {message.sources.map((s) => (
              <CitationChip
                key={s.source_id + s.chunk_id}
                source={s}
              />
            ))}
          </div>
        )}

        {!isUser && message.actions?.length > 0 && (
          <div className="mt-2.5 space-y-2">
            {message.actions.map((a) => (
              <ProposedActionCard
                key={a.action_id}
                action={a}
              />
            ))}
          </div>
        )}
      </div>
    </motion.div>
  );
}