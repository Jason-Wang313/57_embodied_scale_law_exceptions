# Paper 57 Full-Scale Execution Plan

## Objective

Turn Paper 57 from a short workshop-level corpus framing into a final full-scale submission candidate. The final paper must be at least 25 pages before any final PDF is exported to Downloads. The final contribution should be positive and specific: embodied scale laws are useful inside physical regimes, but aggregate scaling curves break when the dominant bottleneck changes from representation capacity to contact, latency, safety, or morphology.

## Current State

- Current manuscript length: 101 TeX lines.
- Prior v2 decision before full-scale hardening: not final.
- Current evidence: 1,500-paper corpus synthesis plus v2 keyword-sensitivity audit.
- Current limitation: no measured scaling curve, no controlled regime benchmark, no page-scale final manuscript.
- Final Downloads artifact: `C:/Users/wangz/Downloads/57.pdf`.

## Final Target

- Final status: `final_v3_full_scale_submission_candidate`.
- Final artifact path: `C:/Users/wangz/Downloads/57.pdf`.
- Final page threshold: at least 25 pages.
- Export rule: copy to Downloads only after the manuscript is final, page threshold passes, docs are updated, and visual QA is run.
- Local PDF rule: remove `paper/main.pdf` after export.
- Desktop rule: no Desktop copy.

## Full-Scale Benchmark Design

The benchmark will be a deterministic compact-grid experiment. Each compact row represents many evaluation seeds and planning ticks, so the output remains RAM-light while representing a very large experimental surface.

Planned factors:

1. Task family, 8 levels:
   - pick-and-place
   - peg insertion
   - cable/deformable manipulation
   - dexterous in-hand rotation
   - legged locomotion
   - mobile manipulation
   - human-shared workspace action
   - tool-use manipulation

2. Physical regime, 6 levels:
   - representation-smooth
   - contact-rich
   - safety-constrained
   - latency-sensitive
   - morphology-shifted
   - mixed physical shift

3. Model scale, 5 levels:
   - 0.3B
   - 1B
   - 3B
   - 10B
   - 30B

4. Data scale, 4 levels:
   - 1x
   - 3x
   - 10x
   - 30x

5. Embodiment diversity, 3 levels:
   - narrow
   - matched
   - broad

6. Contact severity, 3 levels:
   - low contact
   - mode switches
   - discontinuous contact

7. Latency regime, 3 levels:
   - 20 ms
   - 80 ms
   - 240 ms

8. Safety tightness, 3 levels:
   - loose
   - moderate
   - tight

9. Policy family, 7 levels:
   - scale-only foundation policy
   - data-scaled foundation policy
   - embodiment-diverse scaling policy
   - contact-instrumented policy
   - latency/safety guarded policy
   - regime-aware physical router
   - oracle bottleneck router

Expected compact rows: 544,320.

Represented evaluations per row will be a fixed large multiplier, 262,144, yielding 142,690,222,080 represented evaluations. Represented planning-tick decisions will use 20,971,520 ticks per row, yielding 11,415,217,766,400 represented planning-tick decisions.

## Metrics

Each row will report:

- success
- normalized utility
- representation error
- contact failure
- latency miss
- safety violation
- morphology transfer loss
- bottleneck share
- exception severity
- monotonic scale gain
- scale saturation
- intervention recovery
- data efficiency
- physical-regime mismatch

Aggregate summaries will report by policy, task, regime, model scale, data scale, contact severity, latency, safety tightness, and morphology/diversity interaction.

## Expected Positive Findings

The target findings are not anti-scaling. They should show a stronger, more useful result:

- Scale-only policies improve in representation-smooth regimes.
- Scale-only policies saturate or reverse under contact, latency, safety, and morphology shifts.
- Data scaling helps, but cannot fully substitute for the missing physical channel.
- Embodiment diversity helps only when the morphology gap is compatible with the control regime.
- Contact-instrumented and latency/safety-guarded policies recover specific failure modes.
- The regime-aware physical router is the best non-oracle policy by utility.
- The oracle bottleneck router gives an upper bound that exposes remaining room for learned regime inference.

## Implementation Plan

1. Add `run_full_scale_scale_law_exception_suite.py`.
2. Stream `results/full_scale/condition_metrics.csv` row by row.
3. Maintain aggregate statistics online so the full CSV is not loaded into RAM.
4. Write summary CSVs for policy, task, regime, model scale, data scale, contact, latency, safety, and morphology/diversity.
5. Write `results/full_scale/experiment_summary.json`, `experiment_validation.json`, `factor_maps.json`, and `validation.json`.
6. Generate TeX tables in `results/full_scale/`.
7. Generate compact PDF figures in `figures/full_scale/`.
8. Verify row count, represented evaluation count, and planning-tick count.

## Manuscript Plan

The final manuscript will be rewritten around the benchmark:

1. Abstract with the final full-scale counts and the best non-oracle result.
2. Introduction that distinguishes pro-scaling evidence from physical-regime exceptions.
3. Problem framing: aggregate scaling curves vs regime-conditioned scaling.
4. Taxonomy of physical bottlenecks.
5. Benchmark design and deterministic model.
6. Policy families and intervention logic.
7. Main policy comparison.
8. Regime-conditioned scale curves.
9. Data scale vs physical instrumentation.
10. Contact-rich exceptions.
11. Latency-sensitive exceptions.
12. Safety-constrained exceptions.
13. Morphology-shift exceptions.
14. Mixed-regime stress.
15. Ablations and negative controls.
16. Relation to robot foundation models.
17. Relation to scaling laws.
18. Relation to sim-to-real and embodiment diversity.
19. Limitations and falsification criteria.
20. Artifact integrity checklist.
21. Extended implementation details.
22. Reviewer attack responses.
23. Reproducibility details.
24. Claim guardrails.
25. Conclusion and future real-robot validation.

## Documentation Plan

After the experiment and manuscript are final, update:

- `README.md`
- `child_status.md`
- `plan.md`
- `docs/claims.md`
- `docs/experiment_rigor_checklist.md`
- `docs/final_audit.md`
- `docs/final_audit.json`
- `docs/hostile_reviewer_response.md`
- `docs/novelty_boundary_map.md`
- `docs/novelty_decision.md`
- `docs/reproducibility_checklist.md`
- `docs/reviewer_attacks.md`
- `docs/submission_attack_log.md`
- `docs/submission_readiness_decision.md`
- `docs/submission_version_log.md`
- `docs/v2_corpus_sensitivity.json`
- `results/full_scale/README.md`
- `results/full_scale/validation.json`

V2 should be preserved as a negative control showing that keyword counts are insufficient, not as the final decision.

## Build And QA Plan

1. Update `build_pdf.ps1` only after the final manuscript is ready.
2. Add page-count enforcement of at least 25 pages.
3. Record file size, SHA256, page count, export path, and build timestamp in ASCII JSON.
4. Export only to `C:/Users/wangz/Downloads/57.pdf`.
5. Remove `paper/main.pdf`.
6. Render the Downloads PDF to `tmp/pdfs/`.
7. Visually inspect title page, main table/figure pages, stress-result pages, appendix pages, and final references page.
8. Delete `tmp/` after verifying its resolved path is inside the Paper57 repo.
9. Run stale-status scan, JSON parse checks, LaTeX warning scan, ASCII scan on changed source/status files, file-size guard, and Git cached diff check.
10. Commit and push only after all checks pass.

## Stop Condition For Paper 57

Paper57 is complete only when:

- the final PDF is at least 25 pages,
- the canonical PDF exists at `C:/Users/wangz/Downloads/57.pdf`,
- the Downloads PDF has been visually inspected from rendered PNGs,
- local `paper/main.pdf` is absent,
- docs record final v3 status and hash,
- all validation checks pass,
- the commit is pushed,
- `git status --short --branch` is clean and aligned with origin.
