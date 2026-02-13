import pytest
from zwonk.models import TokenMood


@pytest.fixture
def doomer_mood():
    return TokenMood(
        token_mint="DoomerXyz...pump",
        symbol="DOOM",
        price_usd=0.000001,
        price_change_1h_pct=0.5,
        price_change_24h_pct=1.0,
        volume_1h=500,
        volume_24h=60_000,
        holder_count=80,
        holder_count_prev=80,
        market_cap_usd=1_000_000,
        age_hours=240.0,
    )


@pytest.fixture
def feels_mood():
    return TokenMood(
        token_mint="FeelsXyz...pump",
        symbol="FEELS",
        price_usd=0.00055,
        price_change_1h_pct=22.0,
        price_change_24h_pct=60.0,
        volume_1h=90_000,
        volume_24h=720_000,
        holder_count=650,
        holder_count_prev=610,
        market_cap_usd=400_000,
        age_hours=30.0,
    )


@pytest.fixture
def bloomer_mood():
    return TokenMood(
        token_mint="BloomXyz...pump",
        symbol="BLOOM",
        price_usd=0.0028,
        price_change_1h_pct=38.0,
        price_change_24h_pct=140.0,
        volume_1h=380_000,
        volume_24h=1_440_000,
        holder_count=3_200,
        holder_count_prev=2_400,
        market_cap_usd=600_000,
        age_hours=8.0,
    )


@pytest.fixture
def mewing_mood():
    return TokenMood(
        token_mint="MewingXyz...pump",
        symbol="MEW",
        price_usd=0.015,
        price_change_1h_pct=62.0,
        price_change_24h_pct=350.0,
        volume_1h=1_800_000,
        volume_24h=5_040_000,
        holder_count=9_500,
        holder_count_prev=5_800,
        market_cap_usd=950_000,
        age_hours=4.0,
    )
