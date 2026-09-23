import { useRef, useState } from 'react';
import { ArrowUp } from '@phosphor-icons/react';

export default function Composer({ onSend, disabled, departmentName }) {
  const [value, setValue] = useState('');
  const textareaRef = useRef(null);

  const submit = () => {
    if (!value.trim() || disabled) return;
    onSend(value);
    setValue('');
    if (textareaRef.current) textareaRef.current.style.height = 'auto';
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  };

  const autoGrow = (e) => {
    setValue(e.target.value);
    e.target.style.height = 'auto';
    e.target.style.height = `${Math.min(e.target.scrollHeight, 160)}px`;
  };

  return (
    <div className="border-t border-white/5 bg-base-900/80 px-4 pb-4 pt-3 backdrop-blur-xl sm:px-6">
      <div className="mx-auto flex max-w-[760px] items-end gap-2 rounded-2xl border border-white/10 bg-base-800/60 p-2 pl-4 transition-colors duration-150 focus-within:border-current-500/50">
        <textarea
          ref={textareaRef}
          value={value}
          onChange={autoGrow}
          onKeyDown={handleKeyDown}
          rows={1}
          placeholder={`Ask ${departmentName} anything...`}
          className="max-h-40 flex-1 resize-none bg-transparent py-2 text-[14.5px] leading-relaxed text-ink-100 placeholder:text-ink-400 focus:outline-none"
        />
        <button
          onClick={submit}
          disabled={!value.trim() || disabled}
          aria-label="Send message"
          className="grid h-9 w-9 shrink-0 place-items-center rounded-xl bg-gradient-to-br from-signal-500 to-current-500 text-base-950 transition-all duration-150 ease-out active:scale-[0.93] disabled:cursor-not-allowed disabled:opacity-30"
        >
          <ArrowUp size={16} weight="bold" />
        </button>
      </div>
      <p className="mx-auto mt-2 max-w-[760px] text-center text-[11px] text-ink-400">
        One answers from synthetic department data. Review sources before acting.
      </p>
    </div>
  );
}
