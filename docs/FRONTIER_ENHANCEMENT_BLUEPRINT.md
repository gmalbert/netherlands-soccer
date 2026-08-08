# Frontier Enhancement Blueprint

This repository is currently a thin consumer of shared soccer-core contracts and has no prior `docs/` roadmap. The first priority is to preserve that shared-core boundary while adding Dutch-league configuration and tests rather than copying model code locally.

## Architecture first

Define a league profile consumed by the shared package:

```yaml
league: NED1
timezone: Europe/Amsterdam
promotion_source: NED2
winter_break: true
features:
  artificial_turf: true
  academy_minutes: true
  european_congestion: true
markets: [1x2, totals, btts, asian_handicap]
```

Pin the core version and validate artifact schemas at startup. Add a compatibility matrix and a consumer test that runs against both the current and next core release.

## Dutch-specific data and model extensions

- Artificial-grass/home-surface interactions and venue transitions.
- Academy-player minutes, squad age, transfer-window churn, and first-team continuity.
- Winter-break and European-fixture regime effects.
- Promotion priors transferred from Eerste Divisie with calibrated league-strength shrinkage.
- Possession/pressing and set-piece matchup features, plus a coherent scoreline distribution.
- Conformal prediction sets to identify matches where the shared model is outside familiar support.

```python
def league_specific_features(match, profile):
    return {
        "surface_transition": int(match.away_surface != match.surface),
        "academy_share_diff": match.home_academy_share - match.away_academy_share,
        "winter_restart_days": match.days_since_winter_break,
    }
```

## Product and operations

- League-specific data-health page with source freshness and contract version.
- Dutch/English aliases and accessible club search.
- Match cards explaining surface, youth, rest, and lineup uncertainty.
- A visible fallback state when the shared core lacks a compatible artifact.
- Automated precompute, smoke test, and rollback to the last healthy snapshot.

## Acceptance gates

Evaluate by rolling season and promoted-club holdout. Compare with Elo and market baselines using log loss, RPS, calibration, and CLV. Require artifact provenance (`core_version`, `schema_hash`, `source_cutoff`, `model_version`) on every prediction file.
