# Submission Attack Log

## Attack: corpus ratios are not enough

Result: sustained. V2 keyword sensitivity remains as a negative control.

Decision impact: final evidence is the v3 full-scale benchmark, not corpus prevalence.

## Attack: scale-only is unfairly punished

Result: answered. Scale-only remains positive, improves with model scale, and reaches utility 0.312 in representation-smooth regimes. It saturates under mixed physical shift because physical residuals remain.

Decision impact: final claim is regime-conditioned scaling, not anti-scaling.

## Attack: physical router is too close to an oracle

Result: answered. The router has residual exception severity 0.095 and utility 0.888, while the oracle is an upper bound with utility 1.000. The gap is headroom for learned bottleneck inference.

## Attack: synthetic benchmark cannot prove real robots

Result: sustained. The paper states real robot logs and regime annotations as future work.
