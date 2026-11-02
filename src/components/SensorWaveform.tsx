import React, { useMemo } from 'react';
import { SensorKineticsData } from '../lib/types';
import { SENSOR_CHANNELS } from '../lib/inference';

interface Props {
  data: SensorKineticsData;
  activeChannel?: string;
  onSelectChannel?: (key: string) => void;
}

const CHANNEL_COLORS: Record<string, string> = {
  "s1_sno2": "#e2e8f0",     // Bright Silver
  "s2_wo3": "#94a3b8",      // Slate
  "s3_graphene": "#cbd5e1", // Light Gray
  "s4_au_nano": "#3fd6c6",  // Mint Signal (LSPR Optical channel)
  "s5_cnt": "#64748b",      // Steel
  "s6_in2o3": "#a1a1aa",    // Zinc
  "s7_tio2_pt": "#d4d4d8",  // Platinum
  "s8_zno_nw": "#71717a"    // Graphite
};

export const SensorWaveform: React.FC<Props> = ({ data, activeChannel, onSelectChannel }) => {
  const { timePoints, curves } = data;

  const width = 640;
  const height = 240;
  const padding = { top: 20, right: 30, bottom: 35, left: 45 };

  // Determine min and max Y
  const { minY, maxY } = useMemo(() => {
    let min = 0.98;
    let max = 1.05;
    Object.values(curves).forEach((series) => {
      series.forEach((val) => {
        if (val < min) min = val;
        if (val > max) max = val;
      });
    });
    return { minY: Math.max(0.8, min - 0.05), maxY: max + 0.1 };
  }, [curves]);

  const maxT = timePoints[timePoints.length - 1] || 70;

  const scaleX = (t: number) => {
    return padding.left + (t / maxT) * (width - padding.left - padding.right);
  };

  const scaleY = (val: number) => {
    const range = maxY - minY;
    return height - padding.bottom - ((val - minY) / range) * (height - padding.top - padding.bottom);
  };

  // Build SVG path strings
  const paths = useMemo(() => {
    const res: Record<string, string> = {};
    Object.entries(curves).forEach(([key, values]) => {
      let d = "";
      values.forEach((val, idx) => {
        const x = scaleX(timePoints[idx]);
        const y = scaleY(val);
        if (idx === 0) {
          d += `M ${x.toFixed(1)} ${y.toFixed(1)}`;
        } else {
          d += ` L ${x.toFixed(1)} ${y.toFixed(1)}`;
        }
      });
      res[key] = d;
    });
    return res;
  }, [curves, timePoints, minY, maxY]);

  // Exposure region: t = 8s to 45s
  const expStartX = scaleX(8);
  const expEndX = scaleX(45);

  return (
    <div style={{ width: '100%', overflowX: 'auto' }}>
      <svg
        viewBox={`0 0 ${width} ${height}`}
        style={{ width: '100%', height: 'auto', display: 'block' }}
        aria-label="Multi-sensor dynamic reaction kinetics waveform"
      >
        {/* Exposure Zone */}
        <rect
          x={expStartX}
          y={padding.top}
          width={expEndX - expStartX}
          height={height - padding.top - padding.bottom}
          fill="rgba(255, 255, 255, 0.02)"
          stroke="#222222"
          strokeDasharray="2 2"
        />
        <text
          x={(expStartX + expEndX) / 2}
          y={padding.top + 12}
          fill="#8a8d91"
          fontSize="9"
          fontFamily="var(--dp-typography-mono)"
          textAnchor="middle"
          letterSpacing="0.05em"
        >
          EXPOSURE PHASE (8s – 45s)
        </text>

        {/* Horizontal grid lines */}
        {[minY, (minY + maxY) / 2, maxY].map((val, idx) => {
          const y = scaleY(val);
          return (
            <g key={idx}>
              <line
                x1={padding.left}
                y1={y}
                x2={width - padding.right}
                y2={y}
                stroke="#222222"
                strokeWidth="1"
              />
              <text
                x={padding.left - 8}
                y={y + 3}
                fill="#8a8d91"
                fontSize="9"
                fontFamily="var(--dp-typography-mono)"
                textAnchor="end"
              >
                {val.toFixed(2)}
              </text>
            </g>
          );
        })}

        {/* Time axis ticks */}
        {[0, 20, 40, 60].map((t) => {
          const x = scaleX(t);
          return (
            <g key={t}>
              <line
                x1={x}
                y1={height - padding.bottom}
                x2={x}
                y2={height - padding.bottom + 4}
                stroke="#303030"
              />
              <text
                x={x}
                y={height - padding.bottom + 15}
                fill="#8a8d91"
                fontSize="9"
                fontFamily="var(--dp-typography-mono)"
                textAnchor="middle"
              >
                {t}s
              </text>
            </g>
          );
        })}

        {/* Sensor Reaction Lines */}
        {SENSOR_CHANNELS.map((sensor) => {
          const isSelected = activeChannel === sensor.key;
          const strokeColor = CHANNEL_COLORS[sensor.key] || "#94a3b8";
          const strokeWidth = isSelected ? 2.5 : 1.2;
          const opacity = activeChannel && !isSelected ? 0.35 : 0.95;

          return (
            <path
              key={sensor.key}
              d={paths[sensor.key]}
              fill="none"
              stroke={strokeColor}
              strokeWidth={strokeWidth}
              strokeOpacity={opacity}
              style={{
                cursor: 'pointer',
                transition: 'stroke-width 120ms ease-out, stroke-opacity 120ms ease-out'
              }}
              onClick={() => onSelectChannel?.(sensor.key)}
            />
          );
        })}
      </svg>

      {/* Sensor Legend */}
      <div style={{
        display: 'flex',
        flexWrap: 'wrap',
        gap: '8px 16px',
        marginTop: '12px',
        paddingTop: '12px',
        borderTop: '1px solid var(--dp-color-hairline)'
      }}>
        {SENSOR_CHANNELS.map((sensor) => {
          const color = CHANNEL_COLORS[sensor.key];
          const isSelected = activeChannel === sensor.key;
          return (
            <button
              key={sensor.key}
              onClick={() => onSelectChannel?.(sensor.key)}
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px',
                background: isSelected ? 'rgba(255,255,255,0.06)' : 'transparent',
                border: isSelected ? '1px solid #303030' : '1px solid transparent',
                borderRadius: '4px',
                padding: '2px 6px',
                color: isSelected ? 'var(--dp-color-bright)' : 'var(--dp-color-meta)',
                fontSize: '11px',
                fontFamily: 'var(--dp-typography-mono)',
                cursor: 'pointer'
              }}
            >
              <span style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: color }} />
              <span>{sensor.name}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
};
