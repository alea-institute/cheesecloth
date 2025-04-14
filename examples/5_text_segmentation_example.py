#!/usr/bin/env python3
"""
Text Segmentation Example
========================

This script demonstrates Cheesecloth's text segmentation capabilities,
including line, paragraph, and sentence boundary detection and analysis.

Key Features
-----------

1. Segmentation methods
   - Unicode-based line and paragraph segmentation
   - Sentence boundary detection
   - Structural element identification

2. Segment analysis
   - Length statistics for segments
   - Complexity and variety measures
   - Structural organization metrics

3. Document structure analysis
   - Section and subsection detection
   - Hierarchical document organization
   - Content block identification

Usage
-----
```
python 5_text_segmentation_example.py [text_file]
```

If a text file is provided, the script will analyze that file.
Otherwise, it will analyze sample texts to demonstrate segmentation.
"""

import cheesecloth
import sys
from pathlib import Path
import statistics


def analyze_segmentation(text: str, title: str = "Sample Text"):
    """
    Analyze text using Cheesecloth's segmentation capabilities.
    """
    print(f"\n=== {title} ===\n")
    print(f"Text length: {len(text)} characters\n")

    # 1. Line segmentation
    lines = cheesecloth.segment_lines(text)
    line_lengths = [len(line) for line in lines]

    print("1. Line Segmentation:")
    print(f"   Total lines: {len(lines)}")
    if line_lengths:
        print(
            f"   Average line length: {sum(line_lengths) / len(line_lengths):.1f} characters"
        )
        print(f"   Min line length: {min(line_lengths)} characters")
        print(f"   Max line length: {max(line_lengths)} characters")
        if len(line_lengths) > 1:
            print(f"   Line length variance: {statistics.variance(line_lengths):.1f}")

    # 2. Paragraph segmentation
    paragraphs = cheesecloth.segment_paragraphs(text)
    paragraph_lengths = [len(p) for p in paragraphs]

    print("\n2. Paragraph Segmentation:")
    print(f"   Total paragraphs: {len(paragraphs)}")
    if paragraph_lengths:
        print(
            f"   Average paragraph length: {sum(paragraph_lengths) / len(paragraph_lengths):.1f} characters"
        )
        print(f"   Min paragraph length: {min(paragraph_lengths)} characters")
        print(f"   Max paragraph length: {max(paragraph_lengths)} characters")
        if len(paragraph_lengths) > 1:
            print(
                f"   Paragraph length variance: {statistics.variance(paragraph_lengths):.1f}"
            )

    # 3. Sentence segmentation
    sentences = cheesecloth.segment_sentences(text)
    sentence_lengths = [len(s) for s in sentences]

    print("\n3. Sentence Segmentation:")
    print(f"   Total sentences: {len(sentences)}")
    if sentence_lengths:
        print(
            f"   Average sentence length: {sum(sentence_lengths) / len(sentence_lengths):.1f} characters"
        )
        print(f"   Min sentence length: {min(sentence_lengths)} characters")
        print(f"   Max sentence length: {max(sentence_lengths)} characters")
        if len(sentence_lengths) > 1:
            print(
                f"   Sentence length variance: {statistics.variance(sentence_lengths):.1f}"
            )

    # 4. Word counts per sentence
    sentence_word_counts = [len(cheesecloth.tokenize_unigrams(s)) for s in sentences]

    print("\n4. Words per Sentence:")
    if sentence_word_counts:
        print(
            f"   Average words per sentence: {sum(sentence_word_counts) / len(sentence_word_counts):.1f}"
        )
        print(f"   Min words per sentence: {min(sentence_word_counts)}")
        print(f"   Max words per sentence: {max(sentence_word_counts)}")
        if len(sentence_word_counts) > 1:
            print(
                f"   Word count variance: {statistics.variance(sentence_word_counts):.1f}"
            )

    # 5. Section headers detection
    section_count = cheesecloth.count_section_strings(text)
    print(f"\n5. Section Headers: {section_count}")

    # Show sample of first few segments
    if lines:
        print("\nSample Lines:")
        for i, line in enumerate(lines[:3]):
            if line.strip():
                print(f"   Line {i + 1}: {line[:50]}{'...' if len(line) > 50 else ''}")

    if sentences:
        print("\nSample Sentences:")
        for i, sentence in enumerate(sentences[:3]):
            print(
                f"   Sentence {i + 1}: {sentence[:50]}{'...' if len(sentence) > 50 else ''}"
            )

    return {
        "lines": len(lines),
        "paragraphs": len(paragraphs),
        "sentences": len(sentences),
        "avg_line_length": sum(line_lengths) / len(line_lengths) if line_lengths else 0,
        "avg_paragraph_length": sum(paragraph_lengths) / len(paragraph_lengths)
        if paragraph_lengths
        else 0,
        "avg_sentence_length": sum(sentence_lengths) / len(sentence_lengths)
        if sentence_lengths
        else 0,
        "avg_words_per_sentence": sum(sentence_word_counts) / len(sentence_word_counts)
        if sentence_word_counts
        else 0,
    }


def analyze_segmentation_metrics(text: str, title: str = "Sample Text"):
    """
    Analyze and report advanced segmentation metrics.
    """
    # Get basic segmentation
    segments = {
        "lines": cheesecloth.segment_lines(text),
        "paragraphs": cheesecloth.segment_paragraphs(text),
        "sentences": cheesecloth.segment_sentences(text),
    }

    # Calculate basic metrics from HyperAnalyzer
    analyzer = cheesecloth.HyperAnalyzer(include_punctuation=True, case_sensitive=True)
    analyzer.calculate_all_metrics(text)

    # Calculate additional metrics that aren't included in HyperAnalyzer
    line_count = len(segments["lines"])
    paragraph_count = len(segments["paragraphs"])
    sentence_count = len(segments["sentences"])

    # Calculate average line length
    avg_line_length = 0
    if line_count > 0:
        avg_line_length = sum(len(line) for line in segments["lines"]) / line_count

    # Calculate average paragraph length
    avg_paragraph_length = 0
    if paragraph_count > 0:
        avg_paragraph_length = (
            sum(len(para) for para in segments["paragraphs"]) / paragraph_count
        )

    # Calculate average sentence length
    avg_sentence_length = 0
    if sentence_count > 0:
        avg_sentence_length = (
            sum(len(sent) for sent in segments["sentences"]) / sentence_count
        )

    # Words per line
    words_per_line = []
    for line in segments["lines"]:
        if line.strip():  # Skip empty lines
            words_per_line.append(len(cheesecloth.tokenize_unigrams(line)))

    avg_words_per_line = 0
    if words_per_line:
        avg_words_per_line = sum(words_per_line) / len(words_per_line)

    # Words per sentence
    words_per_sentence = []
    for sentence in segments["sentences"]:
        words_per_sentence.append(len(cheesecloth.tokenize_unigrams(sentence)))

    avg_words_per_sentence = 0
    if words_per_sentence:
        avg_words_per_sentence = sum(words_per_sentence) / len(words_per_sentence)

    # Calculate average lines per paragraph
    # For this we need to recalculate paragraphs as groups of lines
    lines_by_paragraph = []
    current_paragraph_lines = []

    for line in segments["lines"]:
        if line.strip():
            current_paragraph_lines.append(line)
        elif current_paragraph_lines:
            lines_by_paragraph.append(current_paragraph_lines)
            current_paragraph_lines = []

    if current_paragraph_lines:
        lines_by_paragraph.append(current_paragraph_lines)

    avg_lines_per_paragraph = 0
    if lines_by_paragraph:
        avg_lines_per_paragraph = sum(len(para) for para in lines_by_paragraph) / len(
            lines_by_paragraph
        )

    print(f"\n=== Segmentation Metrics for {title} ===\n")

    # Line metrics
    print("Line Metrics:")
    print(f"  Line count: {line_count}")
    print(f"  Average line length: {avg_line_length:.1f} characters")
    print(f"  Average words per line: {avg_words_per_line:.1f}")

    # Paragraph metrics
    print("\nParagraph Metrics:")
    print(f"  Paragraph count: {paragraph_count}")
    print(f"  Average paragraph length: {avg_paragraph_length:.1f} characters")
    print(f"  Average lines per paragraph: {avg_lines_per_paragraph:.1f}")

    # Sentence metrics
    print("\nSentence Metrics:")
    print(f"  Sentence count: {sentence_count}")
    print(f"  Average sentence length: {avg_sentence_length:.1f} characters")
    print(f"  Average words per sentence: {avg_words_per_sentence:.1f}")

    # Structure distribution
    word_counts_by_paragraph = []
    for para in segments["paragraphs"]:
        word_counts_by_paragraph.append(len(cheesecloth.tokenize_unigrams(para)))

    print("\nStructure Distribution:")
    print(
        f"  Most words in a paragraph: {max(word_counts_by_paragraph) if word_counts_by_paragraph else 0}"
    )
    print(
        f"  Fewest words in a paragraph: {min(word_counts_by_paragraph) if word_counts_by_paragraph else 0}"
    )

    # Create custom metrics dictionary to return
    custom_metrics = {
        "line_count": line_count,
        "avg_line_length": avg_line_length,
        "avg_words_per_line": avg_words_per_line,
        "paragraph_count": paragraph_count,
        "avg_paragraph_length": avg_paragraph_length,
        "avg_lines_per_paragraph": avg_lines_per_paragraph,
        "sentence_count": sentence_count,
        "avg_sentence_length": avg_sentence_length,
        "avg_words_per_sentence": avg_words_per_sentence,
    }

    return custom_metrics


def analyze_document_samples():
    """
    Analyze sample documents with different structures.
    """
    samples = {
        "Academic Abstract": """
        We present a novel approach to natural language processing that integrates
        contextual understanding with structural analysis. Our method achieves state-of-the-art
        results on multiple benchmark datasets. Experiments show a 15% improvement over
        existing methods. The implications for information retrieval and machine translation
        are significant and suggest new directions for research in these areas.
        """,
        "Legal Document": """
        SECTION 1. DEFINITIONS
        
        1.1 "Agreement" means this license agreement.
        1.2 "Software" means the computer programs provided under this Agreement.
        1.3 "Licensee" means the individual or entity using the Software.
        
        SECTION 2. GRANT OF LICENSE
        
        Subject to the terms of this Agreement, Licensor grants to Licensee a non-exclusive,
        non-transferable license to use the Software for internal purposes only.
        """,
        "Creative Writing": """
        The rain fell in sheets. Anna watched from the window, her breath fogging the glass.
        
        "Will it ever stop?" she whispered.
        
        Behind her, the clock ticked steadily. Five hours until deadline. Five hours until everything changed.
        
        She turned back to her desk. The manuscript lay open, half-finished. Words had always come easily to her before.
        Not today. Today, they hid from her, elusive as mercury.
        """,
        "Technical Documentation": """
        # Installation Guide
        
        ## System Requirements
        
        * Operating System: Linux, macOS, or Windows 10+
        * RAM: 8GB minimum, 16GB recommended
        * Disk Space: 500MB for installation
        
        ## Setup Process
        
        1. Download the installation package from the official website.
        2. Extract the archive to your desired location.
        3. Run the setup script with administrator privileges.
        4. Follow the on-screen prompts to complete installation.
        """,
    }

    results = {}

    for name, text in samples.items():
        results[name] = analyze_segmentation(text, name)
        analyze_segmentation_metrics(text, name)
        print("\n" + "=" * 50 + "\n")

    # Compare segmentation across document types
    print("\n=== Document Structure Comparison ===\n")
    print(
        f"{'Document Type':<25} {'Sentences':<10} {'Paragraphs':<12} {'Avg Words/Sent':<15}"
    )
    print("-" * 65)

    for doc_type, metrics in results.items():
        print(
            f"{doc_type:<25} {metrics['sentences']:<10} {metrics['paragraphs']:<12} {metrics['avg_words_per_sentence']:<15.1f}"
        )


def analyze_file(filepath: str):
    """
    Analyze segmentation in a text file.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        filename = Path(filepath).name
        analyze_segmentation(text, f"File: {filename}")
        analyze_segmentation_metrics(text, f"File: {filename}")

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
        # Analyze document samples
        analyze_document_samples()


if __name__ == "__main__":
    main()
