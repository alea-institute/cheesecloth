"""Tests for the Rust line-structure metrics against the Python reference."""

import random
import sys

import pytest

import cheesecloth

END_P = (".", "!", "?", ":", ";", '"', "”")
NUMERIC_EXTRA = "$%.,()-/:"
KEYS = (
    "short_line_share",
    "end_punct_share",
    "dup_line_share",
    "numeric_line_share",
    "longest_line",
    "n_lines",
)


def reference(t):
    """Python reference semantics for the line-structure metrics."""
    ls = [line.strip() for line in t.split("\n")]
    ne = [line for line in ls if line]
    n = max(1, len(ne))
    counts = {}
    for line in ne:
        counts[line] = counts.get(line, 0) + 1

    def is_numeric(line):
        chars = [c for c in line if not c.isspace()]
        num = sum(1 for c in chars if c.isdigit() or c in NUMERIC_EXTRA)
        return num / len(chars) > 0.5

    return {
        "short_line_share": sum(1 for line in ne if len(line.split()) < 5) / n,
        "end_punct_share": sum(1 for line in ne if line.endswith(END_P)) / n,
        "dup_line_share": sum(c - 1 for c in counts.values() if c > 1) / n,
        "numeric_line_share": sum(1 for line in ne if is_numeric(line)) / n,
        "longest_line": max((len(line) for line in ne), default=0),
        "n_lines": len(ne),
    }


# Every character for which str.isspace() is true (stable across Python 3.10-3.14)
PY_WHITESPACE = [chr(c) for c in range(0x3001) if chr(c).isspace()]

ALPHABET = (
    list("abcXYZ0123456789$%.,()-/:!?;\"'#*")
    + ["”", "“", "é", "中", "½", "²", "①", "٣"]
    + ["\U0001f642", "​", "\x00", "\x0b"]
    + PY_WHITESPACE
    + ["\n"] * 6
)


def random_texts(count, seed):
    rnd = random.Random(seed)
    words = ["the", "court", "$1,000", "12.5%", "(a)", "Section", "§", "2024:", "end."]
    texts = []
    for i in range(count):
        if i % 2:
            n = rnd.choice([0, 1, 2, 5, 20, 100, 400])
            texts.append("".join(rnd.choice(ALPHABET) for _ in range(n)))
        else:
            lines = []
            for _ in range(rnd.randint(0, 25)):
                line = " ".join(rnd.choice(words) for _ in range(rnd.randint(0, 8)))
                line = (
                    rnd.choice(["", " ", "\t", "　"])
                    + line
                    + rnd.choice(["", ".", "\r", " ”", ";  "])
                )
                lines.append(line)
                if rnd.random() < 0.2 and lines:
                    lines.append(rnd.choice(lines))
            texts.append("\n".join(lines))
    return texts


EDGE_CASES = [
    "",
    "\n",
    "\n\n\n",
    "   \n\t\r\n",
    "one",
    "one two three four five",
    "one two three four",
    "Title\nThis is a much longer line of text.\n  Title  \n$1,000.00 (5%)\n",
    "a\r\nb\r\n",
    "12ab",
    "123a",
    "1 2 a b",
    "²²a",
    "½½a",
    "x\u001cy\u001dz\u001e\u001f",
    "\u001fword\u001f",
    "line still same line\u0085\nnext",
    '"quoted"\nsmart “quoted”\nnot quoted“',
    "dup\ndup\ndup\nunique",
    "\U0001f642\U0001f642\U0001f642",
]


@pytest.mark.parametrize("text", EDGE_CASES)
def test_edge_cases_match_reference(text):
    assert cheesecloth.get_line_structure_metrics(text) == reference(text)


def test_random_texts_match_reference():
    for text in random_texts(600, seed=7):
        assert cheesecloth.get_line_structure_metrics(text) == reference(text), repr(
            text
        )


def test_return_keys_and_types():
    result = cheesecloth.get_line_structure_metrics("a b c\nd e f g h i\n")
    assert tuple(result) == KEYS
    assert isinstance(result["longest_line"], int)
    assert isinstance(result["n_lines"], int)
    for key in KEYS[:4]:
        assert isinstance(result[key], float)


def test_individual_functions_match_combined():
    for text in EDGE_CASES + random_texts(50, seed=11):
        combined = cheesecloth.get_line_structure_metrics(text)
        assert cheesecloth.short_line_share(text) == combined["short_line_share"]
        assert cheesecloth.end_punct_share(text) == combined["end_punct_share"]
        assert cheesecloth.dup_line_share(text) == combined["dup_line_share"]
        assert cheesecloth.numeric_line_share(text) == combined["numeric_line_share"]
        assert cheesecloth.longest_line_length(text) == combined["longest_line"]
        assert cheesecloth.count_nonempty_lines(text) == combined["n_lines"]


def test_whitespace_semantics_match_str_isspace():
    # Each whitespace char must be stripped from both ends and split words.
    for ws in PY_WHITESPACE:
        text = f"{ws}a{ws}b{ws}"
        assert cheesecloth.get_line_structure_metrics(text) == reference(text), hex(
            ord(ws)
        )


def test_digit_semantics_match_str_isdigit():
    # Every str.isdigit() character known to this interpreter counts as numeric.
    digits = [chr(c) for c in range(sys.maxunicode + 1) if chr(c).isdigit()]
    assert digits
    text = "\n".join(d * 2 + "x" for d in digits)
    result = cheesecloth.get_line_structure_metrics(text)
    assert result["numeric_line_share"] == 1.0

    # Numeric characters that are not str.isdigit() (fractions, roman numerals,
    # CJK numerals) must not count.
    non_digits = ["½", "⅕", "Ⅰ", "一", "〇", "¼"]
    for ch in non_digits:
        assert not ch.isdigit()
    text = "\n".join(ch * 2 + "x" for ch in non_digits)
    assert cheesecloth.get_line_structure_metrics(text)["numeric_line_share"] == 0.0
