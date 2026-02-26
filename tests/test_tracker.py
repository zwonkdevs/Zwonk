import pytest
from zwonk.models import TokenMood, WojakPhase
from zwonk.tracker import track, track_batch, most_emotional


def make_mood(**kwargs):
    defaults = dict(
        token_mint="TestXyz", symbol="TEST", price_usd=0.001,
        price_change_1h_pct=0.0, price_change_24h_pct=0.0,
        volume_1h=10_000, volume_24h=240_000,
        holder_count=1_000, holder_count_prev=1_000, market_cap_usd=500_000,
    )
    defaults.update(kwargs)
    return TokenMood(**defaults)


class TestTrack:
    def test_returns_report(self, doomer_mood):
        r = track(doomer_mood)
        assert r.token_mint == doomer_mood.token_mint
        assert r.symbol == doomer_mood.symbol

    def test_doomer_phase(self, doomer_mood):
        r = track(doomer_mood)
        assert r.phase == WojakPhase.DOOMER

    def test_mewing_phase(self, mewing_mood):
        r = track(mewing_mood)
        assert r.phase == WojakPhase.MEWING

    def test_score_in_range(self, bloomer_mood):
        r = track(bloomer_mood)
        assert 0.0 <= r.emotion_score <= 100.0

    def test_has_four_signals(self, doomer_mood):
        r = track(doomer_mood)
        assert len(r.signals) == 4

    def test_headline_not_empty(self, doomer_mood):
        r = track(doomer_mood)
        assert len(r.headline) > 0

    def test_score_rounded(self, bloomer_mood):
        r = track(bloomer_mood)
        assert r.emotion_score == round(r.emotion_score, 2)

    def test_bloomer_is_bullish(self, bloomer_mood):
        r = track(bloomer_mood)
        assert r.is_bullish is True

    def test_doomer_not_bullish(self, doomer_mood):
        r = track(doomer_mood)
        assert r.is_bullish is False

    def test_high_price_change_boosts_score(self):
        low = make_mood(price_change_1h_pct=0.0)
        high = make_mood(price_change_1h_pct=80.0)
        assert track(high).emotion_score > track(low).emotion_score

    def test_high_volume_boosts_score(self):
        low = make_mood(volume_1h=1_000, volume_24h=240_000)
        high = make_mood(volume_1h=2_000_000, volume_24h=240_000)
        assert track(high).emotion_score > track(low).emotion_score

    def test_dump_counts_as_velocity(self):
        dump = make_mood(price_change_1h_pct=-40.0)
        flat = make_mood(price_change_1h_pct=0.0)
        assert track(dump).emotion_score > track(flat).emotion_score

    def test_triggered_count_type(self, bloomer_mood):
        r = track(bloomer_mood)
        assert isinstance(r.triggered_count, int)

    def test_feels_phase(self, feels_mood):
        r = track(feels_mood)
        assert r.phase in (WojakPhase.FEELS, WojakPhase.BLOOMER)


class TestTrackBatch:
    def test_empty_list(self):
        assert track_batch([]) == []

    def test_returns_same_count(self, doomer_mood, bloomer_mood, mewing_mood):
        results = track_batch([doomer_mood, bloomer_mood, mewing_mood])
        assert len(results) == 3

    def test_order_preserved(self, doomer_mood, bloomer_mood):
        results = track_batch([doomer_mood, bloomer_mood])
        assert results[0].symbol == doomer_mood.symbol
        assert results[1].symbol == bloomer_mood.symbol

    def test_single_item(self, doomer_mood):
        results = track_batch([doomer_mood])
        assert len(results) == 1

    def test_symbols_correct(self, doomer_mood, mewing_mood):
        results = track_batch([doomer_mood, mewing_mood])
        symbols = [r.symbol for r in results]
        assert "DOOM" in symbols
        assert "MEW" in symbols


class TestMostEmotional:
    def test_returns_highest_score(self, doomer_mood, bloomer_mood, mewing_mood):
        top = most_emotional([doomer_mood, bloomer_mood, mewing_mood])
        assert top.symbol == mewing_mood.symbol

    def test_single_item(self, doomer_mood):
        top = most_emotional([doomer_mood])
        assert top.symbol == doomer_mood.symbol

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            most_emotional([])

    def test_doomer_vs_bloomer(self, doomer_mood, bloomer_mood):
        top = most_emotional([doomer_mood, bloomer_mood])
        assert top.symbol == bloomer_mood.symbol
