# Cheesecloth Implemented Metrics

This document provides a comprehensive list of all metrics implemented in Cheesecloth, organized by category.

## Table of Contents

- [Character Metrics](#character-metrics)
- [Text Segmentation Metrics](#text-segmentation-metrics)
- [Unigram Metrics](#unigram-metrics)
- [Pattern Metrics](#pattern-metrics)
- [Compression Metrics](#compression-metrics)
- [Statistical Distribution Metrics](#statistical-distribution-metrics)
- [Tokenizer Metrics](#tokenizer-metrics)
- [Readability Metrics](#readability-metrics)

## Character Metrics

| Metric Name | Description | Python Method |
|-------------|-------------|---------------|
| Character Count | Total number of characters in the text | `count_chars()` |
| Letter Count | Number of letter characters | `count_letters()` |
| Digit Count | Number of digit characters | `count_digits()` |
| Punctuation Count | Number of punctuation characters | `count_punctuation()` |
| Symbol Count | Number of symbol characters | `count_symbols()` |
| Whitespace Count | Number of whitespace characters | `count_whitespace()` |
| Non-ASCII Count | Number of non-ASCII characters | `count_non_ascii()` |
| Uppercase Count | Number of uppercase characters | `count_uppercase()` |
| Lowercase Count | Number of lowercase characters | `count_lowercase()` |
| Alphanumeric Count | Number of alphanumeric characters | `count_alphanumeric()` |
| ASCII Check | Whether the text is fully ASCII | `is_ascii()` |
| ASCII Ratio | Ratio of ASCII characters to total characters | `ratio_ascii()` |
| Uppercase Ratio | Ratio of uppercase letters to all letters | `ratio_uppercase()` |
| Alphanumeric Ratio | Ratio of alphanumeric characters to total characters | `ratio_alphanumeric()` |
| Alpha to Numeric Ratio | Ratio of alphabetic to numeric characters | `ratio_alpha_to_numeric()` |
| Whitespace Ratio | Ratio of whitespace to total characters | `ratio_whitespace()` |
| Digit Ratio | Ratio of digits to total characters | `ratio_digits()` |
| Punctuation Ratio | Ratio of punctuation to total characters | `ratio_punctuation()` |
| Character Entropy | Shannon entropy of character distribution | `char_entropy()` |
| Character Frequency | Frequency distribution of individual characters | `get_char_frequency()` |
| Character Type Frequency | Frequency distribution of character types | `get_char_type_frequency()` |
| Unicode Category Frequency | Frequency distribution of Unicode categories | `get_unicode_category_frequency()` |
| Unicode Category Group Frequency | Frequency distribution of Unicode category groups | `get_unicode_category_group_frequency()` |
| Unicode Category Bigrams | Bigram frequencies of Unicode categories | `get_unicode_category_bigrams()` |
| Unicode Category Bigram Ratios | Ratio distribution of Unicode category bigrams | `get_unicode_category_bigram_ratios()` |
| Unicode Category Group Bigrams | Bigram frequencies of Unicode category groups | `get_unicode_category_group_bigrams()` |
| Unicode Category Group Bigram Ratios | Ratio distribution of Unicode category group bigrams | `get_unicode_category_group_bigram_ratios()` |
| All Character Metrics | Combined computation of all character metrics | `get_all_char_metrics()` |

## Text Segmentation Metrics

| Metric Name | Description | Python Method |
|-------------|-------------|---------------|
| Word Count | Number of words in the text | `count_words()` |
| Line Count | Number of lines in the text | `count_lines()` |
| Average Line Length | Average number of characters per line | `average_line_length()` |
| Paragraph Count | Number of paragraphs in the text | `count_paragraphs()` |
| Average Paragraph Length | Average number of characters per paragraph | `average_paragraph_length()` |
| Average Word Length | Average number of characters per word | `average_word_length()` |
| Average Sentence Length | Average number of words per sentence | `average_sentence_length()` |
| Split Words | Split text into words using Unicode segmentation rules | `split_words()` |
| Split Lines | Split text into lines | `split_lines()` |
| Segment Lines | Alternative function to split text into lines | `segment_lines()` |
| Split Paragraphs | Split text into paragraphs | `split_paragraphs()` |
| Segment Paragraphs | Alternative function to split text into paragraphs | `segment_paragraphs()` |
| Segment Sentences | Split text into sentences | `segment_sentences()` |

## Unigram Metrics

| Metric Name | Description | Python Method |
|-------------|-------------|---------------|
| Tokenize Unigrams | Split text into unigram tokens (words only) | `tokenize_unigrams()` |
| Tokenize with Punctuation | Split text into tokens including punctuation | `tokenize_unigrams_with_punctuation()` |
| Unigram Count | Total number of unigram tokens | `count_unigram_tokens()` |
| Unique Unigram Count | Number of unique unigram tokens | `count_unique_unigrams()` |
| Type-Token Ratio | Ratio of unique tokens to total tokens | `unigram_type_token_ratio()` |
| Repetition Rate | 1 - type-token ratio | `unigram_repetition_rate()` |
| Unigram Frequency | Frequency distribution of unigram tokens | `get_unigram_frequency()` |
| Unigram Entropy | Shannon entropy of unigram token distribution | `unigram_entropy()` |
| Max Frequency Ratio | Ratio of most frequent token's count to total tokens | `max_unigram_frequency_ratio()` |
| All Unigram Metrics | Combined computation of all unigram metrics | `get_all_unigram_metrics()` |

## Pattern Metrics

| Metric Name | Description | Python Method |
|-------------|-------------|---------------|
| Question Count | Number of question patterns in the text | `count_question_strings()` |
| Interrogative Question Count | Number of interrogative questions | `count_interrogative_questions()` |
| Complex Interrogative Count | Number of complex interrogative patterns | `count_complex_interrogatives()` |
| Factual Statement Count | Number of factual statements | `count_factual_statements()` |
| Logical Reasoning Count | Number of logical reasoning patterns | `count_logical_reasoning()` |
| Section Heading Count | Number of section heading patterns | `count_section_strings()` |
| Copyright Mention Count | Number of copyright mentions | `count_copyright_mentions()` |
| Rights Reserved Count | Number of "rights reserved" mentions | `count_rights_reserved()` |
| Bullet Count | Number of bullet points | `bullet_count` via pattern matching |
| Ellipsis Count | Number of ellipses | `ellipsis_count` via pattern matching |
| Bullet Ellipsis Ratio | Ratio of bullet or ellipsis lines to total lines | `bullet_or_ellipsis_lines_ratio()` |
| Contains Code | Whether the text contains code-like constructs | `contains_code_characters()` |
| Regex Match Count | Generic function to count regex pattern matches | `count_regex_matches()` |
| Contains Regex Pattern | Check if text contains matches for a regex pattern | `contains_regex_pattern()` |
| Contains Blacklist Substring | Check if text contains blacklisted terms | `contains_blacklist_substring()` |
| All Pattern Metrics | Combined computation of all pattern metrics | `get_all_pattern_metrics()` |

## Compression Metrics

| Metric Name | Description | Python Method |
|-------------|-------------|---------------|
| Compression Ratio | Ratio of original text size to compressed size | `compression_ratio()` |
| Unigram Compression Ratio | Compression ratio of word tokens | `unigram_compression_ratio()` |
| All Compression Metrics | Combined computation of all compression metrics | `get_compression_metrics()` |

## Statistical Distribution Metrics

| Metric Name | Description | Python Method |
|-------------|-------------|---------------|
| Zipf Fitness Score | How well the word frequency follows Zipf's law | `zipf_fitness_score()` |
| Power Law Exponent | Exponent of the power law distribution for word frequencies | `power_law_exponent()` |
| Calculate Burstiness | Token burstiness for specific words in text | `calculate_burstiness()` |
| Analyze Vocab Growth | Analysis of vocabulary growth rate in text | `analyze_vocab_growth()` |
| All Zipf Metrics | Combined computation of all Zipf-related metrics | `get_zipf_metrics()` |

## Tokenizer Metrics

| Metric Name | Description | Python Method |
|-------------|-------------|---------------|
| Tokenize ML | Tokenize text using an ML tokenizer | `tokenize_ml()` |
| Batch Tokenize ML | Batch tokenize multiple texts using an ML tokenizer | `batch_tokenize_ml()` |
| Subword Token Count | Count the total number of ML tokenizer tokens | `subword_token_count()` |
| Unique Subword Count | Count the number of unique ML tokenizer tokens | `unique_subword_count()` |
| Subword Type-Token Ratio | Type-token ratio for ML tokenizer tokens | `subword_type_token_ratio()` |
| Subword Repetition Rate | Repetition rate for ML tokenizer tokens | `subword_repetition_rate()` |
| Subword Entropy | Shannon entropy of ML tokenizer token distribution | `subword_entropy()` |
| Subword Efficiency | Tokenization efficiency for ML tokenizer tokens | `subword_efficiency()` |
| All Token Metrics | Combined computation of all ML tokenizer metrics | `get_token_metrics()` |

## Readability Metrics

| Metric Name | Description | Python Method |
|-------------|-------------|---------------|
| Readability Score | Overall readability score (0.0-1.0) | `calculate_readability_score()` |
| Readability Level | Categorical assessment of readability (Easy to Very Complex) | `get_readability_level()` |
| Readability Factors | Detailed breakdown of factors contributing to readability | `get_readability_factors()` |

## Combined Metrics

| Metric Name | Description | Python Method |
|-------------|-------------|---------------|
| All Metrics | Compute all metrics in one efficient pass | `get_all_metrics()` |

## Legacy Functions

These functions have been superseded by more efficient implementations but are maintained for backward compatibility:

| Metric Name | Description | Python Method |
|-------------|-------------|---------------|
| Combined Character Metrics | Older implementation of combined character metrics | `combined_char_metrics()` |
| Get Unicode Categories | Get Unicode category for each character | `get_unicode_categories()` |
| Get Unicode Category Groups | Get Unicode category group for each character | `get_unicode_category_groups()` |
| Count Unicode Categories | Count occurrences of each Unicode category | `count_unicode_categories()` |
| Count Unicode Category Groups | Count occurrences of each Unicode category group | `count_unicode_category_groups()` |
| Get Unicode Category Ratios | Calculate ratio of each Unicode category | `get_unicode_category_ratios()` |
| Get Unicode Category Group Ratios | Calculate ratio of each Unicode category group | `get_unicode_category_group_ratios()` |