import cheesecloth


def test_count_chars():
    assert cheesecloth.count_chars("hello") == 5
    assert cheesecloth.count_chars("") == 0
    assert cheesecloth.count_chars("hello world") == 11
    # Unicode characters count as one character each
    assert cheesecloth.count_chars("你好") == 2


def test_count_words():
    assert cheesecloth.count_words("hello") == 1
    assert cheesecloth.count_words("") == 0
    assert cheesecloth.count_words("hello world") == 2
    assert cheesecloth.count_words("hello  world") == 2
    assert cheesecloth.count_words("hello world!") == 2


def test_is_ascii():
    assert cheesecloth.is_ascii("hello") is True
    assert cheesecloth.is_ascii("") is True
    assert cheesecloth.is_ascii("hello world!") is True
    assert cheesecloth.is_ascii("hello 你好") is False


def test_ratio_ascii():
    assert cheesecloth.ratio_ascii("hello") == 1.0
    # Changed to return 0.0 for empty string for consistency with other ratio functions
    assert cheesecloth.ratio_ascii("") == 0.0
    # 7 ASCII characters out of 9 total
    assert 0.7 < cheesecloth.ratio_ascii("hello 你好") < 0.8


def test_count_letters():
    assert cheesecloth.count_letters("hello") == 5
    assert cheesecloth.count_letters("") == 0
    assert cheesecloth.count_letters("hello world") == 10
    assert cheesecloth.count_letters("hello123") == 5
    assert cheesecloth.count_letters("123") == 0
    # Unicode letters count correctly
    assert cheesecloth.count_letters("你好") == 2


def test_count_digits():
    assert cheesecloth.count_digits("hello") == 0
    assert cheesecloth.count_digits("") == 0
    assert cheesecloth.count_digits("123") == 3
    assert cheesecloth.count_digits("hello123") == 3
    # Unicode digits count correctly
    assert cheesecloth.count_digits("１２３") == 3


def test_count_punctuation():
    assert cheesecloth.count_punctuation("hello") == 0
    assert cheesecloth.count_punctuation("") == 0
    assert cheesecloth.count_punctuation("hello!") == 1
    assert cheesecloth.count_punctuation("hello, world!") == 2
    # Unicode punctuation counts correctly
    assert cheesecloth.count_punctuation("hello「world」") == 2


def test_count_symbols():
    assert cheesecloth.count_symbols("hello") == 0
    assert cheesecloth.count_symbols("") == 0
    assert cheesecloth.count_symbols("hello+world") == 1
    assert cheesecloth.count_symbols("$100 + €200") == 3  # $, +, and € are symbols
    # Unicode symbols count correctly
    assert cheesecloth.count_symbols("©®™") == 3


def test_count_whitespace():
    assert cheesecloth.count_whitespace("hello") == 0
    assert cheesecloth.count_whitespace("") == 0
    assert cheesecloth.count_whitespace("hello world") == 1
    assert cheesecloth.count_whitespace("hello  world") == 2
    assert cheesecloth.count_whitespace("hello\tworld\n") == 2


def test_count_non_ascii():
    assert cheesecloth.count_non_ascii("hello") == 0
    assert cheesecloth.count_non_ascii("") == 0
    assert cheesecloth.count_non_ascii("hello world!") == 0
    assert cheesecloth.count_non_ascii("hello 你好") == 2
    assert cheesecloth.count_non_ascii("你好") == 2
