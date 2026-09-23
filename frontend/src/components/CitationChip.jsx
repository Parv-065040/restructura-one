import { useState } from 'react';
import { FileText, CaretDown } from '@phosphor-icons/react';

// source matches core/schemas/agent_contracts.py::SourceCitation
// { source_id, document_name, excerpt, page, chunk_id, relevance_score }
export default function CitationChip({ source }) {
  const [open, setOpen] = useState(false);

  return (
    <div className="overflow-hidden rounded-lg border border-white/8 bg-base-900/60">
      <button
        onClick={() => setOpen((o) => !o)}
        className="flex w-full items-center gap-2 px-3 py-2 text-left transition-colors hover:bg-white/[0.03]"
        aria-expanded={open}
      >
        <FileText size={14} className="shrink-0 text-signal-400" />
        <span className="flex-1 truncate font-mono text-[12px] text-ink-300">{source.document_name}</span>
        {typeof source.relevance_score === 'number' && (
          <span className="shrink-0 font-mono text-[11px] text-ink-400">
            {Math.round(source.relevance_score * 100)}%
          </span>
        )}
        <CaretDown
          size={12}
          className={`shrink-0 text-ink-400 transition-transform duration-200 ease-out ${open ? 'rotate-180' : ''}`}
        />
      </button>
      {open && source.excerpt && (
        <p className="border-t border-white/5 px-3 py-2.5 text-[12.5px] leading-relaxed text-ink-300">
          {source.excerpt}
        </p>
      )}
    </div>
  );
}
