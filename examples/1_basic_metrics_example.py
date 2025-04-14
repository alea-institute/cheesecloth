#!/usr/bin/env python3
"""
Basic Text Metrics Example
=========================

This script demonstrates the fundamental text metrics provided by Cheesecloth,
focusing on character, unigram, and structural analysis of text documents.

Key Features
-----------

1. Character metrics
   - Basic counts (total characters, letters, digits, symbols)
   - Character ratios (ASCII ratio, case distributions)
   - Unicode category analysis

2. Unigram metrics (linguistic words)
   - Token counts and type-token ratio
   - Lexical diversity and repetition rate
   - Word-level entropy calculations

3. Text structure
   - Line and paragraph analysis
   - Sentence structure metrics
   - Document composition statistics

Usage
-----
```
python 1_basic_metrics_example.py [text_file]
```

If a text file is provided, the script will analyze that file.
Otherwise, it will analyze sample texts to demonstrate different metrics.
"""

import cheesecloth
import sys
from pathlib import Path


def analyze_text(text, title="Sample Text"):
    """
    Perform basic text analysis using Cheesecloth.
    """
    print(f"\n=== {title} ===\n")

    # Create HyperAnalyzer for comprehensive metrics
    analyzer = cheesecloth.HyperAnalyzer(include_punctuation=True, case_sensitive=True)
    metrics = analyzer.calculate_all_metrics(text)

    # Extract key metrics grouped by category
    char_metrics = {
        "Total Characters": metrics["char_count"],
        "Letters": metrics["letter_count"],
        "Digits": metrics["digit_count"],
        "Punctuation": metrics["punctuation_count"],
        "Symbols": metrics["symbol_count"],
        "Whitespace": metrics["whitespace_count"],
        "Non-ASCII": metrics["non_ascii_count"],
        "ASCII Ratio": f"{metrics['ascii_ratio']:.2%}",
        "Uppercase": metrics["uppercase_count"],
        "Lowercase": metrics["lowercase_count"],
        "Uppercase Ratio": f"{metrics['uppercase_ratio']:.2%}",
        "Character Entropy": f"{metrics['char_entropy']:.2f}",
    }

    unigram_metrics = {
        "Unigram Count": metrics["unigram_count"],
        "Unique Unigrams": metrics["unique_unigram_count"],
        "Type-Token Ratio": f"{metrics['unigram_type_token_ratio']:.2f}",
        "Repetition Rate": f"{metrics['unigram_repetition_rate']:.2f}",
        "Unigram Entropy": f"{metrics['unigram_entropy']:.2f}",
    }

    structural_metrics = {
        "Line Count": metrics["line_count"],
        "Avg Line Length": f"{metrics['avg_line_length']:.1f}",
        "Paragraph Count": metrics["paragraph_count"],
        "Avg Paragraph Length": f"{metrics['avg_paragraph_length']:.1f}",
        "Avg Word Length": f"{metrics['avg_word_length']:.1f}",
        "Avg Sentence Length": f"{metrics['avg_sentence_length']:.1f}",
    }

    # Print formatted metrics
    print("Character Metrics:")
    for name, value in char_metrics.items():
        print(f"  {name:<20}: {value}")

    print("\nUnigram Metrics:")
    for name, value in unigram_metrics.items():
        print(f"  {name:<20}: {value}")

    print("\nStructural Metrics:")
    for name, value in structural_metrics.items():
        print(f"  {name:<20}: {value}")

    # Print most frequent unigrams (top 5)
    if "unigram_frequency" in metrics and metrics["unigram_frequency"]:
        print("\nTop 5 Unigrams:")
        sorted_freq = sorted(
            metrics["unigram_frequency"].items(), key=lambda x: x[1], reverse=True
        )[:5]
        for token, freq in sorted_freq:
            print(f"  {token:<15}: {freq}")

    return metrics


def analyze_file(filepath):
    """
    Read and analyze a text file.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        filename = Path(filepath).name
        analyze_text(text, f"File: {filename}")

    except Exception as e:
        print(f"Error analyzing file {filepath}: {e}")


def analyze_samples():
    """
    Analyze sample texts with different characteristics.
    """
    # Sample 1: Simple text
    simple_text = (
        "This is a simple example text. It has a few sentences. Nothing fancy!"
    )
    analyze_text(simple_text, "Simple Text")

    # Sample 2: More complex text
    complex_text = """
    Natural language processing (NLP) is a subfield of linguistics, computer science, 
    and artificial intelligence concerned with the interactions between computers and 
    human language, in particular how to program computers to process and analyze large 
    amounts of natural language data. The goal is a computer capable of "understanding" 
    the contents of documents, including the contextual nuances of the language within 
    them. The technology can then accurately extract information and insights contained 
    in the documents as well as categorize and organize the documents themselves.
    """
    analyze_text(complex_text, "Complex Text")

    # Sample 3: Multilingual text
    multilingual_text = """
    English: Hello, world!
    Spanish: ¡Hola, mundo!
    French: Bonjour, monde!
    German: Hallo, Welt!
    Russian: Привет, мир!
    Japanese: こんにちは世界！
    Chinese: 你好，世界！
    Arabic: مرحبا بالعالم!
    """
    analyze_text(multilingual_text, "Multilingual Text")


def main():
    """
    Main function to handle command line arguments.
    """
    if len(sys.argv) > 1:
        # Analyze a specific file
        analyze_file(sys.argv[1])
    else:
        # Run sample analyses
        analyze_samples()


if __name__ == "__main__":
    main()
