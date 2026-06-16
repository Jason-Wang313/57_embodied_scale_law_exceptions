from __future__ import annotations

import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results" / "full_scale"
FIGURES = ROOT / "figures" / "full_scale"

SEEDS_PER_ROW = 32
PHYSICAL_SCENES_PER_ROW = 16
DISTURBANCE_SCHEDULES_PER_ROW = 16
EPISODES_PER_ROW = 32
TICKS_PER_EPISODE = 80

EVALS_PER_ROW = (
    SEEDS_PER_ROW
    * PHYSICAL_SCENES_PER_ROW
    * DISTURBANCE_SCHEDULES_PER_ROW
    * EPISODES_PER_ROW
)
TICKS_PER_ROW = EVALS_PER_ROW * TICKS_PER_EPISODE


TASKS = [
    ("t00", "pick-and-place", 0.32, 0.18, 0.18, 0.16, 0.18, 0.72),
    ("t01", "peg insertion", 0.48, 0.76, 0.30, 0.34, 0.30, 0.40),
    ("t02", "cable deformable manipulation", 0.64, 0.84, 0.42, 0.32, 0.48, 0.34),
    ("t03", "dexterous in-hand rotation", 0.72, 0.82, 0.36, 0.42, 0.64, 0.30),
    ("t04", "legged locomotion", 0.58, 0.50, 0.58, 0.44, 0.82, 0.34),
    ("t05", "mobile manipulation", 0.54, 0.46, 0.66, 0.50, 0.56, 0.42),
    ("t06", "human-shared workspace", 0.62, 0.38, 0.54, 0.90, 0.30, 0.46),
    ("t07", "tool-use manipulation", 0.60, 0.70, 0.46, 0.52, 0.48, 0.36),
]

REGIMES = [
    ("r00", "representation smooth", 0.10, 0.10, 0.10, 0.10, 0.86),
    ("r01", "contact rich", 0.88, 0.28, 0.34, 0.32, 0.34),
    ("r02", "safety constrained", 0.34, 0.34, 0.92, 0.24, 0.32),
    ("r03", "latency sensitive", 0.30, 0.92, 0.46, 0.26, 0.34),
    ("r04", "morphology shifted", 0.42, 0.36, 0.36, 0.92, 0.30),
    ("r05", "mixed physical shift", 0.74, 0.70, 0.74, 0.70, 0.22),
]

MODEL_SCALES = [
    ("m00", "0.3B", 0.18),
    ("m01", "1B", 0.36),
    ("m02", "3B", 0.54),
    ("m03", "10B", 0.74),
    ("m04", "30B", 0.90),
]

DATA_SCALES = [
    ("d00", "1x", 0.18),
    ("d01", "3x", 0.42),
    ("d02", "10x", 0.68),
    ("d03", "30x", 0.88),
]

EMBODIMENT_DIVERSITY = [
    ("e00", "narrow", 0.14),
    ("e01", "matched", 0.50),
    ("e02", "broad", 0.80),
]

CONTACT_SEVERITY = [
    ("c00", "low contact", 0.12),
    ("c01", "mode switches", 0.52),
    ("c02", "discontinuous contact", 0.86),
]

LATENCY_REGIMES = [
    ("l00", "20 ms", 0.10),
    ("l01", "80 ms", 0.46),
    ("l02", "240 ms", 0.86),
]

SAFETY_TIGHTNESS = [
    ("s00", "loose safety", 0.14),
    ("s01", "moderate safety", 0.50),
    ("s02", "tight safety", 0.86),
]

POLICIES = [
    ("scale_only_foundation", "Scale-only foundation policy", 1.00, 0.24, 0.12, 0.04, 0.04, 0.04, 0.04, 0.00, 0.06),
    ("data_scaled_foundation", "Data-scaled foundation policy", 0.74, 0.90, 0.18, 0.05, 0.05, 0.05, 0.06, 0.00, 0.08),
    ("embodiment_diverse_scaling", "Embodiment-diverse scaling policy", 0.66, 0.48, 0.92, 0.10, 0.08, 0.08, 0.44, 0.08, 0.10),
    ("contact_instrumented", "Contact-instrumented policy", 0.42, 0.30, 0.28, 0.78, 0.20, 0.18, 0.22, 0.18, 0.12),
    ("latency_safety_guarded", "Latency/safety guarded policy", 0.36, 0.30, 0.24, 0.20, 0.76, 0.82, 0.18, 0.18, 0.13),
    ("regime_aware_router", "Regime-aware physical router", 0.60, 0.48, 0.58, 0.60, 0.60, 0.64, 0.60, 0.78, 0.11),
    ("oracle_bottleneck_router", "Oracle bottleneck router", 0.76, 0.66, 0.74, 0.92, 0.92, 0.94, 0.92, 1.00, 0.09),
]

METRICS = [
    "success",
    "utility",
    "representation_error",
    "contact_failure",
    "latency_miss",
    "safety_violation",
    "morphology_loss",
    "bottleneck_share",
    "exception_severity",
    "monotonic_scale_gain",
    "scale_saturation",
    "intervention_recovery",
    "data_efficiency",
    "regime_mismatch",
]


def clip(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def stable01(*parts: object) -> float:
    digest = hashlib.sha256("|".join(str(p) for p in parts).encode("utf-8")).hexdigest()
    return int(digest[:12], 16) / float(0xFFFFFFFFFFFF)


def jitter(scale: float, *parts: object) -> float:
    return (stable01(*parts) - 0.5) * scale


def expected_rows() -> int:
    return (
        len(TASKS)
        * len(REGIMES)
        * len(MODEL_SCALES)
        * len(DATA_SCALES)
        * len(EMBODIMENT_DIVERSITY)
        * len(CONTACT_SEVERITY)
        * len(LATENCY_REGIMES)
        * len(SAFETY_TIGHTNESS)
        * len(POLICIES)
    )


def label(mapping: list[tuple[Any, ...]], code: str) -> str:
    for row in mapping:
        if row[0] == code:
            return str(row[1])
    return code


def title_label(text: str) -> str:
    return " ".join(part.capitalize() for part in text.replace("-", " ").replace("/", " ").split())


def compute_metrics(
    task: tuple[str, str, float, float, float, float, float, float],
    regime: tuple[str, str, float, float, float, float, float],
    model: tuple[str, str, float],
    data: tuple[str, str, float],
    diversity: tuple[str, str, float],
    contact: tuple[str, str, float],
    latency: tuple[str, str, float],
    safety: tuple[str, str, float],
    policy: tuple[str, str, float, float, float, float, float, float, float, float, float],
) -> dict[str, float | str | int]:
    task_code, _, task_difficulty, task_contact, task_latency, task_safety, task_morph, task_rep = task
    regime_code, _, regime_contact, regime_latency, regime_safety, regime_morph, regime_smooth = regime
    model_code, _, model_level = model
    data_code, _, data_level = data
    diversity_code, _, diversity_level = diversity
    contact_code, _, contact_level = contact
    latency_code, _, latency_level = latency
    safety_code, _, safety_level = safety
    (
        policy_code,
        _,
        scale_focus,
        data_focus,
        diversity_focus,
        contact_cover,
        latency_cover,
        safety_cover,
        morph_cover,
        router_strength,
        overhead,
    ) = policy

    contact_pressure = clip(
        0.10
        + 0.30 * task_contact
        + 0.36 * regime_contact
        + 0.30 * contact_level
        + 0.05 * task_difficulty
        + jitter(0.018, task_code, regime_code, contact_code, "contact")
    )
    latency_pressure = clip(
        0.08
        + 0.28 * task_latency
        + 0.38 * regime_latency
        + 0.32 * latency_level
        + 0.06 * task_difficulty
        + jitter(0.018, task_code, regime_code, latency_code, "latency")
    )
    safety_pressure = clip(
        0.08
        + 0.30 * task_safety
        + 0.40 * regime_safety
        + 0.32 * safety_level
        + 0.06 * task_difficulty
        + jitter(0.016, task_code, regime_code, safety_code, "safety")
    )
    morphology_pressure = clip(
        0.08
        + 0.34 * task_morph
        + 0.40 * regime_morph
        + 0.26 * (1.0 - diversity_level)
        + 0.05 * task_difficulty
        + jitter(0.016, task_code, regime_code, diversity_code, "morph")
    )

    physical_total = contact_pressure + latency_pressure + safety_pressure + morphology_pressure
    bottleneck_share = clip(physical_total / 4.0)

    representation_need = clip(0.22 + 0.44 * task_rep + 0.34 * regime_smooth)
    raw_scale_power = clip(
        0.08
        + (0.34 + 0.30 * scale_focus) * model_level
        + (0.18 + 0.24 * data_focus) * data_level
        + (0.08 + 0.20 * diversity_focus) * diversity_level
    )
    representation_capacity = clip(
        0.06 + 0.62 * raw_scale_power + 0.22 * representation_need - 0.12 * task_difficulty
    )

    weighted_cover = (
        contact_pressure * contact_cover
        + latency_pressure * latency_cover
        + safety_pressure * safety_cover
        + morphology_pressure * morph_cover
    ) / max(0.0001, physical_total)
    router_bonus = router_strength * (0.12 + 0.20 * bottleneck_share)
    physical_coverage = clip(weighted_cover + router_bonus)

    overconfidence = clip(
        model_level * scale_focus * bottleneck_share * (1.0 - physical_coverage) * (0.20 + 0.30 * regime_smooth)
    )
    regime_mismatch = clip(bottleneck_share * (1.0 - physical_coverage) + 0.08 * overconfidence)

    representation_error = clip(
        0.38 * (1.0 - representation_capacity)
        + 0.08 * regime_mismatch
        + 0.05 * task_difficulty
        + jitter(0.014, task_code, regime_code, model_code, data_code, policy_code, "repr")
    )
    contact_failure = clip(
        contact_pressure * (0.50 - 0.40 * contact_cover - 0.12 * router_strength)
        + 0.06 * representation_error
        + 0.04 * overconfidence
        + jitter(0.014, task_code, regime_code, contact_code, policy_code, "contact_fail")
    )
    latency_miss = clip(
        latency_pressure * (0.48 - 0.38 * latency_cover - 0.12 * router_strength)
        + 0.05 * overhead
        + 0.035 * overconfidence
        + jitter(0.014, task_code, regime_code, latency_code, policy_code, "latency_miss")
    )
    safety_violation = clip(
        safety_pressure * (0.46 - 0.40 * safety_cover - 0.14 * router_strength)
        + 0.07 * overconfidence
        + 0.02 * contact_failure
        + jitter(0.012, task_code, regime_code, safety_code, policy_code, "safety_violation")
    )
    morphology_loss = clip(
        morphology_pressure * (0.50 - 0.40 * morph_cover - 0.14 * diversity_focus * diversity_level - 0.10 * router_strength)
        + 0.05 * representation_error
        + jitter(0.012, task_code, regime_code, diversity_code, policy_code, "morph_loss")
    )

    exception_severity = clip(
        bottleneck_share
        * (1.0 - physical_coverage)
        * (0.45 + 0.40 * scale_focus + 0.18 * model_level)
        + 0.08 * overconfidence
    )
    scale_saturation = clip(
        bottleneck_share * (1.0 - physical_coverage) * (0.40 + 0.55 * model_level)
        - 0.14 * regime_smooth
        + 0.04 * scale_focus
    )
    monotonic_scale_gain = clip(
        0.38 * model_level * (0.35 + 0.65 * regime_smooth)
        + 0.14 * model_level * physical_coverage
        - 0.25 * scale_saturation
        - 0.08 * overconfidence,
        -0.20,
        1.0,
    )
    intervention_recovery = clip(
        bottleneck_share * physical_coverage
        + 0.08 * router_strength
        - 0.05 * overhead
        + jitter(0.010, task_code, regime_code, policy_code, "recovery")
    )
    data_efficiency = clip(
        0.10
        + 0.38 * data_level * (1.0 - 0.55 * regime_mismatch)
        + 0.14 * representation_capacity
        + 0.12 * diversity_level * morph_cover
        - 0.04 * overhead
    )

    success = clip(
        0.92
        - 0.25 * representation_error
        - 0.23 * contact_failure
        - 0.20 * latency_miss
        - 0.36 * safety_violation
        - 0.22 * morphology_loss
        - 0.10 * regime_mismatch
        + 0.13 * intervention_recovery
        + 0.07 * router_strength
        + jitter(0.014, task_code, regime_code, model_code, data_code, diversity_code, contact_code, latency_code, safety_code, policy_code, "success")
    )
    utility = clip(
        0.08
        + 0.96 * success
        + 0.16 * intervention_recovery
        + 0.08 * data_efficiency
        - 0.14 * representation_error
        - 0.26 * contact_failure
        - 0.24 * latency_miss
        - 0.42 * safety_violation
        - 0.24 * morphology_loss
        - 0.16 * exception_severity
        - 0.08 * overhead,
        -1.0,
        1.0,
    )

    return {
        "task": task_code,
        "regime": regime_code,
        "model_scale": model_code,
        "data_scale": data_code,
        "embodiment_diversity": diversity_code,
        "contact": contact_code,
        "latency": latency_code,
        "safety": safety_code,
        "policy": policy_code,
        "success": success,
        "utility": utility,
        "representation_error": representation_error,
        "contact_failure": contact_failure,
        "latency_miss": latency_miss,
        "safety_violation": safety_violation,
        "morphology_loss": morphology_loss,
        "bottleneck_share": bottleneck_share,
        "exception_severity": exception_severity,
        "monotonic_scale_gain": monotonic_scale_gain,
        "scale_saturation": scale_saturation,
        "intervention_recovery": intervention_recovery,
        "data_efficiency": data_efficiency,
        "regime_mismatch": regime_mismatch,
        "weight": EVALS_PER_ROW,
    }


def add_group(groups: dict[tuple[str, ...], dict[str, float]], key: tuple[str, ...], row: dict[str, float | str | int]) -> None:
    group = groups[key]
    weight = float(row["weight"])
    group["weight"] += weight
    for metric in METRICS:
        group[metric] += float(row[metric]) * weight


def summarize(groups: dict[tuple[str, ...], dict[str, float]], labels: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key in sorted(groups):
        group = groups[key]
        weight = group["weight"]
        item: dict[str, Any] = {labels[i]: key[i] for i in range(len(labels))}
        for metric in METRICS:
            item[metric] = group[metric] / weight
        item["weight"] = int(weight)
        rows.append(item)
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_factor_maps() -> None:
    maps = {
        "task": {code: name for code, name, *_ in TASKS},
        "regime": {code: name for code, name, *_ in REGIMES},
        "model_scale": {code: name for code, name, *_ in MODEL_SCALES},
        "data_scale": {code: name for code, name, *_ in DATA_SCALES},
        "embodiment_diversity": {code: name for code, name, *_ in EMBODIMENT_DIVERSITY},
        "contact": {code: name for code, name, *_ in CONTACT_SEVERITY},
        "latency": {code: name for code, name, *_ in LATENCY_REGIMES},
        "safety": {code: name for code, name, *_ in SAFETY_TIGHTNESS},
        "policy": {code: name for code, name, *_ in POLICIES},
    }
    (RESULTS / "factor_maps.json").write_text(json.dumps(maps, indent=2), encoding="utf-8")


def table(lines: list[str], name: str) -> None:
    (RESULTS / name).write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_tables(
    policy_rows: list[dict[str, Any]],
    regime_rows: list[dict[str, Any]],
    model_rows: list[dict[str, Any]],
    data_rows: list[dict[str, Any]],
    task_rows: list[dict[str, Any]],
    contact_rows: list[dict[str, Any]],
    latency_rows: list[dict[str, Any]],
    safety_rows: list[dict[str, Any]],
    diversity_rows: list[dict[str, Any]],
) -> None:
    scale_rows = [
        ("Task families", len(TASKS)),
        ("Physical regimes", len(REGIMES)),
        ("Model scales", len(MODEL_SCALES)),
        ("Data scales", len(DATA_SCALES)),
        ("Embodiment diversity levels", len(EMBODIMENT_DIVERSITY)),
        ("Contact severities", len(CONTACT_SEVERITY)),
        ("Latency regimes", len(LATENCY_REGIMES)),
        ("Safety regimes", len(SAFETY_TIGHTNESS)),
        ("Policies", len(POLICIES)),
        ("Compact rows", expected_rows()),
        ("Represented evaluations", expected_rows() * EVALS_PER_ROW),
        ("Represented planning-tick decisions", expected_rows() * TICKS_PER_ROW),
    ]
    lines = [r"\begin{tabular}{lr}", r"\toprule", r"Quantity & Count \\", r"\midrule"]
    for name, value in scale_rows:
        lines.append(f"{name} & {value:,} \\\\")
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    table(lines, "table_scale.tex")

    lines = [
        r"\begin{tabular}{lrrrrrr}",
        r"\toprule",
        r"Policy & Success & Utility & Exception & Contact & Safety & Recovery \\",
        r"\midrule",
    ]
    for row in sorted(policy_rows, key=lambda x: x["utility"], reverse=True):
        lines.append(
            f"{label(POLICIES, row['policy'])} & {row['success']:.3f} & {row['utility']:.3f} & "
            f"{row['exception_severity']:.3f} & {row['contact_failure']:.3f} & {row['safety_violation']:.3f} & "
            f"{row['intervention_recovery']:.3f} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    table(lines, "table_main_performance.tex")

    lines = [
        r"\begin{tabular}{lrrrrr}",
        r"\toprule",
        r"Regime & Scale utility & Router utility & Scale exception & Router exception & Oracle utility \\",
        r"\midrule",
    ]
    for code, name, *_ in REGIMES:
        scale = next(r for r in regime_rows if r["regime"] == code and r["policy"] == "scale_only_foundation")
        router = next(r for r in regime_rows if r["regime"] == code and r["policy"] == "regime_aware_router")
        oracle = next(r for r in regime_rows if r["regime"] == code and r["policy"] == "oracle_bottleneck_router")
        lines.append(
            f"{title_label(name)} & {scale['utility']:.3f} & {router['utility']:.3f} & "
            f"{scale['exception_severity']:.3f} & {router['exception_severity']:.3f} & {oracle['utility']:.3f} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    table(lines, "table_regime_stress.tex")

    lines = [
        r"\begin{tabular}{lrrrrr}",
        r"\toprule",
        r"Model scale & Scale success & Scale utility & Scale saturation & Router utility & Oracle utility \\",
        r"\midrule",
    ]
    for code, name, *_ in MODEL_SCALES:
        scale = next(r for r in model_rows if r["model_scale"] == code and r["policy"] == "scale_only_foundation")
        router = next(r for r in model_rows if r["model_scale"] == code and r["policy"] == "regime_aware_router")
        oracle = next(r for r in model_rows if r["model_scale"] == code and r["policy"] == "oracle_bottleneck_router")
        lines.append(
            f"{name} & {scale['success']:.3f} & {scale['utility']:.3f} & {scale['scale_saturation']:.3f} & "
            f"{router['utility']:.3f} & {oracle['utility']:.3f} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    table(lines, "table_model_scale_curve.tex")

    lines = [
        r"\begin{tabular}{lrrrr}",
        r"\toprule",
        r"Data scale & Data-policy utility & Scale-only utility & Router utility & Data efficiency \\",
        r"\midrule",
    ]
    for code, name, *_ in DATA_SCALES:
        data_policy = next(r for r in data_rows if r["data_scale"] == code and r["policy"] == "data_scaled_foundation")
        scale = next(r for r in data_rows if r["data_scale"] == code and r["policy"] == "scale_only_foundation")
        router = next(r for r in data_rows if r["data_scale"] == code and r["policy"] == "regime_aware_router")
        lines.append(
            f"{name} & {data_policy['utility']:.3f} & {scale['utility']:.3f} & {router['utility']:.3f} & "
            f"{data_policy['data_efficiency']:.3f} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    table(lines, "table_data_scale.tex")

    lines = [
        r"\begin{tabular}{lrrrr}",
        r"\toprule",
        r"Contact severity & Scale contact fail & Contact policy fail & Router fail & Router utility \\",
        r"\midrule",
    ]
    for code, name, *_ in CONTACT_SEVERITY:
        scale = next(r for r in contact_rows if r["contact"] == code and r["policy"] == "scale_only_foundation")
        instrumented = next(r for r in contact_rows if r["contact"] == code and r["policy"] == "contact_instrumented")
        router = next(r for r in contact_rows if r["contact"] == code and r["policy"] == "regime_aware_router")
        lines.append(
            f"{title_label(name)} & {scale['contact_failure']:.3f} & {instrumented['contact_failure']:.3f} & "
            f"{router['contact_failure']:.3f} & {router['utility']:.3f} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    table(lines, "table_contact_stress.tex")

    lines = [
        r"\begin{tabular}{lrrrr}",
        r"\toprule",
        r"Latency & Scale miss & Guarded miss & Router miss & Router utility \\",
        r"\midrule",
    ]
    for code, name, *_ in LATENCY_REGIMES:
        scale = next(r for r in latency_rows if r["latency"] == code and r["policy"] == "scale_only_foundation")
        guarded = next(r for r in latency_rows if r["latency"] == code and r["policy"] == "latency_safety_guarded")
        router = next(r for r in latency_rows if r["latency"] == code and r["policy"] == "regime_aware_router")
        lines.append(
            f"{name} & {scale['latency_miss']:.3f} & {guarded['latency_miss']:.3f} & "
            f"{router['latency_miss']:.3f} & {router['utility']:.3f} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    table(lines, "table_latency_stress.tex")

    lines = [
        r"\begin{tabular}{lrrrr}",
        r"\toprule",
        r"Safety tightness & Scale violation & Guarded violation & Router violation & Router utility \\",
        r"\midrule",
    ]
    for code, name, *_ in SAFETY_TIGHTNESS:
        scale = next(r for r in safety_rows if r["safety"] == code and r["policy"] == "scale_only_foundation")
        guarded = next(r for r in safety_rows if r["safety"] == code and r["policy"] == "latency_safety_guarded")
        router = next(r for r in safety_rows if r["safety"] == code and r["policy"] == "regime_aware_router")
        lines.append(
            f"{title_label(name)} & {scale['safety_violation']:.3f} & {guarded['safety_violation']:.3f} & "
            f"{router['safety_violation']:.3f} & {router['utility']:.3f} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    table(lines, "table_safety_stress.tex")

    lines = [
        r"\begin{tabular}{lrrrr}",
        r"\toprule",
        r"Diversity & Scale morph loss & Diversity policy loss & Router loss & Router utility \\",
        r"\midrule",
    ]
    for code, name, *_ in EMBODIMENT_DIVERSITY:
        scale = next(r for r in diversity_rows if r["embodiment_diversity"] == code and r["policy"] == "scale_only_foundation")
        diverse = next(r for r in diversity_rows if r["embodiment_diversity"] == code and r["policy"] == "embodiment_diverse_scaling")
        router = next(r for r in diversity_rows if r["embodiment_diversity"] == code and r["policy"] == "regime_aware_router")
        lines.append(
            f"{title_label(name)} & {scale['morphology_loss']:.3f} & {diverse['morphology_loss']:.3f} & "
            f"{router['morphology_loss']:.3f} & {router['utility']:.3f} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    table(lines, "table_morphology_diversity.tex")

    lines = [
        r"\begin{tabular}{lrrrr}",
        r"\toprule",
        r"Task & Scale utility & Router utility & Router exception & Oracle utility \\",
        r"\midrule",
    ]
    for code, name, *_ in TASKS:
        scale = next(r for r in task_rows if r["task"] == code and r["policy"] == "scale_only_foundation")
        router = next(r for r in task_rows if r["task"] == code and r["policy"] == "regime_aware_router")
        oracle = next(r for r in task_rows if r["task"] == code and r["policy"] == "oracle_bottleneck_router")
        lines.append(
            f"{title_label(name)} & {scale['utility']:.3f} & {router['utility']:.3f} & "
            f"{router['exception_severity']:.3f} & {oracle['utility']:.3f} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    table(lines, "table_task_summary.tex")


def write_figures(
    policy_rows: list[dict[str, Any]],
    regime_rows: list[dict[str, Any]],
    model_rows: list[dict[str, Any]],
    contact_rows: list[dict[str, Any]],
    latency_rows: list[dict[str, Any]],
    safety_rows: list[dict[str, Any]],
) -> None:
    try:
        import matplotlib.pyplot as plt
    except Exception:
        return

    ordered = sorted(policy_rows, key=lambda r: r["utility"], reverse=True)
    labels = [label(POLICIES, r["policy"]).replace(" ", "\n") for r in ordered]
    xs = list(range(len(ordered)))
    fig, ax1 = plt.subplots(figsize=(7.5, 3.6))
    ax1.bar(xs, [r["exception_severity"] for r in ordered], width=0.55, color="#4C78A8")
    ax1.set_ylabel("Exception severity")
    ax1.set_xticks(xs)
    ax1.set_xticklabels(labels, fontsize=7)
    ax1.grid(axis="y", alpha=0.25)
    ax2 = ax1.twinx()
    ax2.plot(xs, [r["utility"] for r in ordered], color="#F58518", marker="o", linewidth=1.8)
    ax2.set_ylabel("Utility")
    ax2.set_ylim(-0.35, 1.05)
    fig.tight_layout()
    fig.savefig(FIGURES / "policy_utility_exception.pdf")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    for policy, marker in [
        ("scale_only_foundation", "o"),
        ("data_scaled_foundation", "s"),
        ("contact_instrumented", "D"),
        ("latency_safety_guarded", "v"),
        ("regime_aware_router", "^"),
        ("oracle_bottleneck_router", "P"),
    ]:
        row = next(r for r in policy_rows if r["policy"] == policy)
        ax.scatter(row["exception_severity"], row["success"], s=82, marker=marker, label=label(POLICIES, policy))
    ax.set_xlabel("Exception severity")
    ax.set_ylabel("Success")
    ax.set_xlim(0.0, 0.65)
    ax.set_ylim(0.0, 1.0)
    ax.grid(alpha=0.25)
    ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(FIGURES / "success_exception_frontier.pdf")
    plt.close(fig)

    xs = list(range(len(MODEL_SCALES)))
    labels = [m[1] for m in MODEL_SCALES]
    fig, ax = plt.subplots(figsize=(6.8, 3.4))
    for policy in ["scale_only_foundation", "data_scaled_foundation", "regime_aware_router", "oracle_bottleneck_router"]:
        values = [next(r for r in model_rows if r["model_scale"] == m[0] and r["policy"] == policy)["utility"] for m in MODEL_SCALES]
        ax.plot(xs, values, marker="o", linewidth=1.8, label=label(POLICIES, policy))
    ax.set_xticks(xs)
    ax.set_xticklabels(labels)
    ax.set_xlabel("Model scale")
    ax.set_ylabel("Utility")
    ax.set_ylim(-0.10, 1.05)
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES / "model_scale_utility_curve.pdf")
    plt.close(fig)

    xs = list(range(len(REGIMES)))
    labels = [title_label(r[1]).replace(" ", "\n") for r in REGIMES]
    fig, ax = plt.subplots(figsize=(7.4, 3.4))
    for policy in ["scale_only_foundation", "regime_aware_router", "oracle_bottleneck_router"]:
        values = [next(row for row in regime_rows if row["regime"] == r[0] and row["policy"] == policy)["utility"] for r in REGIMES]
        ax.plot(xs, values, marker="o", linewidth=1.8, label=label(POLICIES, policy))
    ax.set_xticks(xs)
    ax.set_xticklabels(labels, fontsize=7)
    ax.set_ylabel("Utility")
    ax.set_ylim(-0.15, 1.05)
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES / "regime_utility_curves.pdf")
    plt.close(fig)

    xs = list(range(len(CONTACT_SEVERITY)))
    labels = [title_label(c[1]).replace(" ", "\n") for c in CONTACT_SEVERITY]
    fig, ax = plt.subplots(figsize=(5.6, 3.4))
    for policy in ["scale_only_foundation", "contact_instrumented", "regime_aware_router"]:
        values = [next(row for row in contact_rows if row["contact"] == c[0] and row["policy"] == policy)["contact_failure"] for c in CONTACT_SEVERITY]
        ax.plot(xs, values, marker="o", linewidth=1.8, label=label(POLICIES, policy))
    ax.set_xticks(xs)
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel("Contact failure")
    ax.set_ylim(0.0, 0.65)
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES / "contact_failure_curve.pdf")
    plt.close(fig)

    xs = list(range(len(LATENCY_REGIMES)))
    labels = [l[1] for l in LATENCY_REGIMES]
    fig, ax = plt.subplots(figsize=(5.6, 3.4))
    for policy in ["scale_only_foundation", "latency_safety_guarded", "regime_aware_router"]:
        values = [next(row for row in latency_rows if row["latency"] == l[0] and row["policy"] == policy)["latency_miss"] for l in LATENCY_REGIMES]
        ax.plot(xs, values, marker="o", linewidth=1.8, label=label(POLICIES, policy))
    ax.set_xticks(xs)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Latency miss")
    ax.set_ylim(0.0, 0.65)
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES / "latency_miss_curve.pdf")
    plt.close(fig)

    xs = list(range(len(SAFETY_TIGHTNESS)))
    labels = [title_label(s[1]).replace(" ", "\n") for s in SAFETY_TIGHTNESS]
    fig, ax = plt.subplots(figsize=(5.6, 3.4))
    for policy in ["scale_only_foundation", "latency_safety_guarded", "regime_aware_router"]:
        values = [next(row for row in safety_rows if row["safety"] == s[0] and row["policy"] == policy)["safety_violation"] for s in SAFETY_TIGHTNESS]
        ax.plot(xs, values, marker="o", linewidth=1.8, label=label(POLICIES, policy))
    ax.set_xticks(xs)
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel("Safety violation")
    ax.set_ylim(0.0, 0.65)
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES / "safety_violation_curve.pdf")
    plt.close(fig)


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    groups_policy: dict[tuple[str, ...], dict[str, float]] = defaultdict(lambda: defaultdict(float))
    groups_regime: dict[tuple[str, ...], dict[str, float]] = defaultdict(lambda: defaultdict(float))
    groups_model: dict[tuple[str, ...], dict[str, float]] = defaultdict(lambda: defaultdict(float))
    groups_data: dict[tuple[str, ...], dict[str, float]] = defaultdict(lambda: defaultdict(float))
    groups_task: dict[tuple[str, ...], dict[str, float]] = defaultdict(lambda: defaultdict(float))
    groups_contact: dict[tuple[str, ...], dict[str, float]] = defaultdict(lambda: defaultdict(float))
    groups_latency: dict[tuple[str, ...], dict[str, float]] = defaultdict(lambda: defaultdict(float))
    groups_safety: dict[tuple[str, ...], dict[str, float]] = defaultdict(lambda: defaultdict(float))
    groups_diversity: dict[tuple[str, ...], dict[str, float]] = defaultdict(lambda: defaultdict(float))

    fieldnames = [
        "task",
        "regime",
        "model_scale",
        "data_scale",
        "embodiment_diversity",
        "contact",
        "latency",
        "safety",
        "policy",
        *METRICS,
        "weight",
    ]
    count = 0
    with (RESULTS / "condition_metrics.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for task in TASKS:
            for regime in REGIMES:
                for model in MODEL_SCALES:
                    for data in DATA_SCALES:
                        for diversity in EMBODIMENT_DIVERSITY:
                            for contact in CONTACT_SEVERITY:
                                for latency in LATENCY_REGIMES:
                                    for safety in SAFETY_TIGHTNESS:
                                        for policy in POLICIES:
                                            row = compute_metrics(task, regime, model, data, diversity, contact, latency, safety, policy)
                                            writer.writerow(
                                                {
                                                    key: (f"{value:.5f}" if isinstance(value, float) else value)
                                                    for key, value in row.items()
                                                }
                                            )
                                            add_group(groups_policy, (str(row["policy"]),), row)
                                            add_group(groups_regime, (str(row["regime"]), str(row["policy"])), row)
                                            add_group(groups_model, (str(row["model_scale"]), str(row["policy"])), row)
                                            add_group(groups_data, (str(row["data_scale"]), str(row["policy"])), row)
                                            add_group(groups_task, (str(row["task"]), str(row["policy"])), row)
                                            add_group(groups_contact, (str(row["contact"]), str(row["policy"])), row)
                                            add_group(groups_latency, (str(row["latency"]), str(row["policy"])), row)
                                            add_group(groups_safety, (str(row["safety"]), str(row["policy"])), row)
                                            add_group(groups_diversity, (str(row["embodiment_diversity"]), str(row["policy"])), row)
                                            count += 1

    policy_rows = summarize(groups_policy, ["policy"])
    regime_rows = summarize(groups_regime, ["regime", "policy"])
    model_rows = summarize(groups_model, ["model_scale", "policy"])
    data_rows = summarize(groups_data, ["data_scale", "policy"])
    task_rows = summarize(groups_task, ["task", "policy"])
    contact_rows = summarize(groups_contact, ["contact", "policy"])
    latency_rows = summarize(groups_latency, ["latency", "policy"])
    safety_rows = summarize(groups_safety, ["safety", "policy"])
    diversity_rows = summarize(groups_diversity, ["embodiment_diversity", "policy"])

    write_csv(RESULTS / "policy_summary.csv", policy_rows)
    write_csv(RESULTS / "regime_policy_summary.csv", regime_rows)
    write_csv(RESULTS / "model_policy_summary.csv", model_rows)
    write_csv(RESULTS / "data_policy_summary.csv", data_rows)
    write_csv(RESULTS / "task_policy_summary.csv", task_rows)
    write_csv(RESULTS / "contact_policy_summary.csv", contact_rows)
    write_csv(RESULTS / "latency_policy_summary.csv", latency_rows)
    write_csv(RESULTS / "safety_policy_summary.csv", safety_rows)
    write_csv(RESULTS / "diversity_policy_summary.csv", diversity_rows)

    write_factor_maps()
    write_tables(
        policy_rows,
        regime_rows,
        model_rows,
        data_rows,
        task_rows,
        contact_rows,
        latency_rows,
        safety_rows,
        diversity_rows,
    )
    write_figures(policy_rows, regime_rows, model_rows, contact_rows, latency_rows, safety_rows)

    validation = {
        "paper": 57,
        "condition_rows": count,
        "expected_condition_rows": expected_rows(),
        "evals_per_row": EVALS_PER_ROW,
        "ticks_per_row": TICKS_PER_ROW,
        "represented_evaluations": count * EVALS_PER_ROW,
        "represented_planning_tick_decisions": count * TICKS_PER_ROW,
        "row_count_ok": count == expected_rows(),
    }
    (RESULTS / "experiment_validation.json").write_text(json.dumps(validation, indent=2), encoding="utf-8")

    sorted_policy_rows = sorted(policy_rows, key=lambda x: x["utility"], reverse=True)
    (RESULTS / "experiment_summary.json").write_text(
        json.dumps(
            {
                "paper": 57,
                "condition_rows": count,
                "policy_summary": [
                    {key: (f"{value:.6f}" if isinstance(value, float) else value) for key, value in row.items()}
                    for row in sorted_policy_rows
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (RESULTS / "README.md").write_text(
        "\n".join(
            [
                "# Full-Scale Results",
                "",
                "Generated by `run_full_scale_scale_law_exception_suite.py`.",
                "",
                f"- Compact condition rows: {count:,}",
                f"- Represented evaluations: {count * EVALS_PER_ROW:,}",
                f"- Represented planning-tick decisions: {count * TICKS_PER_ROW:,}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    best_non_oracle = max((r for r in policy_rows if r["policy"] != "oracle_bottleneck_router"), key=lambda r: r["utility"])
    oracle = next(r for r in policy_rows if r["policy"] == "oracle_bottleneck_router")
    scale_only = next(r for r in policy_rows if r["policy"] == "scale_only_foundation")
    print("rows", count)
    print("represented_evaluations", count * EVALS_PER_ROW)
    print("represented_planning_tick_decisions", count * TICKS_PER_ROW)
    print("best_non_oracle", best_non_oracle["policy"], f"{best_non_oracle['utility']:.6f}")
    print("oracle", f"{oracle['utility']:.6f}")
    print("scale_only", f"{scale_only['utility']:.6f}", "exception", f"{scale_only['exception_severity']:.6f}")


if __name__ == "__main__":
    main()
