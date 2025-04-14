//! # Unigram Tokenization and Analysis
//!
//! This module provides functionality for tokenizing text into unigrams (linguistic words)
//! based on Unicode segmentation rules, and analyzing these tokens with various metrics.
//!
//! ## Key Features
//!
//! * Unicode-aware word tokenization
//! * Options for including/excluding punctuation
//! * Token frequency analysis
//! * Lexical diversity metrics (type-token ratio, repetition rate)
//! * Information-theoretic measures (entropy)
//!
//! Unlike subword tokenization used in machine learning models, unigram tokenization
//! follows linguistic word boundaries, making it useful for stylometric analysis,
//! readability assessment, and author identification.

use std::collections::{HashMap, HashSet};
use unicode_segmentation::UnicodeSegmentation;

/// Tokenizes a text into unigram tokens (words and punctuation).
///
/// This function splits text into tokens based on Unicode word boundaries,
/// preserving words, numbers, and punctuation as separate tokens.
///
/// # Arguments
///
/// * `text` - The input text to tokenize
///
/// # Returns
///
/// A vector of string tokens
pub fn tokenize(text: &str) -> Vec<String> {
    // Use unicode_segmentation to split text into words
    let tokens: Vec<String> = UnicodeSegmentation::unicode_words(text)
        .map(|s| s.to_string())
        .collect();

    tokens
}

/// Tokenizes a text into unigram tokens, including words, punctuation, and whitespace.
///
/// Unlike the `tokenize` function, this preserves all characters including punctuation
/// and whitespace as separate tokens, providing a complete representation of the text.
///
/// # Arguments
///
/// * `text` - The input text to tokenize with preservation of all characters
///
/// # Returns
///
/// A vector of string tokens
pub fn tokenize_with_punctuation(text: &str) -> Vec<String> {
    use std::ops::Not;

    // Handle empty text
    if text.is_empty() {
        return Vec::new();
    }

    // A more customized tokenization that separates punctuation from words
    let mut tokens = Vec::new();
    let mut current_token = String::new();
    let mut current_is_punct = None;

    for ch in text.chars() {
        let is_punct = ch.is_ascii_punctuation() || ch.is_whitespace();

        match current_is_punct {
            None => {
                current_token.push(ch);
                current_is_punct = Some(is_punct);
            }
            Some(prev_is_punct) if prev_is_punct == is_punct => {
                // Continue current token if same type
                current_token.push(ch);
            }
            Some(_) => {
                // Switch token type
                if !current_token.is_empty() {
                    tokens.push(current_token);
                    current_token = String::new();
                }
                current_token.push(ch);
                current_is_punct = Some(is_punct);
            }
        }
    }

    // Add the last token if not empty
    if !current_token.is_empty() {
        tokens.push(current_token);
    }

    // If text has period in the middle, further split
    let mut final_tokens = Vec::new();
    for token in tokens {
        if token.len() > 1
            && token.chars().any(|c| c.is_ascii_punctuation())
            && token.chars().any(|c| c.is_ascii_punctuation().not())
        {
            // This is a token that contains both punctuation and non-punctuation
            let mut current = String::new();
            let mut is_punct = None;

            for ch in token.chars() {
                let ch_is_punct = ch.is_ascii_punctuation();

                match is_punct {
                    None => {
                        current.push(ch);
                        is_punct = Some(ch_is_punct);
                    }
                    Some(prev_is_punct) if prev_is_punct == ch_is_punct => {
                        current.push(ch);
                    }
                    Some(_) => {
                        if !current.is_empty() {
                            final_tokens.push(current);
                            current = String::new();
                        }
                        current.push(ch);
                        is_punct = Some(ch_is_punct);
                    }
                }
            }

            if !current.is_empty() {
                final_tokens.push(current);
            }
        } else {
            final_tokens.push(token);
        }
    }

    final_tokens
}

/// Counts the total number of unigram tokens in a text.
///
/// # Arguments
///
/// * `text` - The input text to analyze
/// * `include_punctuation` - Whether to include punctuation in the token count
///
/// # Returns
///
/// The count of tokens in the text
pub fn count_tokens(text: &str, include_punctuation: bool) -> usize {
    if include_punctuation {
        tokenize_with_punctuation(text).len()
    } else {
        tokenize(text).len()
    }
}

/// Counts the number of unique unigram tokens in a text.
///
/// # Arguments
///
/// * `text` - The input text to analyze
/// * `include_punctuation` - Whether to include punctuation in the token count
/// * `case_sensitive` - Whether to treat uppercase and lowercase as different tokens
///
/// # Returns
///
/// The count of unique tokens in the text
pub fn count_unique_tokens(text: &str, include_punctuation: bool, case_sensitive: bool) -> usize {
    let tokens = if include_punctuation {
        tokenize_with_punctuation(text)
    } else {
        tokenize(text)
    };

    let mut unique_tokens = HashSet::new();

    for token in tokens {
        if case_sensitive {
            unique_tokens.insert(token);
        } else {
            unique_tokens.insert(token.to_lowercase());
        }
    }

    unique_tokens.len()
}

/// Calculates the type-token ratio (unique tokens / total tokens) for a text.
///
/// This is a measure of lexical diversity. Higher values indicate more diverse vocabulary.
///
/// # Arguments
///
/// * `text` - The input text to analyze
/// * `include_punctuation` - Whether to include punctuation in the token count
/// * `case_sensitive` - Whether to treat uppercase and lowercase as different tokens
///
/// # Returns
///
/// The type-token ratio (between 0.0 and 1.0)
pub fn type_token_ratio(text: &str, include_punctuation: bool, case_sensitive: bool) -> f64 {
    let tokens = if include_punctuation {
        tokenize_with_punctuation(text)
    } else {
        tokenize(text)
    };

    if tokens.is_empty() {
        return 0.0;
    }

    let total_tokens = tokens.len();
    let unique_count = count_unique_tokens(text, include_punctuation, case_sensitive);

    unique_count as f64 / total_tokens as f64
}

/// Calculates the repetition rate (1 - unique tokens / total tokens) for a text.
///
/// Higher values indicate more repetition in the text.
///
/// # Arguments
///
/// * `text` - The input text to analyze
/// * `include_punctuation` - Whether to include punctuation in the token count
/// * `case_sensitive` - Whether to treat uppercase and lowercase as different tokens
///
/// # Returns
///
/// The repetition rate (between 0.0 and 1.0)
pub fn repetition_rate(text: &str, include_punctuation: bool, case_sensitive: bool) -> f64 {
    let tokens = if include_punctuation {
        tokenize_with_punctuation(text)
    } else {
        tokenize(text)
    };

    // Return 0.0 for empty text (no repetition)
    if tokens.is_empty() {
        return 0.0;
    }

    1.0 - type_token_ratio(text, include_punctuation, case_sensitive)
}

/// Counts the frequency of each token in the text.
///
/// # Arguments
///
/// * `text` - The input text to analyze
/// * `include_punctuation` - Whether to include punctuation in the token count
/// * `case_sensitive` - Whether to treat uppercase and lowercase as different tokens
///
/// # Returns
///
/// A HashMap where keys are tokens and values are occurrence counts
pub fn token_frequency(
    text: &str,
    include_punctuation: bool,
    case_sensitive: bool,
) -> HashMap<String, usize> {
    let tokens = if include_punctuation {
        tokenize_with_punctuation(text)
    } else {
        tokenize(text)
    };

    let mut frequency_map = HashMap::new();

    for token in tokens {
        let key = if case_sensitive {
            token
        } else {
            token.to_lowercase()
        };

        *frequency_map.entry(key).or_insert(0) += 1;
    }

    frequency_map
}

/// Calculates the Shannon entropy of the unigram token distribution.
///
/// This measures the predictability or information content of text.
/// Higher values indicate more unpredictable text with evenly distributed tokens.
///
/// # Arguments
///
/// * `text` - The input text to analyze
/// * `include_punctuation` - Whether to include punctuation in the token count
/// * `case_sensitive` - Whether to treat uppercase and lowercase as different tokens
///
/// # Returns
///
/// The Shannon entropy value
pub fn token_entropy(text: &str, include_punctuation: bool, case_sensitive: bool) -> f64 {
    let frequency = token_frequency(text, include_punctuation, case_sensitive);

    if frequency.is_empty() {
        return 0.0;
    }

    let total_tokens: usize = frequency.values().sum();
    let total_tokens_f64 = total_tokens as f64;

    // Calculate entropy using Shannon's formula: -sum(p_i * log2(p_i))
    let mut entropy = 0.0;
    for &count in frequency.values() {
        let probability = count as f64 / total_tokens_f64;
        entropy -= probability * probability.log2();
    }

    entropy
}

/// Calculates the maximum token frequency ratio in a text.
///
/// This is the ratio of the most common token's frequency to the total token count.
///
/// # Arguments
///
/// * `text` - The input text to analyze
/// * `include_punctuation` - Whether to include punctuation in the token count
/// * `case_sensitive` - Whether to treat uppercase and lowercase as different tokens
///
/// # Returns
///
/// The maximum token frequency ratio (between 0.0 and 1.0)
pub fn max_token_frequency_ratio(
    text: &str,
    include_punctuation: bool,
    case_sensitive: bool,
) -> f64 {
    let frequency = token_frequency(text, include_punctuation, case_sensitive);

    if frequency.is_empty() {
        return 0.0;
    }

    let total_tokens: usize = frequency.values().sum();
    let max_frequency = frequency.values().max().unwrap_or(&0);

    *max_frequency as f64 / total_tokens as f64
}

/// A struct that holds all unigram metrics for efficient calculation.
/// This minimizes passes through the text and improves performance.
pub struct UnigramMetrics {
    pub token_count: usize,
    pub unique_token_count: usize,
    pub type_token_ratio: f64,
    pub repetition_rate: f64,
    pub token_entropy: f64,
    pub max_frequency_ratio: f64,
    pub average_token_length: f64,
    // No longer needed as a field since it's only used during calculation
}

/// Calculates all unigram metrics in a single pass through the text.
///
/// This is significantly more efficient than calling individual metric functions,
/// especially for longer texts, as it minimizes passes and calculations.
///
/// # Arguments
///
/// * `text` - The input text to analyze
/// * `include_punctuation` - Whether to include punctuation in the token count
/// * `case_sensitive` - Whether to treat uppercase and lowercase as different tokens
///
/// # Returns
///
/// A UnigramMetrics struct containing all calculated metrics
pub fn calculate_all_unigram_metrics(
    text: &str,
    include_punctuation: bool,
    case_sensitive: bool,
) -> UnigramMetrics {
    // Get tokens (with or without punctuation)
    let tokens = if include_punctuation {
        tokenize_with_punctuation(text)
    } else {
        tokenize(text)
    };

    // Handle empty text case
    if tokens.is_empty() {
        return UnigramMetrics {
            token_count: 0,
            unique_token_count: 0,
            type_token_ratio: 0.0,
            repetition_rate: 0.0,
            token_entropy: 0.0,
            max_frequency_ratio: 0.0,
            average_token_length: 0.0,
        };
    }

    // Calculate token frequency in a single pass
    let mut frequency_map = HashMap::new();
    let token_count = tokens.len();
    let mut total_token_length = 0;

    for token in tokens {
        total_token_length += token.len();
        let key = if case_sensitive {
            token
        } else {
            token.to_lowercase()
        };

        *frequency_map.entry(key).or_insert(0) += 1;
    }

    let unique_token_count = frequency_map.len();
    let total_tokens_f64 = token_count as f64;

    // Calculate type-token ratio
    let type_token_ratio = unique_token_count as f64 / total_tokens_f64;

    // Calculate repetition rate
    let repetition_rate = 1.0 - type_token_ratio;

    // Calculate entropy
    let mut entropy = 0.0;
    let mut max_frequency = 0;

    for &count in frequency_map.values() {
        if count > max_frequency {
            max_frequency = count;
        }

        let probability = count as f64 / total_tokens_f64;
        entropy -= probability * probability.log2();
    }

    // Calculate max frequency ratio
    let max_frequency_ratio = max_frequency as f64 / total_tokens_f64;

    // Calculate average token length
    let average_token_length = if token_count > 0 {
        total_token_length as f64 / token_count as f64
    } else {
        0.0
    };

    UnigramMetrics {
        token_count,
        unique_token_count,
        type_token_ratio,
        repetition_rate,
        token_entropy: entropy,
        max_frequency_ratio,
        average_token_length,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tokenize() {
        let text = "Hello, world! This is a test.";
        let tokens = tokenize(text);
        assert_eq!(tokens, vec!["Hello", "world", "This", "is", "a", "test"]);
    }

    #[test]
    fn test_tokenize_with_punctuation() {
        let text = "Hello, world!";
        let tokens = tokenize_with_punctuation(text);
        assert_eq!(tokens, vec!["Hello", ",", " ", "world", "!"]);
    }

    #[test]
    fn test_count_tokens() {
        let text = "Hello, world! This is a test.";
        assert_eq!(count_tokens(text, false), 6);
        assert_eq!(count_tokens(text, true), 14); // Including punctuation and spaces as separate tokens
    }

    #[test]
    fn test_count_unique_tokens() {
        let text = "The cat and the dog. The cat ran.";
        // Without punctuation, case insensitive
        assert_eq!(count_unique_tokens(text, false, false), 5); // the, cat, and, dog, ran
                                                                // With punctuation, case insensitive
        assert_eq!(count_unique_tokens(text, true, false), 7); // includes ".", " " and punctuation
                                                               // Without punctuation, case sensitive
        assert_eq!(count_unique_tokens(text, false, true), 6); // "The" and "the" are different
    }

    #[test]
    fn test_type_token_ratio() {
        let text = "The cat and the dog. The cat ran.";
        // 5 unique tokens / 8 total tokens = 0.625
        let ratio = type_token_ratio(text, false, false);
        assert!((ratio - 0.625).abs() < 1e-10);
    }

    #[test]
    fn test_repetition_rate() {
        let text = "The cat and the dog. The cat ran.";
        // 1 - (5 unique tokens / 8 total tokens) = 0.375
        let rate = repetition_rate(text, false, false);
        assert!((rate - 0.375).abs() < 1e-10);
    }

    #[test]
    fn test_token_frequency() {
        let text = "The cat and the dog. The cat ran.";
        let frequency = token_frequency(text, false, false);

        assert_eq!(frequency.get("the").unwrap(), &3);
        assert_eq!(frequency.get("cat").unwrap(), &2);
        assert_eq!(frequency.get("dog").unwrap(), &1);
    }

    #[test]
    fn test_token_entropy() {
        // For a text with uniform distribution (all tokens different), entropy is log2(n)
        let text = "one two three four five";
        let entropy = token_entropy(text, false, true);
        assert!((entropy - 2.32192809489).abs() < 1e-8); // log2(5) = 2.32192809489

        // For a text with all the same token, entropy is 0
        let uniform_text = "one one one one one";
        let uniform_entropy = token_entropy(uniform_text, false, true);
        assert!(uniform_entropy.abs() < 1e-10);
    }

    #[test]
    fn test_max_token_frequency_ratio() {
        let text = "The cat and the dog. The cat ran.";
        // "the" appears 3 times out of 8 tokens
        let ratio = max_token_frequency_ratio(text, false, false);
        assert!((ratio - 0.375).abs() < 1e-10);
    }
}
