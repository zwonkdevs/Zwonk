import pytest
from zwonk.models import EmotionSignal, WojakPhase
from zwonk.scorer import (
    compute_emotion_score,
    classify_phase,
    get_headline,
    triggered_count,
)


def make_signals(scores, weights=None, triggered=None):
    if weights is None:
        weights = [0.35, 0.30, 0.20, 0.15]
    if triggered is None:
        triggered = [True] * len(scores)
    names = ["sentiment_velocity", "crowd_surge", "holder_momentum", "market_depth"]
    return [
        EmotionSignal(name=names[i], triggered=triggered[i], score=scores[i], weight=weights[i])
        for i in range(len(scores))
    ]


class TestComputeEmotionScore:
    def test_all_zero(self):
        sigs = make_signals([0, 0, 0, 0])
        assert compute_emotion_score(sigs) == pytest.approx(0.0)

    def test_all_100(self):
        sigs = make_signals([100, 100, 100, 100])
        assert compute_emotion_score(sigs) == pytest.approx(100.0)

    def test_partial_scores(self):
        sigs = make_signals([80, 60, 40, 20])
        expected = 80*0.35 + 60*0.30 + 40*0.20 + 20*0.15
        assert compute_emotion_score(sigs) == pytest.approx(expected)

    def test_single_signal(self):
        sigs = [EmotionSignal("v", True, 70.0, 1.0)]
        assert compute_emotion_score(sigs) == pytest.approx(70.0)

    def test_independent_of_triggered(self):
        a = make_signals([50, 50, 50, 50], triggered=[True]*4)
        b = make_signals([50, 50, 50, 50], triggered=[False]*4)
        assert compute_emotion_score(a) == compute_emotion_score(b)


class TestClassifyPhase:
    def test_doomer_range(self):
        assert classify_phase(0.0) == WojakPhase.DOOMER
        assert classify_phase(25.0) == WojakPhase.DOOMER

    def test_feels_range(self):
        assert classify_phase(26.0) == WojakPhase.FEELS
        assert classify_phase(50.0) == WojakPhase.FEELS

    def test_bloomer_range(self):
        assert classify_phase(51.0) == WojakPhase.BLOOMER
        assert classify_phase(75.0) == WojakPhase.BLOOMER

    def test_mewing_range(self):
        assert classify_phase(76.0) == WojakPhase.MEWING
        assert classify_phase(100.0) == WojakPhase.MEWING

    def test_zero_is_doomer(self):
        assert classify_phase(0.0) == WojakPhase.DOOMER

    def test_hundred_is_mewing(self):
        assert classify_phase(100.0) == WojakPhase.MEWING

    def test_exact_feels_boundary(self):
        assert classify_phase(26.0) == WojakPhase.FEELS

    def test_exact_bloomer_boundary(self):
        assert classify_phase(51.0) == WojakPhase.BLOOMER

    def test_exact_mewing_boundary(self):
        assert classify_phase(76.0) == WojakPhase.MEWING


class TestGetHeadline:
    def test_doomer_headline(self):
        h = get_headline(WojakPhase.DOOMER)
        assert "doomer" in h.lower()

    def test_feels_headline(self):
        h = get_headline(WojakPhase.FEELS)
        assert len(h) > 0

    def test_bloomer_headline(self):
        h = get_headline(WojakPhase.BLOOMER)
        assert "bloomer" in h.lower()

    def test_mewing_headline(self):
        h = get_headline(WojakPhase.MEWING)
        assert "mewing" in h.lower() or "risk" in h.lower()

    def test_all_phases_return_string(self):
        for phase in WojakPhase:
            h = get_headline(phase)
            assert isinstance(h, str) and len(h) > 5


class TestTriggeredCount:
    def test_all_triggered(self):
        sigs = make_signals([80]*4, triggered=[True]*4)
        assert triggered_count(sigs) == 4

    def test_none_triggered(self):
        sigs = make_signals([0]*4, triggered=[False]*4)
        assert triggered_count(sigs) == 0

    def test_partial(self):
        sigs = make_signals([80, 60, 10, 5], triggered=[True, True, False, False])
        assert triggered_count(sigs) == 2

    def test_single(self):
        sigs = make_signals([80, 0, 0, 0], triggered=[True, False, False, False])
        assert triggered_count(sigs) == 1

    def test_empty(self):
        assert triggered_count([]) == 0
