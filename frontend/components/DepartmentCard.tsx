"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import type { DepartmentMeta } from "@/lib/departments";

export function DepartmentCard({ dept, index }: { dept: DepartmentMeta; index: number }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-40px" }}
      transition={{ duration: 0.35, delay: index * 0.04 }}
    >
      <Link
        href={`/workspace/${dept.slug}`}
        className="group block panel p-5 transition-colors hover:border-accent-teal/60"
      >
        <div className="flex items-start justify-between gap-4">
          <div>
            <h3 className="text-base font-medium text-ink">{dept.name}</h3>
            <p className="mt-1.5 text-sm leading-relaxed text-muted">{dept.focus}</p>
          </div>
          <span
            aria-hidden
            className="mt-1 h-2 w-2 shrink-0 rounded-full bg-accent-teal/40 transition-colors group-hover:bg-accent-teal"
          />
        </div>
      </Link>
    </motion.div>
  );
}
