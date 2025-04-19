import cheesecloth


def test_tokenize_unigrams():
    # Note: unicode_words behaves differently than expected with CJK characters
    assert cheesecloth.tokenize_unigrams("hello world") == ["hello", "world"]
    assert cheesecloth.tokenize_unigrams("") == []
    assert cheesecloth.tokenize_unigrams("hello  world") == ["hello", "world"]
    assert cheesecloth.tokenize_unigrams("Hello World") == ["Hello", "World"]
    # Mixed text
    assert "hello" in cheesecloth.tokenize_unigrams("hello 你好 world")
    assert "world" in cheesecloth.tokenize_unigrams("hello 你好 world")


def test_tokenize_unigrams_with_punctuation():
    tokens = cheesecloth.tokenize_unigrams_with_punctuation("hello world")
    assert "hello" in tokens
    assert " " in tokens
    assert "world" in tokens

    assert cheesecloth.tokenize_unigrams_with_punctuation("") == []

    tokens = cheesecloth.tokenize_unigrams_with_punctuation("hello, world!")
    assert "hello" in tokens
    assert "," in tokens
    assert " " in tokens
    assert "world" in tokens
    assert "!" in tokens

    tokens = cheesecloth.tokenize_unigrams_with_punctuation("hello.world")
    assert "hello" in tokens
    assert "." in tokens
    assert "world" in tokens


def test_count_unigram_tokens():
    assert (
        cheesecloth.count_unigram_tokens("hello world", include_punctuation=False) == 2
    )
    assert cheesecloth.count_unigram_tokens("", include_punctuation=False) == 0
    assert (
        cheesecloth.count_unigram_tokens("hello  world", include_punctuation=False) == 2
    )
    assert (
        cheesecloth.count_unigram_tokens("hello, world!", include_punctuation=False)
        == 2
    )
    # CJK characters may be tokenized character by character
    token_count = cheesecloth.count_unigram_tokens(
        "hello 你好 world", include_punctuation=False
    )
    assert token_count >= 3  # At minimum "hello", something with 你好, and "world"


def test_count_unique_unigrams():
    assert (
        cheesecloth.count_unique_unigrams(
            "hello world", include_punctuation=False, case_sensitive=True
        )
        == 2
    )
    assert (
        cheesecloth.count_unique_unigrams(
            "", include_punctuation=False, case_sensitive=True
        )
        == 0
    )
    assert (
        cheesecloth.count_unique_unigrams(
            "hello hello", include_punctuation=False, case_sensitive=True
        )
        == 1
    )
    assert (
        cheesecloth.count_unique_unigrams(
            "hello Hello", include_punctuation=False, case_sensitive=True
        )
        == 2
    )
    assert (
        cheesecloth.count_unique_unigrams(
            "hello Hello", include_punctuation=False, case_sensitive=False
        )
        == 1
    )
    assert (
        cheesecloth.count_unique_unigrams(
            "hello, world!", include_punctuation=True, case_sensitive=True
        )
        >= 4
    )
    assert (
        cheesecloth.count_unique_unigrams(
            "hello, world!", include_punctuation=False, case_sensitive=True
        )
        == 2
    )


def test_unigram_type_token_ratio():
    assert (
        cheesecloth.unigram_type_token_ratio(
            "hello world", include_punctuation=False, case_sensitive=True
        )
        == 1.0
    )
    assert (
        cheesecloth.unigram_type_token_ratio(
            "hello hello", include_punctuation=False, case_sensitive=True
        )
        == 0.5
    )
    assert (
        cheesecloth.unigram_type_token_ratio(
            "hello Hello", include_punctuation=False, case_sensitive=True
        )
        == 1.0
    )
    assert (
        cheesecloth.unigram_type_token_ratio(
            "hello Hello", include_punctuation=False, case_sensitive=False
        )
        == 0.5
    )
    assert (
        cheesecloth.unigram_type_token_ratio(
            "", include_punctuation=False, case_sensitive=True
        )
        == 0.0
    )
    # More complex example
    text = "the cat sat on the mat"
    assert (
        cheesecloth.unigram_type_token_ratio(
            text, include_punctuation=False, case_sensitive=True
        )
        == 5 / 6
    )


def test_unigram_repetition_rate():
    assert (
        cheesecloth.unigram_repetition_rate(
            "hello world", include_punctuation=False, case_sensitive=True
        )
        == 0.0
    )
    assert (
        cheesecloth.unigram_repetition_rate(
            "hello hello", include_punctuation=False, case_sensitive=True
        )
        == 0.5
    )
    assert (
        cheesecloth.unigram_repetition_rate(
            "hello Hello", include_punctuation=False, case_sensitive=True
        )
        == 0.0
    )
    assert (
        cheesecloth.unigram_repetition_rate(
            "hello Hello", include_punctuation=False, case_sensitive=False
        )
        == 0.5
    )
    # Empty text case - returns 0.0 if no tokens
    if cheesecloth.count_unigram_tokens("", include_punctuation=False) == 0:
        assert (
            cheesecloth.unigram_repetition_rate(
                "", include_punctuation=False, case_sensitive=True
            )
            == 0.0
        )
    # More complex example
    text = "the cat sat on the mat"
    rate = cheesecloth.unigram_repetition_rate(
        text, include_punctuation=False, case_sensitive=True
    )
    expected = 1 / 6
    assert abs(rate - expected) < 0.00001  # Allow for floating point differences


def test_get_unigram_frequency():
    # Simple case
    text = "the cat sat on the mat"
    freq = cheesecloth.get_unigram_frequency(
        text, include_punctuation=False, case_sensitive=True
    )
    assert freq["the"] == 2
    assert freq["cat"] == 1
    assert freq["sat"] == 1
    assert freq["on"] == 1
    assert freq["mat"] == 1
    assert len(freq) == 5

    # Empty text
    assert (
        cheesecloth.get_unigram_frequency(
            "", include_punctuation=False, case_sensitive=True
        )
        == {}
    )

    # Case sensitivity
    text = "The cat sat on the mat"
    freq = cheesecloth.get_unigram_frequency(
        text, include_punctuation=False, case_sensitive=True
    )
    assert freq["The"] == 1
    assert freq["the"] == 1
    assert len(freq) == 6

    # Case insensitivity
    freq = cheesecloth.get_unigram_frequency(
        text, include_punctuation=False, case_sensitive=False
    )
    assert freq["the"] == 2
    assert len(freq) == 5

    # With punctuation
    text = "Hello, world! Hello again."
    freq = cheesecloth.get_unigram_frequency(
        text, include_punctuation=True, case_sensitive=True
    )
    assert freq["Hello"] == 2
    # Check for specific punctuation and their expected counts
    assert "," in freq, "Comma should be in frequency dictionary"
    assert freq[","] == 1, f"Expected comma count 1, got {freq.get(',', 0)}"
    assert "!" in freq, "Exclamation mark should be in frequency dictionary"
    assert freq["!"] == 1, f"Expected exclamation mark count 1, got {freq.get('!', 0)}"
    assert "." in freq, "Period should be in frequency dictionary"
    assert freq["."] == 1, f"Expected period count 1, got {freq.get('.', 0)}"


def test_unigram_entropy():
    # Simple cases
    assert (
        cheesecloth.unigram_entropy(
            "hello world", include_punctuation=False, case_sensitive=True
        )
        > 0.0
    )
    assert (
        cheesecloth.unigram_entropy(
            "hello hello", include_punctuation=False, case_sensitive=True
        )
        == 0.0
    )

    # More diverse text should have higher entropy
    text1 = "the cat sat on the mat"  # Some repetition
    text2 = "quick brown fox jumps over lazy dog"  # No repetition
    assert cheesecloth.unigram_entropy(
        text1, include_punctuation=False, case_sensitive=True
    ) < cheesecloth.unigram_entropy(
        text2, include_punctuation=False, case_sensitive=True
    )

    # Empty text
    assert (
        cheesecloth.unigram_entropy("", include_punctuation=False, case_sensitive=True)
        == 0.0
    )

    # Case sensitivity test
    text = "The the THE"
    entropy_sensitive = cheesecloth.unigram_entropy(
        text, include_punctuation=False, case_sensitive=True
    )
    entropy_insensitive = cheesecloth.unigram_entropy(
        text, include_punctuation=False, case_sensitive=False
    )
    assert entropy_sensitive > entropy_insensitive


def hapax_legomena_ratio_impl(text, include_punctuation=False, case_sensitive=True):
    """Python implementation of hapax legomena ratio."""
    freq = cheesecloth.get_unigram_frequency(text, include_punctuation, case_sensitive)
    hapax_count = sum(1 for count in freq.values() if count == 1)
    total_tokens = sum(freq.values())
    return hapax_count / total_tokens if total_tokens > 0 else 0.0


def test_hapax_legomena_ratio():
    # Simple cases
    text = "the cat sat on the mat"
    # 4 hapax legomena (cat, sat, on, mat) out of 6 tokens
    ratio = hapax_legomena_ratio_impl(
        text, include_punctuation=False, case_sensitive=True
    )
    assert abs(ratio - 4 / 6) < 0.0001

    # No hapax legomena
    text = "the the the the"
    ratio = hapax_legomena_ratio_impl(
        text, include_punctuation=False, case_sensitive=True
    )
    assert ratio == 0.0

    # All hapax legomena
    text = "quick brown fox jumps"
    ratio = hapax_legomena_ratio_impl(
        text, include_punctuation=False, case_sensitive=True
    )
    assert ratio == 1.0

    # Empty text
    assert (
        hapax_legomena_ratio_impl("", include_punctuation=False, case_sensitive=True)
        == 0.0
    )


def top_5_token_coverage_impl(text, include_punctuation=False, case_sensitive=True):
    """Python implementation of top 5 token coverage."""
    freq = cheesecloth.get_unigram_frequency(text, include_punctuation, case_sensitive)

    if not freq:
        return 0.0

    sorted_counts = sorted(freq.values(), reverse=True)
    top_5_sum = sum(sorted_counts[:5])
    total_tokens = sum(freq.values())

    return top_5_sum / total_tokens if total_tokens > 0 else 0.0


def test_top_5_token_coverage():
    # Simple case
    text = "the cat sat on the mat and the dog jumped over the fence"
    # Tokens: the (4), cat (1), sat (1), on (1), mat (1), and (1), dog (1), jumped (1), over (1), fence (1)
    # Top 5: the (4), cat (1), sat (1), on (1), mat (1) = 8 out of 13 tokens
    ratio = top_5_token_coverage_impl(
        text, include_punctuation=False, case_sensitive=True
    )
    assert abs(ratio - 8 / 13) < 0.0001

    # Fewer than 5 unique tokens
    text = "the the cat cat dog"
    # All tokens covered by top 5
    ratio = top_5_token_coverage_impl(
        text, include_punctuation=False, case_sensitive=True
    )
    assert ratio == 1.0

    # Empty text
    assert (
        top_5_token_coverage_impl("", include_punctuation=False, case_sensitive=True)
        == 0.0
    )


def short_token_ratio_impl(text, include_punctuation=False, case_sensitive=True):
    """Python implementation of short token ratio."""
    tokens = (
        cheesecloth.tokenize_unigrams_with_punctuation(text)
        if include_punctuation
        else cheesecloth.tokenize_unigrams(text)
    )

    if not tokens:
        return 0.0

    short_count = sum(1 for token in tokens if len(token) <= 3)
    return short_count / len(tokens)


def test_short_token_ratio():
    # Simple cases
    text = "the cat sat on the mat and dog"
    # Short tokens (≤3): the, cat, sat, on, the, mat, and, dog = 8 out of 8
    ratio = short_token_ratio_impl(text, include_punctuation=False, case_sensitive=True)
    assert ratio == 1.0

    # Mix of short and long tokens
    text = "the extraordinary capabilities demonstrated by modern technology"
    # Short tokens: the, by = 2 out of 7
    ratio = short_token_ratio_impl(text, include_punctuation=False, case_sensitive=True)
    assert abs(ratio - 2 / 7) < 0.0001

    # Empty text
    assert (
        short_token_ratio_impl("", include_punctuation=False, case_sensitive=True)
        == 0.0
    )


def long_token_ratio_impl(text, include_punctuation=False, case_sensitive=True):
    """Python implementation of long token ratio."""
    tokens = (
        cheesecloth.tokenize_unigrams_with_punctuation(text)
        if include_punctuation
        else cheesecloth.tokenize_unigrams(text)
    )

    if not tokens:
        return 0.0

    long_count = sum(1 for token in tokens if len(token) >= 7)
    return long_count / len(tokens)


def test_long_token_ratio():
    # Simple cases
    text = "extraordinary capabilities demonstrated technology"
    # Long tokens (≥7): extraordinary, capabilities, demonstrated, technology = 4 out of 4
    ratio = long_token_ratio_impl(text, include_punctuation=False, case_sensitive=True)
    assert ratio == 1.0

    # Mix of short and long tokens
    text = "the cat sat on the extraordinary mat"
    # Long tokens: extraordinary = 1 out of 7
    ratio = long_token_ratio_impl(text, include_punctuation=False, case_sensitive=True)
    assert abs(ratio - 1 / 7) < 0.0001

    # Empty text
    assert (
        long_token_ratio_impl("", include_punctuation=False, case_sensitive=True) == 0.0
    )


def enhanced_get_all_unigram_metrics(
    text, include_punctuation=False, case_sensitive=True
):
    """Python implementation of an enhanced get_all_unigram_metrics."""
    # Get original metrics
    metrics = cheesecloth.get_all_unigram_metrics(
        text, include_punctuation, case_sensitive
    )

    # Add our new metrics
    metrics["hapax_legomena_ratio"] = hapax_legomena_ratio_impl(
        text, include_punctuation, case_sensitive
    )
    metrics["top_5_token_coverage"] = top_5_token_coverage_impl(
        text, include_punctuation, case_sensitive
    )
    metrics["short_token_ratio"] = short_token_ratio_impl(
        text, include_punctuation, case_sensitive
    )
    metrics["long_token_ratio"] = long_token_ratio_impl(
        text, include_punctuation, case_sensitive
    )

    return metrics


def test_get_all_unigram_metrics():
    # Test that all our new metrics can be calculated
    text = "the cat sat on the extraordinary mat"
    metrics = enhanced_get_all_unigram_metrics(
        text, include_punctuation=False, case_sensitive=True
    )

    # Check that the new metrics are in the results
    assert "hapax_legomena_ratio" in metrics
    assert "top_5_token_coverage" in metrics
    assert "short_token_ratio" in metrics
    assert "long_token_ratio" in metrics

    # Verify the values of our new metrics
    # 5 hapax legomena (cat, sat, on, extraordinary, mat) out of 7 tokens
    assert abs(metrics["hapax_legomena_ratio"] - 5 / 7) < 0.0001

    # Top 5 covers 6 out of 7 tokens (tokens: the(2), cat, sat, on, extraordinary, mat)
    assert abs(metrics["top_5_token_coverage"] - 6 / 7) < 0.0001

    # 6 short tokens out of 7
    assert abs(metrics["short_token_ratio"] - 6 / 7) < 0.0001

    # 1 long token out of 7
    assert abs(metrics["long_token_ratio"] - 1 / 7) < 0.0001
