# Experiment Rigor Checklist

- Corpus rows: 1,500.
- V2 sensitivity variants: baseline, strict terms, scale-favorable.
- V2 status: negative control, not final decision.
- Full-scale compact condition rows: 544,320.
- Represented evaluations: 142,690,222,080.
- Represented planning-tick decisions: 11,415,217,766,400.
- Axes: 8 task families, 6 regimes, 5 model scales, 4 data scales, 3 embodiment-diversity levels, 3 contact severities, 3 latency regimes, 3 safety regimes, 7 policies.
- Metrics: success, utility, representation error, contact failure, latency miss, safety violation, morphology loss, bottleneck share, exception severity, monotonic scale gain, scale saturation, intervention recovery, data efficiency, regime mismatch.
- Generated tables and figures: yes, from `results/full_scale/`.
- RAM-light execution: streamed condition CSV and online aggregates.
- Hardware experiment: no.
- Final decision: final v3 full-scale submission candidate with explicit real-robot limitation.
