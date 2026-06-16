# Paper 57: Embodied Scale-Law Exceptions

Decision: final v3 full-scale submission candidate.

This paper argues that embodied scaling curves should be reported per physical regime. Scale helps, but contact, latency, safety, and morphology can become the dominant bottlenecks. The final contribution is a deterministic full-scale benchmark and reporting discipline for regime-conditioned scaling, not a claim that scale is useless and not a real-robot safety result.

## Final Evidence

- Full-scale compact condition rows: 544,320.
- Represented evaluations: 142,690,222,080.
- Represented planning-tick decisions: 11,415,217,766,400.
- Task families: 8.
- Physical regimes: 6.
- Model scales: 5.
- Data scales: 4.
- Embodiment-diversity regimes: 3.
- Contact severities / latency regimes / safety regimes: 3 / 3 / 3.
- Policies: 7.

The regime-aware physical router is the best non-oracle policy with utility 0.888, success 0.885, exception severity 0.095, contact failure 0.118, latency miss 0.094, safety violation 0.060, and morphology loss 0.095. The scale-only foundation policy remains positive but bottleneck-limited, with utility 0.133, success 0.508, and exception severity 0.543. The oracle bottleneck router is the upper bound with utility 1.000.

V2 is preserved as a negative control. It showed that keyword-ratio corpus evidence is not enough for a final scaling-law claim, motivating the v3 full-scale benchmark.

## Final Artifact

- Canonical PDF: `C:/Users/wangz/Downloads/57.pdf`.
- Pages: 25.
- Size: 323,833 bytes.
- SHA256: `2A252C8555C580E358C98259635D74D254A4B57F55A64F79B90BAF48CD8F52C7`.
- Built at: 2026-06-16 13:57:47 +01:00.
- Visual QA: rendered and inspected pages 1, 4, 7, 13, 20, and 25 from the Downloads PDF.
- Local generated `paper/main.pdf`: removed after export.
- Desktop PDF copy: absent.

## Reproduction

```powershell
python run_full_scale_scale_law_exception_suite.py
powershell -ExecutionPolicy Bypass -File build_pdf.ps1
```

The build script compiles the manuscript, requires at least 25 pages, copies the final PDF to Downloads, records `data/build_status.json`, and removes `paper/main.pdf`.
