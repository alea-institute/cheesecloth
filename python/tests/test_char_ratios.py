import cheesecloth


def test_ratio_whitespace():
    """Test the ratio_whitespace function"""
    assert cheesecloth.ratio_whitespace("abc") == 0.0
    assert cheesecloth.ratio_whitespace("a b c") == 2.0 / 5.0
    assert cheesecloth.ratio_whitespace("   ") == 1.0
    assert cheesecloth.ratio_whitespace("") == 0.0

    # Test with multiple types of whitespace
    text = "a\tb\nc\rd"
    # 3 whitespace chars out of 7 total
    assert cheesecloth.ratio_whitespace(text) == 3.0 / 7.0


def test_ratio_digits():
    """Test the ratio_digits function"""
    assert cheesecloth.ratio_digits("abc") == 0.0
    assert cheesecloth.ratio_digits("a1b2c3") == 3.0 / 6.0
    assert cheesecloth.ratio_digits("123") == 1.0
    assert cheesecloth.ratio_digits("") == 0.0

    # Test with unicode digits
    text = "a1b２c３"  # Contains ASCII and full-width digits
    assert cheesecloth.ratio_digits(text) == 3.0 / 6.0


def test_ratio_punctuation():
    """Test the ratio_punctuation function"""
    assert cheesecloth.ratio_punctuation("abc") == 0.0
    assert cheesecloth.ratio_punctuation("a,b.c!") == 3.0 / 6.0
    assert cheesecloth.ratio_punctuation(",.;:") == 1.0
    assert cheesecloth.ratio_punctuation("") == 0.0

    # Test with unicode punctuation
    text = "a,b。c！"  # Contains ASCII and CJK punctuation
    assert cheesecloth.ratio_punctuation(text) == 3.0 / 6.0
