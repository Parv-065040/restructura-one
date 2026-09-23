import { lazy, Suspense } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowRight, Circle } from '@phosphor-icons/react';

const OrbScene = lazy(() => import('./OrbScene'));

const container = {
  hidden: {},
  show: { transition: { staggerChildren: 0.08, delayChildren: 0.05 } },
};

const item = {
  hidden: { opacity: 0, y: 14 },
  show: { opacity: 1, y: 0, transition: { duration: 0.6, ease: [0.23, 1, 0.32, 1] } },
};

export default function Hero() {
  return (
    <section id="top" className="relative mx-auto grid max-w-shell grid-cols-1 gap-10 px-6 pb-16 pt-14 md:grid-cols-[1.05fr_0.95fr] md:gap-6 md:pb-24 md:pt-20">
      <motion.div variants={container} initial="hidden" animate="show" className="flex flex-col justify-center">
        <motion.div
          variants={item}
          className="mb-6 inline-flex w-fit items-center gap-2 rounded-full border border-white/10 bg-base-800/60 px-3 py-1.5 text-xs text-ink-300"
        >
          <Circle size={7} weight="fill" className="text-current-400" />
          Synthetic-data academic workspace — human review on every action
        </motion.div>

        <motion.h1
          variants={item}
          className="text-[2.6rem] font-semibold leading-[1.04] tracking-tight text-ink-100 sm:text-5xl lg:text-[3.4rem]"
        >
          One assistant.
          <br />
          Eight departments that actually
          <br className="hidden lg:block" /> know the business.
        </motion.h1>

        <motion.p variants={item} className="mt-6 max-w-[46ch] text-[17px] leading-relaxed text-ink-300">
          Restructura One routes every question to the department that can actually answer it — Finance, Risk,
          Legal, HR, and more — each grounded in its own knowledge base, with sources attached and every
          recommendation left for a human to review.
        </motion.p>

        <motion.div variants={item} className="mt-9 flex flex-wrap items-center gap-3">
          <Link
            to="/chat/finance"
            className="group inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-signal-500 to-current-500 px-5 py-3 text-sm font-medium text-base-950 transition-transform duration-150 ease-out active:scale-[0.97]"
          >
            Ask One a question
            <ArrowRight size={16} weight="bold" className="transition-transform duration-200 ease-out group-hover:translate-x-1" />
          </Link>
          <a
            href="#method"
            className="rounded-full border border-white/10 px-5 py-3 text-sm font-medium text-ink-200 transition-colors duration-150 hover:border-white/25 hover:text-ink-100"
          >
            See how it answers
          </a>
        </motion.div>

        <motion.dl variants={item} className="mt-12 grid max-w-md grid-cols-3 gap-6 border-t border-white/5 pt-6">
          <div>
            <dt className="text-2xl font-semibold tracking-tight text-ink-100">8</dt>
            <dd className="mt-1 text-xs text-ink-400">Department agents</dd>
          </div>
          <div>
            <dt className="text-2xl font-semibold tracking-tight text-ink-100">1</dt>
            <dd className="mt-1 text-xs text-ink-400">Shared orchestrator</dd>
          </div>
          <div>
            <dt className="text-2xl font-semibold tracking-tight text-ink-100">100%</dt>
            <dd className="mt-1 text-xs text-ink-400">Human-reviewed actions</dd>
          </div>
        </motion.dl>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, scale: 0.94 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.9, ease: [0.23, 1, 0.32, 1], delay: 0.15 }}
        className="relative h-[360px] sm:h-[440px] md:h-[560px]"
      >
        <div className="pointer-events-none absolute inset-0 rounded-[2rem] bg-gradient-to-b from-signal-500/10 via-transparent to-current-500/10" />
        <Suspense fallback={<div className="h-full w-full animate-pulse rounded-[2rem] bg-base-800/40" />}>
          <OrbScene className="h-full w-full" />
        </Suspense>
      </motion.div>
    </section>
  );
}
