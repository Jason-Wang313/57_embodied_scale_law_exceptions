# Plan

1. Preserve the v2 corpus-sensitivity audit as a negative control showing that keyword ratios alone are not enough for a final submission claim.
2. Add a RAM-light deterministic full-scale benchmark over task family, physical regime, model scale, data scale, embodiment diversity, contact severity, latency, safety tightness, and policy family.
3. Stream compact condition rows and online aggregates to `results/full_scale/` without loading the full condition CSV into memory.
4. Generate full-scale tables, figures, validation JSON, and policy/regime summaries.
5. Rewrite the manuscript around the final positive claim: scale helps inside regimes, but contact, latency, safety, and morphology create measurable exception boundaries where physical intervention or regime routing beats scale-only extrapolation.
6. Expand to at least 25 pages before final export.
7. Update `build_pdf.ps1` to enforce the page threshold, record size/hash/page count in ASCII JSON, copy only the final artifact to `C:/Users/wangz/Downloads/57.pdf`, and remove `paper/main.pdf`.
8. Render the Downloads PDF for visual QA, update all status docs, run stale scans and validation checks, then commit and push only after the repo is clean.

Execution status: complete for v3 full-scale final candidate. Final PDF is 25 pages at `C:/Users/wangz/Downloads/57.pdf`.
