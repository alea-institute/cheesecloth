"""
Cheesecloth: High-Performance Text Analysis Library
==================================================

Cheesecloth is a comprehensive text analysis library that combines high-performance
Rust implementations with Python bindings to provide fast and thorough text metrics
for data science, natural language processing, and corpus analysis.

Core Components
--------------

1. Character-level Analysis
   - Character counts, ratios, and distributions
   - Unicode category classification and analysis
   - ASCII/non-ASCII metrics

2. Word-level Analysis (Unigrams)
   - Linguistic word tokenization based on Unicode boundaries
   - Type-token ratio, repetition rates, and entropy
   - Word frequency analysis

3. ML Tokenizer Analysis
   - Support for Hugging Face tokenizers
   - Subword token metrics for machine learning applications
   - Tokenization efficiency metrics

4. Text Structure Analysis
   - Line, paragraph, and sentence segmentation
   - Document structure metrics

5. Information Theory and Statistics
   - Compression-based analysis
   - Zipf's law and power law distributions
   - Burstiness and vocabulary growth metrics

6. Data Processing Utilities
   - Batch processing for large datasets
   - Support for various input formats (text, JSONL, Hugging Face datasets)
   - Efficient parallel processing

High-Performance Architecture
----------------------------

Cheesecloth is built with a dual-approach architecture:

1. BatchProcessor: For selective computation of specific metrics
2. HyperAnalyzer: For high-performance computation of all metrics in a single pass

Both approaches provide batch processing capabilities for efficient analysis of
large text corpora, with optimized implementations in Rust.

Example Usage
-----------

Basic character metrics:
```python
import cheesecloth
text = "Hello, world!"
print(cheesecloth.count_chars(text))  # 13
print(cheesecloth.is_ascii(text))     # True
```

HyperAnalyzer for comprehensive metrics:
```python
analyzer = cheesecloth.HyperAnalyzer(include_punctuation=True, case_sensitive=True)
metrics = analyzer.calculate_all_metrics("Hello, world!")
print(metrics["char_count"])        # 13
print(metrics["unigram_count"])     # 3
```

Processing a batch of texts:
```python
texts = ["First example.", "Second example with more words.", "Third!"]
results = analyzer.calculate_batch_metrics(texts)
for i, metrics in enumerate(results):
    print(f"Text {i+1} has {metrics['char_count']} characters")
```
"""

# Import all Rust binding functions
from .cheesecloth import *

# Import data loading and processing utilities
from .data import (
    TextDataLoader,
    TextBatchProcessor,
    TokenizerWrapper,
    process_text_file,
    process_jsonl_file,
    process_huggingface_dataset,
)

# Import tokenized metrics utilities
from .tokenized_metrics import (
    TokenizedAnalyzer,
    calculate_token_metrics,
    process_tokenized_text,
    process_tokenized_batch,
    process_tokenized_data,
)

# Add version number
__version__ = "0.1.0"

# Ensure docstring is properly set
__doc__ = __doc__ or cheesecloth.__doc__

# Update __all__ to include Python module additions
if hasattr(cheesecloth, "__all__"):
    __all__ = cheesecloth.__all__ + [
        # Data processing
        "TextDataLoader",
        "TextBatchProcessor",
        "TokenizerWrapper",
        "process_text_file",
        "process_jsonl_file",
        "process_huggingface_dataset",
        # Tokenized metrics
        "TokenizedAnalyzer",
        "calculate_token_metrics",
        "process_tokenized_text",
        "process_tokenized_batch",
        "process_tokenized_data",
    ]
