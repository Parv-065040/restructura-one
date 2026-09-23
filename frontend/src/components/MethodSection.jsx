import { motion } from 'framer-motion';
import { ChatCircleText, GitBranch, MagnifyingGlass, Sparkle, CheckCircle } from '@phosphor-icons/react';

const steps = [
  {
    icon: ChatCircleText,
    title: 'Ask in plain language',
    detail: 'You ask One a question from inside a department workspace — no forms, no ticket to file.',
  },
  {
    icon: GitBranch,
    title: 'Orchestrator routes it',
    detail: 'The shared orchestrator classifies intent and hands the question to that department\'s agent.',
  },
  {
    icon: MagnifyingGlass,
    title: 'Retrieves real evidence',
    detail: 'The agent searches its own knowledge base — FAISS + sentence embeddings — for grounded passages.',
  },
  {
    icon: Sparkle,
    title: 'Generates a sourced answer',
    detail: 'The Groq gateway drafts a response from your question, the evidence, and recent conversation.',
  },
  {
    icon: CheckCircle,
    title: 'You review and decide',
    detail: 'Citations and any proposed action are shown for review — nothing executes on its own.',
  },
];

export default function MethodSection() {
  return (
    <section id="method" className="border-t border-white/5 bg-base-950/60">
      <div className="mx-auto max-w-shell px-6 py-20">
        <h2 className="text-3xl font-semibold tracking-tight text-ink-100">How a question becomes an answer.</h2>
        <p className="mt-3 max-w-[58ch] text-[15px] leading-relaxed text-ink-300">
          Every response follows the same five-step path, department to department, so the answer you get is
          always traceable back to something real.
        </p>

        <ol className="mt-12 grid grid-cols-1 gap-px overflow-hidden rounded-2xl border border-white/8 bg-white/5 md:grid-cols-5">
          {steps.map((step, i) => {
            const Icon = step.icon;
            return (
              <motion.li
                key={step.title}
                initial={{ opacity: 0, y: 12 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: '-80px' }}
                transition={{ duration: 0.45, ease: [0.23, 1, 0.32, 1], delay: i * 0.06 }}
                className="relative flex flex-col gap-4 bg-base-900 p-6"
              >
                <span className="font-mono text-xs text-ink-400">{String(i + 1).padStart(2, '0')}</span>
                <span className="grid h-9 w-9 place-items-center rounded-lg border border-white/10 bg-base-800">
                  <Icon size={17} weight="duotone" className="text-current-400" />
                </span>
                <div>
                  <h3 className="text-sm font-semibold text-ink-100">{step.title}</h3>
                  <p className="mt-1.5 text-[13px] leading-relaxed text-ink-300">{step.detail}</p>
                </div>
              </motion.li>
            );
          })}
        </ol>
      </div>
    </section>
  );
}
