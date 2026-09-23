import { Link, useNavigate } from 'react-router-dom';
import { House } from '@phosphor-icons/react';
import { departments } from '../data/departments';

export default function Sidebar({ activeSlug }) {
  const navigate = useNavigate();

  return (
    <aside
      className="flex shrink-0 border-b border-white/5 bg-base-950/60 md:h-[100dvh] md:w-[76px] md:flex-col md:border-b-0 md:border-r"
      aria-label="Departments"
    >
      <div className="hidden shrink-0 items-center justify-center py-4 md:flex">
        <Link
          to="/"
          className="grid h-9 w-9 place-items-center rounded-lg border border-white/10 bg-base-800 text-ink-300 transition-colors hover:text-ink-100"
          title="Back to overview"
        >
          <House size={16} weight="bold" />
        </Link>
      </div>

      <nav className="flex flex-1 items-center gap-1.5 overflow-x-auto px-3 py-2.5 md:flex-col md:items-stretch md:gap-1 md:overflow-x-visible md:overflow-y-auto md:px-2.5 md:py-2">
        {departments.map((dept) => {
          const Icon = dept.icon;
          const active = dept.slug === activeSlug;
          return (
            <button
              key={dept.slug}
              onClick={() => navigate(`/chat/${dept.slug}`)}
              title={dept.name}
              aria-current={active ? 'page' : undefined}
              className={`group relative flex shrink-0 items-center gap-2 rounded-xl px-3 py-2.5 text-left transition-colors duration-150 ease-out md:w-full md:justify-center md:px-0 ${
                active ? 'bg-white/8 text-ink-100' : 'text-ink-400 hover:bg-white/5 hover:text-ink-200'
              }`}
            >
              {active && (
                <span className="absolute left-0 top-1/2 hidden h-5 w-[3px] -translate-y-1/2 rounded-full bg-gradient-to-b from-signal-400 to-current-400 md:block" />
              )}
              <Icon size={18} weight={active ? 'fill' : 'regular'} />
              <span className="text-xs font-medium md:hidden">{dept.short}</span>
            </button>
          );
        })}
      </nav>
    </aside>
  );
}
