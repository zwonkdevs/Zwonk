from .models import EmotionSignal, WojakPhase

_THRESHOLDS = {
    WojakPhase.MEWING: 76.0,
    WojakPhase.BLOOMER: 51.0,
    WojakPhase.FEELS: 26.0,
    WojakPhase.DOOMER: 0.0,
}

_HEADLINES = {
    WojakPhase.DOOMER: "Token sits in the doomer zone. No emotional momentum detected. Could be accumulation — or just despair.",
    WojakPhase.FEELS: "Early feelings stirring. The crowd is starting to notice. Not confirmed, but worth watching.",
    WojakPhase.BLOOMER: "Bloomer phase confirmed. Community energy is building. Emotional cycle is in motion.",
    WojakPhase.MEWING: "Mewing. Peak emotional momentum. The wojak has transformed — but late entries carry maximum risk.",
}


def compute_emotion_score(signals: list[EmotionSignal]) -> float:
    return sum(s.weighted_score for s in signals)


def classify_phase(score: float) -> WojakPhase:
    if score >= _THRESHOLDS[WojakPhase.MEWING]:
        return WojakPhase.MEWING
    if score >= _THRESHOLDS[WojakPhase.BLOOMER]:
        return WojakPhase.BLOOMER
    if score >= _THRESHOLDS[WojakPhase.FEELS]:
        return WojakPhase.FEELS
    return WojakPhase.DOOMER


def get_headline(phase: WojakPhase) -> str:
    return _HEADLINES[phase]


def triggered_count(signals: list[EmotionSignal]) -> int:
    return sum(1 for s in signals if s.triggered)
