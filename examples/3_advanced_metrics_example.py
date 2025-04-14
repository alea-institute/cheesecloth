#!/usr/bin/env python3
"""
Advanced Text Metrics Example
=============================

This script demonstrates Cheesecloth's advanced text analysis capabilities,
focusing on compression-based metrics, Zipf's law analysis, and pattern detection.

Key Features
-----------

1. Compression metrics
   - Text compressibility as a measure of complexity and redundancy
   - Normalized compression ratios for different types of text
   - Relationship between compression and information content

2. Zipf's law analysis
   - Statistical measurements of word frequency distributions
   - Power law exponent calculation and interpretation
   - Zipf fitness score for natural language assessment

3. Pattern detection
   - Content pattern identification (code fragments, headers, etc.)
   - Statistical pattern analysis
   - Document structure assessment

Usage
-----
```
python 3_advanced_metrics_example.py [text_file]
```

If a text file is provided, the script will analyze that file.
Otherwise, it will analyze sample texts to demonstrate different metrics.
"""

import cheesecloth
import sys
from pathlib import Path


def analyze_advanced_metrics(text: str, title: str = "Sample Text"):
    """
    Analyze text using Cheesecloth's advanced metrics.
    """
    print(f"\n=== {title} ===\n")

    # 1. Compression metrics
    compression_metrics = cheesecloth.get_compression_metrics(text)

    print("1. Compression Metrics:")
    print(f"   Text length: {len(text)} characters")
    print(f"   Compression ratio: {compression_metrics['compression_ratio']:.2f}")
    print(
        f"   Normalized compression ratio: {compression_metrics['normalized_compression_ratio']:.2f}"
    )
    print(
        f"   Compression efficiency: {compression_metrics['compression_efficiency']:.2f} ({compression_metrics['compression_efficiency'] * 100:.1f}%)"
    )
    print(
        f"   Unigram compression ratio: {compression_metrics['unigram_compression_ratio']:.2f}"
    )

    # 2. Zipf's law metrics
    zipf_metrics = cheesecloth.get_zipf_metrics(text, False, True)

    print("\n2. Zipf's Law Metrics:")
    print(f"   Zipf fitness score: {zipf_metrics['zipf_fitness_score']:.2f}")
    print(f"   Power law exponent: {zipf_metrics['power_law_exponent']:.2f}")

    # Get token burstiness (if there are frequent tokens)
    unigram_freq = cheesecloth.get_unigram_frequency(text, False, True)
    top_tokens = [
        token
        for token, _ in sorted(unigram_freq.items(), key=lambda x: x[1], reverse=True)[
            :3
        ]
    ]

    if top_tokens:
        burstiness = cheesecloth.calculate_burstiness(text, top_tokens)
        print(f"   Burstiness of top tokens: {burstiness:.2f}")
        print(f"   Top tokens analyzed: {', '.join(top_tokens)}")

    # 3. Vocabulary growth analysis
    chunk_size = min(len(text) // 10, 500)  # Reasonable chunk size
    if chunk_size > 0:
        vocab_growth = cheesecloth.analyze_vocab_growth(text, chunk_size)

        print("\n3. Vocabulary Growth:")
        print(f"   Chunks analyzed: {vocab_growth['chunks_analyzed']}")
        print(
            f"   Average new tokens per chunk: {vocab_growth['average_new_tokens_per_chunk']:.2f}"
        )
        print(
            f"   Final vocabulary size: {vocab_growth['cumulative_vocab_sizes'][-1] if vocab_growth['cumulative_vocab_sizes'] else 0}"
        )

    # 4. Pattern analysis
    print("\n4. Pattern Analysis:")
    print(f"   Copyright mentions: {cheesecloth.count_copyright_mentions(text)}")
    print(f"   Section headings: {cheesecloth.count_section_strings(text)}")
    print(f"   Question strings: {cheesecloth.count_question_strings(text)}")
    print(f"   Contains code: {cheesecloth.contains_code_characters(text)}")
    print(
        f"   Bullet/ellipsis ratio: {cheesecloth.bullet_or_ellipsis_lines_ratio(text):.2f}"
    )

    return {
        "compression": compression_metrics,
        "zipf": zipf_metrics,
        "text_length": len(text),
    }


def compare_text_types():
    """
    Compare different types of text using advanced metrics.
    """
    text_examples = {
        "Natural Language": """
        Natural language processing (NLP) is a subfield of linguistics, computer
        science, and artificial intelligence concerned with the interactions
        between computers and human language. The goal is to enable computers
        to process and analyze large amounts of natural language data. NLP
        combines computational linguistics—rule-based modeling of human language—with
        statistical, machine learning, and deep learning models.
        """,
        "Repetitive Text": "The cat sat on the mat. " * 20,
        "Code Sample": """
        def fibonacci(n):
            if n <= 1:
                return n
            else:
                return fibonacci(n-1) + fibonacci(n-2)
                
        for i in range(10):
            print(f"Fibonacci({i}) = {fibonacci(i)}")
        """,
        "Random Text": "".join([chr(97 + i % 26) for i in range(500)]),
    }

    results = {}

    for name, text in text_examples.items():
        results[name] = analyze_advanced_metrics(text, name)

    # Print comparison summary
    print("\n=== Comparison Summary ===\n")
    print(
        f"{'Text Type':<20} {'Compression Ratio':<20} {'Zipf Fitness':<15} {'Power Law Exp':<15}"
    )
    print("-" * 70)

    for name, metrics in results.items():
        comp_ratio = metrics["compression"]["compression_ratio"]
        zipf_score = metrics["zipf"]["zipf_fitness_score"]
        power_law = metrics["zipf"]["power_law_exponent"]

        print(f"{name:<20} {comp_ratio:<20.2f} {zipf_score:<15.2f} {power_law:<15.2f}")


def analyze_file(filepath: str):
    """
    Analyze a text file using advanced metrics.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        filename = Path(filepath).name
        analyze_advanced_metrics(text, f"File: {filename}")

    except Exception as e:
        print(f"Error analyzing file {filepath}: {e}")


def main():
    """
    Main function handling command line arguments.
    """
    if len(sys.argv) > 1:
        # Analyze a specific file
        analyze_file(sys.argv[1])
    else:
        # Compare different text types
        compare_text_types()


if __name__ == "__main__":
    main()
