"use client";

import { useMemo } from "react";
import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowLeft } from "lucide-react";
import { getDepartment } from "@/lib/departments";
import { ChatWindow } from "@/components/ChatWindow";

export default function DepartmentWorkspace({
  params,
}: {
  params: { department: string };
}) {
  const dept = getDepartment(params.department);
  const sessionId = useMemo(
    () => `${params.department}-${Math.random().toString(36).slice(2, 10)}`,
    [params.department]
  );

  if (!dept) return notFound();

  return (
    <main className="mx-auto max-w-6xl px-6 pb-16 pt-10 sm:px-8">
      <Link href="/" className="inline-flex items-center gap-1.5 text-sm text-muted hover:text-ink">
        <ArrowLeft size={14} /> All departments
      </Link>

      <div className="mt-4 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-medium">{dept.name}</h1>
          <p className="mt-1 text-sm text-muted">{dept.focus}</p>
        </div>
        <button
          onClick={() => window.location.reload()}
          className="rounded-card border border-border px-3 py-2 text-xs text-muted transition-colors hover:border-accent-teal/60 hover:text-ink"
        >
          New chat
        </button>
      </div>

      <div className="mt-6">
        <ChatWindow dept={dept} sessionId={sessionId} />
      </div>

      <p className="mt-6 text-xs text-muted">
        Synthetic data and AI-generated content — review sources and proposed actions before acting.
      </p>
    </main>
  );
}
