from .models import TokenMood, MoodReport
from .signals import run_all_signals
from .scorer import compute_emotion_score, classify_phase, get_headline


def track(mood: TokenMood) -> MoodReport:
    signals = run_all_signals(mood)
    score = compute_emotion_score(signals)
    phase = classify_phase(score)
    headline = get_headline(phase)
    return MoodReport(
        token_mint=mood.token_mint,
        symbol=mood.symbol,
        phase=phase,
        emotion_score=round(score, 2),
        signals=signals,
        headline=headline,
    )


def track_batch(moods: list[TokenMood]) -> list[MoodReport]:
    return [track(m) for m in moods]


def most_emotional(moods: list[TokenMood]) -> TokenMood:
    if not moods:
        raise ValueError("cannot find most emotional token in empty list")
    return max(moods, key=lambda m: track(m).emotion_score)
