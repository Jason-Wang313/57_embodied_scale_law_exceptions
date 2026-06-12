# Novelty Boundary Map

## What prior work already covers
- More data usually helps robot policies.
- More model capacity usually helps robot foundation models.
- More embodiment diversity usually helps locomotion generalization.
- More modality fusion is often beneficial in VLA-style systems.

## What prior work does not settle
- Whether scaling continues to help when the bottleneck is hybrid contact dynamics rather than representation capacity.
- Whether latency-induced semantic mismatch creates a separate failure curve.
- Whether morphology diversity and task diversity obey the same law.
- Whether safety constraints shift the scaling regime from capability to calibration.
- Whether manipulation and locomotion should be modeled with a shared scaling theory.

## Proposed novelty boundary
Our contribution is not a new model, a larger dataset, or a broader benchmark.
It is a regime-level explanation: robotics scaling is piecewise, and the piecewise boundaries are determined by physical interaction structure.

## Candidate directions
1. Regime decomposition: explicitly partition embodied tasks by contact/safety/morphology class and fit separate scaling curves.
2. Latency as state: model observation delay as a first-class bottleneck variable in contact-rich control.
3. Bottleneck switching: detect when representation scale stops being the limiting factor and interaction scale takes over.
4. Regime-aware evaluation: report scaling only after stratifying by interaction complexity.

## Chosen direction
Direction 1 plus a narrow version of 2: use literature evidence to argue that scaling laws in embodied intelligence are piecewise across physical regimes, with contact-age mismatch as the clearest exception mechanism.
