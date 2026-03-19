export type WojakPhase = "DOOMER" | "FEELS" | "BLOOMER" | "MEWING";

export interface EmotionSignal {
  name: string;
  triggered: boolean;
  score: number;
  weight: number;
  raw: Record<string, number>;
}

export interface MoodReport {
  token_mint: string;
  symbol: string;
  phase: WojakPhase;
  emotion_score: number;
  signals: EmotionSignal[];
  headline: string;
  is_bullish: boolean;
  triggered_count: number;
}

export interface TokenMood {
  token_mint: string;
  symbol: string;
  price_usd: number;
  price_change_1h_pct: number;
  price_change_24h_pct: number;
  volume_1h: number;
  volume_24h: number;
  holder_count: number;
  holder_count_prev: number;
  market_cap_usd: number;
  age_hours?: number;
}
