import pytest
from zwonk.models import MoodReport, WojakPhase, EmotionSignal
from zwonk.tracker import track
from zwonk.utils.helpers import format_report, filter_by_phase, sort_by_score, summary_table


def make_report(symbol, score, phase):
    sigs = [
        EmotionSignal("sentiment_velocity", True, score, 0.35),
        EmotionSignal("crowd_surge", True, score, 0.30),
        EmotionSignal("holder_momentum", False, score * 0.5, 0.20),
        EmotionSignal("market_depth", False, score * 0.3, 0.15),
    ]
    return MoodReport(token_mint=f"{symbol}xyz", symbol=symbol, phase=phase,
                      emotion_score=score, signals=sigs, headline="test headline")


class TestFormatReport:
    def test_contains_symbol(self, doomer_mood):
        r = track(doomer_mood)
        assert "DOOM" in format_report(r)

    def test_contains_phase(self, doomer_mood):
        r = track(doomer_mood)
        assert "DOOMER" in format_report(r)

    def test_contains_score(self, doomer_mood):
        r = track(doomer_mood)
        out = format_report(r)
        assert str(int(r.emotion_score)) in out or f"{r.emotion_score:.1f}" in out

    def test_contains_signal_names(self, doomer_mood):
        r = track(doomer_mood)
        out = format_report(r)
        assert "sentiment_velocity" in out
        assert "crowd_surge" in out
        assert "holder_momentum" in out
        assert "market_depth" in out

    def test_returns_string(self, doomer_mood):
        r = track(doomer_mood)
        assert isinstance(format_report(r), str)


class TestFilterByPhase:
    def test_filters_correctly(self):
        reports = [
            make_report("A", 10, WojakPhase.DOOMER),
            make_report("B", 40, WojakPhase.FEELS),
            make_report("C", 65, WojakPhase.BLOOMER),
        ]
        doomers = filter_by_phase(reports, WojakPhase.DOOMER)
        assert len(doomers) == 1
        assert doomers[0].symbol == "A"

    def test_empty_result(self):
        reports = [make_report("A", 10, WojakPhase.DOOMER)]
        mewing = filter_by_phase(reports, WojakPhase.MEWING)
        assert mewing == []

    def test_multiple_match(self):
        reports = [
            make_report("A", 30, WojakPhase.FEELS),
            make_report("B", 45, WojakPhase.FEELS),
        ]
        feels = filter_by_phase(reports, WojakPhase.FEELS)
        assert len(feels) == 2

    def test_empty_input(self):
        assert filter_by_phase([], WojakPhase.MEWING) == []


class TestSortByScore:
    def test_descending_default(self):
        reports = [
            make_report("A", 10, WojakPhase.DOOMER),
            make_report("B", 80, WojakPhase.MEWING),
            make_report("C", 40, WojakPhase.FEELS),
        ]
        sorted_r = sort_by_score(reports)
        assert sorted_r[0].symbol == "B"
        assert sorted_r[-1].symbol == "A"

    def test_ascending(self):
        reports = [
            make_report("A", 10, WojakPhase.DOOMER),
            make_report("B", 80, WojakPhase.MEWING),
        ]
        sorted_r = sort_by_score(reports, descending=False)
        assert sorted_r[0].symbol == "A"

    def test_empty_list(self):
        assert sort_by_score([]) == []

    def test_single_item(self):
        reports = [make_report("X", 50, WojakPhase.BLOOMER)]
        assert sort_by_score(reports)[0].symbol == "X"


class TestSummaryTable:
    def test_returns_string(self):
        reports = [make_report("A", 70, WojakPhase.BLOOMER)]
        assert isinstance(summary_table(reports), str)

    def test_contains_header(self):
        reports = [make_report("A", 70, WojakPhase.BLOOMER)]
        table = summary_table(reports)
        assert "SYMBOL" in table and "PHASE" in table and "SCORE" in table

    def test_contains_symbol(self):
        reports = [make_report("WOJAK", 50, WojakPhase.FEELS)]
        assert "WOJAK" in summary_table(reports)

    def test_empty_table(self):
        assert isinstance(summary_table([]), str)
