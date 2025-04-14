import pytest
import cheesecloth


def test_is_uppercase():
    """Test the is_uppercase function"""
    assert cheesecloth.is_uppercase("A") is True
    assert cheesecloth.is_uppercase("Z") is True
    assert cheesecloth.is_uppercase("É") is True
    assert cheesecloth.is_uppercase("a") is False
    assert cheesecloth.is_uppercase("1") is False
    assert cheesecloth.is_uppercase(" ") is False


def test_is_lowercase():
    """Test the is_lowercase function"""
    assert cheesecloth.is_lowercase("a") is True
    assert cheesecloth.is_lowercase("z") is True
    assert cheesecloth.is_lowercase("é") is True
    assert cheesecloth.is_lowercase("A") is False
    assert cheesecloth.is_lowercase("1") is False
    assert cheesecloth.is_lowercase(" ") is False


def test_count_uppercase():
    """Test the count_uppercase function"""
    assert cheesecloth.count_uppercase("") == 0
    assert cheesecloth.count_uppercase("abc") == 0
    assert cheesecloth.count_uppercase("ABC") == 3
    assert cheesecloth.count_uppercase("AbC") == 2
    assert cheesecloth.count_uppercase("Hello, World!") == 2
    assert cheesecloth.count_uppercase("123") == 0
    assert cheesecloth.count_uppercase("CAFÉ") == 4  # Unicode uppercase


def test_count_lowercase():
    """Test the count_lowercase function"""
    assert cheesecloth.count_lowercase("") == 0
    assert cheesecloth.count_lowercase("abc") == 3
    assert cheesecloth.count_lowercase("ABC") == 0
    assert cheesecloth.count_lowercase("AbC") == 1
    assert cheesecloth.count_lowercase("Hello, World!") == 8
    assert cheesecloth.count_lowercase("123") == 0
    assert cheesecloth.count_lowercase("café") == 4  # Unicode lowercase


def test_ratio_uppercase():
    """Test the ratio_uppercase function"""
    assert cheesecloth.ratio_uppercase("") == 0.0
    assert cheesecloth.ratio_uppercase("abc") == 0.0
    assert cheesecloth.ratio_uppercase("ABC") == 1.0
    assert cheesecloth.ratio_uppercase("AbC") == 2 / 3
    assert pytest.approx(cheesecloth.ratio_uppercase("Hello"), 0.0001) == 0.2
    assert cheesecloth.ratio_uppercase("CAFÉ") == 1.0
    assert cheesecloth.ratio_uppercase("café") == 0.0
    assert cheesecloth.ratio_uppercase("123") == 0.0  # No letters
    assert cheesecloth.ratio_uppercase("123ABC") == 1.0  # All letters are uppercase


def test_combined_metrics_includes_case():
    """Test that combined_char_metrics includes uppercase and lowercase counts"""
    result = cheesecloth.combined_char_metrics("Hello, World! 123")

    assert "uppercase" in result
    assert "lowercase" in result
    assert result["uppercase"] == 2
    assert result["lowercase"] == 8
