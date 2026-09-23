import { HourglassMedium } from '@phosphor-icons/react';

// action matches core/schemas/agent_contracts.py::ActionProposal
// { action_id, action_type, description, requires_approval, status, parameters }
// status is one of: proposed, pending_approval, approved, rejected, completed.
// This card only ever renders the "not yet acted on" framing — it never
// shows approved/completed styling, matching the product's human-review
// requirement. If a real approval workflow lands later, that state should
// be surfaced elsewhere (e.g. an audit list), not by relabeling this card.
export default function ProposedActionCard({ action }) {
  return (
    <div className="rounded-xl border border-amber-500/25 bg-amber-500/[0.06] p-4">
      <div className="flex items-center gap-2 text-amber-400">
        <HourglassMedium size={14} weight="bold" />
        <span className="text-[11px] font-medium uppercase tracking-wide">
          {action.action_type.replace('_', ' ')} — awaiting human review
        </span>
      </div>
      <p className="mt-2.5 text-[13px] leading-relaxed text-ink-300">{action.description}</p>
      <p className="mt-3 text-[11px] text-ink-400">
        This is decision support only. Nothing has been executed or approved.
      </p>
    </div>
  );
}
