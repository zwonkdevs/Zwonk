from .models import TokenMood, EmotionSignal

SENTIMENT_VELOCITY_WEIGHT = 0.35
CROWD_SURGE_WEIGHT = 0.30
HOLDER_MOMENTUM_WEIGHT = 0.20
MARKET_DEPTH_WEIGHT = 0.15

SENTIMENT_VELOCITY_THRESHOLD = 18.0   # |1h price change| >= 18%
CROWD_SURGE_THRESHOLD = 2.8           # 1h vol >= 2.8× hourly baseline
HOLDER_MOMENTUM_THRESHOLD = 5.0       # holder growth >= 5%
MARKET_DEPTH_THRESHOLD = 12.0         # holders per $1k mcap >= 12


def sentiment_velocity_signal(mood: TokenMood) -> EmotionSignal:
    """
    Measures the speed of emotional contagion through price.
    Wojak doesn't walk — he runs. When a token moves fast in either direction,
    the crowd's emotional state is shifting. Velocity is the heartbeat of the narrative.
    """
    change = abs(mood.price_change_1h_pct)
    triggered = change >= SENTIMENT_VELOCITY_THRESHOLD
    score = min(change * (100 / 50), 100.0)
    return EmotionSignal(
        name="sentiment_velocity",
        triggered=triggered,
        score=score,
        weight=SENTIMENT_VELOCITY_WEIGHT,
        raw={"price_change_1h_pct": mood.price_change_1h_pct, "abs_change": change},
    )


def crowd_surge_signal(mood: TokenMood) -> EmotionSignal:
    """
    Measures the size of the emotional crowd gathering around a token.
    In Wojak lore, nothing spreads faster than collective feeling.
    Volume above baseline means Wojak has left his room and gone outside.
    """
    baseline = mood.volume_24h / 24 if mood.volume_24h > 0 else 1.0
    ratio = mood.volume_1h / baseline if baseline > 0 else 0.0
    triggered = ratio >= CROWD_SURGE_THRESHOLD
    score = min(ratio * (100 / CROWD_SURGE_THRESHOLD), 100.0)
    return EmotionSignal(
        name="crowd_surge",
        triggered=triggered,
        score=score,
        weight=CROWD_SURGE_WEIGHT,
        raw={"volume_1h": mood.volume_1h, "baseline": baseline, "ratio": ratio},
    )


def holder_momentum_signal(mood: TokenMood) -> EmotionSignal:
    """
    Tracks the growth of the Wojak family — new believers joining the narrative.
    A doomer token loses holders. A bloomer token gains them.
    Holder momentum is the clearest sign that the emotional cycle is turning.
    """
    if mood.holder_count_prev <= 0:
        growth_pct = 0.0
    else:
        growth_pct = (mood.holder_count - mood.holder_count_prev) / mood.holder_count_prev * 100
    triggered = growth_pct >= HOLDER_MOMENTUM_THRESHOLD
    score = max(0.0, min(growth_pct * 4.0, 100.0))
    return EmotionSignal(
        name="holder_momentum",
        triggered=triggered,
        score=score,
        weight=HOLDER_MOMENTUM_WEIGHT,
        raw={"holder_count": mood.holder_count, "holder_count_prev": mood.holder_count_prev, "growth_pct": growth_pct},
    )


def market_depth_signal(mood: TokenMood) -> EmotionSignal:
    """
    Measures the emotional authenticity of the community.
    Wojak's pain is real because it belongs to everyone, not just whales.
    High holders relative to market cap = distributed emotion = organic traction.
    """
    if mood.market_cap_usd <= 0:
        ratio = 0.0
    else:
        ratio = mood.holder_count / (mood.market_cap_usd / 1000)
    triggered = ratio >= MARKET_DEPTH_THRESHOLD
    score = min(ratio * (100 / MARKET_DEPTH_THRESHOLD), 100.0)
    return EmotionSignal(
        name="market_depth",
        triggered=triggered,
        score=score,
        weight=MARKET_DEPTH_WEIGHT,
        raw={"holder_count": mood.holder_count, "market_cap_usd": mood.market_cap_usd, "ratio": ratio},
    )


def run_all_signals(mood: TokenMood) -> list[EmotionSignal]:
    return [
        sentiment_velocity_signal(mood),
        crowd_surge_signal(mood),
        holder_momentum_signal(mood),
        market_depth_signal(mood),
    ]
