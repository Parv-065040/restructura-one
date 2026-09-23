export default function ThinkingIndicator({ label = 'One is retrieving evidence' }) {
  return (
    <div className="flex items-center gap-3 px-1 py-2 text-ink-400">
      <span className="flex items-center gap-1">
        <span className="h-1.5 w-1.5 animate-pulse-dot rounded-full bg-current-400 [animation-delay:0ms]" />
        <span className="h-1.5 w-1.5 animate-pulse-dot rounded-full bg-current-400 [animation-delay:150ms]" />
        <span className="h-1.5 w-1.5 animate-pulse-dot rounded-full bg-current-400 [animation-delay:300ms]" />
      </span>
      <span className="text-[13px]">{label}</span>
    </div>
  );
}
