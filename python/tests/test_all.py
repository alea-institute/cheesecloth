import cheesecloth


# Placeholder for general integration tests
def test_module_imports():
    assert cheesecloth is not None


def test_integration_char_and_unigram():
    """Test that character metrics and unigram tokenization work together."""
    text = "Hello, world! This is a test."

    # Get character metrics
    char_count = cheesecloth.count_chars(text)

    # Get unigram metrics
    tokens = cheesecloth.tokenize_unigrams(text)
    tokens_with_punct = cheesecloth.tokenize_unigrams_with_punctuation(text)

    # Verify basic relationships
    assert char_count > 0
    assert len(tokens) > 0
    assert len(tokens_with_punct) > len(tokens)

    # Verify that character counts match token characters
    total_token_chars = sum(len(token) for token in tokens)
    assert (
        total_token_chars < char_count
    )  # Should be less because of spaces and punctuation

    # Test entropy and frequency distributions
    char_freq = cheesecloth.get_char_frequency(text)
    token_freq = cheesecloth.get_unigram_frequency(
        text, include_punctuation=False, case_sensitive=True
    )

    assert len(char_freq) > 0
    assert len(token_freq) > 0
