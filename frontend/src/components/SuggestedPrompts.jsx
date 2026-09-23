export default function SuggestedPrompts({ prompts, onPick }) {
  return (
    <div className="flex flex-wrap gap-2">
      {prompts.map((p) => (
        <button
          key={p}
          onClick={() => onPick(p)}
          className="rounded-full border border-white/10 bg-base-800/50 px-3.5 py-2 text-left text-[13px] text-ink-300 transition-colors duration-150 ease-out hover:border-white/25 hover:text-ink-100"
        >
          {p}
        </button>
      ))}
    </div>
  );
}
