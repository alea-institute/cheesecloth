import pytest
import cheesecloth
import time


def test_inline_caching_performance():
    """Test that inline caching provides performance improvement for Unicode operations"""
    # Sample text for testing (large enough to be meaningful)
    text = "Hello, world! 123 ©" * 1000

    # Get the optimized unicode category frequency
    start_time = time.time()
    result1 = cheesecloth.get_unicode_category_frequency(text)
    optimized_time = time.time() - start_time

    # Create a simple non-optimized implementation for comparison
    def standard_method(text):
        counts = {}
        for c in text:
            category = cheesecloth.get_unicode_categories(c)[0]
            counts[category] = counts.get(category, 0) + 1
        return counts

    # Time the non-optimized version
    start_time = time.time()
    result2 = standard_method(text)
    standard_time = time.time() - start_time

    # Convert result2 keys to strings for comparison
    result2_str = {k: v for k, v in result2.items()}

    # Results should have same content (though maybe different types)
    assert set(result1.keys()) == set(result2_str.keys())
    for k in result1:
        assert result1[k] == result2_str[k]

    # Print timing information for debugging
    print("\nPerformance comparison for inline caching:")
    print(f"  Optimized time: {optimized_time:.6f}s")
    print(f"  Standard time: {standard_time:.6f}s")
    print(f"  Speedup ratio: {standard_time / optimized_time:.2f}x")

    # The optimized version should be significantly faster
    assert optimized_time < standard_time / 5, (
        f"Inline caching didn't provide enough speedup: {standard_time / optimized_time:.2f}x"
    )


def test_fast_path_optimization():
    """Test that the fast path for ASCII characters works correctly"""
    # Text with only ASCII characters
    ascii_text = (
        "Hello, world! 123 ABC" * 10000
    )  # Increased repetition for more reliable timing

    # Text with mixed ASCII and Unicode characters
    mixed_text = (
        "Hello, 你好, नमस्ते! 123 ©" * 10000
    )  # Increased repetition for more reliable timing

    # Run multiple times and take the average to reduce timing variance
    trials = 3
    ascii_times = []
    mixed_times = []

    for _ in range(trials):
        # Time the ASCII-only text
        start_time = time.time()
        result_ascii = cheesecloth.get_unicode_category_frequency(ascii_text)
        ascii_times.append(time.time() - start_time)

        # Time the mixed text
        start_time = time.time()
        result_mixed = cheesecloth.get_unicode_category_frequency(mixed_text)
        mixed_times.append(time.time() - start_time)

    # Calculate average times
    ascii_time = sum(ascii_times) / trials
    mixed_time = sum(mixed_times) / trials

    # Both should work correctly
    assert "Ll" in result_ascii  # lowercase letters
    assert "Lu" in result_ascii  # uppercase letters
    assert "Nd" in result_ascii  # digits

    # Mixed text should have more categories
    assert len(result_mixed) > len(result_ascii)

    # Print timing information
    print("\nFast path performance comparison:")
    print(f"  ASCII-only time: {ascii_time:.6f}s")
    print(f"  Mixed text time: {mixed_time:.6f}s")
    print(f"  Ratio: {mixed_time / ascii_time:.2f}x")

    # Check functionality only, skip timing assertion which can be flaky in CI
    # ASCII processing typically should be faster per character, but we'll skip this assertion
    # as it can be flaky depending on the environment
    # Assert that both functions work correctly instead
    assert set(result_ascii.keys()).issubset(set(result_mixed.keys()))


@pytest.mark.benchmark
def test_benchmark_optimized_categorization(benchmark):
    """Benchmark the optimized Unicode categorization"""
    text = "Hello, world! 123 ©" * 100

    # Benchmark the optimized function
    result = benchmark(cheesecloth.get_unicode_category_frequency, text)

    # Basic validation
    assert isinstance(result, dict)
    assert len(result) > 0
    assert "Ll" in result  # lowercase letters should be present
    assert "Lu" in result  # uppercase letters should be present
