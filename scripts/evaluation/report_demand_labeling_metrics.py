"""Summarize Rule, Model Only, and Hybrid Demand labeling metrics."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from moongcheap_ai.data_foundation.labeling import load_taxonomy


def _json(value: object) -> object:
    try:
        return json.loads(str(value))
    except (TypeError, json.JSONDecodeError):
        return {}


def _expected_codes(row: pd.Series, taxonomy) -> dict[str, int]:
    category = taxonomy.category(row.get("category_id", "")) or {}
    expected = _json(row.get("expected_facet_profile", "{}"))
    expected = expected if isinstance(expected, dict) else {}
    facets = sorted(category.get("facets", []), key=lambda item: int(item.get("order", 0)))
    return {str(facet["name"]): int(expected.get(str(facet["name"]), {}).get("code", 0)) for facet in facets}


def _label_matches_expected(label: object, row: pd.Series, taxonomy) -> bool | None:
    if label is None or pd.isna(label) or not str(label).strip():
        return None
    codes = [int(part) for part in str(label).split("-") if str(part).strip().isdigit()]
    expected = _expected_codes(row, taxonomy)
    category = taxonomy.category(row.get("category_id", "")) or {}
    facets = sorted(category.get("facets", []), key=lambda item: int(item.get("order", 0)))
    if len(codes) != len(facets):
        return False
    return all(codes[index] == expected[str(facet["name"])] for index, facet in enumerate(facets) if expected[str(facet["name"])] != 0)


def _unresolved(value: object) -> bool:
    parsed = _json(value)
    return bool(parsed) if isinstance(parsed, (list, dict)) else bool(str(value).strip())


def _metric_row(method: str, frame: pd.DataFrame, status_column: str, label_column: str, taxonomy, model_failures: int = 0, model_calls: object = None) -> dict[str, object]:
    labeled = frame[label_column].fillna("").astype(str).str.strip().ne("")
    status = frame[status_column].fillna("").astype(str)
    diagnostic = [_label_matches_expected(label, row, taxonomy) for label, (_, row) in zip(frame[label_column], frame.iterrows())]
    diagnostic_values = [value for value in diagnostic if value is not None]
    return {
        "method": method,
        "dataset_rows": len(frame),
        "labeled_rows": int(labeled.sum()),
        "review_rows": int(status.str.contains("REVIEW|FAILURE|LIMIT|BLOCKED", case=False, regex=True).sum()),
        "unresolved_rows": int(frame.get("unresolved_items", pd.Series([], dtype=str)).map(_unresolved).sum()) if "unresolved_items" in frame else None,
        "model_failure_rows": model_failures,
        "diagnostic_agreement_rows": sum(value is True for value in diagnostic_values),
        "diagnostic_comparable_rows": len(diagnostic_values),
        "diagnostic_agreement": round(sum(value is True for value in diagnostic_values) / len(diagnostic_values), 4) if diagnostic_values else None,
        "normal_scenario_rows": int(frame.get("scenario_type", pd.Series([], dtype=str)).astype(str).str.startswith("NORMAL").sum()) if "scenario_type" in frame else None,
        "ambiguous_scenario_rows": int(frame.get("scenario_type", pd.Series([], dtype=str)).eq("AMBIGUOUS").sum()) if "scenario_type" in frame else None,
        "conflict_scenario_rows": int(frame.get("scenario_type", pd.Series([], dtype=str)).eq("CONFLICT").sum()) if "scenario_type" in frame else None,
        "out_of_taxonomy_rows": int(frame.get("scenario_type", pd.Series([], dtype=str)).eq("OUT_OF_TAXONOMY").sum()) if "scenario_type" in frame else None,
        "model_calls": model_calls,
    }


def build_metrics(input_dir: Path, taxonomy_path: Path) -> pd.DataFrame:
    taxonomy = load_taxonomy(taxonomy_path)
    raw = pd.read_csv(input_dir / "grounded_demand_5000_raw.csv", dtype=str).fillna("")
    rule = pd.read_csv(input_dir / "demand_5000_rule_labeled_v1.csv", dtype=str).fillna("").merge(raw[["demand_id", "expected_facet_profile", "scenario_type"]], on="demand_id", how="left", suffixes=("", "_raw"))
    hybrid = pd.read_csv(input_dir / "model2_rule_llm_hybrid_comparison_v1.csv", dtype=str).fillna("").merge(raw[["demand_id", "expected_facet_profile"]], on="demand_id", how="left")
    llm = pd.read_csv(input_dir / "model2_llm_labeled_200_v1.csv", dtype=str).fillna("").merge(raw[["demand_id", "expected_facet_profile", "scenario_type"]], on="demand_id", how="left")
    rows = [
        _metric_row("RULE_BASELINE", rule, "label_status", "label", taxonomy, model_calls=0),
        _metric_row("MODEL_ONLY_SAMPLE_200", llm, "model_status", "model_label", taxonomy, model_failures=int(llm["model_status"].eq("MODEL_FAILURE").sum()), model_calls=4),
        _metric_row("HYBRID_RULE_FIRST", hybrid, "hybrid_status", "hybrid_label", taxonomy, model_failures=int(hybrid["hybrid_model_status"].eq("MODEL_FAILURE").sum()), model_calls=int(hybrid["hybrid_model_status"].isin(["LLM_ASSISTED", "MODEL_FAILURE"]).sum())),
    ]
    result = pd.DataFrame(rows)
    result.attrs["rule_rows"] = len(rule)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Report Demand labeling method metrics")
    parser.add_argument("--input-dir", type=Path, default=Path("data/processed/demand_5000_v1"))
    parser.add_argument("--taxonomy", type=Path, default=Path("data/processed/downstream_v2_1/taxonomy_candidate_v2_1.json"))
    args = parser.parse_args()
    metrics = build_metrics(args.input_dir, args.taxonomy)
    output_csv = args.input_dir / "demand_labeling_method_metrics_v1.csv"
    output_md = args.input_dir / "demand_labeling_method_metrics_v1.md"
    metrics.to_csv(output_csv, index=False, encoding="utf-8-sig")
    lines = [
        "# Demand Labeling 방식별 지표", "",
        "Rule Baseline과 Hybrid는 5,000건 전체를 대상으로 집계했고, Model Only는 실제 실행된 대표 Sample 200건 기준입니다.",
        "`diagnostic_agreement`는 생성 시 사용한 expected facet profile과의 비교이며 Human Gold Accuracy가 아닙니다.", "",
        "```", metrics.to_string(index=False), "```", "",
        "## 해석", "",
        "- Rule Baseline: Alias/규칙으로 전체를 빠르게 처리하며 검토 대상은 별도 표시합니다.",
        "- Model Only: 200건 Sample에 실제 Model 2를 적용한 결과입니다. 모델 실패는 정상 Label로 간주하지 않습니다.",
        "- Hybrid: Rule 성공 건은 Rule을 사용하고, 검토 대상만 제한적으로 Model을 호출합니다.",
        "- 가격·수량·대체 가능 여부는 Labeling 정확도 지표가 아니라 Synthetic 정책 값입니다.",
    ]
    output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(metrics.to_dict("records"))


if __name__ == "__main__":
    main()
