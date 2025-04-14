"""
Test Suite for Compression Metrics
=================================

This module tests the compression-based metrics provided by Cheesecloth,
ensuring they work correctly across a variety of input texts with different
compression characteristics.

Tests cover:
1. Basic compression ratio calculation
2. Unigram-based compression ratio (with and without punctuation)
3. Comprehensive compression metrics (efficiency, normalization)

The tests verify both functionality and expected behavior with different
text types (repetitive, natural language, mixed content), making sure
the metrics provide meaningful and consistent values.
"""

import unittest
import cheesecloth


class TestCompression(unittest.TestCase):
    def test_compression_ratio(self):
        # Test with an empty string
        self.assertAlmostEqual(cheesecloth.compression_ratio(""), 1.0)

        # Test with a repetitive string (highly compressible)
        repetitive_text = "a" * 1000
        ratio1 = cheesecloth.compression_ratio(repetitive_text)
        self.assertGreater(ratio1, 10.0)  # Should be highly compressible

        # Test with a less repetitive string
        mixed_text = "This is a test of the compression ratio function. " * 10
        ratio2 = cheesecloth.compression_ratio(mixed_text)
        self.assertGreater(ratio2, 1.5)  # Should be somewhat compressible
        self.assertLess(ratio2, ratio1)  # But less than the highly repetitive text

        # Test with random-like text
        lorem_ipsum = """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor 
        incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis 
        nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
        Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu 
        fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in 
        culpa qui officia deserunt mollit anim id est laborum.
        """
        ratio3 = cheesecloth.compression_ratio(lorem_ipsum)
        self.assertGreater(ratio3, 1.0)  # Still compressible
        self.assertLess(ratio3, ratio1)  # But less than highly repetitive text

    def test_unigram_compression_ratio(self):
        # Test with repeated words
        repeated_words = "the the the cat cat cat sat sat on on the the mat mat mat"
        ratio1 = cheesecloth.unigram_compression_ratio(repeated_words, False)
        self.assertGreater(ratio1, 1.5)  # Should be compressible due to repetition

        # Test with and without punctuation
        text_with_punct = "Hello, world! How are you? I am fine, thank you!"
        ratio_no_punct = cheesecloth.unigram_compression_ratio(text_with_punct, False)
        ratio_with_punct = cheesecloth.unigram_compression_ratio(text_with_punct, True)
        self.assertNotEqual(
            ratio_no_punct, ratio_with_punct
        )  # Should give different results

    def test_get_compression_metrics(self):
        # Test comprehensive metrics
        text = "This is a test of the compression metrics. " * 5
        metrics = cheesecloth.get_compression_metrics(text)

        # Check all expected metrics are present
        self.assertIn("compression_ratio", metrics)
        self.assertIn("unigram_compression_ratio", metrics)
        self.assertIn("unigram_compression_ratio_with_punct", metrics)
        self.assertIn("normalized_compression_ratio", metrics)
        self.assertIn("compression_efficiency", metrics)

        # Check that metrics have reasonable values
        self.assertGreater(metrics["compression_ratio"], 1.0)
        self.assertGreater(metrics["unigram_compression_ratio"], 1.0)
        self.assertGreater(metrics["compression_efficiency"], 0.0)
        self.assertLess(metrics["compression_efficiency"], 1.0)


if __name__ == "__main__":
    unittest.main()
