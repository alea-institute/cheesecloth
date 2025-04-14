## Comprehensive Text Corpus Metrics & Filters Overview

This document provides a complete, detailed inventory of metrics and filters used in large-scale text corpora quality assessment. Each metric includes clear categorization and references to significant projects.

### Character-Level Metrics

| Metric                   | Description                         | Complexity | Category           | Example Projects        |
| ------------------------ | ----------------------------------- | ---------- | ------------------ | ----------------------- |
| `total_characters`       | Total number of characters          | Low        | Length             | General                 |
| `whitespace_count`       | Number of whitespace characters     | Low        | Composition        | General                 |
| `ratio_whitespace`       | Proportion of whitespace characters | Low        | Composition        | MassiveText             |
| `alphanumeric_count`     | Alphanumeric characters count       | Low        | Composition        | General                 |
| `ratio_alphanumeric`     | Ratio of alphanumeric characters    | Low        | Composition        | C4, MassiveText         |
| `alpha_count`            | Alphabetic character count          | Low        | Composition        | General                 |
| `digit_count`            | Digit character count               | Low        | Composition        | General                 |
| `ratio_alpha_to_numeric` | Alphabetic-to-digit character ratio | Low        | Composition        | General                 |
| `non_alphanumeric_count` | Non-alphanumeric character count    | Low        | Composition        | General                 |
| `non_ascii_count`        | Non-ASCII character count           | Low        | Encoding Quality   | C4, MassiveText         |
| `ratio_non_ascii`        | Proportion non-ASCII characters     | Low        | Encoding Quality   | C4, MassiveText         |
| `capital_count`          | Capital letters count               | Low        | Composition        | General                 |
| `ratio_capital`          | Proportion capital letters          | Low        | Composition        | General                 |
| `digit_ratio`            | Digit proportion                    | Low        | Composition        | General                 |
| `punctuation_count`      | Punctuation count                   | Low        | Composition        | General                 |
| `ratio_punctuation`      | Punctuation proportion              | Low        | Composition        | MassiveText             |
| `char_entropy`           | Shannon entropy of characters       | Medium     | Information Theory | CCNet, Gigaword Corpora |

### Word-Level Metrics

| Metric                     | Description                       | Complexity | Category   | Example Projects |
| -------------------------- | --------------------------------- | ---------- | ---------- | ---------------- |
| `num_words`                | Total words count                 | Low        | Length     | General          |
| `average_word_length`      | Mean characters per word          | Low        | Complexity | MassiveText      |
| `num_lines`                | Total lines count                 | Low        | Structure  | General          |
| `average_line_length`      | Mean characters per line          | Low        | Structure  | MassiveText      |
| `num_paragraphs`           | Paragraph count (heuristic-based) | Low        | Structure  | General          |
| `average_paragraph_length` | Mean characters per paragraph     | Low        | Structure  | General          |
| `avg_sentence_length`      | Average tokens per sentence       | Low        | Complexity | General          |

### Unigram Token Metrics (Word/Punctuation-level)

| Metric                        | Description                          | Complexity | Category           | Example Projects        |
| ----------------------------- | ------------------------------------ | ---------- | ------------------ | ----------------------- |
| `unigram_token_count`         | Total word/punctuation token count   | Low        | Tokenization       | General                 |
| `unique_unigram_count`        | Unique words/punctuation count       | Medium     | Lexical Diversity  | General                 |
| `unigram_type_token_ratio`    | Word-level lexical diversity         | Medium     | Lexical Diversity  | CCNet, Gigaword Corpora |
| `unigram_entropy`             | Word distribution Shannon entropy    | Medium     | Information Theory | CCNet, Gigaword Corpora |
| `max_unigram_frequency_ratio` | Most common word proportion          | Medium     | Lexical Diversity  | General                 |
| `unigram_repetition_rate`     | Word repetition (1-unique/total)     | Medium     | Lexical Diversity  | C4, MassiveText         |

### Subword Token Metrics (BPE/WordPiece)

| Metric                       | Description                       | Complexity | Category           | Example Projects        |
| ---------------------------- | --------------------------------- | ---------- | ------------------ | ----------------------- |
| `subword_token_count`        | Total ML-tokenizer token count    | Low        | Tokenization       | General                 |
| `unique_subword_count`       | Unique subword tokens count       | Medium     | Lexical Diversity  | General                 |
| `subword_type_token_ratio`   | Subword-level lexical diversity   | Medium     | Lexical Diversity  | CCNet, Gigaword Corpora |
| `subword_entropy`            | Subword token Shannon entropy     | Medium     | Information Theory | CCNet, Gigaword Corpora |
| `subword_repetition_rate`    | Subword repetition (1-unique/total)| Medium     | Lexical Diversity  | C4, MassiveText         |
| `subword_efficiency`         | Information per subword length    | Medium     | Tokenization Efficiency | Proposed        |

### Format & Special Token Metrics

| Metric                  | Description                      | Complexity | Category            | Example Projects |
| ----------------------- | -------------------------------- | ---------- | ------------------- | ---------------- |
| `num_nospace_bigrams`   | Problematic bigram tokens count  | Medium     | Tokenization Issues | General          |
| `ratio_nospace_bigrams` | Proportion problematic bigrams   | Medium     | Tokenization Issues | General          |
| `num_format_tokens`     | Formatting tokens count          | Medium     | Tokenization Issues | General          |
| `ratio_format_tokens`   | Proportion formatting tokens     | Medium     | Tokenization Issues | General          |
| `startswith_begin`      | Starts with specific begin token | Low        | Format Compliance   | General          |

### Content Indicator Metrics

| Metric                 | Description                      | Complexity | Category           | Example Projects |
| ---------------------- | -------------------------------- | ---------- | ------------------ | ---------------- |
| `num_copyright`        | Copyright mentions count         | Low        | Content Filtering  | General          |
| `num_rights_reserved`  | "Rights reserved" mentions count | Low        | Content Filtering  | General          |
| `num_section_strings`  | Section headings count           | Medium     | Structural Content | General          |
| `num_question_strings` | Question phrases count           | Medium     | Structural Content | General          |

### Quality & Statistical Filters

| Filter                           | Description                                   | Complexity | Category              | Example Projects |
| -------------------------------- | --------------------------------------------- | ---------- | --------------------- | ---------------- |
| `contains_blacklist_substring`   | Presence of blacklisted substrings            | Low        | Heuristic Filtering   | C4, MassiveText  |
| `code_characters_presence`       | Presence of code-specific chars (`{}`, `</>`) | Low        | Heuristic Filtering   | C4               |
| `stopword_ratio`                 | Presence of common stopwords                  | Low        | Linguistic Quality    | C4, MassiveText  |
| `min_sentence_count`             | Minimum sentence count threshold              | Low        | Structure Filtering   | C4               |
| `terminal_punctuation`           | Lines ending punctuation check                | Low        | Structural Filtering  | C4               |
| `symbol_to_word_ratio`           | Excessive symbols relative to words           | Low        | Composition Filtering | MassiveText      |
| `duplicate_line_fraction`        | Fraction of duplicate lines/n-grams           | Medium     | Repetition Filtering  | C4, MassiveText  |
| `bullet_or_ellipsis_lines_ratio` | Fraction of bullet or ellipsis lines          | Low        | Structural Filtering  | MassiveText      |
| `mean_word_length`               | Threshold-based mean word length              | Low        | Linguistic Quality    | MassiveText      |
| `alpha_ratio`                    | Proportion alphabetic characters              | Low        | Composition Filtering | MassiveText      |
| `language_id_confidence`         | Confidence in language identification         | Medium     | Language Filtering    | C4, MassiveText  |

### Advanced & Proposed Metrics

| Metric               | Description                       | Complexity | Category                 | Example Projects |
| -------------------- | --------------------------------- | ---------- | ------------------------ | ---------------- |
| `compression_ratio`  | Original-to-compressed text ratio | Medium     | Information Density      | Proposed         |
| `zipf_fitness_score` | Adherence to Zipf's law           | Medium     | Linguistic Naturalness   | Proposed         |
| `burstiness`         | Clustering of token occurrences   | Medium     | Structural Patterns      | Proposed         |
| `kl_divergence`      | Divergence from reference corpus  | Medium     | Domain Specificity       | Proposed         |
| `token_cooccurrence` | Token collocation statistics      | High       | Lexical Patterns         | Proposed         |
| `subword_efficiency` | Information per subword length    | Medium     | Tokenization Efficiency  | Proposed         |
| `lm_perplexity`      | Language model perplexity         | High       | Fluency & Predictability | CCNet, MC4       |
| `vocab_growth_rate`  | Rate of vocabulary introduction   | Medium     | Lexical Diversity        | Proposed         |

