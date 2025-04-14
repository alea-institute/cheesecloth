# Cheesecloth

**Cheesecloth is a high-performance text analysis toolkit for filtering large-scale corpora using statistical properties
of character, unigram, and token metrics.**

Our primary goals are:

1. Provide low-latency curation and filtering of LLM pretraining datasets, allowing for real-time filtering of data
   during training or inference pipeline
2. Support empirical research on text corpora characteristics and quality assessment

For a list of all metrics tracked and implemented, see [docs/METRICS.md](docs/METRICS.md).

## Development Roadmap

Cheesecloth development follows a phased approach:

1. **Phase 1 (Complete)**: Building underlying calculations and metrics implementation
    - Comprehensive suite of 100+ text metrics from character-level to advanced statistical measures
    - High-performance Rust core with Python bindings
    - CLI tools for dataset analysis

2. **Phase 2 (In Progress)**: Statistical analysis over 1T token sample from KL3M Data Project
    - Establish empirical baselines for text quality metrics across diverse domains
    - Identify statistical patterns and correlations between metrics and content quality
    - Publication of research findings (see citation below)

3. **Phase 3 (Pending)**: Implementing filters based on empirical results
    - Develop configurable filtering pipelines based on Phase 2 findings
    - Create intelligent, adaptive filtering mechanisms for streaming data
    - Release production-ready tools for large-scale text corpus management

## Current Status

Cheesecloth is currently in Phase 2 of development:

- Core metrics implementation is complete and stable
- Python API and CLI tools are available for use
- Calculation on KL3M Data Project and other samples in progress

## 🌟 Features

- **Corpus Filtering**: Statistical methods for efficiently filtering large-scale text corpora
- **High Performance**: Core algorithms implemented in Rust for maximum speed and throughput
- **Comprehensive Metrics**: 100+ metrics from character-level to advanced statistical measures
- **Flexible APIs**: Both high-level convenience functions and low-level customizable components
- **LLM Integration**: Support for machine learning tokenizers (GPT-2, BERT, etc.)
- **Statistical Analysis**: Tools for analyzing metric distributions across corpus samples
- **Minimal Dependencies**: Lightweight core with optional integrations

## 📦 Installation

```bash
pip install cheesecloth
```

## 🚀 Examples

Cheesecloth offers two primary ways to analyze text data:

1. Python API for programmatic access and custom analysis workflows
2. Command-line interface (CLI) for analyzing files and datasets at scale

### Example 1: Character and Unigram Metrics with Python

```python
import cheesecloth

# Sample text to analyze
text = "The quick brown fox jumps over the lazy dog! 123 + πр漢字"

# Get all character metrics at once (most efficient)
char_metrics = cheesecloth.get_all_char_metrics(text)

# Display basic character counts
print(f"Character count: {char_metrics['char_count']}")
print(f"Letters: {char_metrics['letter_count']}")
print(f"Digits: {char_metrics['digit_count']}")
print(f"Symbols: {char_metrics['symbol_count']}")
print(f"Whitespace: {char_metrics['whitespace_count']}")
print(f"ASCII ratio: {char_metrics['ascii_ratio']:.2f}")
print(f"Character entropy: {char_metrics['char_entropy']:.2f}")

# Get all unigram (word) metrics
unigram_metrics = cheesecloth.get_all_unigram_metrics(text, include_punctuation=False, case_sensitive=False)

print("\nUnigram metrics:")
print(f"Token count: {unigram_metrics['token_count']}")
print(f"Unique token count: {unigram_metrics['unique_token_count']}")
print(f"Type-token ratio: {unigram_metrics['type_token_ratio']:.2f}")
print(f"Token entropy: {unigram_metrics['token_entropy']:.2f}")
```

### Example 1B: Advanced Metrics - Zipf's Law and Compression

```python
import cheesecloth

# Longer text sample for meaningful statistical analysis
text = """
Natural language processing (NLP) is a subfield of linguistics, computer 
science, and artificial intelligence concerned with the interactions between 
computers and human language. The goal is to enable computers to process 
and analyze large amounts of natural language data. NLP combines computational 
linguistics with statistical, machine learning, and deep learning models.
"""

# Check Zipf's law fitness (how well word frequency follows Zipf's distribution)
zipf_metrics = cheesecloth.get_zipf_metrics(text, include_punctuation=False, case_sensitive=True)
print(f"Zipf fitness score: {zipf_metrics['zipf_fitness_score']:.2f}")
print(f"Power law exponent: {zipf_metrics['power_law_exponent']:.2f}")

# Compression-based metrics (measures text complexity and redundancy)
compression_metrics = cheesecloth.get_compression_metrics(text)
print(f"\nCompression ratio: {compression_metrics['compression_ratio']:.2f}")
print(f"Normalized compression ratio: {compression_metrics['normalized_compression_ratio']:.2f}")
print(f"Compression efficiency: {compression_metrics['compression_efficiency']:.2f}")

# Content pattern detection
print(f"\nContains code characters: {cheesecloth.contains_code_characters(text)}")
print(f"Copyright mentions: {cheesecloth.count_copyright_mentions(text)}")
print(f"Section headings: {cheesecloth.count_section_strings(text)}")
print(f"Question strings: {cheesecloth.count_question_strings(text)}")

# Analyze burstiness (clustering of frequent terms)
# Get most common words for burstiness analysis
unigram_freq = cheesecloth.get_unigram_frequency(text, include_punctuation=False, case_sensitive=False)
top_words = [word for word, _ in sorted(unigram_freq.items(), key=lambda x: x[1], reverse=True)[:3]]
burstiness = cheesecloth.calculate_burstiness(text, top_words)
print(f"Burstiness of top words: {burstiness:.2f}")
```

### Example 2: Using the CLI on Data Files and Datasets

Cheesecloth's CLI provides several ways to analyze text data. Here are some common use cases:

#### Local JSONL.GZ file:

```bash
uv run python3 -m cheesecloth.cli data/usc-1000.jsonl.gz
```

This command will:

1. Automatically detect and decompress the JSONL.GZ file
2. Extract text content from each JSON record
3. Calculate comprehensive text metrics for each record
4. Save the results to a JSONL file named after the input file

#### Hugging Face dataset:

```bash
uv run python3 -m cheesecloth.cli imdb --text-column text
```

This command will:

1. Load the IMDB dataset from Hugging Face
2. Extract text from the "text" column of each record
3. Calculate text metrics for each example
4. Save analysis results to a file named "imdb_train_stats.jsonl"

#### Pre-tokenized data with a tokenizer:

```bash
uv run python3 -m cheesecloth.cli alea-institute/kl3m-data-usc-sample --token-field tokens --tokenizer-name alea-institute/kl3m-004-128k-cased
```

This command will:

1. Load a dataset with pre-tokenized content
2. Use the specified tokenizer to decode tokens into text
3. Analyze the decoded text content
4. Save metrics to a file with the dataset name

The output file for all these commands will contain three types of records:

- A metadata record with information about the dataset and metrics
- Individual example records with metrics for each document
- A summary record with aggregated statistics across all documents

You can customize the analysis with various options:

```bash
# Analyze specific metrics (space-separated group names)
uv run python3 -m cheesecloth.cli data/usc-1000.jsonl.gz --include-groups basic entropy

# Specify the text field to analyze
uv run python3 -m cheesecloth.cli data/usc-1000.jsonl.gz --text-column content

# Limit the number of examples
uv run python3 -m cheesecloth.cli data/usc-1000.jsonl.gz --limit 100

# Use optimized analyzer for faster processing
uv run python3 -m cheesecloth.cli data/usc-1000.jsonl.gz --use-hyper
```

Available metric groups include:

- `basic`: Character count and word count
- `char_type`: Letter, digit, punctuation, symbol, whitespace counts
- `ratios`: ASCII ratio, uppercase ratio, whitespace ratio, etc.
- `entropy`: Character and unigram entropy
- `segmentation`: Line and paragraph counts and lengths
- `frequency`: Character and unicode category frequencies
- `unigram`: Word-level metrics (count, unique, TTR, etc.)

You can use `--include-groups all` (default) to include all metrics or exclude specific groups with
`--exclude-groups frequency` to avoid large output files.

## 📋 Documentation

For more information, check out the documentation in the [docs](docs/) directory,
particularly [OUTLINE.md](docs/METRICS) for a complete list of available metrics.


## Citation

If you use Cheesecloth in your research, please cite the KL3M Data Project for now:

```bibtex
@misc{bommarito2025kl3mdata,
  title={The KL3M Data Project: Copyright-Clean Training Resources for Large Language Models},
  author={Bommarito II, Michael J. and Bommarito, Jillian and Katz, Daniel Martin},
  year={2025},
  eprint={2504.07854},
  archivePrefix={arXiv},
  primaryClass={cs.CL}
}
```

## 🤝 Contributing

We welcome contributions to Cheesecloth! As we move through our development phases, there are many opportunities to
help:

- Phase 1: Implementing additional metrics and optimizing existing ones
- Phase 2: Running analysis on diverse text samples and interpreting results
- Phase 3: Developing filter pipelines and text quality assessment models

See [DEVELOPING.md](DEVELOPING.md) for development setup instructions.

## 📜 License

Cheesecloth is distributed under the MIT License. See LICENSE for more information.

## 🔬 Research

Cheesecloth is an [ALEA Institute](https://aleainstitute.ai) Project. The statistical methods and findings from this
project will be published as part of our ongoing research into high-quality, copyright-clean training resources for
large language models.