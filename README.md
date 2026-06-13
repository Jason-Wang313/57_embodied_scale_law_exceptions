# Paper 57: Embodied Scale Law Exceptions

Decision: workshop-only.

This paper argues that embodied scaling laws are regime-specific: contact-rich, safety-constrained, latency-sensitive, and morphology-fragmented settings can move the bottleneck away from model size and toward physical interaction structure.

V1 evidence:

- 1,500 filtered robotics and embodied-AI corpus rows.
- Baseline keyword counts: scale-positive 142, contact-rich 735, morphology 275.
- Corpus synthesis and hostile prior-work map.

V2 hardening adds a corpus-sensitivity audit:

- Baseline keywords: physical-regime / scale ratio 7.11; bootstrap physical-greater-than-scale rate 1.00.
- Strict terms: ratio 19.87; bootstrap rate 1.00.
- Scale-favorable terms: ratio 1.15; bootstrap rate 0.93.

The supported claim is a workshop-level regime-map framing, not a measured scaling law or a complete empirical map.

## Reproduction

```powershell
python analyze_corpus.py
python v2_corpus_sensitivity.py
powershell -ExecutionPolicy Bypass -File build_pdf.ps1
```

The canonical built PDF is `C:/Users/wangz/Downloads/57.pdf`.

Local generated PDFs are not tracked. The build script copies the generated PDF to the canonical Downloads path and removes `paper/main.pdf`.
