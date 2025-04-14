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
    assert "," in freq
    assert "!" in freq
    assert "." in freq


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
