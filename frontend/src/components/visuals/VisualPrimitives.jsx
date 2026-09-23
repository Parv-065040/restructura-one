// Pure presentational SVG fragments. Each takes one frame (array of
// values in [0,1]) and a color, and renders a small enterprise-dashboard
// style motif — deliberately abstract, never a literal chart of real data.

const VIEW_W = 240;
const VIEW_H = 120;

export function BarsVisual({ frame, color }) {
  const barWidth = VIEW_W / (frame.length * 1.6);
  const gap = barWidth * 0.6;
  const startX = (VIEW_W - (barWidth + gap) * frame.length + gap) / 2;

  const points = frame.map((v, i) => {
    const x = startX + i * (barWidth + gap) + barWidth / 2;
    const y = VIEW_H - v * (VIEW_H - 16) - 8;
    return [x, y];
  });
  const linePath = points.map(([x, y], i) => `${i === 0 ? 'M' : 'L'}${x},${y}`).join(' ');

  return (
    <>
      {frame.map((v, i) => {
        const x = startX + i * (barWidth + gap);
        const h = v * (VIEW_H - 24);
        return (
          <rect
            key={i}
            x={x}
            y={VIEW_H - h - 8}
            width={barWidth}
            height={h}
            rx={2}
            fill={color}
            opacity={0.16 + (v - 0.2) * 0.35}
          />
        );
      })}
      <path d={linePath} fill="none" stroke={color} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round" opacity={0.85} />
      {points.map(([x, y], i) => (
        <circle key={i} cx={x} cy={y} r={2.4} fill={color} />
      ))}
    </>
  );
}

export function NodesVisual({ frame, color }) {
  const positions = frame.map((v, i) => {
    const col = i % 3;
    const row = Math.floor(i / 3);
    const x = 40 + col * 80 + (v - 0.5) * 20;
    const y = 32 + row * 56 + (v - 0.5) * 16;
    return [x, y];
  });

  const edges = [
    [0, 1], [1, 2], [0, 3], [1, 4], [2, 5], [3, 4], [4, 5],
  ].filter(([a, b]) => positions[a] && positions[b]);

  return (
    <>
      {edges.map(([a, b], i) => (
        <line
          key={i}
          x1={positions[a][0]}
          y1={positions[a][1]}
          x2={positions[b][0]}
          y2={positions[b][1]}
          stroke={color}
          strokeWidth={1}
          opacity={0.3}
        />
      ))}
      {positions.map(([x, y], i) => (
        <circle key={i} cx={x} cy={y} r={4 + frame[i] * 3} fill={color} opacity={0.25 + frame[i] * 0.45} />
      ))}
    </>
  );
}

export function WavesVisual({ frame, color }) {
  const cx = VIEW_W / 2;
  const cy = VIEW_H / 2;
  return (
    <>
      {frame.map((v, i) => (
        <circle
          key={i}
          cx={cx}
          cy={cy}
          r={14 + i * 16 + v * 10}
          fill="none"
          stroke={color}
          strokeWidth={1.2}
          opacity={0.5 - i * 0.07}
        />
      ))}
      <circle cx={cx} cy={cy} r={5} fill={color} />
    </>
  );
}

export function RadarVisual({ frame, color }) {
  const cx = VIEW_W / 2;
  const cy = VIEW_H / 2 + 4;
  const maxR = 44;
  const n = frame.length;

  const pointAt = (i, r) => {
    const angle = (Math.PI * 2 * i) / n - Math.PI / 2;
    return [cx + r * Math.cos(angle), cy + r * Math.sin(angle)];
  };

  const outline = frame.map((v, i) => pointAt(i, v * maxR));
  const path = outline.map(([x, y], i) => `${i === 0 ? 'M' : 'L'}${x},${y}`).join(' ') + ' Z';
  const rings = [0.4, 0.7, 1];

  return (
    <>
      {rings.map((r, i) => {
        const ringPts = Array.from({ length: n }, (_, k) => pointAt(k, r * maxR));
        const ringPath = ringPts.map(([x, y], k) => `${k === 0 ? 'M' : 'L'}${x},${y}`).join(' ') + ' Z';
        return <path key={i} d={ringPath} fill="none" stroke={color} strokeWidth={0.75} opacity={0.15} />;
      })}
      <path d={path} fill={color} fillOpacity={0.14} stroke={color} strokeWidth={1.5} strokeLinejoin="round" />
      {outline.map(([x, y], i) => (
        <circle key={i} cx={x} cy={y} r={2.2} fill={color} />
      ))}
    </>
  );
}


