# Hostile Prior Work

This list intentionally collects papers that make the eventual thesis harder.

1. Neural Scaling Laws in Robotics.
- Problem claimed: measure how robotics performance scales with data, model size, and compute.
- Actual mechanism: meta-analysis over 327 papers, fitting power-law-style trends.
- Hidden assumptions: aggregate task families are comparable; scaling is smooth; meta-data fidelity is sufficient.
- Fixed variables: benchmark semantics, task regime boundaries, evaluation protocol heterogeneity.
- Failure modes ignored: contact transitions, safety-critical edges, morphology-specific discontinuities.
- Makes less novel: claims that larger robot models are usually better.
- Leaves open: when scaling saturates or reverses in specific physical regimes.

2. Data Scaling Laws in Imitation Learning for Robotic Manipulation.
- Problem claimed: whether data scaling helps robot manipulation.
- Actual mechanism: larger environment/object diversity plus demonstrations, with a power-law trend.
- Hidden assumptions: manipulation subregimes remain within one curve; diversity is the dominant variable after thresholding.
- Fixed variables: task family, control architecture, sensor suite.
- Failure modes ignored: contact-mode switches, long-horizon recovery, safety envelopes.
- Makes less novel: saying more diverse data helps manipulation.
- Leaves open: which physical regimes refuse the benefit.

3. Towards Embodiment Scaling Laws in Robot Locomotion.
- Problem claimed: whether more embodiments improve generalization.
- Actual mechanism: procedural embodiment diversity and generalist policy training.
- Hidden assumptions: embodiment variation is a scaling axis that can be traversed smoothly.
- Fixed variables: locomotion as the main benchmark family, observation/action canonicalization.
- Failure modes ignored: manipulation, contact-rich deformations, tool use, delicate force control.
- Makes less novel: using embodiment diversity as a broad generalization principle.
- Leaves open: whether morphology scale breaks in interaction-heavy settings.

4. Vision-Language-Action review and challenge papers.
- Problem claimed: organize the VLA landscape and future directions.
- Actual mechanism: architectural synthesis and open problems.
- Hidden assumptions: integration is the primary bottleneck; scale remains the default route.
- Fixed variables: language-conditioning paradigm, broad task framing.
- Failure modes ignored: hardware-limited contact stability and timing mismatch.
- Makes less novel: proposing unified multimodal robot policies.
- Leaves open: physical regimes where the integration story stops helping.

5. Contact-rich manipulation and sim-to-real papers.
- Problem claimed: solve manipulation under contact and transfer.
- Actual mechanism: task-specific contact reasoning, tactile fusion, and transfer heuristics.
- Hidden assumptions: local fixes can patch the core bottleneck.
- Fixed variables: contact physics, sensing latency, object set.
- Failure modes ignored: cross-task scaling laws and global regime maps.
- Makes less novel: claiming contact-rich tasks are the natural next target for scale.
- Leaves open: a principled explanation for why scaling stalls.

## Boundary statement
The thesis survives only if it does not try to prove that all scaling fails. It must instead isolate the physical regimes where scaling ceases to be the central mechanism.
