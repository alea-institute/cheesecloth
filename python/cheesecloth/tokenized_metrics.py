#!/usr/bin/env python3
"""
Tokenized Data Processing and Analysis
=====================================

This module provides specialized functionality for analyzing pre-tokenized text data,
particularly focusing on the token sequences produced by machine learning tokenizers
like BPE (Byte-Pair Encoding), WordPiece, and SentencePiece.

Key Components
-------------

1. TokenizedAnalyzer
   - Unified analyzer for pre-tokenized text
   - Combines HyperAnalyzer functionality with token-specific metrics
   - Handles both raw text and token IDs together
   - Provides consistent naming and organization of metrics

2. Token-specific Metrics
   - Token count and unique token statistics
   - Type-token ratio for tokenized data
   - Repetition rate and entropy measures
   - Direct calculation from token IDs without requiring decoded text

3. Processing Functions
   - calculate_token_metrics: Core metrics from token IDs
   - process_tokenized_text: Process individual texts
   - process_tokenized_batch: Efficient batch processing
   - process_tokenized_data: Combined processing of text and tokens

Use Cases
--------

This module is particularly valuable for:

1. Analyzing how machine learning models "see" text through their tokenization
2. Comparing linguistic (unigram) metrics with ML tokenization metrics
3. Working with pre-tokenized datasets like those used in large language models
4. Studying tokenization efficiency and behavior across different text types
5. Processing data that comes already tokenized from ML pipelines

The metrics provided help bridge the gap between traditional linguistic analysis
and machine learning approaches to text processing.
"""

import math
from collections import Counter
from typing import List, Dict, Any, Optional

import cheesecloth


def calculate_token_metrics(tokens: List[int]) -> Dict[str, Any]:
    """
    Calculate metrics directly from token IDs.

    Args:
        tokens: List of token IDs

    Returns:
        Dictionary of token metrics with consistent naming
    """
    if not tokens:
        return {
            "token_count": 0,
            "unique_token_count": 0,
            "token_type_token_ratio": 0.0,
            "token_repetition_rate": 0.0,
            "token_entropy": 0.0,
        }

    # Count tokens
    token_count = len(tokens)

    # Count unique tokens
    unique_tokens = set(tokens)
    unique_token_count = len(unique_tokens)

    # Calculate type-token ratio
    type_token_ratio = unique_token_count / token_count if token_count > 0 else 0.0

    # Calculate repetition rate
    repetition_rate = 1.0 - type_token_ratio

    # Calculate token entropy
    token_freq = Counter(tokens)
    entropy = 0.0
    for count in token_freq.values():
        probability = count / token_count
        entropy -= probability * math.log2(probability)

    return {
        "token_count": token_count,
        "unique_token_count": unique_token_count,
        "token_type_token_ratio": type_token_ratio,
        "token_repetition_rate": repetition_rate,
        "token_entropy": entropy,
    }


def process_tokenized_text(
    text: str,
    include_token_metrics: bool = True,
    include_unigram_metrics: bool = True,
    include_char_metrics: bool = True,
    include_punctuation: bool = False,
    case_sensitive: bool = True,
) -> Dict[str, Any]:
    """
    Process text with multiple metric types.

    Args:
        text: The text to analyze
        include_token_metrics: Whether to include BPE token metrics
        include_unigram_metrics: Whether to include unigram metrics
        include_char_metrics: Whether to include character metrics
        include_punctuation: Whether to include punctuation in unigram analysis
        case_sensitive: Whether to perform case-sensitive analysis

    Returns:
        Dictionary of metrics with consistent naming
    """
    result = {}

    # Use HyperAnalyzer for character and unigram metrics
    if include_char_metrics or include_unigram_metrics:
        analyzer = cheesecloth.HyperAnalyzer(include_punctuation, case_sensitive)
        metrics = analyzer.calculate_all_metrics(text)

        # Filter metrics based on flags
        for key, value in metrics.items():
            if key.startswith("unigram_") and include_unigram_metrics:
                result[key] = value
            elif (
                not key.startswith("unigram_")
                and not key.startswith("token_")
                and include_char_metrics
            ):
                result[key] = value

    # For token metrics, we would need actual token IDs
    # This is handled separately with calculate_token_metrics

    return result


def process_tokenized_batch(
    texts: List[str],
    batch_size: int = 32,
    include_token_metrics: bool = True,
    include_unigram_metrics: bool = True,
    include_char_metrics: bool = True,
    include_punctuation: bool = False,
    case_sensitive: bool = True,
) -> List[Dict[str, Any]]:
    """
    Process a batch of texts with multiple metric types.

    Args:
        texts: List of texts to analyze
        batch_size: Batch size for processing
        include_token_metrics: Whether to include BPE token metrics
        include_unigram_metrics: Whether to include unigram metrics
        include_char_metrics: Whether to include character metrics
        include_punctuation: Whether to include punctuation in unigram analysis
        case_sensitive: Whether to perform case-sensitive analysis

    Returns:
        List of dictionaries with metrics for each text
    """
    results = []

    # Process in batches
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]

        # Use HyperAnalyzer for character and unigram metrics
        if include_char_metrics or include_unigram_metrics:
            analyzer = cheesecloth.HyperAnalyzer(include_punctuation, case_sensitive)
            batch_metrics = analyzer.calculate_batch_metrics(batch)

            for j, metrics in enumerate(batch_metrics):
                # Create result dict if needed
                if i + j >= len(results):
                    results.append({})

                # Filter metrics based on flags
                for key, value in metrics.items():
                    if key.startswith("unigram_") and include_unigram_metrics:
                        results[i + j][key] = value
                    elif (
                        not key.startswith("unigram_")
                        and not key.startswith("token_")
                        and include_char_metrics
                    ):
                        results[i + j][key] = value

    return results


def process_tokenized_data(
    texts: List[str],
    token_ids: List[List[int]],
    batch_size: int = 32,
    include_token_metrics: bool = True,
    include_unigram_metrics: bool = True,
    include_char_metrics: bool = True,
    include_punctuation: bool = False,
    case_sensitive: bool = True,
) -> List[Dict[str, Any]]:
    """
    Process texts and corresponding token IDs together.

    Args:
        texts: List of text strings
        token_ids: List of token ID lists corresponding to each text
        batch_size: Batch size for processing
        include_token_metrics: Whether to include BPE token metrics
        include_unigram_metrics: Whether to include unigram metrics
        include_char_metrics: Whether to include character metrics
        include_punctuation: Whether to include punctuation in unigram analysis
        case_sensitive: Whether to perform case-sensitive analysis

    Returns:
        List of dictionaries with metrics for each text
    """
    # Validate inputs
    if len(texts) != len(token_ids):
        raise ValueError(
            f"Length mismatch: {len(texts)} texts vs {len(token_ids)} token lists"
        )

    # Get text metrics
    results = process_tokenized_batch(
        texts,
        batch_size,
        include_token_metrics=False,  # We'll add token metrics separately
        include_unigram_metrics=include_unigram_metrics,
        include_char_metrics=include_char_metrics,
        include_punctuation=include_punctuation,
        case_sensitive=case_sensitive,
    )

    # Add token metrics
    if include_token_metrics:
        for i, tokens in enumerate(token_ids):
            token_metrics = calculate_token_metrics(tokens)
            results[i].update(token_metrics)

    return results


class TokenizedAnalyzer:
    """
    Analyzer for pre-tokenized data.

    This class provides a unified interface for calculating metrics on
    pre-tokenized data, such as text with corresponding BPE token IDs.
    """

    def __init__(self, include_punctuation: bool = False, case_sensitive: bool = True):
        """
        Initialize the analyzer.

        Args:
            include_punctuation: Whether to include punctuation in unigram analysis
            case_sensitive: Whether to perform case-sensitive analysis
        """
        self.include_punctuation = include_punctuation
        self.case_sensitive = case_sensitive

        # Create a HyperAnalyzer for text metrics
        self.hyper_analyzer = cheesecloth.HyperAnalyzer(
            include_punctuation, case_sensitive
        )

    def calculate_metrics(
        self, text: str, token_ids: Optional[List[int]] = None
    ) -> Dict[str, Any]:
        """
        Calculate metrics for a single text.

        Args:
            text: The text to analyze
            token_ids: Optional token IDs for the text

        Returns:
            Dictionary of metrics
        """
        # Calculate text metrics
        result = self.hyper_analyzer.calculate_all_metrics(text)

        # Add token metrics if provided
        if token_ids is not None:
            token_metrics = calculate_token_metrics(token_ids)
            result.update(token_metrics)

        # Add advanced metrics - compression ratio and Zipf metrics
        try:
            # Add compression metrics
            compression_metrics = cheesecloth.get_compression_metrics(text)
            result.update(compression_metrics)

            # Add Zipf/power law metrics
            zipf_metrics = cheesecloth.get_zipf_metrics(
                text,
                include_punctuation=self.include_punctuation,
                case_sensitive=self.case_sensitive,
            )
            result.update(zipf_metrics)
        except Exception as e:
            # If advanced metrics fail for any reason, log it but continue
            print(f"Warning: Failed to calculate advanced metrics: {e}")

        return result

    def calculate_batch_metrics(
        self, texts: List[str], token_ids: Optional[List[List[int]]] = None
    ) -> List[Dict[str, Any]]:
        """
        Calculate metrics for a batch of texts.

        Args:
            texts: List of texts to analyze
            token_ids: Optional list of token ID lists for each text

        Returns:
            List of dictionaries with metrics for each text
        """
        # Calculate text metrics
        results = list(self.hyper_analyzer.calculate_batch_metrics(texts))

        # Add token metrics if provided
        if token_ids is not None:
            if len(texts) != len(token_ids):
                raise ValueError(
                    f"Length mismatch: {len(texts)} texts vs {len(token_ids)} token lists"
                )

            for i, tokens in enumerate(token_ids):
                token_metrics = calculate_token_metrics(tokens)
                results[i].update(token_metrics)

        # Add advanced metrics for each text
        for i, text in enumerate(texts):
            try:
                # Add compression metrics
                compression_metrics = cheesecloth.get_compression_metrics(text)
                results[i].update(compression_metrics)

                # Add Zipf/power law metrics
                zipf_metrics = cheesecloth.get_zipf_metrics(
                    text,
                    include_punctuation=self.include_punctuation,
                    case_sensitive=self.case_sensitive,
                )
                results[i].update(zipf_metrics)
            except Exception:
                # If advanced metrics fail for any reason, continue
                pass

        return results


# Example of how to use this module:
"""
# Example 1: Calculate metrics for a single text and its tokens
text = "This is an example sentence."
token_ids = [101, 2023, 2003, 2019, 6251, 6202, 102]  # Example token IDs

analyzer = TokenizedAnalyzer()
result = analyzer.calculate_metrics(text, token_ids)
print(json.dumps(result, indent=2))

# Example 2: Calculate metrics for a batch of texts
texts = ["First example.", "Second example."]
tokens_batch = [[101, 2034, 6251, 102], [101, 2117, 6251, 102]]

results = analyzer.calculate_batch_metrics(texts, tokens_batch)
for i, result in enumerate(results):
    print(f"Text {i+1} metrics:")
    print(json.dumps(result, indent=2))
"""
