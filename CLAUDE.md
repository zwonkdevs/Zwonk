# Zwonk — Claude Context

## What this is
Solana meme token emotional sentiment engine. Classifies where a token sits on the Wojak emotional spectrum using 4 on-chain signals.

## Cycle phases
- DOOMER (0–25): no emotional momentum
- FEELS (26–50): early sentiment stirring
- BLOOMER (51–75): emotional cycle in motion
- MEWING (76–100): peak, gigachad mode, exit risk elevated

## Signals (weights sum to 1.0)
- `sentiment_velocity` — |1h price change| (weight: 35%)
- `crowd_surge` — 1h vol vs baseline (weight: 30%)
- `holder_momentum` — holder growth rate (weight: 20%)
- `market_depth` — holders per $1k mcap (weight: 15%)

## Entry point
```python
from zwonk import track, TokenMood
report = track(mood)
print(report.phase)          # BLOOMER
print(report.emotion_score)  # 67.2
```

## Tests
```bash
pytest tests/ -v  # 130+ tests
```
