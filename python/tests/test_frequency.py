import cheesecloth


def test_get_char_frequency():
    text = "hello world"
    freq = cheesecloth.get_char_frequency(text)

    # Check character frequencies
    assert freq["h"] == 1
    assert freq["e"] == 1
    assert freq["l"] == 3
    assert freq["o"] == 2
    assert freq[" "] == 1
    assert freq["w"] == 1
    assert freq["r"] == 1
    assert freq["d"] == 1

    # Check total matches text length
    assert sum(freq.values()) == len(text)


def test_get_char_type_frequency():
    text = "hello, world! 123"
    freq = cheesecloth.get_char_type_frequency(text)

    # Check character type frequencies
    assert freq["letter"] == 10  # h,e,l,l,o,w,o,r,l,d
    assert freq["digit"] == 3  # 1,2,3
    assert freq["punctuation"] == 2  # comma, exclamation
    assert freq["whitespace"] == 2  # Two spaces
    assert freq["symbol"] == 0
    assert freq["other"] == 0

    # Check total matches text length
    assert sum(freq.values()) == len(text)


def test_get_unicode_category_frequency():
    text = "Hello, world! 123 ©"
    freq = cheesecloth.get_unicode_category_frequency(text)

    # Check Unicode category frequencies
    assert freq["Lu"] == 1  # H (uppercase letter)
    assert freq["Ll"] == 9  # e,l,l,o,w,o,r,l,d (lowercase letters)
    assert freq["Po"] == 2  # Comma, exclamation mark (punctuation)
    assert freq["Zs"] == 3  # Spaces (space separator) - corrected count
    assert freq["Nd"] == 3  # 1,2,3 (digits)
    assert freq["So"] == 1  # © (symbol)

    # Check total matches text length
    assert sum(freq.values()) == len(text)


def test_get_unicode_category_group_frequency():
    text = "Hello, world! 123 ©"
    freq = cheesecloth.get_unicode_category_group_frequency(text)

    # Check Unicode category group frequencies
    assert freq["L"] == 10  # All letters (H,e,l,l,o,w,o,r,l,d)
    assert freq["P"] == 2  # Punctuation (comma, exclamation mark)
    assert freq["Z"] == 3  # Spaces - corrected count
    assert freq["N"] == 3  # Numbers (1,2,3)
    assert freq["S"] == 1  # Symbols (©)

    # Check total matches text length
    assert sum(freq.values()) == len(text)


def test_empty_string():
    assert cheesecloth.get_char_frequency("") == {}
    assert cheesecloth.get_char_type_frequency("") == {
        "letter": 0,
        "digit": 0,
        "punctuation": 0,
        "symbol": 0,
        "whitespace": 0,
        "other": 0,
    }
    assert cheesecloth.get_unicode_category_frequency("") == {}
    assert cheesecloth.get_unicode_category_group_frequency("") == {}


def test_multilingual():
    text = "Hello 你好 नमस्ते!"

    # Character frequency
    char_freq = cheesecloth.get_char_frequency(text)
    assert len(char_freq) > 0
    assert char_freq["H"] == 1

    # Unicode category frequency
    cat_freq = cheesecloth.get_unicode_category_frequency(text)
    assert "Lu" in cat_freq  # Uppercase Latin
    assert "Lo" in cat_freq  # Other letters (Chinese, Devanagari)
    assert "Po" in cat_freq  # Punctuation
    assert "Zs" in cat_freq  # Spaces

    # Unicode category group frequency
    group_freq = cheesecloth.get_unicode_category_group_frequency(text)
    assert "L" in group_freq  # Letters
    assert "P" in group_freq  # Punctuation
    assert "Z" in group_freq  # Spaces

    # Check sum of frequencies equals text length
    assert sum(cat_freq.values()) == len(text)
    assert sum(group_freq.values()) == len(text)


def test_performance_large_text(benchmark):
    """Test performance on a larger text string"""
    # Create a larger text (100x "Hello, world! 123 ©")
    text = "Hello, world! 123 ©" * 100

    # Benchmark get_unicode_category_frequency
    result = benchmark(cheesecloth.get_unicode_category_frequency, text)

    # Basic validation of the result
    assert isinstance(result, dict)
    assert "Lu" in result
    assert "Ll" in result
    assert sum(result.values()) == len(text)
