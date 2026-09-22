"use client";

export function SourcesPanel({
  citations,
  proposedActions,
}: {
  citations: Record<string, unknown>[];
  proposedActions: Record<string, unknown>[];
}) {
  const hasCitations = citations.length > 0;
  const hasActions = proposedActions.length > 0;

  return (
    <aside className="panel h-fit w-full shrink-0 p-5 lg:w-72">
      <div>
        <h4 className="text-xs font-medium text-muted">Sources</h4>
        {hasCitations ? (
          <ul className="mt-3 space-y-2">
            {citations.map((c, i) => (
              <li key={i} className="rounded-card border border-border p-3 text-xs leading-relaxed text-muted">
                {/* NOTE: field names are placeholders — align with the
                    real SourceCitation shape once confirmed. */}
                {String(c.source ?? c.title ?? c.excerpt ?? JSON.stringify(c))}
              </li>
            ))}
          </ul>
        ) : (
          <p className="mt-3 text-xs text-muted">No supporting source retrieved for this answer.</p>
        )}
      </div>

      <div className="mt-6">
        <h4 className="text-xs font-medium text-muted">Proposed actions</h4>
        {hasActions ? (
          <ul className="mt-3 space-y-2">
            {proposedActions.map((a, i) => (
              <li
                key={i}
                className="rounded-card border border-status-warn/40 bg-status-warn/5 p-3 text-xs leading-relaxed"
              >
                <span className="mb-1 block font-medium text-status-warn">Awaiting human review</span>
                {String(a.description ?? a.title ?? JSON.stringify(a))}
              </li>
            ))}
          </ul>
        ) : (
          <p className="mt-3 text-xs text-muted">No actions proposed.</p>
        )}
      </div>
    </aside>
  );
}
