//! # Pattern Matching and Content Analysis
//!
//! This module provides functionality for identifying specific patterns and content
//! characteristics in text, using regular expressions and specialized detectors.
//!
//! ## Key Features
//!
//! * Regular expression pattern matching with efficient caching
//! * Copyright and rights reserved mention detection
//! * Document structure pattern recognition (sections, questions)
//! * Code fragment detection
//! * Bullet point and list analysis
//!
//! These pattern-matching functions enable content filtering, structural analysis,
//! and identification of special text elements that might require specific handling
//! or indicate particular document types. They're especially useful for corpus
//! cleaning and content classification tasks.

use lazy_static::lazy_static;
use regex::Regex;
use std::collections::HashMap;

// Cache for compiled regular expressions
lazy_static! {
    static ref REGEX_CACHE: std::sync::Mutex<HashMap<String, Regex>> =
        std::sync::Mutex::new(HashMap::new());
}

/// Generic function to count regex pattern matches in text
///
/// This function uses a cached regex pattern to efficiently count matches
/// in the provided text.
///
/// # Arguments
///
/// * `text` - The text to search within
/// * `pattern` - The regular expression pattern as a string
///
/// # Returns
///
/// The count of matches found
pub fn count_regex_matches(text: &str, pattern: &str) -> std::io::Result<usize> {
    // Get or create the compiled regex
    let regex = {
        let mut cache = REGEX_CACHE.lock().unwrap();

        if let Some(regex) = cache.get(pattern) {
            regex.clone()
        } else {
            match Regex::new(pattern) {
                Ok(regex) => {
                    cache.insert(pattern.to_string(), regex.clone());
                    regex
                }
                Err(e) => {
                    return Err(std::io::Error::new(
                        std::io::ErrorKind::InvalidInput,
                        format!("Invalid regex pattern: {}", e),
                    ))
                }
            }
        }
    };

    // Count the matches
    let count = regex.find_iter(text).count();

    Ok(count)
}

/// Check if text contains matches for a regex pattern
///
/// This function uses a cached regex pattern to efficiently check for matches
/// in the provided text.
///
/// # Arguments
///
/// * `text` - The text to search within
/// * `pattern` - The regular expression pattern as a string
///
/// # Returns
///
/// Boolean indicating if any matches were found
pub fn contains_regex_pattern(text: &str, pattern: &str) -> std::io::Result<bool> {
    // Get or create the compiled regex
    let regex = {
        let mut cache = REGEX_CACHE.lock().unwrap();

        if let Some(regex) = cache.get(pattern) {
            regex.clone()
        } else {
            match Regex::new(pattern) {
                Ok(regex) => {
                    cache.insert(pattern.to_string(), regex.clone());
                    regex
                }
                Err(e) => {
                    return Err(std::io::Error::new(
                        std::io::ErrorKind::InvalidInput,
                        format!("Invalid regex pattern: {}", e),
                    ))
                }
            }
        }
    };

    // Check for matches
    let contains = regex.is_match(text);

    Ok(contains)
}

/// Common predefined patterns for various text analysis tasks
pub mod common_patterns {
    /// Pattern to match copyright symbols and mentions
    pub fn copyright_pattern() -> &'static str {
        r"(?i)copyright|\(c\)|©|\bcopyrt\b"
    }

    /// Pattern to match "all rights reserved" and variations
    pub fn rights_reserved_pattern() -> &'static str {
        r"(?i)all\s+rights\s+reserved|rights\s+reserved|all\s+right\s+reserved"
    }

    /// Pattern to match section headings (various formats)
    pub fn section_heading_pattern() -> &'static str {
        r"(?im)^\s*(?:section|chapter|part)\s+\d+|^\s*\d+(?:\.\d+)*\s+[A-Z]|\b(?:[IVX]+\.|[A-Z]\.)\s+[A-Z][a-zA-Z]+"
    }

    /// Pattern to match question phrases/sentences
    pub fn question_pattern() -> &'static str {
        r"(?i)[^.!?]*\?\s*"
    }

    /// Pattern to detect code-like content (braces, brackets, etc.)
    pub fn code_pattern() -> &'static str {
        r"(?:[{}<>\[\];()]|\b(?:function|var|let|const|if|else|for|while|return|class|import|export|from)\b)"
    }

    /// Pattern for bullet points and list items
    pub fn bullet_pattern() -> &'static str {
        r"(?m)^\s*(?:[•●○◦-]|\d+\.|\([a-zA-Z0-9]+\)|\[[a-zA-Z0-9]+\])\s+"
    }

    /// Pattern for ellipsis lines (potentially truncated content)
    pub fn ellipsis_pattern() -> &'static str {
        r"(?m)^.*?[.]{3,}\s*$|^.*?…\s*$"
    }
}

/// Count copyright mentions in text
pub fn count_copyright_mentions(text: &str) -> std::io::Result<usize> {
    count_regex_matches(text, common_patterns::copyright_pattern())
}

/// Count "rights reserved" mentions in text
pub fn count_rights_reserved(text: &str) -> std::io::Result<usize> {
    count_regex_matches(text, common_patterns::rights_reserved_pattern())
}

/// Count section headings in text
pub fn count_section_strings(text: &str) -> std::io::Result<usize> {
    count_regex_matches(text, common_patterns::section_heading_pattern())
}

/// Count question phrases/sentences in text
pub fn count_question_strings(text: &str) -> std::io::Result<usize> {
    count_regex_matches(text, common_patterns::question_pattern())
}

/// Check if text contains code-like constructs
pub fn contains_code_characters(text: &str) -> std::io::Result<bool> {
    contains_regex_pattern(text, common_patterns::code_pattern())
}

/// Count bullet point or list item lines
pub fn count_bullet_lines(text: &str) -> std::io::Result<usize> {
    count_regex_matches(text, common_patterns::bullet_pattern())
}

/// Count ellipsis lines (potentially truncated content)
pub fn count_ellipsis_lines(text: &str) -> std::io::Result<usize> {
    count_regex_matches(text, common_patterns::ellipsis_pattern())
}

/// Calculate the ratio of bullet or ellipsis lines to total lines
pub fn bullet_or_ellipsis_lines_ratio(text: &str) -> std::io::Result<f64> {
    let bullet_count = count_bullet_lines(text)?;
    let ellipsis_count = count_ellipsis_lines(text)?;

    // Count total lines
    let total_lines = text.lines().count();

    if total_lines == 0 {
        return Ok(0.0);
    }

    let ratio = (bullet_count + ellipsis_count) as f64 / total_lines as f64;
    Ok(ratio)
}

/// Check if text contains any of the provided blacklisted terms
pub fn contains_blacklist_substring(text: &str, blacklist: &[&str]) -> bool {
    let lowercase_text = text.to_lowercase();

    for term in blacklist {
        if lowercase_text.contains(&term.to_lowercase()) {
            return true;
        }
    }

    false
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_count_regex_matches() {
        let text = "The quick brown fox jumps over the lazy dog. Another fox appears.";

        // Test basic word matching
        assert_eq!(count_regex_matches(text, r"\bfox\b").unwrap(), 2);

        // Test with no matches
        assert_eq!(count_regex_matches(text, r"\bcat\b").unwrap(), 0);

        // Test with case-insensitive flag
        assert_eq!(count_regex_matches(text, r"(?i)\bquick\b").unwrap(), 1);
    }

    #[test]
    fn test_contains_regex_pattern() {
        let text = "The quick brown fox jumps over the lazy dog.";

        // Test basic word matching
        assert!(contains_regex_pattern(text, r"\bfox\b").unwrap());

        // Test with no matches
        assert!(!contains_regex_pattern(text, r"\bcat\b").unwrap());

        // Test with case-insensitive flag
        assert!(contains_regex_pattern(text, r"(?i)\bQUICK\b").unwrap());
    }

    #[test]
    fn test_copyright_pattern() {
        let text_with_copyright = "Copyright © 2023 Example Company. All rights reserved.";
        // Note: Avoid using the word "copyright" in the negative test case
        let text_without_copyright = "This is a regular text with no legal notices.";

        // The pattern matches both "Copyright" and "©" separately
        assert_eq!(count_copyright_mentions(text_with_copyright).unwrap(), 2);
        assert_eq!(count_copyright_mentions(text_without_copyright).unwrap(), 0);
    }

    #[test]
    fn test_rights_reserved_pattern() {
        let text_with_rights = "Copyright © 2023 Example Company. All rights reserved.";
        let text_without_rights = "This is a regular text with no rights information.";

        assert_eq!(count_rights_reserved(text_with_rights).unwrap(), 1);
        assert_eq!(count_rights_reserved(text_without_rights).unwrap(), 0);
    }

    #[test]
    fn test_section_strings_pattern() {
        let text_with_sections = "Section 1: Introduction\nThis is the introduction.\nSection 2: Methods\nThis describes the methods.";
        let text_without_sections = "This is a regular text with no section headings.";

        assert_eq!(count_section_strings(text_with_sections).unwrap(), 2);
        assert_eq!(count_section_strings(text_without_sections).unwrap(), 0);
    }

    #[test]
    fn test_question_strings_pattern() {
        let text_with_questions =
            "What is the meaning of life? This is not a question. Where is the library?";
        let text_without_questions = "This is a statement. This is another statement.";

        assert_eq!(count_question_strings(text_with_questions).unwrap(), 2);
        assert_eq!(count_question_strings(text_without_questions).unwrap(), 0);
    }

    #[test]
    fn test_contains_code_characters() {
        let code_text = "function greeting() { return 'Hello, world!'; }";
        let normal_text = "This is a regular text without code.";

        assert!(contains_code_characters(code_text).unwrap());
        assert!(!contains_code_characters(normal_text).unwrap());
    }

    #[test]
    fn test_bullet_and_ellipsis_patterns() {
        let text_with_bullets = "• First item\n• Second item\n- Third item\n1. Fourth item";
        let text_with_ellipsis =
            "This line ends with...\nAnother normal line\nThis also trails off…";

        assert_eq!(count_bullet_lines(text_with_bullets).unwrap(), 4);
        assert_eq!(count_ellipsis_lines(text_with_ellipsis).unwrap(), 2);
    }

    #[test]
    fn test_bullet_or_ellipsis_ratio() {
        let text = "• First bullet\nRegular line\n- Second bullet\nAnother line ends...\nFinal regular line";

        // 3 special lines (2 bullets + 1 ellipsis) out of 5 total lines = 0.6
        assert_eq!(bullet_or_ellipsis_lines_ratio(text).unwrap(), 0.6);

        // Empty text
        assert_eq!(bullet_or_ellipsis_lines_ratio("").unwrap(), 0.0);
    }

    #[test]
    fn test_contains_blacklist_substring() {
        let text = "This contains some sensitive information like passwords and credentials.";
        let blacklist = &["password", "credential", "secret", "key"];

        assert!(contains_blacklist_substring(text, blacklist));

        let safe_text = "This is a completely safe text.";
        assert!(!contains_blacklist_substring(safe_text, blacklist));
    }
}
