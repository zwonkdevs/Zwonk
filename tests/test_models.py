import pytest
from zwonk.models import TokenMood, EmotionSignal, WojakPhase, MoodReport


class TestTokenMood:
    def test_basic_creation(self):
        m = TokenMood(
            token_mint="abc", symbol="TEST", price_usd=0.001,
            price_change_1h_pct=5.0, price_change_24h_pct=10.0,
            volume_1h=1000, volume_24h=24000,
            holder_count=100, holder_count_prev=90, market_cap_usd=50000,
        )
        assert m.symbol == "TEST"
        assert m.price_usd == 0.001

    def test_default_age_hours(self):
        m = TokenMood(
            token_mint="x", symbol="X", price_usd=1.0,
            price_change_1h_pct=0.0, price_change_24h_pct=0.0,
            volume_1h=0, volume_24h=0, holder_count=0,
            holder_count_prev=0, market_cap_usd=0,
        )
        assert m.age_hours == 24.0

    def test_custom_age_hours(self):
        m = TokenMood(
            token_mint="x", symbol="X", price_usd=1.0,
            price_change_1h_pct=0.0, price_change_24h_pct=0.0,
            volume_1h=0, volume_24h=0, holder_count=0,
            holder_count_prev=0, market_cap_usd=0, age_hours=12.0,
        )
        assert m.age_hours == 12.0

    def test_volume_prev_default(self):
        m = TokenMood(
            token_mint="x", symbol="X", price_usd=1.0,
            price_change_1h_pct=0.0, price_change_24h_pct=0.0,
            volume_1h=0, volume_24h=0, holder_count=0,
            holder_count_prev=0, market_cap_usd=0,
        )
        assert m.volume_prev_24h == 0.0

    def test_negative_price_change(self):
        m = TokenMood(
            token_mint="x", symbol="CRASH", price_usd=0.0001,
            price_change_1h_pct=-40.0, price_change_24h_pct=-80.0,
            volume_1h=100000, volume_24h=500000, holder_count=200,
            holder_count_prev=300, market_cap_usd=80000,
        )
        assert m.price_change_1h_pct == -40.0

    def test_zero_market_cap(self):
        m = TokenMood(
            token_mint="x", symbol="ZERO", price_usd=0.0,
            price_change_1h_pct=0.0, price_change_24h_pct=0.0,
            volume_1h=0, volume_24h=0, holder_count=0,
            holder_count_prev=0, market_cap_usd=0,
        )
        assert m.market_cap_usd == 0


class TestEmotionSignal:
    def test_weighted_score(self):
        sig = EmotionSignal(name="test", triggered=True, score=80.0, weight=0.35)
        assert sig.weighted_score == pytest.approx(28.0)

    def test_weighted_score_zero(self):
        sig = EmotionSignal(name="test", triggered=False, score=0.0, weight=0.35)
        assert sig.weighted_score == pytest.approx(0.0)

    def test_raw_default_empty(self):
        sig = EmotionSignal(name="test", triggered=False, score=10.0, weight=0.20)
        assert sig.raw == {}

    def test_raw_custom(self):
        sig = EmotionSignal(name="test", triggered=True, score=60.0, weight=0.30, raw={"ratio": 3.1})
        assert sig.raw["ratio"] == 3.1

    def test_partial_weight(self):
        sig = EmotionSignal(name="test", triggered=True, score=50.0, weight=0.30)
        assert sig.weighted_score == pytest.approx(15.0)


class TestWojakPhase:
    def test_all_phases(self):
        phases = [WojakPhase.DOOMER, WojakPhase.FEELS, WojakPhase.BLOOMER, WojakPhase.MEWING]
        assert len(phases) == 4

    def test_phase_values(self):
        assert WojakPhase.DOOMER.value == "DOOMER"
        assert WojakPhase.FEELS.value == "FEELS"
        assert WojakPhase.BLOOMER.value == "BLOOMER"
        assert WojakPhase.MEWING.value == "MEWING"

    def test_string_comparison(self):
        assert WojakPhase.DOOMER == "DOOMER"


class TestMoodReport:
    def _make_signals(self):
        return [
            EmotionSignal("sentiment_velocity", True, 80.0, 0.35),
            EmotionSignal("crowd_surge", True, 70.0, 0.30),
            EmotionSignal("holder_momentum", False, 10.0, 0.20),
            EmotionSignal("market_depth", False, 5.0, 0.15),
        ]

    def test_triggered_count(self):
        r = MoodReport("x", "T", WojakPhase.BLOOMER, 55.0, self._make_signals(), "test")
        assert r.triggered_count == 2

    def test_is_bullish_bloomer(self):
        r = MoodReport("x", "T", WojakPhase.BLOOMER, 60.0, self._make_signals(), "test")
        assert r.is_bullish is True

    def test_is_bullish_mewing(self):
        r = MoodReport("x", "T", WojakPhase.MEWING, 85.0, self._make_signals(), "test")
        assert r.is_bullish is True

    def test_not_bullish_doomer(self):
        r = MoodReport("x", "T", WojakPhase.DOOMER, 10.0, self._make_signals(), "test")
        assert r.is_bullish is False

    def test_not_bullish_feels(self):
        r = MoodReport("x", "T", WojakPhase.FEELS, 35.0, self._make_signals(), "test")
        assert r.is_bullish is False

    def test_triggered_count_all(self):
        sigs = [EmotionSignal(f"s{i}", True, 50.0, 0.25) for i in range(4)]
        r = MoodReport("x", "T", WojakPhase.MEWING, 80.0, sigs, "test")
        assert r.triggered_count == 4

    def test_triggered_count_none(self):
        sigs = [EmotionSignal(f"s{i}", False, 0.0, 0.25) for i in range(4)]
        r = MoodReport("x", "T", WojakPhase.DOOMER, 0.0, sigs, "test")
        assert r.triggered_count == 0
