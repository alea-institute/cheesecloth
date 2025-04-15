#!/usr/bin/env python3
"""
Example 5: Comprehensive Metrics with get_all_metrics

This example demonstrates how to use the new get_all_metrics function to obtain
a comprehensive set of text metrics with minimal Rust-Python round trips.
The function combines character metrics, unigram metrics, segmentation metrics, 
and pattern-based metrics in a single call for maximum efficiency.

It also demonstrates the new get_all_pattern_metrics function that can be used
independently for pattern-only analysis with optimized paragraph processing.
"""

import json
import gzip
import time
from pathlib import Path

import cheesecloth

# Path to sample data
DATA_PATH = Path(__file__).parent.parent / "data"
WAR_AND_PEACE_PATH = DATA_PATH / "war_and_peace.txt"
USC_PATH = DATA_PATH / "usc-1000.jsonl.gz"


def analyze_single_text():
    """Analyze a single text file with the comprehensive metrics function."""
    print("\n== Single Text Analysis ==\n")
    
    # Load the full War and Peace text to demonstrate real-world performance
    with open(WAR_AND_PEACE_PATH, "r", encoding="utf-8") as f:
        # Use the complete text for a real benchmark
        text = f.read(100000)
    
    print(f"Analyzing text of length: {len(text):,} characters")
    
    # Time the get_all_metrics function with standard processing
    start_time = time.time()
    
    # Get all metrics at once (standard)
    metrics = cheesecloth.get_all_metrics(
        text=text,
        include_punctuation=True,
        case_sensitive=False,
        use_paragraph_processing=False,
    )
    
    elapsed_standard = time.time() - start_time
    print(f"Time with standard processing: {elapsed_standard:.2f} seconds")
    
    # Time the get_all_metrics function with paragraph-based processing
    start_time = time.time()
    
    # Get all metrics with paragraph processing
    metrics_paragraph = cheesecloth.get_all_metrics(
        text=text,
        include_punctuation=True,
        case_sensitive=False,
        use_paragraph_processing=True,
    )
    
    elapsed_paragraph = time.time() - start_time
    print(f"Time with paragraph processing: {elapsed_paragraph:.2f} seconds")
    print(f"Speed improvement: {elapsed_standard/elapsed_paragraph:.1f}x faster")
    
    # Compare with separate calls for reference
    start_time = time.time()
    
    char_metrics = cheesecloth.get_all_char_metrics(text)
    unigram_metrics = cheesecloth.get_all_unigram_metrics(
        text=text,
        include_punctuation=True,
        case_sensitive=False,
    )
    question_count = cheesecloth.count_question_strings(text)
    factual_count = cheesecloth.count_factual_statements(text)
    
    elapsed_separate = time.time() - start_time
    print(f"Time for separate calls: {elapsed_separate:.2f} seconds")
    
    # For actual metrics, we'll use the paragraph processing results
    metrics = metrics_paragraph
    
    # Examine a few key metrics from each category
    print("\nCharacter metrics:")
    print(f"- Total chars: {metrics['character']['char_count']:,}")
    print(f"- Letters: {metrics['character']['letter_count']:,}")
    print(f"- Character entropy: {metrics['character']['char_entropy']:.2f}")
    
    print("\nUnigram metrics:")
    print(f"- Total tokens: {metrics['unigram']['token_count']:,}")
    print(f"- Unique tokens: {metrics['unigram']['unique_token_count']:,}")
    print(f"- Type-token ratio: {metrics['unigram']['type_token_ratio']:.4f}")
    
    print("\nSegmentation metrics:")
    print(f"- Line count: {metrics['segmentation']['line_count']:,}")
    print(f"- Paragraph count: {metrics['segmentation']['paragraph_count']:,}")
    print(f"- Average sentence length: {metrics['segmentation']['average_sentence_length']:.2f} words")
    
    print("\nPattern metrics:")
    print(f"- Questions: {metrics['patterns']['question_count']:,}")
    print(f"- Interrogative questions: {metrics['patterns']['interrogative_question_count']:,}")
    print(f"- Factual statements: {metrics['patterns']['factual_statement_count']:,}")
    print(f"- Logical reasoning: {metrics['patterns']['logical_reasoning_count']:,}")
    print(f"- Contains code: {metrics['patterns']['contains_code']}")


def analyze_multiple_texts():
    """Analyze a corpus of texts using the BatchProcessor with the get_all_metrics function."""
    print("\n== Multiple Text Analysis ==\n")
    
    # Load the first 5 US Code sections
    with gzip.open(USC_PATH, "rt", encoding="utf-8") as f:
        corpus = [json.loads(line) for line in f][:5]
    
    print(f"Analyzing corpus of {len(corpus)} documents")
    
    # Create a BatchProcessor for multi-document analysis
    # Define metrics to compute - we'll include all available metrics
    metrics = [
        "char_count", "word_count", "letter_count", "digit_count", 
        "punctuation_count", "symbol_count", "whitespace_count", 
        "non_ascii_count", "uppercase_count", "lowercase_count", 
        "alphanumeric_count", "is_ascii", "ascii_ratio", "uppercase_ratio", 
        "alphanumeric_ratio", "alpha_to_numeric_ratio", "whitespace_ratio", 
        "digit_ratio", "punctuation_ratio", "char_entropy", "line_count", 
        "avg_line_length", "paragraph_count", "avg_paragraph_length", 
        "avg_word_length", "avg_sentence_length", "unigram_count", 
        "unique_unigram_count", "unigram_type_token_ratio", 
        "unigram_repetition_rate", "unigram_entropy"
    ]
    
    processor = cheesecloth.BatchProcessor(
        metrics=metrics,
        include_punctuation=True,
        case_sensitive=False
    )
    
    # Process the corpus and get aggregate metrics
    start_time = time.time()
    
    # Use compute_batch_metrics instead of process_documents
    results = processor.compute_batch_metrics([doc["text"] for doc in corpus])
    
    elapsed = time.time() - start_time
    print(f"Time to process {len(corpus)} documents: {elapsed:.2f} seconds")
    
    # Show summary of some key metrics across documents
    print("\nAverage metrics across documents:")
    
    # BatchProcessor results have different structure from get_all_metrics
    avg_char_count = sum(r.get("char_count", 0) for r in results) / len(results)
    avg_word_count = sum(r.get("word_count", 0) for r in results) / len(results)
    avg_ttr = sum(r.get("unigram_type_token_ratio", 0) for r in results) / len(results)
    avg_letter_count = sum(r.get("letter_count", 0) for r in results) / len(results)
    avg_paragraph_count = sum(r.get("paragraph_count", 0) for r in results) / len(results)
    
    print(f"- Average character count: {avg_char_count:.2f}")
    print(f"- Average word count: {avg_word_count:.2f}")
    print(f"- Average type-token ratio: {avg_ttr:.4f}")
    print(f"- Average letter count: {avg_letter_count:.2f}")
    print(f"- Average paragraph count: {avg_paragraph_count:.2f}")


def patterns_only_analysis():
    """Demonstrate using just the pattern metrics for a faster, focused analysis."""
    print("\n== Pattern-Only Analysis ==\n")
    
    # Load the full War and Peace text for a comprehensive benchmark
    with open(WAR_AND_PEACE_PATH, "r", encoding="utf-8") as f:
        text = f.read(100000)
    
    print(f"Analyzing patterns in text of length: {len(text):,} characters")
    
    # We'll just use the full War and Peace text without synthetic test cases
    # to measure real-world performance on unaltered literary text
    
    # Time the get_all_pattern_metrics function with default settings
    start_time = time.time()
    pattern_metrics = cheesecloth.get_all_pattern_metrics(text)
    elapsed = time.time() - start_time
    
    # Also try with a smaller segment size to trigger more line-based processing
    start_time = time.time()
    pattern_metrics_small_segment = cheesecloth.get_all_pattern_metrics(
        text, 
        max_segment_size=512  # Force more paragraphs to be broken down by lines
    )
    elapsed_small_segment = time.time() - start_time
    
    print(f"Pattern analysis of full War and Peace text:")
    print(f"- Default segment size (4KB): {elapsed:.2f} seconds")
    print(f"- Smaller segment size (512B): {elapsed_small_segment:.2f} seconds")
    print(f"- Performance improvement: {(elapsed-elapsed_small_segment)/elapsed*100:.1f}%")
    print(f"Used paragraph processing: {pattern_metrics.get('_used_paragraph_processing', False)}")
    print(f"Number of paragraphs processed: {pattern_metrics.get('_paragraph_count', 0):,}")
    print(f"Large paragraphs broken down: {pattern_metrics.get('_large_paragraphs_broken_down', 0)}")
    print(f"Extremely long lines chunked: {pattern_metrics.get('_extremely_long_lines_chunked', 0)}")
    print(f"Max segment size used: {pattern_metrics.get('_max_segment_size', 0):,} bytes")
    
    # Display key content indicators
    print("\nContent Indicators:")
    print(f"- Questions: {pattern_metrics.get('question_count', 0):,}")
    print(f"- Interrogative questions: {pattern_metrics.get('interrogative_question_count', 0):,}")
    print(f"- Factual statements: {pattern_metrics.get('factual_statement_count', 0):,}")
    print(f"- Logical reasoning: {pattern_metrics.get('logical_reasoning_count', 0):,}")
    print(f"- Section headings: {pattern_metrics.get('section_heading_count', 0):,}")
    print(f"- Contains code: {pattern_metrics.get('contains_code', False)}")
    print(f"- Copyright mentions: {pattern_metrics.get('copyright_mention_count', 0):,}")
    
    # Calculate content type indicators as ratios
    # These can help classify the text as educational, legal, etc.
    print("\nContent Type Indicators:")
    paragraph_count = pattern_metrics.get('_paragraph_count', 1)
    question_ratio = pattern_metrics.get('question_count', 0) / paragraph_count
    fact_ratio = pattern_metrics.get('factual_statement_count', 0) / paragraph_count
    reasoning_ratio = pattern_metrics.get('logical_reasoning_count', 0) / paragraph_count
    
    print(f"- Educational content score: {question_ratio + fact_ratio:.3f}")
    print(f"- Analytical content score: {reasoning_ratio:.3f}")
    print(f"- Legal content indicator: {pattern_metrics.get('copyright_mention_count', 0) > 0 or pattern_metrics.get('rights_reserved_count', 0) > 0}")


def main():
    print("Cheesecloth Comprehensive Metrics Example")
    print("---------------------------------------")
    print("\nThis example demonstrates two powerful functions:")
    print("1. get_all_metrics - calculates all metrics in a single call")
    print("2. get_all_pattern_metrics - focused pattern analysis with paragraph processing")
    
    # Run only the pattern analysis which focuses on our optimization
    patterns_only_analysis()
    
    print("\nAnalysis complete!")


if __name__ == "__main__":
    main()