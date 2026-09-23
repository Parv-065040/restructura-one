import { Link } from 'react-router-dom';
import { ArrowUpRight } from '@phosphor-icons/react';

export default function Navbar() {
  return (
    <header className="sticky top-0 z-30 border-b border-white/5 bg-base-900/80 backdrop-blur-xl">
      <div className="mx-auto flex h-16 max-w-shell items-center justify-between px-6">
        <a href="#top" className="flex items-center gap-2.5">
          <span className="grid h-8 w-8 place-items-center rounded-lg bg-gradient-to-br from-signal-500 to-current-500">
            <span className="h-2.5 w-2.5 rounded-full bg-base-900" />
          </span>
          <span className="text-[15px] font-semibold tracking-tight text-ink-100">
            Restructura <span className="text-ink-300">One</span>
          </span>
        </a>

        <nav className="hidden items-center gap-8 text-sm text-ink-300 md:flex">
          <a href="#departments" className="transition-colors hover:text-ink-100">
            Departments
          </a>
          <a href="#method" className="transition-colors hover:text-ink-100">
            How it answers
          </a>
          <a href="#stack" className="transition-colors hover:text-ink-100">
            Stack
          </a>
        </nav>

        <Link
          to="/chat/finance"
          className="group inline-flex items-center gap-1.5 rounded-full bg-ink-100 px-4 py-2 text-sm font-medium text-base-900 transition-transform duration-150 ease-out active:scale-[0.97]"
        >
          Open workspace
          <ArrowUpRight
            size={15}
            weight="bold"
            className="transition-transform duration-200 ease-out group-hover:translate-x-0.5 group-hover:-translate-y-0.5"
          />
        </Link>
      </div>
    </header>
  );
}
