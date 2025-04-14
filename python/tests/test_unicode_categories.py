import cheesecloth


def test_get_unicode_categories():
    text = "Hello!"
    categories = cheesecloth.get_unicode_categories(text)
    assert len(categories) == 6
    assert categories[0] == "Lu"  # Uppercase letter
    assert categories[1] == "Ll"  # Lowercase letter
    assert categories[5] == "Po"  # Other punctuation


def test_get_unicode_category_groups():
    text = "Hello!"
    groups = cheesecloth.get_unicode_category_groups(text)
    assert len(groups) == 6
    assert groups[0] == "L"  # Letter
    assert groups[1] == "L"  # Letter
    assert groups[5] == "P"  # Punctuation


def test_count_unicode_categories():
    text = "Hello, world!"
    counts = cheesecloth.count_unicode_categories(text)
    assert counts["Lu"] == 1  # 1 uppercase letter
    assert counts["Ll"] == 9  # 9 lowercase letters
    assert counts["Po"] == 2  # 2 punctuation marks
    assert counts["Zs"] == 1  # 1 space


def test_count_unicode_category_groups():
    text = "Hello, world!"
    counts = cheesecloth.count_unicode_category_groups(text)
    assert counts["L"] == 10  # 10 letters
    assert counts["P"] == 2  # 2 punctuation marks
    assert counts["Z"] == 1  # 1 separator (space)


def test_get_unicode_category_ratios():
    text = "Hello, world!"
    ratios = cheesecloth.get_unicode_category_ratios(text)
    assert abs(ratios["Lu"] - 1 / 13) < 1e-10
    assert abs(ratios["Ll"] - 9 / 13) < 1e-10
    assert abs(ratios["Po"] - 2 / 13) < 1e-10
    assert abs(ratios["Zs"] - 1 / 13) < 1e-10


def test_get_unicode_category_group_ratios():
    text = "Hello, world!"
    ratios = cheesecloth.get_unicode_category_group_ratios(text)
    assert abs(ratios["L"] - 10 / 13) < 1e-10
    assert abs(ratios["P"] - 2 / 13) < 1e-10
    assert abs(ratios["Z"] - 1 / 13) < 1e-10


def test_empty_string():
    assert cheesecloth.get_unicode_categories("") == []
    assert cheesecloth.get_unicode_category_groups("") == []
    assert cheesecloth.count_unicode_categories("") == {}
    assert cheesecloth.count_unicode_category_groups("") == {}
    assert cheesecloth.get_unicode_category_ratios("") == {}
    assert cheesecloth.get_unicode_category_group_ratios("") == {}


def test_special_characters():
    # Test string with various special characters
    text = "abc123!@#$%^&*()_+{}[]|\\:;\"'<>,.?/~`§±€£¥©®™"
    categories = cheesecloth.get_unicode_categories(text)
    groups = cheesecloth.get_unicode_category_groups(text)

    # Verify length
    assert len(categories) == len(text)
    assert len(groups) == len(text)

    # Check counts
    counts = cheesecloth.count_unicode_categories(text)
    assert counts["Ll"] == 3  # a, b, c
    assert counts["Nd"] == 3  # 1, 2, 3
    assert "Sc" in counts  # Currency symbols
    assert "Sm" in counts  # Math symbols

    # Check group counts
    group_counts = cheesecloth.count_unicode_category_groups(text)
    assert group_counts["L"] == 3  # Letters
    assert group_counts["N"] == 3  # Numbers
    assert group_counts["P"] > 0  # Punctuation
    assert group_counts["S"] > 0  # Symbols


def test_multilingual_text():
    text = "Hello 你好 नमस्ते!"
    categories = cheesecloth.get_unicode_categories(text)
    groups = cheesecloth.get_unicode_category_groups(text)

    # Verify length
    assert len(categories) == len(text)
    assert len(groups) == len(text)

    # Check counts
    counts = cheesecloth.count_unicode_categories(text)
    assert counts["Lu"] == 1  # 1 uppercase letter 'H'
    assert counts["Ll"] == 4  # 4 lowercase letters 'ello'
    assert counts["Lo"] >= 5  # Other letters (for Chinese and Devanagari)
    assert counts["Zs"] == 2  # Spaces
    assert counts["Po"] == 1  # Punctuation

    # Check group counts
    group_counts = cheesecloth.count_unicode_category_groups(text)
    assert group_counts["L"] >= 10  # All letters (Latin, Chinese, Devanagari)
    assert group_counts["Z"] == 2  # 2 spaces
    assert group_counts["P"] == 1  # 1 punctuation mark

    # Check category to group mapping
    for i, (cat, group) in enumerate(zip(categories, groups)):
        # Letters
        if cat in ["Lu", "Ll", "Lt", "Lm", "Lo"]:
            assert group == "L"
        # Punctuation
        elif cat in ["Pc", "Pd", "Ps", "Pe", "Pi", "Pf", "Po"]:
            assert group == "P"
        # Spaces
        elif cat in ["Zs", "Zl", "Zp"]:
            assert group == "Z"


def test_unicode_blocks():
    """Test different Unicode blocks"""
    # Basic Latin
    latin = "ABCabc123"
    latin_cats = cheesecloth.get_unicode_categories(latin)
    assert latin_cats[:3] == ["Lu", "Lu", "Lu"]  # Uppercase
    assert latin_cats[3:6] == ["Ll", "Ll", "Ll"]  # Lowercase
    assert latin_cats[6:9] == ["Nd", "Nd", "Nd"]  # Digits

    # Cyrillic
    cyrillic = "Привет"
    cyrillic_cats = cheesecloth.get_unicode_categories(cyrillic)
    assert cyrillic_cats[0] == "Lu"  # П - Uppercase
    assert all(cat == "Ll" for cat in cyrillic_cats[1:])  # ривет - Lowercase

    # Arabic
    arabic = "مرحبا"
    arabic_cats = cheesecloth.get_unicode_categories(arabic)
    assert all(cat == "Lo" for cat in arabic_cats)  # Other letters

    # Emoji
    emoji = "😀🌍🚀"
    emoji_cats = cheesecloth.get_unicode_categories(emoji)
    assert all(cat == "So" for cat in emoji_cats)  # Other symbols


def test_combined_characters():
    """Test combined Unicode characters like accented letters"""
    # Decomposed form
    text1 = "e\u0301"  # e + combining acute accent
    categories1 = cheesecloth.get_unicode_categories(text1)
    assert len(categories1) == 2
    assert categories1[0] == "Ll"  # Lowercase letter
    assert categories1[1] == "Mn"  # Non-spacing mark

    # Precomposed form
    text2 = "\u00e9"  # é (Latin small letter e with acute)
    categories2 = cheesecloth.get_unicode_categories(text2)
    assert len(categories2) == 1
    assert categories2[0] == "Ll"  # Still a lowercase letter


def test_category_ratio_sums():
    """Test that category ratios sum to 1.0"""
    texts = [
        "Simple ASCII text",
        "Multilingual: 你好, नमस्ते, Привет!",
        "Special chars: ©®™€£¥$¢±§",
        "Mixed: abc123!@#$%^&*()",
    ]

    for text in texts:
        # Category ratios
        ratios = cheesecloth.get_unicode_category_ratios(text)
        total = sum(ratios.values())
        assert abs(total - 1.0) < 1e-10

        # Category group ratios
        group_ratios = cheesecloth.get_unicode_category_group_ratios(text)
        group_total = sum(group_ratios.values())
        assert abs(group_total - 1.0) < 1e-10
