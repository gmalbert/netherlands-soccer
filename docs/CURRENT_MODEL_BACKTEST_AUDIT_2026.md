# Current-model backtest audit (2026)

## Verdict

The most defensible artifact is the three-fold chronological ablation over 611 test rows. The 41-feature no-odds model achieved 51.39% accuracy, 1.0306 log loss, 0.6139 multiclass Brier, and 7.64% draw recall, beating the rolling class-prior baseline (44.84%, 1.0700, 0.6467). The odds-heavy model was substantially overconfident (1.3635 log loss, 0.6987 Brier). The deployed metadata describes chronological train/calibration/test slices (729/248/247) and temperature scaling. There is no settled odds ledger, so ROI and CLV are unavailable.

Poisson is also a useful benchmark: 54.41% outcome accuracy, 0.9698 log loss, and 0.5782 Brier in the stored performance artifact, though it still has 0% draw recall.

## Changes justified by the result

1. **Keep the no-odds model and Poisson; reject odds-heavy XGB.** The ablation directly shows worse probability quality from the large odds-heavy feature set.
2. **Blend out-of-fold no-odds and Poisson probabilities.** Learn constrained weights on chronological folds and require improvement over Poisson, not merely class prior.
3. **Repair draws.** Add Dixon-Coles low-score correlation, class-weighted/ordinal calibration, and draw-specific reliability reporting.
4. **Add a market comparison outside training.** Use de-vigged closing probabilities only as baseline/residual input with strict timestamp provenance.

## Betting strategy decision

- **1X2:** model quality is promising versus class prior but unproven versus books; paper-trade.
- **DNB/double chance/Asian handicap:** derive coherently from score probabilities and validate push/half outcomes.
- **Totals/BTTS:** Poisson is the preferred starting point; calibrate each line.
- **Correct score/props/parlays:** no validated edge.
- **Staking:** flat research stakes; no Kelly without market calibration and CLV.

## Release gate

Beat both Poisson and de-vigged market on an untouched season, retain positive CLV across 300+ bets, and report draw recall, calibration error, log loss, Brier, ROI, drawdown, and uncertainty by market.
