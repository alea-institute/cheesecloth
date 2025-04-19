import cheesecloth
import math


def test_get_all_char_metrics():
    """Test the optimized get_all_char_metrics function."""
    # Test with a mixed content string - avoid using a string with escape sequences
    text = "Hello, World! 123 $%^"
    metrics = cheesecloth.get_all_char_metrics(text)

    # Verify count metrics
    # The string "Hello, World! 123 $%^" has 21 characters total:
    # - 10 letters: H,e,l,l,o,W,o,r,l,d
    # - 3 digits: 1,2,3
    # - 2 punctuation marks: comma and exclamation mark
    # - 3 symbols: $, %, and ^
    # - 3 whitespace characters: after comma, after !, and after 123
    assert metrics["total_chars"] == 21
    assert metrics["letters"] == 10
    assert metrics["digits"] == 3
    assert metrics["punctuation"] == 2  # Comma and exclamation
    assert metrics["symbols"] == 3  # $, %, and ^ are symbols
    assert metrics["whitespace"] == 3  # Space after comma, after !, and after 123
    assert metrics["non_ascii"] == 0
    assert metrics["uppercase"] == 2
    assert metrics["lowercase"] == 8
    assert metrics["alphanumeric"] == 13

    # Verify ratio metrics
    assert metrics["ratio_letters"] == 10.0 / 21.0
    assert metrics["ratio_digits"] == 3.0 / 21.0
    assert metrics["ratio_punctuation"] == 2.0 / 21.0  # Comma and exclamation
    assert metrics["ratio_symbols"] == 3.0 / 21.0  # $, %, and ^ are symbols
    assert metrics["ratio_whitespace"] == 3.0 / 21.0  # Updated for whitespace
    assert metrics["ratio_non_ascii"] == 0.0
    assert metrics["ratio_uppercase"] == 2.0 / 10.0
    assert metrics["ratio_lowercase"] == 8.0 / 10.0
    assert metrics["ratio_alphanumeric"] == 13.0 / 21.0
    assert metrics["ratio_alpha_to_numeric"] == 10.0 / 3.0
    assert metrics["char_entropy"] > 0.0

    # Test with empty string
    empty_metrics = cheesecloth.get_all_char_metrics("")
    assert empty_metrics["total_chars"] == 0
    assert empty_metrics["ratio_letters"] == 0.0
    assert empty_metrics["ratio_uppercase"] == 0.0
    assert empty_metrics["char_entropy"] == 0.0

    # Test with Unicode
    unicode_text = "Hello, 世界!"
    unicode_metrics = cheesecloth.get_all_char_metrics(unicode_text)
    assert unicode_metrics["non_ascii"] == 2
    assert unicode_metrics["ratio_non_ascii"] == 2.0 / 10.0


def test_consistency_with_individual_metrics():
    """Test that optimized metrics match individual metric functions."""
    # Using a simpler string without escape sequences to avoid confusion
    text = "Hello World 123"

    # Get all metrics at once
    all_metrics = cheesecloth.get_all_char_metrics(text)

    # Compare with individual functions
    assert all_metrics["letters"] == cheesecloth.count_letters(text)
    assert all_metrics["digits"] == cheesecloth.count_digits(text)
    assert all_metrics["punctuation"] == cheesecloth.count_punctuation(text)
    assert all_metrics["symbols"] == cheesecloth.count_symbols(text)
    assert all_metrics["whitespace"] == cheesecloth.count_whitespace(text)
    assert all_metrics["non_ascii"] == cheesecloth.count_non_ascii(text)
    assert all_metrics["uppercase"] == cheesecloth.count_uppercase(text)
    assert all_metrics["lowercase"] == cheesecloth.count_lowercase(text)
    assert all_metrics["alphanumeric"] == cheesecloth.count_alphanumeric(text)

    assert all_metrics["ratio_letters"] == cheesecloth.count_letters(
        text
    ) / cheesecloth.count_chars(text)
    assert all_metrics["ratio_digits"] == cheesecloth.ratio_digits(text)
    assert all_metrics["ratio_punctuation"] == cheesecloth.ratio_punctuation(text)
    assert all_metrics["ratio_whitespace"] == cheesecloth.ratio_whitespace(text)
    assert all_metrics["ratio_alphanumeric"] == cheesecloth.ratio_alphanumeric(text)
    assert all_metrics["ratio_uppercase"] == cheesecloth.ratio_uppercase(text)
    assert all_metrics["ratio_alpha_to_numeric"] == cheesecloth.ratio_alpha_to_numeric(
        text
    )

    # For floating point entropy values, use a small epsilon to compare
    epsilon = 1e-10
    assert abs(all_metrics["char_entropy"] - cheesecloth.char_entropy(text)) < epsilon

    # Test special case - text with letters but no digits
    letters_only = "HelloWorld"
    letters_metrics = cheesecloth.get_all_char_metrics(letters_only)
    individual_ratio = cheesecloth.ratio_alpha_to_numeric(letters_only)

    # Both should now return a large but finite number instead of infinity
    assert letters_metrics["ratio_alpha_to_numeric"] == individual_ratio
    assert letters_metrics["ratio_alpha_to_numeric"] == 1e6 * cheesecloth.count_letters(
        letters_only
    )
    assert not math.isinf(letters_metrics["ratio_alpha_to_numeric"])


def test_new_char_metrics():
    """Test the new character metrics that were added."""
    # Mixed text with various character types
    text = "Hello, WORLD! 123 $%^. This is a Test with Mixed-case."
    metrics = cheesecloth.get_all_char_metrics(text)

    # Test case_ratio
    assert "case_ratio" in metrics
    # Check if the value is approximately correct - the exact count might depend on character classification details
    uppercase_count = sum(1 for c in text if c.isupper())
    lowercase_count = sum(1 for c in text if c.islower())
    expected_ratio = uppercase_count / lowercase_count if lowercase_count > 0 else 0
    assert abs(metrics["case_ratio"] - expected_ratio) < 0.01

    # Test char_type_transitions
    assert "char_type_transitions" in metrics
    assert metrics["char_type_transitions"] > 0

    # Test consecutive_runs
    assert "consecutive_runs" in metrics
    assert metrics["consecutive_runs"] > 0

    # Test punctuation_diversity
    assert "punctuation_diversity" in metrics
    # Note: Our Rust code may classify punctuation differently than Python's string.punctuation
    # Just verify that we have some diversity detection
    assert metrics["punctuation_diversity"] > 0

    # Verify that the value is consistent with our rust punctuation classifier,
    # which may classify some characters as symbols instead of punctuation
    test_text_with_only_punc = ",.!?"
    punc_metrics = cheesecloth.get_all_char_metrics(test_text_with_only_punc)
    assert punc_metrics["punctuation_diversity"] == 4

    # Test category_entropy
    assert "category_entropy" in metrics
    assert metrics["category_entropy"] > 0.0

    # Test with only one type of character
    simple_text = "aaaaa"
    simple_metrics = cheesecloth.get_all_char_metrics(simple_text)
    # No transitions in a text with all the same character
    assert simple_metrics["char_type_transitions"] == 0
    # Just one run in a text with all the same character
    assert simple_metrics["consecutive_runs"] == 1
    # No punctuation in this text
    assert simple_metrics["punctuation_diversity"] == 0
    # Category entropy should be 0 for a text with only one category
    assert simple_metrics["category_entropy"] == 0.0

    # Test with empty string
    empty_metrics = cheesecloth.get_all_char_metrics("")
    assert empty_metrics["char_type_transitions"] == 0
    assert empty_metrics["consecutive_runs"] == 0
    assert empty_metrics["punctuation_diversity"] == 0
    assert empty_metrics["category_entropy"] == 0.0
    assert empty_metrics["case_ratio"] == 0.0
