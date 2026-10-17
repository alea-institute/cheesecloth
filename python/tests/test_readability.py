"""Tests for the Rust readability functions."""

import math

import pytest

import cheesecloth
from cheesecloth.tokenized_metrics import AllMetrics

TEXTS = [
    "",
    "Hi.",
    "The cat sat on the mat. The dog barked.",
    "The court held that the agreement was void.\n\nIt was signed under duress.",
    "Notwithstanding the foregoing provisions, the indemnifying party shall, "
    "pursuant to Section 12(b), reimburse all reasonable expenses incurred.",
    "Ünïcödé façade naïve. Straße! Größe.\n\nZweiter Absatz hier.",
    "word " * 500,
]

LEVELS = {"Easy", "Moderate", "Challenging", "Complex", "Very Complex"}


def all_metrics(text, include_punctuation=False, case_sensitive=True):
    return AllMetrics.from_dict(
        cheesecloth.get_all_metrics(
            text,
            include_punctuation=include_punctuation,
            case_sensitive=case_sensitive,
            use_paragraph_processing=True,
        )
    )


def test_functions_are_exported():
    for name in (
        "calculate_readability_score",
        "get_readability_level",
        "get_readability_factors",
    ):
        assert callable(getattr(cheesecloth, name))


@pytest.mark.parametrize("text", TEXTS)
@pytest.mark.parametrize("include_punctuation", [False, True])
@pytest.mark.parametrize("case_sensitive", [False, True])
def test_matches_all_metrics_wrapper(text, include_punctuation, case_sensitive):
    reference = all_metrics(text, include_punctuation, case_sensitive)
    score = cheesecloth.calculate_readability_score(
        text, include_punctuation, case_sensitive
    )
    assert math.isclose(
        score, reference.calculate_readability_score(), rel_tol=1e-9, abs_tol=1e-12
    )
    assert (
        cheesecloth.get_readability_level(text, include_punctuation, case_sensitive)
        == reference.get_readability_level()
    )

    factors = cheesecloth.get_readability_factors(
        text, include_punctuation, case_sensitive
    )
    expected = reference.get_readability_assessment()
    assert factors["level"] == expected["level"]
    assert math.isclose(
        factors["score"], expected["score"], rel_tol=1e-9, abs_tol=1e-12
    )
    assert set(factors["factors"]) == set(expected["factors"])
    for name, values in expected["factors"].items():
        got = factors["factors"][name]
        assert set(got) == {"raw_value", "normalized_score", "weight"}
        assert got["weight"] == values["weight"]
        for key in ("raw_value", "normalized_score"):
            assert math.isclose(got[key], values[key], rel_tol=1e-9, abs_tol=1e-12)


def test_defaults():
    text = TEXTS[3]
    assert cheesecloth.calculate_readability_score(text) == pytest.approx(
        cheesecloth.calculate_readability_score(text, False, True)
    )


def test_score_range_and_level():
    for text in TEXTS:
        score = cheesecloth.calculate_readability_score(text)
        assert 0.0 <= score <= 1.0
        assert cheesecloth.get_readability_level(text) in LEVELS
    assert cheesecloth.calculate_readability_score("") == 0.0
    assert cheesecloth.get_readability_level("") == "Easy"


def test_average_sentence_length_override():
    text = TEXTS[2]
    factors = cheesecloth.get_readability_factors(text, average_sentence_length=25.0)
    sentence = factors["factors"]["sentence_complexity"]
    assert sentence["raw_value"] == 25.0
    assert sentence["normalized_score"] == pytest.approx(0.5)
    base = cheesecloth.calculate_readability_score(text)
    longer = cheesecloth.calculate_readability_score(
        text, average_sentence_length=100.0
    )
    assert longer > base
    assert (
        cheesecloth.get_readability_level(text, average_sentence_length=100.0) in LEVELS
    )


def test_cli_helpers_use_rust_functions():
    from cheesecloth import cli

    text = TEXTS[4]
    assert cli.calculate_readability_score(
        text
    ) == cheesecloth.calculate_readability_score(text)
    assert cli.get_readability_level(text) == cheesecloth.get_readability_level(text)
    assert cli.get_readability_factors(text) == cheesecloth.get_readability_factors(
        text
    )
