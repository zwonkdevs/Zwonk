# Zwonk

**Solana meme token emotional sentiment engine.**

`$ZWONK` — `3CZvoRPEyZ3QpXUQb3i1iw3rVWdkqgmWDDRVypP4pump` — `pip install zwonk`

---

*SOLANA, April 2026* — A new open-source tool is quietly reading the emotional pulse of Solana's most volatile meme tokens — and its framework is borrowed not from quantitative finance, but from the internet's most enduring meme character.

Wojak is not just a face. He is a cycle. Every meme trader has lived it: the doomer who buys the bottom too early, the feels guy who hesitates at the right entry, the bloomer who rides the wave, the gigachad who exits at the top. What most analysis tools miss is that this emotional arc is not a metaphor — it is measurable. It leaves a trace in price velocity, volume behavior, holder growth, and community depth.

Zwonk formalises this trace into a four-phase classification engine. Feed it on-chain data. It tells you which version of Wojak the market is currently feeling.

Four phases: **DOOMER → FEELS → BLOOMER → MEWING**

---

## The four signals

```
sentiment_velocity      weight: 35%
  |1h price change| >= 18% triggers
  score = min(abs(change) × 2, 100)
  Fast moves in either direction are emotional events.
  A 40% dump is Wojak crying. A 40% pump is Wojak gigachad-posting.
  Velocity is the heartbeat of sentiment.

crowd_surge             weight: 30%
  1h volume >= 2.8× hourly baseline triggers
  baseline = volume_24h / 24
  score = min(ratio × (100/2.8), 100)
  Volume above baseline means the crowd has gathered.
  In Wojak terms: he left his room. People noticed.

holder_momentum         weight: 20%
  holder count grew >= 5% vs previous snapshot triggers
  score = min(growth_pct × 4, 100)
  New believers joining. The doomer stays home alone.
  The bloomer brings friends.

market_depth            weight: 15%
  holders / (market_cap_usd / 1000) >= 12 triggers
  score = min(ratio × (100/12), 100)
  Distributed emotion vs concentrated whale game.
  Wojak feels real because he belongs to everyone.
```

All four weighted and averaged → emotion score 0–100 → phase classification.

---

## Phases

```
0–25    DOOMER    Dark room. No momentum. Pure despair or quiet accumulation.
26–50   FEELS     Something stirs. The feels are assembling. Unconfirmed.
51–75   BLOOMER   Emotional cycle in motion. Community growing. Energy real.
76–100  MEWING    Peak. Gigachad mode. Maximum emotional momentum. Exit risk elevated.
```

---

## Usage

```python
from zwonk import track, TokenMood

mood = TokenMood(
    token_mint="ZwonkXyz...pump",
    symbol="ZWONK",
    price_usd=0.00088,
    price_change_1h_pct=41.0,
    price_change_24h_pct=190.0,
    volume_1h=520_000,
    volume_24h=1_680_000,
    holder_count=5_200,
    holder_count_prev=3_800,
    market_cap_usd=720_000,
)

report = track(mood)

print(report.phase)          # BLOOMER
print(report.emotion_score)  # ~67.2
print(report.headline)       # "Bloomer phase confirmed..."
print(report.is_bullish)     # True
print(report.triggered_count) # 3
```

For batch tracking:

```python
from zwonk import track_batch, most_emotional

reports = track_batch(moods)
top = most_emotional(moods)  # returns the mood with highest emotion score
```

---

## Install

```bash
pip install zwonk
```

No external dependencies. Pure Python 3.10+.

---

## Tests

```bash
pip install -e ".[dev]"
pytest tests/ -v
# 130+ tests — signals, scorer, tracker, models, helpers
```

---

## Dashboard

```bash
cd dashboard && npm install && npm run dev
# → http://localhost:5173
```

6 mock meme tokens updating every 4 seconds. Mood card with Wojak phase emoji, signal panel with weighted bars, emotion feed sorted by score. Most emotional token pinned at top.

---

## Docker

```bash
docker compose up
```

---

## Why sentiment velocity gets 35%

Because Wojak does not move gradually. When a token pumps 40% in an hour, that is not a price event — it is an emotional contagion event. Attention flows toward it faster than any other signal can capture. The |1h price change| is the most immediate indicator that the crowd's emotional state is actively shifting.

The signal uses absolute value because dumps generate Wojak-posting too. A 45% crash in an hour produces more emotional activity than a flat token with decent volume. The meme spreads fastest when the feeling is strongest — in either direction.

---

## Why market depth is only 15%

Market depth — the ratio of holders to market cap — tells you what *kind* of token it is, not whether the emotional cycle is turning. A deeply distributed token with authentic community can sit in DOOMER phase for weeks while the narrative builds quietly. Depth is context. It scores the quality of the emotion. That is why it gets the smallest weight.

---

## The name

Wojak's origins trace to a Polish internet forum in 2009. He was called *Wojak* — the soldier — but he became something else entirely: the universal face of human feeling in the digital age. Zwonk is his on-chain descendant. The meme found the blockchain. The emotional cycle found a quantitative engine.

Now you can read it before the rest of the market does.

---

<sub>built by zwonkdev · wojakwatch · solfeels</sub>
