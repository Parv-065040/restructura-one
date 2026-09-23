import { departments } from '../data/departments';
import DepartmentCard from './DepartmentCard';

export default function DepartmentGrid() {
  return (
    <section id="departments" className="mx-auto max-w-shell px-6 py-20">
      <div className="mb-10 flex flex-col items-start justify-between gap-4 md:flex-row md:items-end">
        <div>
          <h2 className="text-3xl font-semibold tracking-tight text-ink-100">Pick a department, not a menu.</h2>
          <p className="mt-3 max-w-[52ch] text-[15px] leading-relaxed text-ink-300">
            Each card opens straight into a scoped conversation — no setup screen in between. One click in, One
            answering from that department's evidence.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {departments.map((dept, i) => (
          <DepartmentCard key={dept.slug} department={dept} index={i} featured={i === 0 || i === 5} />
        ))}
      </div>
    </section>
  );
}
