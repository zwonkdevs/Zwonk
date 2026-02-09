from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class WojakPhase(str, Enum):
    DOOMER = "DOOMER"
    FEELS = "FEELS"
    BLOOMER = "BLOOMER"
    MEWING = "MEWING"


@dataclass
class TokenMood:
    token_mint: str
    symbol: str
    price_usd: float
    price_change_1h_pct: float
    price_change_24h_pct: float
    volume_1h: float
    volume_24h: float
    holder_count: int
    holder_count_prev: int
    market_cap_usd: float
    age_hours: float = 24.0
    volume_prev_24h: float = 0.0


@dataclass
class EmotionSignal:
    name: str
    triggered: bool
    score: float
    weight: float
    raw: dict = field(default_factory=dict)

    @property
    def weighted_score(self) -> float:
        return self.score * self.weight


@dataclass
class MoodReport:
    token_mint: str
    symbol: str
    phase: WojakPhase
    emotion_score: float
    signals: list[EmotionSignal]
    headline: str

    @property
    def is_bullish(self) -> bool:
        return self.phase in (WojakPhase.BLOOMER, WojakPhase.MEWING)

    @property
    def triggered_count(self) -> int:
        return sum(1 for s in self.signals if s.triggered)
