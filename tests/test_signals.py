import pytest
from zwonk.models import TokenMood
from zwonk.signals import (
    sentiment_velocity_signal,
    crowd_surge_signal,
    holder_momentum_signal,
    market_depth_signal,
    run_all_signals,
    SENTIMENT_VELOCITY_WEIGHT,
    CROWD_SURGE_WEIGHT,
    HOLDER_MOMENTUM_WEIGHT,
    MARKET_DEPTH_WEIGHT,
    SENTIMENT_VELOCITY_THRESHOLD,
    CROWD_SURGE_THRESHOLD,
    HOLDER_MOMENTUM_THRESHOLD,
    MARKET_DEPTH_THRESHOLD,
)


def make_mood(**kwargs):
    defaults = dict(
        token_mint="TestXyz", symbol="TEST", price_usd=0.001,
        price_change_1h_pct=0.0, price_change_24h_pct=0.0,
        volume_1h=10_000, volume_24h=240_000,
        holder_count=1_000, holder_count_prev=1_000,
        market_cap_usd=500_000, age_hours=24.0,
    )
    defaults.update(kwargs)
    return TokenMood(**defaults)


class TestWeights:
    def test_sum_to_one(self):
        total = (SENTIMENT_VELOCITY_WEIGHT + CROWD_SURGE_WEIGHT +
                 HOLDER_MOMENTUM_WEIGHT + MARKET_DEPTH_WEIGHT)
        assert total == pytest.approx(1.0)

    def test_sentiment_velocity_weight(self):
        assert SENTIMENT_VELOCITY_WEIGHT == pytest.approx(0.35)

    def test_crowd_surge_weight(self):
        assert CROWD_SURGE_WEIGHT == pytest.approx(0.30)

    def test_holder_momentum_weight(self):
        assert HOLDER_MOMENTUM_WEIGHT == pytest.approx(0.20)

    def test_market_depth_weight(self):
        assert MARKET_DEPTH_WEIGHT == pytest.approx(0.15)


class TestSentimentVelocity:
    def test_triggers_above_threshold(self):
        m = make_mood(price_change_1h_pct=SENTIMENT_VELOCITY_THRESHOLD + 5)
        sig = sentiment_velocity_signal(m)
        assert sig.triggered is True

    def test_not_triggered_below_threshold(self):
        m = make_mood(price_change_1h_pct=5.0)
        sig = sentiment_velocity_signal(m)
        assert sig.triggered is False

    def test_negative_dump_triggers(self):
        m = make_mood(price_change_1h_pct=-30.0)
        sig = sentiment_velocity_signal(m)
        assert sig.triggered is True

    def test_score_capped_at_100(self):
        m = make_mood(price_change_1h_pct=200.0)
        sig = sentiment_velocity_signal(m)
        assert sig.score == pytest.approx(100.0)

    def test_zero_change_zero_score(self):
        m = make_mood(price_change_1h_pct=0.0)
        sig = sentiment_velocity_signal(m)
        assert sig.score == pytest.approx(0.0)

    def test_score_scales_linearly(self):
        m = make_mood(price_change_1h_pct=25.0)
        sig = sentiment_velocity_signal(m)
        assert sig.score == pytest.approx(50.0)

    def test_weight_correct(self):
        m = make_mood(price_change_1h_pct=10.0)
        sig = sentiment_velocity_signal(m)
        assert sig.weight == pytest.approx(SENTIMENT_VELOCITY_WEIGHT)

    def test_name_correct(self):
        m = make_mood()
        sig = sentiment_velocity_signal(m)
        assert sig.name == "sentiment_velocity"

    def test_raw_contains_keys(self):
        m = make_mood(price_change_1h_pct=20.0)
        sig = sentiment_velocity_signal(m)
        assert "price_change_1h_pct" in sig.raw
        assert "abs_change" in sig.raw

    def test_exact_threshold_triggers(self):
        m = make_mood(price_change_1h_pct=SENTIMENT_VELOCITY_THRESHOLD)
        sig = sentiment_velocity_signal(m)
        assert sig.triggered is True


class TestCrowdSurge:
    def test_triggers_above_threshold(self):
        # baseline = 240k/24 = 10k. 28k/10k = 2.8 >= 2.8
        m = make_mood(volume_1h=28_000, volume_24h=240_000)
        sig = crowd_surge_signal(m)
        assert sig.triggered is True

    def test_not_triggered_below_threshold(self):
        m = make_mood(volume_1h=5_000, volume_24h=240_000)
        sig = crowd_surge_signal(m)
        assert sig.triggered is False

    def test_score_capped_at_100(self):
        m = make_mood(volume_1h=50_000_000, volume_24h=240_000)
        sig = crowd_surge_signal(m)
        assert sig.score == pytest.approx(100.0)

    def test_zero_volume_zero_score(self):
        m = make_mood(volume_1h=0, volume_24h=0)
        sig = crowd_surge_signal(m)
        assert sig.score == pytest.approx(0.0)

    def test_weight_correct(self):
        m = make_mood(volume_1h=10_000, volume_24h=240_000)
        sig = crowd_surge_signal(m)
        assert sig.weight == pytest.approx(CROWD_SURGE_WEIGHT)

    def test_name_correct(self):
        m = make_mood()
        sig = crowd_surge_signal(m)
        assert sig.name == "crowd_surge"

    def test_raw_contains_ratio(self):
        m = make_mood(volume_1h=28_000, volume_24h=240_000)
        sig = crowd_surge_signal(m)
        assert "ratio" in sig.raw

    def test_baseline_fallback_nonzero(self):
        m = make_mood(volume_1h=100, volume_24h=0)
        sig = crowd_surge_signal(m)
        assert sig.score > 0

    def test_score_at_threshold(self):
        # ratio exactly 2.8 → score = 100
        m = make_mood(volume_1h=28_000, volume_24h=240_000)
        sig = crowd_surge_signal(m)
        assert sig.score == pytest.approx(100.0)


class TestHolderMomentum:
    def test_triggers_above_threshold(self):
        # growth = (1060-1000)/1000 * 100 = 6% >= 5%
        m = make_mood(holder_count=1_060, holder_count_prev=1_000)
        sig = holder_momentum_signal(m)
        assert sig.triggered is True

    def test_not_triggered_below_threshold(self):
        m = make_mood(holder_count=1_020, holder_count_prev=1_000)
        sig = holder_momentum_signal(m)
        assert sig.triggered is False

    def test_shrinking_holders_zero_score(self):
        m = make_mood(holder_count=900, holder_count_prev=1_000)
        sig = holder_momentum_signal(m)
        assert sig.score == pytest.approx(0.0)
        assert sig.triggered is False

    def test_score_capped_at_100(self):
        m = make_mood(holder_count=5_000, holder_count_prev=1_000)
        sig = holder_momentum_signal(m)
        assert sig.score == pytest.approx(100.0)

    def test_zero_prev_no_crash(self):
        m = make_mood(holder_count=100, holder_count_prev=0)
        sig = holder_momentum_signal(m)
        assert sig.score == pytest.approx(0.0)

    def test_weight_correct(self):
        m = make_mood(holder_count=1_100, holder_count_prev=1_000)
        sig = holder_momentum_signal(m)
        assert sig.weight == pytest.approx(HOLDER_MOMENTUM_WEIGHT)

    def test_name_correct(self):
        m = make_mood()
        sig = holder_momentum_signal(m)
        assert sig.name == "holder_momentum"

    def test_raw_contains_growth_pct(self):
        m = make_mood(holder_count=1_100, holder_count_prev=1_000)
        sig = holder_momentum_signal(m)
        assert "growth_pct" in sig.raw
        assert sig.raw["growth_pct"] == pytest.approx(10.0)

    def test_exact_threshold_triggers(self):
        m = make_mood(holder_count=1_050, holder_count_prev=1_000)
        sig = holder_momentum_signal(m)
        assert sig.triggered is True


class TestMarketDepth:
    def test_triggers_above_threshold(self):
        # ratio = 12000 / (500000/1000) = 12000/500 = 24 >= 12
        m = make_mood(holder_count=12_000, market_cap_usd=500_000)
        sig = market_depth_signal(m)
        assert sig.triggered is True

    def test_not_triggered_below_threshold(self):
        m = make_mood(holder_count=1_000, market_cap_usd=500_000)
        sig = market_depth_signal(m)
        assert sig.triggered is False

    def test_zero_market_cap_no_crash(self):
        m = make_mood(holder_count=1_000, market_cap_usd=0)
        sig = market_depth_signal(m)
        assert sig.score == pytest.approx(0.0)

    def test_score_capped_at_100(self):
        m = make_mood(holder_count=1_000_000, market_cap_usd=1_000)
        sig = market_depth_signal(m)
        assert sig.score == pytest.approx(100.0)

    def test_weight_correct(self):
        m = make_mood(holder_count=5_000, market_cap_usd=500_000)
        sig = market_depth_signal(m)
        assert sig.weight == pytest.approx(MARKET_DEPTH_WEIGHT)

    def test_name_correct(self):
        m = make_mood()
        sig = market_depth_signal(m)
        assert sig.name == "market_depth"

    def test_raw_contains_ratio(self):
        m = make_mood(holder_count=6_000, market_cap_usd=500_000)
        sig = market_depth_signal(m)
        assert "ratio" in sig.raw

    def test_high_mcap_few_holders_low_score(self):
        m = make_mood(holder_count=10, market_cap_usd=10_000_000)
        sig = market_depth_signal(m)
        assert sig.score < 1.0


class TestRunAllSignals:
    def test_returns_four(self, doomer_mood):
        sigs = run_all_signals(doomer_mood)
        assert len(sigs) == 4

    def test_signal_names(self, doomer_mood):
        names = [s.name for s in run_all_signals(doomer_mood)]
        assert "sentiment_velocity" in names
        assert "crowd_surge" in names
        assert "holder_momentum" in names
        assert "market_depth" in names

    def test_weights_sum_one(self, doomer_mood):
        sigs = run_all_signals(doomer_mood)
        assert sum(s.weight for s in sigs) == pytest.approx(1.0)
