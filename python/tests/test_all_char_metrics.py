import cheesecloth
import math


def test_get_all_char_metrics():
    """Test the optimized get_all_char_metrics function."""
    # Test with a mixed content string - avoid using a string with escape sequences
    text = "Hello, World! 123 $%^"
    metrics = cheesecloth.get_all_char_metrics(text)

    # Verify count metrics
    assert (
        metrics["total_chars"] == 21
    )  # Updated from 20 to 21 to account for escaped character
    assert metrics["letters"] == 10
    assert metrics["digits"] == 3
    assert metrics["punctuation"] == 2  # Comma and exclamation
    assert metrics["symbols"] == 3  # $, %, and ^ are symbols
    assert metrics["whitespace"] == 3  # Updated to match 3 whitespace characters
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
