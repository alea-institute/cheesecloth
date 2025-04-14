import cheesecloth


def test_split_words():
    """Test the split_words function with various inputs."""
    assert cheesecloth.split_words("Hello world") == ["Hello", "world"]
    assert cheesecloth.split_words("") == []
    assert cheesecloth.split_words(
        'The quick ("brown") fox can\'t jump 32.3 feet, right?'
    ) == ["The", "quick", "brown", "fox", "can't", "jump", "32.3", "feet", "right"]
    # Unicode words (the segmenter will treat each character as a word)
    unicode_words = cheesecloth.split_words("こんにちは世界")
    assert len(unicode_words) > 0


def test_split_lines():
    """Test the split_lines function with various line ending styles."""
    # Test different line endings
    assert cheesecloth.split_lines("Line 1\nLine 2\r\nLine 3") == [
        "Line 1",
        "Line 2",
        "Line 3",
    ]
    assert cheesecloth.split_lines("") == []
    assert cheesecloth.split_lines("Single line") == ["Single line"]

    # Test empty lines
    assert cheesecloth.split_lines("Line 1\n\nLine 3") == ["Line 1", "", "Line 3"]


def test_count_lines():
    """Test the count_lines function."""
    assert cheesecloth.count_lines("Line 1\nLine 2\r\nLine 3") == 3
    assert cheesecloth.count_lines("") == 0
    assert cheesecloth.count_lines("Single line") == 1
    assert cheesecloth.count_lines("Line 1\n\nLine 3") == 3


def test_average_line_length():
    """Test the average_line_length function."""
    assert cheesecloth.average_line_length("123\n12345\n1") == 3.0
    assert cheesecloth.average_line_length("") == 0.0
    assert cheesecloth.average_line_length("12345") == 5.0

    # Test with multi-byte Unicode characters
    assert cheesecloth.average_line_length("αβγ\nαβγδε") == 4.0


def test_split_paragraphs():
    """Test the split_paragraphs function."""
    text = "Paragraph 1.\n\nParagraph 2.\n\r\nParagraph 3."
    assert cheesecloth.split_paragraphs(text) == [
        "Paragraph 1.",
        "Paragraph 2.",
        "Paragraph 3.",
    ]

    # Test with indentation and extra whitespace
    text_with_spaces = "   Paragraph 1.   \n\n   Paragraph 2.   "
    assert cheesecloth.split_paragraphs(text_with_spaces) == [
        "Paragraph 1.",
        "Paragraph 2.",
    ]

    # Test empty text
    assert cheesecloth.split_paragraphs("") == []

    # Test single paragraph
    assert cheesecloth.split_paragraphs("Just one paragraph.") == [
        "Just one paragraph."
    ]


def test_count_paragraphs():
    """Test the count_paragraphs function."""
    text = "Paragraph 1.\n\nParagraph 2.\n\r\nParagraph 3."
    assert cheesecloth.count_paragraphs(text) == 3

    assert cheesecloth.count_paragraphs("") == 0
    assert cheesecloth.count_paragraphs("Just one paragraph.") == 1


def test_average_paragraph_length():
    """Test the average_paragraph_length function."""
    text = "123.\n\n12345.\n\n1."
    # Each paragraph includes the period, so lengths are 4, 6, and 2 (avg = 4.0)
    assert cheesecloth.average_paragraph_length(text) == 4.0

    assert cheesecloth.average_paragraph_length("") == 0.0
    assert cheesecloth.average_paragraph_length("12345") == 5.0

    # Test with multi-byte Unicode characters
    text_unicode = "αβγ.\n\nαβγδε."
    assert cheesecloth.average_paragraph_length(text_unicode) == 5.0


def test_average_word_length():
    """Test the average_word_length function."""
    text = "The quick brown fox"
    # Unicode segmentation might treat words slightly differently
    # Let's check what it actually returns
    words = cheesecloth.split_words(text)
    expected_avg = sum(len(word) for word in words) / len(words)
    assert cheesecloth.average_word_length(text) == expected_avg

    assert cheesecloth.average_word_length("") == 0.0
    # Test simple words with varying lengths
    simple_text = "a bb ccc dddd"
    simple_words = cheesecloth.split_words(simple_text)
    simple_expected_avg = sum(len(word) for word in simple_words) / len(simple_words)
    assert cheesecloth.average_word_length(simple_text) == simple_expected_avg

    # Test with Unicode characters
    unicode_text = "αβ γδε"
    unicode_words = cheesecloth.split_words(unicode_text)
    unicode_expected_avg = sum(len(word) for word in unicode_words) / len(unicode_words)
    assert cheesecloth.average_word_length(unicode_text) == unicode_expected_avg

    # Test with punctuation
    text_with_punctuation = "Hello, world!"
    # Unicode segmentation strips punctuation, so only "Hello" and "world" count
    punct_words = cheesecloth.split_words(text_with_punctuation)
    punct_expected_avg = sum(len(word) for word in punct_words) / len(punct_words)
    assert cheesecloth.average_word_length(text_with_punctuation) == punct_expected_avg


def test_average_sentence_length():
    """Test the average_sentence_length function."""
    text = "This is sentence one. This is the second sentence! Is this the third?"

    # The expected average should be approximately 4 words per sentence
    avg = cheesecloth.average_sentence_length(text)
    assert 3.0 <= avg <= 5.0

    assert cheesecloth.average_sentence_length("") == 0.0
    assert (
        cheesecloth.average_sentence_length("Single sentence with five words.") == 5.0
    )
