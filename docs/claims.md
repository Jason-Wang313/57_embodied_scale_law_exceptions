# Claims

## Supported

- Embodied scaling curves should be reported per physical regime rather than only as aggregate model-size or data-size curves.
- Scale-only policies improve but saturate when contact, latency, safety, and morphology become the active bottlenecks.
- In the deterministic full-scale benchmark, the regime-aware physical router is the best non-oracle policy: utility 0.888, success 0.885, exception severity 0.095.
- Scale-only remains positive but bottleneck-limited: utility 0.133, success 0.508, exception severity 0.543.
- Data scaling, embodiment diversity, contact instrumentation, and latency/safety guarding each recover specific failure modes but do not dominate the full mixed-regime grid alone.

## Not Supported

- Universal robotics scaling exponents.
- Deployment-ready robot safety.
- A claim that scale is useless.
- A claim that the deterministic utility values transfer directly to hardware.
- A complete taxonomy of all embodied physical regimes.

## Boundary

The paper supports a full-scale deterministic benchmark and reporting discipline. V2 remains a negative control showing that corpus keyword ratios are not enough for a final empirical scaling-law claim.
