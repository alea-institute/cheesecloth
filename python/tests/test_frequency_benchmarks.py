import pytest
import cheesecloth


# Load War and Peace text
@pytest.fixture(scope="module")
def war_and_peace_text():
    with open(
        "/home/mjbommar/RustroverProjects/cheesecloth/data/war_and_peace.txt",
        "r",
        encoding="utf-8",
    ) as f:
        text = f.read()
        print(f"\nWar and Peace full text: {len(text)} characters")
        return text


# Smaller sample for more detailed tests
@pytest.fixture(scope="module")
def war_and_peace_sample(war_and_peace_text):
    # First 100,000 characters
    return war_and_peace_text[:100000]


def test_bench_char_frequency(benchmark, war_and_peace_sample):
    """Benchmark character frequency function"""
    result = benchmark(cheesecloth.get_char_frequency, war_and_peace_sample)
    assert isinstance(result, dict)
    assert len(result) > 26  # At least all English letters
    assert sum(result.values()) == len(war_and_peace_sample)


def test_bench_char_type_frequency(benchmark, war_and_peace_sample):
    """Benchmark character type frequency function"""
    result = benchmark(cheesecloth.get_char_type_frequency, war_and_peace_sample)
    assert isinstance(result, dict)
    assert "letter" in result
    assert "digit" in result
    assert "punctuation" in result
    assert sum(result.values()) == len(war_and_peace_sample)


def test_bench_unicode_category_frequency_sample(benchmark, war_and_peace_sample):
    """Benchmark Unicode category frequency function on a sample"""
    result = benchmark(cheesecloth.get_unicode_category_frequency, war_and_peace_sample)
    assert isinstance(result, dict)
    assert "Lu" in result  # Uppercase letters
    assert "Ll" in result  # Lowercase letters
    assert sum(result.values()) == len(war_and_peace_sample)


def test_bench_unicode_category_group_frequency(benchmark, war_and_peace_sample):
    """Benchmark Unicode category group frequency function"""
    result = benchmark(
        cheesecloth.get_unicode_category_group_frequency, war_and_peace_sample
    )
    assert isinstance(result, dict)
    assert "L" in result  # Letters
    assert "P" in result  # Punctuation
    assert sum(result.values()) == len(war_and_peace_sample)


# Compare standard and optimized methods on the sample
def test_bench_compare_unicode_category_standard(benchmark, war_and_peace_sample):
    """Benchmark standard Unicode category counting approach"""

    def standard_method(text):
        # Similar to what count_unicode_categories would do internally, but returning string keys
        counts = {}
        for c in text:
            category = cheesecloth.get_unicode_categories(c)[0]
            counts[category] = counts.get(category, 0) + 1
        return counts

    result = benchmark(standard_method, war_and_peace_sample)
    assert isinstance(result, dict)


def test_bench_compare_unicode_category_optimized(benchmark, war_and_peace_sample):
    """Benchmark optimized Unicode category counting approach on sample"""
    result = benchmark(cheesecloth.get_unicode_category_frequency, war_and_peace_sample)
    assert isinstance(result, dict)


# Run only the optimized function on the full War and Peace text
def test_bench_unicode_category_frequency_full(benchmark, war_and_peace_text):
    """Benchmark optimized Unicode category frequency function on FULL War and Peace text"""
    print(f"\nFull War and Peace text size: {len(war_and_peace_text)} characters")
    result = benchmark(cheesecloth.get_unicode_category_frequency, war_and_peace_text)
    assert isinstance(result, dict)
    assert "Lu" in result  # Uppercase letters
    assert "Ll" in result  # Lowercase letters
    assert sum(result.values()) == len(war_and_peace_text)
