import type { EmotionSignal } from "../types";

const LABELS: Record<string, string> = {
  sentiment_velocity: "Sentiment Velocity",
  crowd_surge: "Crowd Surge",
  holder_momentum: "Holder Momentum",
  market_depth: "Market Depth",
};

interface Props {
  signals: EmotionSignal[];
}

export function SignalPanel({ signals }: Props) {
  return (
    <div style={{
      background: "#070d07",
      border: "1px solid #1a2a1a",
      borderRadius: 12,
      padding: "20px 24px",
    }}>
      <h3 style={{ color: "#4b5563", fontSize: 11, letterSpacing: 2, marginBottom: 16, textTransform: "uppercase" }}>
        Signal Breakdown
      </h3>
      <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
        {signals.map((sig) => (
          <SignalRow key={sig.name} signal={sig} />
        ))}
      </div>
    </div>
  );
}

function SignalRow({ signal }: { signal: EmotionSignal }) {
  const label = LABELS[signal.name] || signal.name;
  const color = signal.triggered ? "#84cc16" : "#334155";
  const pct = `${(signal.weight * 100).toFixed(0)}%`;

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
        <span style={{ fontSize: 12, color: signal.triggered ? "#cbd5e1" : "#475569" }}>
          {signal.triggered ? "◆" : "◇"} {label}
          <span style={{ color: "#334155", marginLeft: 8, fontSize: 10 }}>weight {pct}</span>
        </span>
        <span style={{ fontSize: 12, color, fontWeight: 600 }}>
          {signal.score.toFixed(1)}
        </span>
      </div>
      <div style={{ background: "#0f1a0f", borderRadius: 3, height: 4, overflow: "hidden" }}>
        <div style={{
          height: "100%", width: `${signal.score}%`,
          background: signal.triggered ? `linear-gradient(90deg, #365314, #84cc16)` : "#1e2d1e",
          borderRadius: 3, transition: "width 0.5s ease",
        }} />
      </div>
    </div>
  );
}
