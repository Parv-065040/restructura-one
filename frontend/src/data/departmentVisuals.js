import { BarsVisual, NodesVisual, WavesVisual, RadarVisual } from '../components/visuals/VisualPrimitives';

// Deterministic "random" frames so each department's hover visual looks
// intentional and stays identical across renders/reloads, without hand
// authoring dozens of coordinate sets by hand.

function hashSeed(str) {
  let h = 1779033703 ^ str.length;
  for (let i = 0; i < str.length; i++) {
    h = Math.imul(h ^ str.charCodeAt(i), 3432918353);
    h = (h << 13) | (h >>> 19);
  }
  return () => {
    h = Math.imul(h ^ (h >>> 16), 2246822507);
    h = Math.imul(h ^ (h >>> 13), 3266489909);
    h ^= h >>> 16;
    return (h >>> 0) / 4294967296;
  };
}

/** Returns `frameCount` frames, each an array of `points` values in [0.22, 0.92]. */
export function makeFrames(seed, frameCount = 3, points = 6) {
  const rand = hashSeed(seed);
  return Array.from({ length: frameCount }, () =>
    Array.from({ length: points }, () => 0.22 + rand() * 0.7)
  );
}

// One of four abstract "visual languages", assigned per department below —
// each reads as an evidence-backed enterprise dashboard motif rather than
// decoration, and none of them are photographic (no licensing surface,
// and it keeps the same restrained, line-art register as the rest of the UI).
export const VISUAL_TYPE = {
  finance: 'bars',
  sales: 'bars',
  it: 'nodes',
  hr: 'nodes',
  marketing: 'waves',
  customer_support: 'waves',
  risk_restructuring: 'radar',
  legal_compliance: 'radar',
};

export const ACCENT_HEX = {
  signal: '#5C8DFF',
  current: '#3FE8C7',
  amber: '#F0A857',
};

export const VISUAL_COMPONENTS = {
  bars: BarsVisual,
  nodes: NodesVisual,
  waves: WavesVisual,
  radar: RadarVisual,
};

export const VISUAL_VIEWBOX = '0 0 240 120';
