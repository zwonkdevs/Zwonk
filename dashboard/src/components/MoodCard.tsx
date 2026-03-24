import type { MoodReport, WojakPhase } from "../types";

const PHASE_COLORS: Record<WojakPhase, string> = {
  DOOMER: "#64748b",
  FEELS: "#d97706",
  BLOOMER: "#65a30d",
  MEWING: "#ca8a04",
};

const PHASE_BG: Record<WojakPhase, string> = {
  DOOMER: "#0f1a14",
  FEELS: "#1c1305",
  BLOOMER: "#0f1a0a",
  MEWING: "#1a1400",
};

const WOJAK_EMOJI: Record<WojakPhase, string> = {
  DOOMER: "😔",
  FEELS: "🥺",
  BLOOMER: "😊",
  MEWING: "😤",
};

interface Props {
  report: MoodReport;
  isPinned?: boolean;
}

export function MoodCard({ report, isPinned }: Props) {
  const color = PHASE_COLORS[report.phase];
  const bg = PHASE_BG[report.phase];
  const emoji = WOJAK_EMOJI[report.phase];

  return (
    <div style={{
      background: bg,
      border: `1px solid ${color}44`,
      borderRadius: 12,
      padding: "20px 24px",
      position: "relative",
      boxShadow: isPinned ? `0 0 24px ${color}33` : "none",
    }}>
      {isPinned && (
        <div style={{
          position: "absolute", top: 10, right: 14,
          fontSize: 10, color: color, letterSpacing: 2, textTransform: "uppercase",
        }}>
          ★ most emotional
        </div>
      )}

      <div style={{ display: "flex", alignItems: "baseline", gap: 12, marginBottom: 8 }}>
        <span style={{ fontSize: 20, marginRight: 4 }}>{emoji}</span>
        <span style={{ fontSize: 22, fontWeight: 700, color: "#f1f5f9" }}>
          ${report.symbol}
        </span>
        <span style={{
          fontSize: 11, fontWeight: 600, color: color,
          background: `${color}22`, padding: "2px 8px", borderRadius: 4,
          textTransform: "uppercase", letterSpacing: 1,
        }}>
          {report.phase}
        </span>
      </div>

      <div style={{ fontSize: 28, fontWeight: 800, color, marginBottom: 4 }}>
        {report.emotion_score.toFixed(1)}
        <span style={{ fontSize: 14, color: "#475569", marginLeft: 4 }}>/100</span>
      </div>

      <p style={{ fontSize: 12, color: "#94a3b8", marginBottom: 16, lineHeight: 1.5 }}>
        {report.headline}
      </p>

      <div style={{ background: "#0a0f0a", borderRadius: 4, height: 6, overflow: "hidden", marginBottom: 10 }}>
        <div style={{
          height: "100%", width: `${report.emotion_score}%`,
          background: `linear-gradient(90deg, ${color}88, ${color})`,
          borderRadius: 4, transition: "width 0.6s ease",
        }} />
      </div>

      <div style={{ fontSize: 11, color: "#475569" }}>
        {report.triggered_count}/4 signals active
      </div>
    </div>
  );
}
