import { motion } from 'framer-motion';
import { WarningCircle } from '@phosphor-icons/react';
import CitationChip from './CitationChip';
import ProposedActionCard from './ProposedActionCard';

const NON_SUCCESS_LABEL = {
  needs_clarification: 'Needs clarification',
  insufficient_evidence: 'Insufficient evidence in the knowledge base',
  error: 'Something went wrong',
};

export default function MessageBubble({ message }) {
  const isUser = message.role === 'user';
  const statusLabel = !isUser && message.status && message.status !== 'success' ? NON_SUCCESS_LABEL[message.status] : null;

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
          {message.text}
        </div>

        {!isUser && message.sources?.length > 0 && (
          <div className="mt-2.5 space-y-1.5">
            <p className="px-1 text-[11px] font-medium uppercase tracking-wide text-ink-400">Sources</p>
            {message.sources.map((s) => (
              <CitationChip key={s.source_id + s.chunk_id} source={s} />
            ))}
          </div>
        )}

        {!isUser && message.actions?.length > 0 && (
          <div className="mt-2.5 space-y-2">
            {message.actions.map((a) => (
              <ProposedActionCard key={a.action_id} action={a} />
            ))}
          </div>
        )}
      </div>
    </motion.div>
  );
}
