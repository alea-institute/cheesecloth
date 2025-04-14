import cheesecloth


def test_get_unicode_category_bigrams():
    """Test basic functionality of Unicode category bigrams."""
    text = "Hi!"
    bigrams = cheesecloth.get_unicode_category_bigrams(text)

    # Expected transitions for "Hi!"
    # We expect (None,Lu), (Lu,Ll), (Ll,Po), (Po,None)
    assert len(bigrams) == 4
    assert bigrams.get(("START", "Lu")) == 1  # Start → H
    assert bigrams.get(("Lu", "Ll")) == 1  # H → i
    assert bigrams.get(("Ll", "Po")) == 1  # i → !
    assert bigrams.get(("Po", "END")) == 1  # ! → End


def test_get_unicode_category_bigram_ratios():
    """Test ratio calculations for Unicode category bigrams."""
    text = "Hi!"
    ratios = cheesecloth.get_unicode_category_bigram_ratios(text)

    # Each bigram should have ratio of 1/4 of the total bigrams
    assert len(ratios) == 4
    assert abs(ratios.get(("START", "Lu")) - 0.25) < 1e-10
    assert abs(ratios.get(("Lu", "Ll")) - 0.25) < 1e-10
    assert abs(ratios.get(("Ll", "Po")) - 0.25) < 1e-10
    assert abs(ratios.get(("Po", "END")) - 0.25) < 1e-10


def test_get_unicode_category_group_bigrams():
    """Test basic functionality of Unicode category group bigrams."""
    text = "Hi!"
    bigrams = cheesecloth.get_unicode_category_group_bigrams(text)

    # Expected transitions for "Hi!" at group level
    # We expect (None,L), (L,L), (L,P), (P,None)
    assert len(bigrams) == 4
    assert bigrams.get(("START", "L")) == 1  # Start → H
    assert bigrams.get(("L", "L")) == 1  # H → i
    assert bigrams.get(("L", "P")) == 1  # i → !
    assert bigrams.get(("P", "END")) == 1  # ! → End


def test_get_unicode_category_group_bigram_ratios():
    """Test ratio calculations for Unicode category group bigrams."""
    text = "Hi!"
    ratios = cheesecloth.get_unicode_category_group_bigram_ratios(text)

    # Each bigram should have ratio of 1/4 of the total bigrams
    assert len(ratios) == 4
    assert abs(ratios.get(("START", "L")) - 0.25) < 1e-10
    assert abs(ratios.get(("L", "L")) - 0.25) < 1e-10
    assert abs(ratios.get(("L", "P")) - 0.25) < 1e-10
    assert abs(ratios.get(("P", "END")) - 0.25) < 1e-10


def test_bigrams_with_longer_text():
    """Test with a longer text that has repeating patterns."""
    text = "Hello, world!"

    # Get category bigrams
    bigrams = cheesecloth.get_unicode_category_bigrams(text)

    # Check some key transitions
    assert bigrams.get(("START", "Lu")) == 1  # Start → H
    assert bigrams.get(("Lu", "Ll")) == 1  # H → e
    assert bigrams.get(("Ll", "Ll")) >= 5  # Multiple lowercase to lowercase transitions
    assert bigrams.get(("Ll", "Po")) >= 1  # Lowercase to punctuation (e.g., o → ,)
    assert bigrams.get(("Po", "Zs")) == 1  # Punctuation to space (e.g., , → space)
    assert bigrams.get(("Po", "END")) == 1  # Punctuation to end (e.g., ! → end)

    # Get group bigrams
    group_bigrams = cheesecloth.get_unicode_category_group_bigrams(text)

    # Check key group transitions
    assert group_bigrams.get(("START", "L")) == 1  # Start → letter
    assert group_bigrams.get(("L", "L")) >= 6  # Letter to letter
    assert group_bigrams.get(("L", "P")) >= 1  # Letter to punctuation
    assert group_bigrams.get(("P", "Z")) == 1  # Punctuation to space
    assert group_bigrams.get(("Z", "L")) == 1  # Space to letter
    assert group_bigrams.get(("P", "END")) == 1  # Punctuation to end


def test_empty_string():
    """Test behavior with empty string."""
    text = ""

    # All results should be empty dictionaries
    assert cheesecloth.get_unicode_category_bigrams(text) == {}
    assert cheesecloth.get_unicode_category_bigram_ratios(text) == {}
    assert cheesecloth.get_unicode_category_group_bigrams(text) == {}
    assert cheesecloth.get_unicode_category_group_bigram_ratios(text) == {}


def test_single_character():
    """Test behavior with a single character."""
    text = "A"

    # For a single character, we expect 2 bigrams: (None, Lu) and (Lu, None)
    cat_bigrams = cheesecloth.get_unicode_category_bigrams(text)
    assert len(cat_bigrams) == 2
    assert cat_bigrams.get(("START", "Lu")) == 1  # Start → A
    assert cat_bigrams.get(("Lu", "END")) == 1  # A → End

    # Same for group bigrams
    group_bigrams = cheesecloth.get_unicode_category_group_bigrams(text)
    assert len(group_bigrams) == 2
    assert group_bigrams.get(("START", "L")) == 1  # Start → A
    assert group_bigrams.get(("L", "END")) == 1  # A → End


def test_multilingual_text():
    """Test behavior with multilingual text."""
    text = "Hello你好!"

    # Get category bigrams
    bigrams = cheesecloth.get_unicode_category_bigrams(text)

    # Unicode category bigrams should handle different scripts correctly
    assert bigrams.get(("START", "Lu")) == 1  # Start → H
    assert bigrams.get(("Lu", "Ll")) == 1  # H → e
    assert bigrams.get(("Ll", "Lo")) == 1  # o → Chinese character
    assert bigrams.get(("Lo", "Lo")) == 1  # Chinese character → Chinese character
    assert bigrams.get(("Lo", "Po")) == 1  # Chinese character → !
    assert bigrams.get(("Po", "END")) == 1  # ! → End

    # Group bigrams should be more generalized
    group_bigrams = cheesecloth.get_unicode_category_group_bigrams(text)
    assert group_bigrams.get(("START", "L")) == 1  # Start → letter
    assert group_bigrams.get(("L", "L")) >= 5  # Letter to letter (multiple times)
    assert group_bigrams.get(("L", "P")) == 1  # Letter to punctuation
    assert group_bigrams.get(("P", "END")) == 1  # Punctuation to end


def test_bigram_ratio_sums():
    """Test that bigram ratios sum to 1.0."""
    texts = ["Hello!", "ABC123", "Hello, world!", "Mixed: 你好, नमस्ते!"]

    for text in texts:
        # Category bigram ratios
        ratios = cheesecloth.get_unicode_category_bigram_ratios(text)
        total = sum(ratios.values())
        assert abs(total - 1.0) < 1e-10

        # Category group bigram ratios
        group_ratios = cheesecloth.get_unicode_category_group_bigram_ratios(text)
        group_total = sum(group_ratios.values())
        assert abs(group_total - 1.0) < 1e-10


def test_numeric_transitions():
    """Test transitions involving numeric characters."""
    text = "A1B2C3"

    # Category bigrams
    bigrams = cheesecloth.get_unicode_category_bigrams(text)
    assert bigrams.get(("Lu", "Nd")) == 3  # A→1, B→2, C→3
    assert bigrams.get(("Nd", "Lu")) == 2  # 1→B, 2→C

    # Group bigrams
    group_bigrams = cheesecloth.get_unicode_category_group_bigrams(text)
    assert group_bigrams.get(("L", "N")) == 3  # Letter→Number
    assert group_bigrams.get(("N", "L")) == 2  # Number→Letter


def test_punctuation_transitions():
    """Test transitions involving punctuation characters."""
    text = "Hello, world! Test."

    # Category bigrams
    bigrams = cheesecloth.get_unicode_category_bigrams(text)
    assert bigrams.get(("Ll", "Po")) >= 2  # o→, d→!
    assert bigrams.get(("Po", "Zs")) >= 1  # ,→space

    # Note: There's no direct !→T transition in our implementation,
    # as there's a space between ! and T, so it's !→space→T
    assert bigrams.get(("Po", "Zs")) >= 1  # !→space
    assert bigrams.get(("Zs", "Lu")) >= 1  # space→T

    # Group bigrams
    group_bigrams = cheesecloth.get_unicode_category_group_bigrams(text)
    assert group_bigrams.get(("L", "P")) >= 2  # Letter→Punctuation
    assert group_bigrams.get(("P", "Z")) >= 1  # Punctuation→Space
    assert group_bigrams.get(("Z", "L")) >= 1  # Space→Letter
