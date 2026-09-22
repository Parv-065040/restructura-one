"use client";

import { motion } from "framer-motion";
import { DEPARTMENTS } from "@/lib/departments";
import { DepartmentCard } from "@/components/DepartmentCard";

const STEPS = [
  { label: "Choose", detail: "Pick the department that owns the question." },
  { label: "Ask", detail: "Describe the decision or situation in plain language." },
  { label: "Review", detail: "Read the grounded answer, check sources, decide what to do." },
];

export default function HomePage() {
  return (
    <main className="mx-auto max-w-6xl px-6 pb-24 pt-16 sm:px-8">
      {/* Hero */}
      <section className="grid gap-12 sm:grid-cols-[1.2fr_1fr] sm:items-center">
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, ease: "easeOut" }}
        >
          <p className="text-sm text-muted">Restructura One</p>
          <h1 className="mt-3 max-w-lg text-4xl font-medium leading-[1.1] sm:text-5xl">
            One workspace.
            <br />
            Eight specialists.
            <br />
            <span className="text-accent-teal">Grounded</span> answers.
          </h1>
          <p className="mt-5 max-w-md text-base leading-relaxed text-muted">
            Every department gets an assistant that answers from its own
            knowledge base, shows its sources, and leaves the decision to
            you. This is a decision-support tool, not an autonomous one.
          </p>
          <div className="mt-8 flex items-center gap-4">
            <a
              href="#departments"
              className="rounded-card bg-accent-teal px-5 py-2.5 text-sm font-medium text-base transition-opacity hover:opacity-90"
            >
              Open a department
            </a>
            <span className="text-sm text-muted">8 agents · 1 workspace</span>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.97 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6, delay: 0.15, ease: "easeOut" }}
          className="panel p-6"
        >
          <p className="text-xs text-muted">Live scope</p>
          <ul className="mt-4 space-y-2.5">
            {DEPARTMENTS.map((d, i) => (
              <li key={d.slug} className="flex items-center gap-3 text-sm">
                <motion.span
                  aria-hidden
                  className="h-1.5 w-1.5 rounded-full bg-accent-teal"
                  initial={{ opacity: 0.3 }}
                  animate={{ opacity: [0.3, 1, 0.3] }}
                  transition={{ duration: 2.4, repeat: Infinity, delay: i * 0.18 }}
                />
                <span className="text-ink/90">{d.name}</span>
              </li>
            ))}
          </ul>
        </motion.div>
      </section>

      {/* Workflow */}
      <section className="mt-24 grid gap-6 sm:grid-cols-3">
        {STEPS.map((step, i) => (
          <div key={step.label} className="panel p-5">
            <p className="text-xs text-muted">Step {i + 1}</p>
            <h3 className="mt-1.5 text-lg font-medium">{step.label}</h3>
            <p className="mt-1.5 text-sm leading-relaxed text-muted">{step.detail}</p>
          </div>
        ))}
      </section>

      {/* Department directory */}
      <section id="departments" className="mt-24">
        <div className="flex items-baseline justify-between">
          <h2 className="text-xl font-medium">Departments</h2>
          <p className="text-sm text-muted">Synthetic data · human review required</p>
        </div>
        <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {DEPARTMENTS.map((dept, i) => (
            <DepartmentCard key={dept.slug} dept={dept} index={i} />
          ))}
        </div>
      </section>
    </main>
  );
}
