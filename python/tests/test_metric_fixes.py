"""Regression tests for correctness fixes in character and unigram metrics."""

import random
import unicodedata

import pytest

import cheesecloth

SAMPLE = (
    "Hello, World! a-b*c/d%e^f\n\tg\r\x0b\x0c\x00\x1f\x7f ­éß中½²①٣€©—“” ​\U0001f642ǅ̈"
)


def test_unicode_categories_match_unicodedata_for_latin1():
    text = "".join(chr(c) for c in range(256))
    assert cheesecloth.get_unicode_categories(text) == [
        unicodedata.category(ch) for ch in text
    ]


def test_unicode_categories_match_unicodedata_sample():
    assert cheesecloth.get_unicode_categories(SAMPLE) == [
        unicodedata.category(ch) for ch in SAMPLE
    ]
    groups = cheesecloth.get_unicode_category_groups(SAMPLE)
    assert groups == [unicodedata.category(ch)[0] for ch in SAMPLE]


def test_newlines_tabs_are_control_characters():
    ratios = cheesecloth.get_unicode_category_ratios("a\nb\tc\r")
    assert ratios["Cc"] == pytest.approx(3 / 6)
    assert "Zs" not in ratios


def test_control_chars_excluding_whitespace():
    metrics = cheesecloth.get_all_char_metrics("ab\n\t\r\x0b\x0c\x85\x00\x1b\x7f")
    # \x00, \x1b and \x7f are Cc and not whitespace; the rest are whitespace
    assert metrics["control_chars_excluding_whitespace"] == 3
    assert metrics["ratio_control_chars_excluding_whitespace"] == pytest.approx(3 / 11)
    assert metrics["unicode_category_ratios"]["Cc"] == pytest.approx(9 / 11)

    clean = cheesecloth.get_all_char_metrics("plain text\nwith lines\n")
    assert clean["control_chars_excluding_whitespace"] == 0
    assert clean["ratio_control_chars_excluding_whitespace"] == 0.0

    empty = cheesecloth.get_all_char_metrics("")
    assert empty["control_chars_excluding_whitespace"] == 0
    assert empty["ratio_control_chars_excluding_whitespace"] == 0.0


def _ngram_reference(text, group=False):
    cats = [unicodedata.category(ch) for ch in text]
    if group:
        cats = [c[0] for c in cats]
    bigrams, trigrams = {}, {}
    if cats:
        seq = ["START"] + cats + ["END"]
        for a, b in zip(seq, seq[1:]):
            bigrams[(a, b)] = bigrams.get((a, b), 0) + 1
        for i, cur in enumerate(cats):
            prev = cats[i - 1] if i > 0 else "START"
            nxt = cats[i + 1] if i + 1 < len(cats) else "END"
            trigrams[(prev, cur, nxt)] = trigrams.get((prev, cur, nxt), 0) + 1
    return bigrams, trigrams


@pytest.mark.parametrize("text", ["", "a", "ab", "abc", SAMPLE, SAMPLE * 3])
def test_category_ngrams_match_reference(text):
    bigrams, trigrams = _ngram_reference(text)
    group_bigrams, group_trigrams = _ngram_reference(text, group=True)
    assert cheesecloth.get_unicode_category_bigrams(text) == bigrams
    assert cheesecloth.get_unicode_category_trigrams(text) == trigrams
    assert cheesecloth.get_unicode_category_group_bigrams(text) == group_bigrams
    assert cheesecloth.get_unicode_category_group_trigrams(text) == group_trigrams

    metrics = cheesecloth.get_all_char_metrics(text)
    total_bi = sum(bigrams.values())
    total_tri = sum(trigrams.values())
    assert metrics["unicode_category_bigram_ratios"] == pytest.approx(
        {k: v / total_bi for k, v in bigrams.items()}
    )
    assert metrics["unicode_category_trigram_ratios"] == pytest.approx(
        {k: v / total_tri for k, v in trigrams.items()}
    )
    assert metrics["unicode_category_group_bigram_ratios"] == pytest.approx(
        {k: v / total_bi for k, v in group_bigrams.items()}
    )
    assert metrics["unicode_category_group_trigram_ratios"] == pytest.approx(
        {k: v / total_tri for k, v in group_trigrams.items()}
    )


def test_char_frequency_and_runs():
    text = SAMPLE * 2
    metrics = cheesecloth.get_all_char_metrics(text)
    expected = {}
    for ch in text:
        expected[ch] = expected.get(ch, 0) + 1
    assert metrics["char_frequency"] == expected
    assert metrics["consecutive_runs"] == metrics["char_type_transitions"] + 1
    assert cheesecloth.get_all_char_metrics("")["consecutive_runs"] == 0


def _random_text(rnd):
    alphabet = list("abc XYZ 019.,!?\n") + ["é", "ß", "中", "Α", "ǅ"]
    return "".join(rnd.choice(alphabet) for _ in range(rnd.randint(0, 200)))


@pytest.mark.parametrize("include_punctuation", [False, True])
@pytest.mark.parametrize("case_sensitive", [False, True])
def test_unigram_metrics_consistent_with_standalone_functions(
    include_punctuation, case_sensitive
):
    rnd = random.Random(3)
    for _ in range(100):
        text = _random_text(rnd)
        metrics = cheesecloth.get_all_unigram_metrics(
            text, include_punctuation, case_sensitive
        )
        tokens = (
            cheesecloth.tokenize_unigrams_with_punctuation(text)
            if include_punctuation
            else cheesecloth.tokenize_unigrams(text)
        )
        freq = cheesecloth.get_unigram_frequency(
            text, include_punctuation, case_sensitive
        )
        n = len(tokens)
        assert metrics["token_count"] == n
        assert metrics["unique_token_count"] == len(freq)
        if n == 0:
            assert metrics["average_token_length"] == 0.0
            continue
        # Lengths are measured in code points, not UTF-8 bytes
        assert metrics["average_token_length"] == pytest.approx(
            sum(len(t) for t in tokens) / n
        )
        assert metrics["short_token_ratio"] == pytest.approx(
            sum(1 for t in tokens if len(t) <= 3) / n
        )
        assert metrics["long_token_ratio"] == pytest.approx(
            sum(1 for t in tokens if len(t) >= 7) / n
        )
        assert metrics["hapax_legomena_ratio"] == pytest.approx(
            sum(1 for c in freq.values() if c == 1) / n
        )
        assert metrics["top_5_token_coverage"] == pytest.approx(
            sum(sorted(freq.values(), reverse=True)[:5]) / n
        )
        assert metrics["max_frequency_ratio"] == pytest.approx(max(freq.values()) / n)
        assert metrics["short_token_ratio"] == pytest.approx(
            cheesecloth.short_token_ratio(text, include_punctuation, case_sensitive)
        )
        assert metrics["long_token_ratio"] == pytest.approx(
            cheesecloth.long_token_ratio(text, include_punctuation, case_sensitive)
        )
        assert metrics["hapax_legomena_ratio"] == pytest.approx(
            cheesecloth.hapax_legomena_ratio(text, include_punctuation, case_sensitive)
        )
        assert metrics["top_5_token_coverage"] == pytest.approx(
            cheesecloth.top_5_token_coverage(text, include_punctuation, case_sensitive)
        )


def test_get_all_metrics_unigram_section_matches_get_all_unigram_metrics():
    text = "Ünïcödé façade naïve. Straße! naïve"
    nested = cheesecloth.get_all_metrics(
        text, include_punctuation=False, case_sensitive=False
    )
    direct = cheesecloth.get_all_unigram_metrics(text, False, False)
    for key, value in direct.items():
        assert nested["unigram"][key] == pytest.approx(value)


def test_case_insensitive_folding():
    metrics = cheesecloth.get_all_unigram_metrics(
        "Straße STRASSE straße ÉTÉ été", False, False
    )
    # "Straße"/"straße" and "ÉTÉ"/"été" fold together; "STRASSE" lowercases to "strasse"
    assert metrics["unique_token_count"] == 3


def test_cli_module_imports():
    # cli.py previously used a backslash inside an f-string expression, which is
    # a SyntaxError before Python 3.12.
    import cheesecloth.cli  # noqa: F401
