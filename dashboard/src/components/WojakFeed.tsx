import type { MoodReport, WojakPhase } from "../types";

const PHASE_COLOR: Record<WojakPhase, string> = {
  DOOMER: "#64748b",
  FEELS: "#d97706",
  BLOOMER: "#65a30d",
  MEWING: "#ca8a04",
};

const EMOJI: Record<WojakPhase, string> = {
  DOOMER: "😔",
  FEELS: "🥺",
  BLOOMER: "😊",
  MEWING: "😤",
};

interface Props {
  reports: MoodReport[];
}

export function WojakFeed({ reports }: Props) {
  const sorted = [...reports].sort((a, b) => b.emotion_score - a.emotion_score);

  return (
    <div style={{
      background: "#070d07",
      border: "1px solid #1a2a1a",
      borderRadius: 12,
      padding: "20px 24px",
    }}>
      <h3 style={{ color: "#4b5563", fontSize: 11, letterSpacing: 2, marginBottom: 16, textTransform: "uppercase" }}>
        Emotion Feed
      </h3>
      <div style={{ display: "flex", flexDirection: "column", gap: 2 }}>
        {sorted.map((r, i) => (
          <FeedRow key={r.token_mint} report={r} rank={i + 1} />
        ))}
      </div>
    </div>
  );
}

function FeedRow({ report, rank }: { report: MoodReport; rank: number }) {
  const color = PHASE_COLOR[report.phase];
  const emoji = EMOJI[report.phase];

  return (
    <div style={{
      display: "flex", alignItems: "center", gap: 10,
      padding: "10px 8px", borderRadius: 6,
      background: rank === 1 ? "#0f1a0f" : "transparent",
    }}>
      <span style={{ color: "#334155", fontSize: 11, width: 16, textAlign: "right" }}>{rank}</span>
      <span style={{ fontSize: 14 }}>{emoji}</span>
      <span style={{ fontSize: 13, color: "#e2e8f0", fontWeight: 600, flex: 1 }}>
        ${report.symbol}
      </span>
      <span style={{ fontSize: 11, color, letterSpacing: 1, textTransform: "uppercase" }}>
        {report.phase}
      </span>
      <span style={{ fontSize: 13, color, fontWeight: 700, width: 44, textAlign: "right" }}>
        {report.emotion_score.toFixed(1)}
      </span>
    </div>
  );
}
