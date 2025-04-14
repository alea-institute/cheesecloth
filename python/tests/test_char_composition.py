import pytest
import cheesecloth


def test_is_alphanumeric():
    """Test the is_alphanumeric function"""
    assert cheesecloth.is_alphanumeric("a") is True
    assert cheesecloth.is_alphanumeric("Z") is True
    assert cheesecloth.is_alphanumeric("0") is True
    assert cheesecloth.is_alphanumeric("9") is True
    assert cheesecloth.is_alphanumeric("!") is False
    assert cheesecloth.is_alphanumeric(" ") is False
    assert cheesecloth.is_alphanumeric(".") is False


def test_count_alphanumeric():
    """Test the count_alphanumeric function"""
    assert cheesecloth.count_alphanumeric("abc123") == 6
    assert cheesecloth.count_alphanumeric("abc 123") == 6
    assert cheesecloth.count_alphanumeric("!@#") == 0
    assert cheesecloth.count_alphanumeric("") == 0
    assert cheesecloth.count_alphanumeric("Hello, World! 123") == 13


def test_ratio_alphanumeric():
    """Test the ratio_alphanumeric function"""
    assert cheesecloth.ratio_alphanumeric("abc123") == 1.0
    assert pytest.approx(cheesecloth.ratio_alphanumeric("abc 123"), 0.0001) == 6.0 / 7.0
    assert cheesecloth.ratio_alphanumeric("!@#") == 0.0
    assert cheesecloth.ratio_alphanumeric("") == 0.0
    text = "Hello, World! 123"
    # Count actual number of characters (commas and spaces count too)
    total_chars = len(text)
    alphanumeric_chars = 13
    assert (
        pytest.approx(cheesecloth.ratio_alphanumeric(text), 0.0001)
        == alphanumeric_chars / total_chars
    )


def test_ratio_alpha_to_numeric():
    """Test the ratio_alpha_to_numeric function"""
    assert cheesecloth.ratio_alpha_to_numeric("abc123") == 1.0
    assert cheesecloth.ratio_alpha_to_numeric("abcde12") == 2.5
    assert cheesecloth.ratio_alpha_to_numeric("12345") == 0.0
    # Changed from infinity to large number (1e6 * letters)
    # This is more consistent with other metrics
    all_letters_value = cheesecloth.ratio_alpha_to_numeric("abcde")
    assert all_letters_value == 1e6 * 5.0  # 5 million (5 letters * 1e6)
    assert cheesecloth.ratio_alpha_to_numeric("") == 0.0
    assert cheesecloth.ratio_alpha_to_numeric("Hello, World! 123") == 10.0 / 3.0


def test_char_entropy():
    """Test the char_entropy function"""
    # For a string with all the same character, entropy = 0
    assert cheesecloth.char_entropy("aaaaa") == 0.0

    # For a string with perfect distribution (all characters equally likely),
    # entropy = log2(n) where n is the number of unique characters
    assert pytest.approx(cheesecloth.char_entropy("abcd"), 0.0001) == 2.0  # log2(4) = 2

    # Empty string
    assert cheesecloth.char_entropy("") == 0.0

    # String with varied distribution
    entropy = cheesecloth.char_entropy("Hello, World!")
    assert entropy > 0.0

    # Longer text should have higher entropy than repetitive text
    varied_text = "The quick brown fox jumps over the lazy dog."
    repetitive_text = "aaa bbb ccc ddd eee"
    assert cheesecloth.char_entropy(varied_text) > cheesecloth.char_entropy(
        repetitive_text
    )


def test_combined_char_metrics_includes_alphanumeric():
    """Test that combined_char_metrics includes alphanumeric count"""
    result = cheesecloth.combined_char_metrics("Hello, World! 123")

    assert "alphanumeric" in result
    assert result["alphanumeric"] == 13
    assert result["letters"] == 10
    assert result["digits"] == 3
