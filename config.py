"""League-owned configuration for a thin Pitch Oracle consumer."""

from dataclasses import replace

from pitch_oracle_core import get_league_config


# Replace with any key in pitch_oracle_core.BUILTIN_LEAGUES.
_THEME_CHOICES = (
    "☀️ Daytime · Alpine Mist", "☀️ Daytime · Amsterdam Canal",
    "☀️ Daytime · Apricot Studio", "☀️ Daytime · Blue Sky Ledger",
    "☀️ Daytime · Botanical Field", "☀️ Daytime · Citrus Press",
    "☀️ Daytime · Cloudline", "☀️ Daytime · Delft Blue",
    "☀️ Daytime · Desert Paper", "☀️ Daytime · Glacier Glass",
    "☀️ Daytime · Linen & Ink", "☀️ Daytime · Meadow Scoreboard",
    "☀️ Daytime · Nordic Slate", "☀️ Daytime · Sandstone Matchday",
    "☀️ Daytime · Tulip Terrace", "🌙 Nighttime · Aurora Floodlights",
    "🌙 Nighttime · Blackout Pitch", "🌙 Nighttime · Blue Hour",
    "🌙 Nighttime · Carbon & Lime", "🌙 Nighttime · City Neon",
    "🌙 Nighttime · Deep Sea", "🌙 Nighttime · Midnight Oranje",
    "🌙 Nighttime · Moonlit Turf", "🌙 Nighttime · Night Watch",
    "🌙 Nighttime · Obsidian Gold", "🌙 Nighttime · Purple Rain",
    "🌙 Nighttime · Stadium Shadow", "🌙 Nighttime · Velvet Navy",
    "🌙 Nighttime · Voltage Violet", "🌙 Nighttime · Winter Night",
)

_BASE_CONFIG = get_league_config("eredivisie")
LEAGUE_CONFIG = replace(
    _BASE_CONFIG,
    theme=replace(_BASE_CONFIG.theme, launch_theme_choices=_THEME_CHOICES),
)
