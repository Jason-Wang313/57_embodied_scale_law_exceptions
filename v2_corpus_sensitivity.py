import csv
import json
import random
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
PAPER = ROOT / "paper"
OUT_CSV = DOCS / "v2_corpus_sensitivity_summary.csv"
OUT_JSON = DOCS / "v2_corpus_sensitivity.json"
OUT_TEX = PAPER / "v2_corpus_sensitivity_table.tex"


PATTERNS = {
    "baseline": {
        "scale": r"(scal|power law|generalization|zero-shot|more data|more embodiments|more compute)",
        "contact": r"(contact|tactile|force|grasp|dexter|friction)",
        "morphology": r"(embodiment|morpholog|locomotion|humanoid|quadruped|hexapod)",
    },
    "strict_terms": {
        "scale": r"(scaling law|power law|data scaling|model scaling|parameter scaling)",
        "contact": r"(contact-rich|tactile|force control|friction|dexterous manipulation)",
        "morphology": r"(morphology|cross-embodiment|locomotion|humanoid|quadruped)",
    },
    "scale_favorable": {
        "scale": r"(scal|power law|generalization|zero-shot|foundation model|vision-language-action|vla|more data|more embodiments|more compute)",
        "contact": r"(contact-rich|tactile|force control|friction)",
        "morphology": r"(morphology|cross-embodiment|humanoid|quadruped)",
    },
}


def load_rows():
    with (DOCS / "related_work_matrix.csv").open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        row["_text"] = f"{row.get('title', '')} {row.get('abstract', '')}"
    return rows


def build_hits(rows, patterns):
    regex = {key: re.compile(pattern, re.I) for key, pattern in patterns.items()}
    return {key: [1 if pattern.search(row["_text"]) else 0 for row in rows] for key, pattern in regex.items()}


def summarize_counts(counts):
    scale = counts["scale"]
    physical = counts["contact"] + counts["morphology"]
    return {
        **counts,
        "physical_regime": physical,
        "physical_to_scale_ratio": physical / max(1, scale),
        "contact_to_scale_ratio": counts["contact"] / max(1, scale),
    }


def classify_from_hits(hits, indices=None):
    if indices is None:
        counts = {key: sum(values) for key, values in hits.items()}
    else:
        counts = {key: sum(values[i] for i in indices) for key, values in hits.items()}
    return summarize_counts(counts)


def bootstrap(hits, row_count, n=400, seed=57057):
    rng = random.Random(seed)
    wins = 0
    ratios = []
    for _ in range(n):
        sample = [rng.randrange(row_count) for _ in range(row_count)]
        result = classify_from_hits(hits, sample)
        ratios.append(result["physical_to_scale_ratio"])
        if result["physical_regime"] > result["scale"]:
            wins += 1
    ratios.sort()
    return {
        "bootstrap_n": n,
        "physical_gt_scale_rate": wins / n,
        "ratio_p05": ratios[int(0.05 * (n - 1))],
        "ratio_p50": ratios[int(0.50 * (n - 1))],
        "ratio_p95": ratios[int(0.95 * (n - 1))],
    }


def main():
    rows = load_rows()
    summary = []
    for name, patterns in PATTERNS.items():
        hits = build_hits(rows, patterns)
        counts = classify_from_hits(hits)
        boot = bootstrap(hits, len(rows))
        summary.append({"variant": name, "rows": len(rows), **counts, **boot})

    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary[0].keys()))
        writer.writeheader()
        writer.writerows(summary)

    OUT_JSON.write_text(
        json.dumps(
            {
                "decision": "workshop-only",
                "reason": "Corpus synthesis is sensitive to keyword definitions; physical-regime language remains above scale language, but exact ratios are not stable enough for a strong empirical claim.",
                "summary": summary,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    OUT_TEX.write_text(
        "\n".join(
            [
                r"\begin{tabular}{lrrrr}",
                r"\toprule",
                r"Variant & Scale & Physical & Ratio & Boot win \\",
                r"\midrule",
                *[
                    (
                        f"{row['variant'].replace('_', ' ')} & {row['scale']} & {row['physical_regime']} & "
                        f"{row['physical_to_scale_ratio']:.2f} & {row['physical_gt_scale_rate']:.2f} \\\\"
                    )
                    for row in summary
                ],
                r"\bottomrule",
                r"\end{tabular}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    for row in summary:
        print(
            row["variant"],
            f"scale={row['scale']}",
            f"physical={row['physical_regime']}",
            f"ratio={row['physical_to_scale_ratio']:.2f}",
            f"boot_win={row['physical_gt_scale_rate']:.2f}",
        )


if __name__ == "__main__":
    main()
