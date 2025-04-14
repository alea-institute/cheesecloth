import os
import pytest
import cheesecloth


# Path to War and Peace text file
DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data"
)
WAR_AND_PEACE_PATH = os.path.join(DATA_DIR, "war_and_peace.txt")


# Load War and Peace text
@pytest.fixture(scope="module")
def war_and_peace_text():
    with open(WAR_AND_PEACE_PATH, "r", encoding="utf-8") as f:
        return f.read()


# Load shorter samples for more expensive tests
@pytest.fixture(scope="module")
def war_and_peace_start(war_and_peace_text):
    # First 10,000 characters
    return war_and_peace_text[:10000]


@pytest.fixture(scope="module")
def war_and_peace_middle(war_and_peace_text):
    # 10,000 characters from the middle
    middle = len(war_and_peace_text) // 2
    return war_and_peace_text[middle : middle + 10000]


# Benchmarking basic character metrics
def test_bench_count_chars(benchmark, war_and_peace_text):
    benchmark(cheesecloth.count_chars, war_and_peace_text)


def test_bench_count_words(benchmark, war_and_peace_text):
    benchmark(cheesecloth.count_words, war_and_peace_text)


def test_bench_is_ascii(benchmark, war_and_peace_text):
    benchmark(cheesecloth.is_ascii, war_and_peace_text)


def test_bench_ratio_ascii(benchmark, war_and_peace_text):
    benchmark(cheesecloth.ratio_ascii, war_and_peace_text)


# Benchmarking character classification metrics
def test_bench_count_letters(benchmark, war_and_peace_text):
    benchmark(cheesecloth.count_letters, war_and_peace_text)


def test_bench_count_digits(benchmark, war_and_peace_text):
    benchmark(cheesecloth.count_digits, war_and_peace_text)


def test_bench_count_punctuation(benchmark, war_and_peace_text):
    benchmark(cheesecloth.count_punctuation, war_and_peace_text)


def test_bench_count_symbols(benchmark, war_and_peace_text):
    benchmark(cheesecloth.count_symbols, war_and_peace_text)


def test_bench_count_whitespace(benchmark, war_and_peace_text):
    benchmark(cheesecloth.count_whitespace, war_and_peace_text)


def test_bench_count_non_ascii(benchmark, war_and_peace_text):
    benchmark(cheesecloth.count_non_ascii, war_and_peace_text)


# Benchmarking Unicode category functions (using smaller samples for expensive operations)
def test_bench_get_unicode_categories(benchmark, war_and_peace_start):
    benchmark(cheesecloth.get_unicode_categories, war_and_peace_start)


def test_bench_get_unicode_category_groups(benchmark, war_and_peace_start):
    benchmark(cheesecloth.get_unicode_category_groups, war_and_peace_start)


def test_bench_count_unicode_categories(benchmark, war_and_peace_text):
    benchmark(cheesecloth.count_unicode_categories, war_and_peace_text)


def test_bench_count_unicode_category_groups(benchmark, war_and_peace_text):
    benchmark(cheesecloth.count_unicode_category_groups, war_and_peace_text)


def test_bench_get_unicode_category_ratios(benchmark, war_and_peace_text):
    benchmark(cheesecloth.get_unicode_category_ratios, war_and_peace_text)


def test_bench_get_unicode_category_group_ratios(benchmark, war_and_peace_text):
    benchmark(cheesecloth.get_unicode_category_group_ratios, war_and_peace_text)


# Combined benchmarks for common tasks
def test_bench_basic_metrics_combined(benchmark, war_and_peace_middle):
    """Benchmark combined basic character metrics"""

    def run_basic_metrics(text):
        char_count = cheesecloth.count_chars(text)
        word_count = cheesecloth.count_words(text)
        letter_count = cheesecloth.count_letters(text)
        digit_count = cheesecloth.count_digits(text)
        punct_count = cheesecloth.count_punctuation(text)
        whitespace_count = cheesecloth.count_whitespace(text)
        return (
            char_count,
            word_count,
            letter_count,
            digit_count,
            punct_count,
            whitespace_count,
        )

    benchmark(run_basic_metrics, war_and_peace_middle)


def test_bench_unicode_analysis_combined(benchmark, war_and_peace_middle):
    """Benchmark combined Unicode category analysis"""

    def run_unicode_analysis(text):
        category_counts = cheesecloth.count_unicode_categories(text)
        group_counts = cheesecloth.count_unicode_category_groups(text)
        category_ratios = cheesecloth.get_unicode_category_ratios(text)
        group_ratios = cheesecloth.get_unicode_category_group_ratios(text)
        return (category_counts, group_counts, category_ratios, group_ratios)

    benchmark(run_unicode_analysis, war_and_peace_middle)


# Separate comparative benchmarks (each function needs its own benchmark fixture)
def test_bench_compare_count_chars(benchmark, war_and_peace_start):
    benchmark.pedantic(
        cheesecloth.count_chars, args=(war_and_peace_start,), rounds=10, iterations=5
    )


def test_bench_compare_count_words(benchmark, war_and_peace_start):
    benchmark.pedantic(
        cheesecloth.count_words, args=(war_and_peace_start,), rounds=10, iterations=5
    )


def test_bench_compare_count_letters(benchmark, war_and_peace_start):
    benchmark.pedantic(
        cheesecloth.count_letters, args=(war_and_peace_start,), rounds=10, iterations=5
    )


def test_bench_compare_count_digits(benchmark, war_and_peace_start):
    benchmark.pedantic(
        cheesecloth.count_digits, args=(war_and_peace_start,), rounds=10, iterations=5
    )


def test_bench_compare_count_unicode_categories(benchmark, war_and_peace_start):
    benchmark.pedantic(
        cheesecloth.count_unicode_categories,
        args=(war_and_peace_start,),
        rounds=10,
        iterations=5,
    )


def test_bench_compare_count_unicode_category_groups(benchmark, war_and_peace_start):
    benchmark.pedantic(
        cheesecloth.count_unicode_category_groups,
        args=(war_and_peace_start,),
        rounds=10,
        iterations=5,
    )
