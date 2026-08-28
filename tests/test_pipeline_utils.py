import json
from pathlib import Path

import pandas as pd

from moongcheap_ai.facet import repeated_terms, taxonomy_v0
from moongcheap_ai.preprocess import category_path, clean_title


def test_clean_title_removes_html_and_normalizes():
    assert clean_title(" <b>비타민&nbsp;C</b>  1000㎎ ") == "비타민 C 1000mg"


def test_category_path_ignores_empty_levels():
    assert category_path({"category1": "식품", "category2": "", "category3": "건강"}) == "식품 > 건강"


def test_repeated_terms_counts_documents_not_tokens():
    frame = pd.DataFrame({"name": ["분말 비타민", "분말 유산균", "분말 홍삼"], "main_functionality": ["", "", ""]})
    result = repeated_terms(frame, ["name"], min_documents=2, min_ratio=0)
    assert int(result.loc[result.term == "분말", "document_count"].iloc[0]) == 3


def test_taxonomy_is_deterministic_and_all_is_zero():
    terms = pd.DataFrame([{"term": "분말", "document_count": 3}, {"term": "캡슐", "document_count": 2}])
    first = taxonomy_v0("SEED", "x", terms)
    second = taxonomy_v0("SEED", "x", terms)
    assert first == second
    assert first["facets"][0]["values"][0]["code"] == 0
