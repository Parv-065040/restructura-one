import { ArrowClockwise } from '@phosphor-icons/react';

export default function ChatHeader({ department, onReset }) {
  const Icon = department.icon;
  return (
    <header className="flex shrink-0 items-center justify-between border-b border-white/5 px-5 py-3.5 sm:px-6">
      <div className="flex items-center gap-3">
        <span className="grid h-9 w-9 place-items-center rounded-lg border border-white/10 bg-base-800">
          <Icon size={17} weight="duotone" className="text-current-400" />
        </span>
        <div>
          <h1 className="text-sm font-semibold text-ink-100">{department.name}</h1>
          <p className="text-[12px] text-ink-400">Scoped to the {department.name.toLowerCase()} knowledge base</p>
        </div>
      </div>

      <button
        onClick={onReset}
        className="flex items-center gap-1.5 rounded-lg border border-white/10 px-3 py-1.5 text-xs text-ink-300 transition-colors duration-150 hover:border-white/25 hover:text-ink-100"
      >
        <ArrowClockwise size={13} />
        New chat
      </button>
    </header>
  );
}
