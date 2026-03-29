import { useState, useEffect } from "react";
import type { MoodReport } from "./types";
import { MOCK_REPORTS } from "./mockData";
import { MoodCard } from "./components/MoodCard";
import { SignalPanel } from "./components/SignalPanel";
import { WojakFeed } from "./components/WojakFeed";

function jitter(reports: MoodReport[]): MoodReport[] {
  return reports.map((r) => ({
    ...r,
    emotion_score: Math.max(0, Math.min(100, r.emotion_score + (Math.random() - 0.5) * 4)),
    signals: r.signals.map((s) => ({
      ...s,
      score: Math.max(0, Math.min(100, s.score + (Math.random() - 0.5) * 6)),
    })),
  }));
}

export default function App() {
  const [reports, setReports] = useState<MoodReport[]>(MOCK_REPORTS);
  const [selected, setSelected] = useState<MoodReport>(MOCK_REPORTS[0]);

  useEffect(() => {
    const id = setInterval(() => {
      const updated = jitter(reports);
      setReports(updated);
      setSelected((prev) => updated.find((r) => r.token_mint === prev.token_mint) ?? updated[0]);
    }, 4000);
    return () => clearInterval(id);
  }, [reports]);

  const sorted = [...reports].sort((a, b) => b.emotion_score - a.emotion_score);
  const top = sorted[0];

  return (
    <div style={{ minHeight: "100vh", background: "#030803", color: "#f1f5f9", fontFamily: "monospace" }}>
      <div style={{
        borderBottom: "1px solid #0f1a0f",
        padding: "16px 32px",
        display: "flex", alignItems: "center", justifyContent: "space-between",
      }}>
        <div style={{ display: "flex", alignItems: "baseline", gap: 12 }}>
          <span style={{ fontSize: 18, fontWeight: 800, color: "#84cc16", letterSpacing: 1 }}>
            ZW<span style={{ color: "#ca8a04" }}>ONK</span>
          </span>
          <span style={{ fontSize: 11, color: "#1a3a0a", letterSpacing: 2, textTransform: "uppercase" }}>
            solana meme emotion engine
          </span>
        </div>
        <span style={{ fontSize: 11, color: "#1a2a1a", letterSpacing: 1 }}>
          live · updates every 4s
        </span>
      </div>

      <div style={{ maxWidth: 1200, margin: "0 auto", padding: "32px 24px" }}>
        <div style={{ marginBottom: 32 }}>
          <p style={{ fontSize: 10, color: "#1a2a1a", letterSpacing: 3, textTransform: "uppercase", marginBottom: 12 }}>
            Most emotional
          </p>
          <MoodCard report={top} isPinned />
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 340px", gap: 24 }}>
          <div>
            <p style={{ fontSize: 10, color: "#1a2a1a", letterSpacing: 3, textTransform: "uppercase", marginBottom: 12 }}>
              All tokens
            </p>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
              {sorted.map((r) => (
                <div
                  key={r.token_mint}
                  onClick={() => setSelected(r)}
                  style={{ cursor: "pointer", opacity: selected.token_mint === r.token_mint ? 1 : 0.75 }}
                >
                  <MoodCard report={r} />
                </div>
              ))}
            </div>
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
            <div>
              <p style={{ fontSize: 10, color: "#1a2a1a", letterSpacing: 3, textTransform: "uppercase", marginBottom: 12 }}>
                ${selected.symbol} signals
              </p>
              <SignalPanel signals={selected.signals} />
            </div>
            <WojakFeed reports={reports} />
          </div>
        </div>
      </div>
    </div>
  );
}
