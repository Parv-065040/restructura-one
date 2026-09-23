import { useState } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowRight } from '@phosphor-icons/react';
import DepartmentVisual from './visuals/DepartmentVisual';

const borderAccent = {
  signal: 'hover:border-signal-500/40',
  current: 'hover:border-current-500/40',
  amber: 'hover:border-amber-500/40',
};

const iconAccent = {
  signal: 'text-signal-400',
  current: 'text-current-400',
  amber: 'text-amber-400',
};

export default function DepartmentCard({ department, index, featured = false }) {
  const Icon = department.icon;
  const [hovered, setHovered] = useState(false);

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-60px' }}
      transition={{ duration: 0.5, ease: [0.23, 1, 0.32, 1], delay: (index % 4) * 0.05 }}
      className={featured ? 'md:col-span-2 md:row-span-2' : ''}
    >
      <Link
        to={`/chat/${department.slug}`}
        onMouseEnter={() => setHovered(true)}
        onMouseLeave={() => setHovered(false)}
        className={`group relative flex h-full min-h-[220px] flex-col justify-between overflow-hidden rounded-2xl border border-white/8 bg-base-800/50 p-6 transition-colors duration-200 ease-out ${
          borderAccent[department.accent] ?? borderAccent.signal
        }`}
      >
        {/* Abstract, brand-colored motif — cycles through a few frames on
            hover, fades into the card surface so it reads as texture
            rather than a separate image. */}
        <DepartmentVisual department={department} hovered={hovered} />

        <div className="relative z-10 flex items-start justify-between">
          <span className="grid h-10 w-10 place-items-center rounded-xl border border-white/10 bg-base-900/70 backdrop-blur-sm">
            <Icon size={18} weight="duotone" className={iconAccent[department.accent] ?? iconAccent.signal} />
          </span>
          <ArrowRight
            size={16}
            weight="bold"
            className="text-ink-400 opacity-0 transition-all duration-200 ease-out group-hover:translate-x-0.5 group-hover:opacity-100"
          />
        </div>

        <div className="relative z-10 mt-8">
          <h3 className="text-lg font-semibold tracking-tight text-ink-100">{department.name}</h3>
          <p className="mt-1.5 text-sm leading-relaxed text-ink-300">
            {featured ? department.description : department.tagline}
          </p>
        </div>
      </Link>
    </motion.div>
  );
}
