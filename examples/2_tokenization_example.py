#!/usr/bin/env python3
"""
Tokenization and Token Analysis Example
=====================================

This script demonstrates Cheesecloth's tokenization capabilities,
comparing different tokenization approaches (unigram and machine learning)
and analyzing their metrics.

Key Features
-----------

1. Unigram tokenization
   - Linguistic word boundary detection using Unicode segmentation
   - Natural language tokenization with/without punctuation
   - Word-level statistics and frequency analysis

2. ML tokenizer integration
   - Support for popular ML tokenizers (GPT-2, BERT, etc.)
   - Subword token analysis
   - Comparison between different tokenizers

3. Token-based metrics
   - Type-token ratio and repetition rate
   - Token entropy
   - Tokenization efficiency

Usage
-----
```
python 2_tokenization_example.py [text_file]
```

If a text file is provided, the script will analyze that file with multiple tokenizers.
Otherwise, it will analyze sample texts to demonstrate different tokenization approaches.
"""

import cheesecloth
import sys
from pathlib import Path


def compare_tokenization_approaches(text: str, title: str = "Sample Text"):
    """
    Compare different tokenization approaches on the same text.
    """
    print(f"\n=== {title} ===\n")
    print(f"Text: {text[:100]}{'...' if len(text) > 100 else ''}")
    print(f"Length: {len(text)} characters\n")

    # 1. Unigram tokenization (linguistic words)
    unigram_tokens = cheesecloth.tokenize_unigrams(text)
    unigram_tokens_with_punct = cheesecloth.tokenize_unigrams_with_punctuation(text)

    print("1. Unigram Tokenization (linguistic words):")
    print(f"   Without punctuation: {len(unigram_tokens)} tokens")
    print(f"   With punctuation: {len(unigram_tokens_with_punct)} tokens")
    print(f"   Sample tokens: {', '.join(unigram_tokens[:5])}")

    # 2. Unigram metrics
    unigram_type_token_ratio = cheesecloth.unigram_type_token_ratio(text, False, True)
    unigram_repetition_rate = cheesecloth.unigram_repetition_rate(text, False, True)
    unigram_entropy = cheesecloth.unigram_entropy(text, False, True)

    print("\n   Unigram Metrics:")
    print(f"   Type-token ratio: {unigram_type_token_ratio:.2f}")
    print(f"   Repetition rate: {unigram_repetition_rate:.2f}")
    print(f"   Entropy: {unigram_entropy:.2f}")

    # Get top unigram frequencies
    unigram_freq = cheesecloth.get_unigram_frequency(text, False, True)
    top_unigrams = sorted(unigram_freq.items(), key=lambda x: x[1], reverse=True)[:5]

    print("\n   Top Unigrams:")
    for token, freq in top_unigrams:
        print(f"     {token}: {freq}")

    # 3. ML-based tokenization (try different tokenizers)
    tokenizers = ["gpt2", "bert-base-uncased"]

    for tokenizer_name in tokenizers:
        try:
            # Try tokenizing with this ML tokenizer
            token_ids = cheesecloth.tokenize_ml(text, tokenizer_name)
            token_count = len(token_ids)
            unique_token_count = len(set(token_ids))
            type_token_ratio = (
                unique_token_count / token_count if token_count > 0 else 0
            )

            print(f"\n2. ML Tokenization ({tokenizer_name}):")
            print(f"   Token count: {token_count}")
            print(f"   Unique tokens: {unique_token_count}")
            print(f"   Type-token ratio: {type_token_ratio:.2f}")
            print(f"   First 5 token IDs: {token_ids[:5]}")

            # Get more metrics if available
            try:
                token_metrics = cheesecloth.get_token_metrics(text, tokenizer_name)
                print(
                    f"   Subword entropy: {token_metrics.get('subword_entropy', 'N/A')}"
                )
                print(
                    f"   Tokenization efficiency: {token_metrics.get('subword_efficiency', 'N/A')}"
                )
            except Exception as e:
                print(f"   Note: Additional token metrics unavailable: {e}")

        except Exception as e:
            print(f"\n2. ML Tokenization ({tokenizer_name}):")
            print(f"   Error: {e}")

    print("\n3. Tokenization Comparison:")
    print(f"   Unigram tokens: {len(unigram_tokens)}")
    print(
        f"   GPT-2 tokens: {len(cheesecloth.tokenize_ml(text, 'gpt2')) if 'gpt2' in tokenizers else 'N/A'}"
    )
    print(
        f"   BERT tokens: {len(cheesecloth.tokenize_ml(text, 'bert-base-uncased')) if 'bert-base-uncased' in tokenizers else 'N/A'}"
    )


def analyze_file(filepath: str):
    """
    Read and analyze a text file with different tokenization approaches.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        filename = Path(filepath).name
        compare_tokenization_approaches(text, f"File: {filename}")

    except Exception as e:
        print(f"Error analyzing file {filepath}: {e}")


def analyze_samples():
    """
    Analyze sample texts with different tokenization characteristics.
    """
    # Sample 1: Simple English
    simple_text = (
        "This is a simple example text. It has a few sentences. Nothing fancy!"
    )
    compare_tokenization_approaches(simple_text, "Simple English Text")

    # Sample 2: Text with uncommon words and compounds
    complex_text = "The supercalifragilisticexpialidocious antidisestablishmentarianism of the electroencephalographically-monitored subjects demonstrated pseudopseudohypoparathyroidism."
    compare_tokenization_approaches(complex_text, "Text with Uncommon Words")

    # Sample 3: Multilingual text (to show how tokenizers handle different languages)
    multilingual_text = "English: Hello world! Español: ¡Hola mundo! Français: Bonjour le monde! Deutsch: Hallo Welt! 日本語: こんにちは世界!"
    compare_tokenization_approaches(multilingual_text, "Multilingual Text")

    # Sample 4: Code-mixed text
    code_mixed_text = "function sayHello() { console.log('Hello, world!'); } // This is a JavaScript function that prints 'Hello, world!'"
    compare_tokenization_approaches(code_mixed_text, "Code-Mixed Text")


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
