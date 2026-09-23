import { useEffect, useMemo, useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import {
  makeFrames,
  VISUAL_TYPE,
  ACCENT_HEX,
  VISUAL_COMPONENTS,
  VISUAL_VIEWBOX,
} from '../../data/departmentVisuals';

/**
 * A small abstract SVG "slider" that quietly cycles through a few
 * generated frames while the parent card is hovered. No external images —
 * the visual language (bars / node graph / broadcast waves / radar)
 * matches the enterprise dashboard register of the rest of the UI instead
 * of standing apart from it, and avoids any licensing question a stock
 * photo would raise.
 */
export default function DepartmentVisual({ department, hovered }) {
  const type = VISUAL_TYPE[department.slug] ?? 'bars';
  const Visual = VISUAL_COMPONENTS[type];
  const color = ACCENT_HEX[department.accent] ?? ACCENT_HEX.signal;

  // Computed once per department, not re-rolled on every render.
  const frames = useMemo(() => makeFrames(department.slug), [department.slug]);
  const [frameIndex, setFrameIndex] = useState(0);

  useEffect(() => {
    if (!hovered) return undefined;
    const id = setInterval(() => {
      setFrameIndex((i) => (i + 1) % frames.length);
    }, 1300);
    return () => clearInterval(id);
  }, [hovered, frames.length]);

  return (
    <div className="pointer-events-none absolute inset-0 overflow-hidden opacity-70 transition-opacity duration-300 ease-out group-hover:opacity-100">
      <AnimatePresence mode="wait">
        <motion.svg
          key={frameIndex}
          viewBox={VISUAL_VIEWBOX}
          className="h-full w-full"
          initial={{ opacity: 0, scale: 0.97 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 1.02 }}
          transition={{ duration: 0.5, ease: [0.23, 1, 0.32, 1] }}
          preserveAspectRatio="xMidYMax meet"
        >
          <Visual frame={frames[frameIndex]} color={color} />
        </motion.svg>
      </AnimatePresence>
      {/* Fades the visual into the card's surface so it reads as texture, not an inserted image */}
      <div className="absolute inset-0 bg-gradient-to-t from-base-800/95 via-base-800/10 to-transparent" />
    </div>
  );
}
