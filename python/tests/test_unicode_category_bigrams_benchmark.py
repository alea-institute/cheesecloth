import pytest
import cheesecloth
import time


@pytest.mark.benchmark(group="unicode_category_bigrams")
def test_benchmark_unicode_category_bigrams(benchmark):
    """Benchmark for Unicode category bigram calculation."""
    # Medium-sized text sample for benchmark
    text = "The quick brown fox jumps over the lazy dog. " * 50

    # Benchmark the function
    result = benchmark(cheesecloth.get_unicode_category_bigrams, text)

    # Basic validation
    assert len(result) > 5  # Should have multiple transitions


@pytest.mark.benchmark(group="unicode_category_bigrams")
def test_benchmark_unicode_category_bigram_ratios(benchmark):
    """Benchmark for Unicode category bigram ratio calculation."""
    # Medium-sized text sample for benchmark
    text = "The quick brown fox jumps over the lazy dog. " * 50

    # Benchmark the function
    result = benchmark(cheesecloth.get_unicode_category_bigram_ratios, text)

    # Basic validation
    assert len(result) > 5  # Should have multiple transitions
    assert abs(sum(result.values()) - 1.0) < 1e-10  # Ratios should sum to 1


@pytest.mark.benchmark(group="unicode_category_bigrams")
def test_benchmark_unicode_category_group_bigrams(benchmark):
    """Benchmark for Unicode category group bigram calculation."""
    # Medium-sized text sample for benchmark
    text = "The quick brown fox jumps over the lazy dog. " * 50

    # Benchmark the function
    result = benchmark(cheesecloth.get_unicode_category_group_bigrams, text)

    # Basic validation
    assert len(result) > 5  # Should have multiple transitions


@pytest.mark.benchmark(group="unicode_category_bigrams")
def test_benchmark_unicode_category_group_bigram_ratios(benchmark):
    """Benchmark for Unicode category group bigram ratio calculation."""
    # Medium-sized text sample for benchmark
    text = "The quick brown fox jumps over the lazy dog. " * 50

    # Benchmark the function
    result = benchmark(cheesecloth.get_unicode_category_group_bigram_ratios, text)

    # Basic validation
    assert len(result) > 5  # Should have multiple transitions
    assert abs(sum(result.values()) - 1.0) < 1e-10  # Ratios should sum to 1


@pytest.mark.benchmark(group="unicode_category_bigrams")
def test_benchmark_unicode_category_bigrams_large(benchmark):
    """Benchmark for Unicode category bigram calculation with a large text."""
    # Larger text sample for benchmark
    text = "The quick brown fox jumps over the lazy dog. " * 500

    # Time the function without pytest.benchmark for large input
    start_time = time.time()
    result = cheesecloth.get_unicode_category_bigrams(text)
    execution_time = time.time() - start_time

    # Only benchmark if it's fast enough for the benchmark suite
    if execution_time < 1.0:  # If it takes less than 1 second
        # Benchmark the function
        result = benchmark(cheesecloth.get_unicode_category_bigrams, text)

        # Basic validation
        assert len(result) > 5
    else:
        # Skip benchmark but report time
        pytest.skip(f"Function too slow for benchmark: {execution_time:.2f}s")
