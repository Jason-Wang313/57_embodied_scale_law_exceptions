# Literature Map

## Seed thesis
Robotics scaling is real, but the monotonic story breaks in physical regimes where contact, morphology, and safety convert additional model capacity into the wrong bottleneck.

## Core clusters
- Scaling-law meta-analyses: robot foundation models, imitation learning scaling, embodiment scaling, and VLA reviews.
- Regime-boundary papers: contact-rich manipulation, tactile control, sim-to-real transfer, constrained environments, and safety surveys.
- Adjacent mechanisms: world models, motion planning, diffusion policies, latent action models, and multimodal perception.

## Key hostile priors
1. Neural Scaling Laws in Robotics: argues broad power-law improvement with data, compute, and model size.
2. Data Scaling Laws in Imitation Learning for Robotic Manipulation: finds environment and object diversity dominate per-environment demo count.
3. Towards Embodiment Scaling Laws in Robot Locomotion: argues more embodiments improve generalization.
4. VLA surveys and open-challenge papers: frame scaling and integration as the main path forward.
5. Contact-rich manipulation papers: repeatedly introduce task-specific mechanisms because generic scaling is insufficient.

## Synthesis
The literature splits into two halves:
- A scale-positive half, where more data/model/embodiments usually helps in open-world or locomotion-style settings.
- A regime-fracture half, where latency, contact mode switches, safety envelopes, and morphology-specific constraints produce bottlenecks that do not move with scale alone.

The paper thesis is not that scaling laws are false. It is that the relevant object in embodied intelligence is a family of regime-specific scaling curves, and the exceptions are not noise. They are the signal that the central mechanism has changed.

## Hidden assumption inventory
- The training and deployment embodiment spaces are smoothly connected.
- Contact mode boundaries are negligible or can be averaged away.
- More parameters can absorb environment variation without changing controller structure.
- Data diversity and data quantity are interchangeable above a modest threshold.
- Safety failures are secondary evaluation noise rather than a distinct bottleneck.
- Latency is only a nuisance, not a semantic state variable.
- Morphology variation can be handled by a single policy class without regime indexing.
- Sim-to-real gaps are mostly visual, not interaction-structural.
- Manipulation can be analyzed with the same scaling story as locomotion.
- World-model improvements transfer uniformly into closed-loop control performance.
- Contact-rich tasks obey the same trend as non-contact tasks.
- Zero-shot generalization is a single axis rather than several orthogonal ones.
- Performance curves are smooth over task families.
- Failure modes are independent across hardware, environment, and object class.
- Larger models reduce brittleness rather than sometimes amplifying it.
- Benchmarks are regime-faithful proxies for deployed operation.
- High-level language grounding and low-level force regulation scale similarly.
- Tactile, proprioceptive, and visual streams are exchangeable within one scaling law.
- Transfer across embodiments and across tasks are the same problem.
- Adversarial contact conditions do not create new asymptotes.

## Promising breakpoints
- Contact-age mismatch in delayed force feedback.
- Morphology-conditioned regime switching.
- Safety-constrained interaction where scaling adds confidence, not capability.
- World-model uncertainty spikes at contact transitions.
- Task family fragmentation: manipulation vs locomotion vs navigation vs aerial robotics.
