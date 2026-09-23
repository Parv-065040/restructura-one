const stack = [
  { name: 'React + Vite', role: 'This workspace' },
  { name: 'Groq', role: 'openai/gpt-oss-120b inference' },
  { name: 'FAISS', role: 'Vector retrieval' },
  { name: 'Sentence Transformers', role: 'Embeddings' },
  { name: 'Pydantic', role: 'Structured contracts' },
  { name: 'Python orchestrator', role: 'Agent routing' },
];

export default function StackSection() {
  return (
    <section id="stack" className="mx-auto max-w-shell px-6 py-20">
      <div className="flex flex-col items-start justify-between gap-6 rounded-2xl border border-white/8 bg-base-800/40 p-8 md:flex-row md:items-center">
        <div className="max-w-sm">
          <h2 className="text-xl font-semibold tracking-tight text-ink-100">Built on real infrastructure.</h2>
          <p className="mt-2 text-sm leading-relaxed text-ink-300">
            This is the interface layer. Retrieval, grounding, and generation run on the stack below.
          </p>
        </div>
        <dl className="grid flex-1 grid-cols-2 gap-x-8 gap-y-5 sm:grid-cols-3">
          {stack.map((s) => (
            <div key={s.name}>
              <dt className="font-mono text-[13px] text-ink-100">{s.name}</dt>
              <dd className="mt-0.5 text-xs text-ink-400">{s.role}</dd>
            </div>
          ))}
        </dl>
      </div>
    </section>
  );
}
