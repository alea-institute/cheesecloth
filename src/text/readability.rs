//! # Readability
//!
//! A composite readability score in `[0, 1]` (higher = harder to read), built
//! from four normalised factors:
//!
//! | Factor | Raw value | Normalisation | Weight |
//! |---|---|---|---|
//! | word complexity | average unigram token length (code points) | `min(1, x / 10)` | 0.25 |
//! | sentence complexity | average sentence length (words) | `min(1, x / 50)` | 0.35 |
//! | paragraph complexity | average paragraph length (chars) | `min(1, x / 800)` | 0.15 |
//! | vocabulary complexity | unigram token entropy (bits) | `min(1, x / 8)` | 0.25 |
//!
//! This is the same formula as the Python `AllMetrics.calculate_readability_score()`
//! wrapper, computed directly from text without building the full metrics dict.
//!
//! The sentence factor uses the library's existing terminator-based
//! [`segmentation::average_sentence_length`]. Callers that already have a
//! better sentence segmentation can pass their own average sentence length
//! instead via `average_sentence_length_override`.

use crate::text::segmentation;
use crate::unigram;

/// Weight of the word-length factor
pub const WORD_LENGTH_WEIGHT: f64 = 0.25;
/// Weight of the sentence-length factor
pub const SENTENCE_LENGTH_WEIGHT: f64 = 0.35;
/// Weight of the paragraph-length factor
pub const PARAGRAPH_LENGTH_WEIGHT: f64 = 0.15;
/// Weight of the token-entropy factor
pub const ENTROPY_WEIGHT: f64 = 0.25;

/// Raw inputs, normalised factors, score and level for one text
#[derive(Debug, Clone, PartialEq)]
pub struct ReadabilityAssessment {
    pub average_token_length: f64,
    pub average_sentence_length: f64,
    pub average_paragraph_length: f64,
    pub token_entropy: f64,
    pub norm_word_length: f64,
    pub norm_sentence_length: f64,
    pub norm_paragraph_length: f64,
    pub norm_entropy: f64,
    pub score: f64,
    pub level: &'static str,
}

/// Map a readability score onto its categorical level
pub fn readability_level(score: f64) -> &'static str {
    if score < 0.3 {
        "Easy"
    } else if score < 0.5 {
        "Moderate"
    } else if score < 0.7 {
        "Challenging"
    } else if score < 0.85 {
        "Complex"
    } else {
        "Very Complex"
    }
}

/// Combine the four raw factor values into a full assessment
pub fn assess_from_factors(
    average_token_length: f64,
    average_sentence_length: f64,
    average_paragraph_length: f64,
    token_entropy: f64,
) -> ReadabilityAssessment {
    let norm_word_length = (average_token_length / 10.0).min(1.0);
    let norm_sentence_length = (average_sentence_length / 50.0).min(1.0);
    let norm_paragraph_length = (average_paragraph_length / 800.0).min(1.0);
    let norm_entropy = (token_entropy / 8.0).min(1.0);
    let score = WORD_LENGTH_WEIGHT * norm_word_length
        + SENTENCE_LENGTH_WEIGHT * norm_sentence_length
        + PARAGRAPH_LENGTH_WEIGHT * norm_paragraph_length
        + ENTROPY_WEIGHT * norm_entropy;
    ReadabilityAssessment {
        average_token_length,
        average_sentence_length,
        average_paragraph_length,
        token_entropy,
        norm_word_length,
        norm_sentence_length,
        norm_paragraph_length,
        norm_entropy,
        score,
        level: readability_level(score),
    }
}

/// Assess the readability of `text`.
///
/// `include_punctuation` / `case_sensitive` control the unigram tokenisation
/// used for the word-length and entropy factors. When
/// `average_sentence_length_override` is `Some`, it replaces the built-in
/// sentence-length estimate.
pub fn assess(
    text: &str,
    include_punctuation: bool,
    case_sensitive: bool,
    average_sentence_length_override: Option<f64>,
) -> ReadabilityAssessment {
    let unigram_metrics =
        unigram::calculate_all_unigram_metrics(text, include_punctuation, case_sensitive);
    let average_sentence_length = average_sentence_length_override
        .unwrap_or_else(|| segmentation::average_sentence_length(text));
    assess_from_factors(
        unigram_metrics.average_token_length,
        average_sentence_length,
        segmentation::average_paragraph_length(text),
        unigram_metrics.token_entropy,
    )
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_levels() {
        assert_eq!(readability_level(0.0), "Easy");
        assert_eq!(readability_level(0.3), "Moderate");
        assert_eq!(readability_level(0.5), "Challenging");
        assert_eq!(readability_level(0.7), "Complex");
        assert_eq!(readability_level(0.85), "Very Complex");
    }

    #[test]
    fn test_empty_text() {
        let a = assess("", false, true, None);
        assert_eq!(a.score, 0.0);
        assert_eq!(a.level, "Easy");
    }

    #[test]
    fn test_factor_caps() {
        let a = assess_from_factors(100.0, 100.0, 10_000.0, 100.0);
        assert!((a.score - 1.0).abs() < 1e-12);
        assert_eq!(a.level, "Very Complex");
    }

    #[test]
    fn test_assess_matches_formula() {
        let text = "The court held that the agreement was void.\n\nIt was signed under duress.";
        let a = assess(text, false, true, None);
        let expected = 0.25 * (a.average_token_length / 10.0).min(1.0)
            + 0.35 * (a.average_sentence_length / 50.0).min(1.0)
            + 0.15 * (a.average_paragraph_length / 800.0).min(1.0)
            + 0.25 * (a.token_entropy / 8.0).min(1.0);
        assert!((a.score - expected).abs() < 1e-12);
        assert!(a.score > 0.0 && a.score < 1.0);
    }

    #[test]
    fn test_sentence_override() {
        let text = "One two three. Four five six.";
        let base = assess(text, false, true, None);
        let overridden = assess(text, false, true, Some(50.0));
        assert_eq!(overridden.average_sentence_length, 50.0);
        assert!((overridden.norm_sentence_length - 1.0).abs() < 1e-12);
        assert!(overridden.score > base.score);
    }
}
