from ..models import MoodReport, WojakPhase


def format_report(report: MoodReport) -> str:
    lines = [
        f"Token:    {report.symbol} ({report.token_mint[:8]}...)",
        f"Phase:    {report.phase.value}",
        f"Score:    {report.emotion_score:.1f}/100",
        f"Headline: {report.headline}",
        "",
        "Signals:",
    ]
    for sig in report.signals:
        flag = "[✓]" if sig.triggered else "[ ]"
        lines.append(f"  {flag} {sig.name:<24} score={sig.score:5.1f}  weight={sig.weight:.2f}")
    return "\n".join(lines)


def filter_by_phase(reports: list[MoodReport], phase: WojakPhase) -> list[MoodReport]:
    return [r for r in reports if r.phase == phase]


def sort_by_score(reports: list[MoodReport], descending: bool = True) -> list[MoodReport]:
    return sorted(reports, key=lambda r: r.emotion_score, reverse=descending)


def summary_table(reports: list[MoodReport]) -> str:
    header = f"{'SYMBOL':<12} {'PHASE':<10} {'SCORE':>6}  {'TRIGGERED':>9}"
    sep = "-" * len(header)
    rows = [header, sep]
    for r in sort_by_score(reports):
        rows.append(
            f"{r.symbol:<12} {r.phase.value:<10} {r.emotion_score:>6.1f}  {r.triggered_count:>9}"
        )
    return "\n".join(rows)
