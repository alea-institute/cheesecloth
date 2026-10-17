//! # Line Structure Metrics
//!
//! Fast, single-pass metrics describing how a document is laid out in lines:
//! the share of short lines, lines ending in terminal punctuation, duplicated
//! lines and numeric (table-like) lines, plus the longest line length and the
//! number of non-empty lines. These are useful boilerplate / layout signals for
//! pretraining-data filtering.
//!
//! ## Reference semantics
//!
//! The metrics reproduce this Python reference exactly (whitespace follows
//! `str.isspace`/`str.strip`/`str.split`, digits follow `str.isdigit`, and
//! lengths are in Unicode code points):
//!
//! ```python
//! END_P = (".", "!", "?", ":", ";", "\"", "”")
//! ls = [l.strip() for l in t.split("\n")]; ne = [l for l in ls if l]; n = max(1, len(ne))
//! short_line_share = #(l in ne with len(l.split()) < 5) / n
//! end_punct_share = #(l in ne with l.endswith(END_P)) / n
//! dup_line_share = sum(count - 1 for each distinct line with count > 1) / n
//! numeric_line_share = #(l in ne where, among non-space chars, the share of
//!                        (isdigit or in "$%.,()-/:") is > 0.5) / n
//! longest_line = max(len(l) for l in ne) (0 when there are none); n_lines = len(ne)
//! ```
//!
//! Lines are split on `'\n'` only (a trailing `'\r'` is removed by the strip).
//! No sentence segmentation is involved.

use std::collections::HashSet;

/// Characters that end a line for `end_punct_share`.
pub const END_PUNCTUATION: [char; 7] = ['.', '!', '?', ':', ';', '"', '\u{201D}'];

/// Non-digit characters that count as "numeric" for `numeric_line_share`.
pub const NUMERIC_PUNCTUATION: [char; 9] = ['$', '%', '.', ',', '(', ')', '-', '/', ':'];

/// Lines with fewer whitespace-separated words than this are "short".
pub const SHORT_LINE_WORDS: usize = 5;

/// Python's `str.isspace()`: Unicode `White_Space` plus the information
/// separators U+001C..=U+001F (bidi classes B/S), which Rust's
/// `char::is_whitespace` does not include.
#[inline]
pub fn is_python_whitespace(c: char) -> bool {
    c.is_whitespace() || ('\u{1C}'..='\u{1F}').contains(&c)
}

/// Inclusive code point ranges for which Python's `str.isdigit()` is true
/// (Numeric_Type = Decimal or Digit), generated from Unicode 16.0
/// (CPython 3.14's `unicodedata`).
static PYTHON_DIGIT_RANGES: &[(u32, u32)] = &[
    (0x30, 0x39),
    (0xB2, 0xB3),
    (0xB9, 0xB9),
    (0x660, 0x669),
    (0x6F0, 0x6F9),
    (0x7C0, 0x7C9),
    (0x966, 0x96F),
    (0x9E6, 0x9EF),
    (0xA66, 0xA6F),
    (0xAE6, 0xAEF),
    (0xB66, 0xB6F),
    (0xBE6, 0xBEF),
    (0xC66, 0xC6F),
    (0xCE6, 0xCEF),
    (0xD66, 0xD6F),
    (0xDE6, 0xDEF),
    (0xE50, 0xE59),
    (0xED0, 0xED9),
    (0xF20, 0xF29),
    (0x1040, 0x1049),
    (0x1090, 0x1099),
    (0x1369, 0x1371),
    (0x17E0, 0x17E9),
    (0x1810, 0x1819),
    (0x1946, 0x194F),
    (0x19D0, 0x19DA),
    (0x1A80, 0x1A89),
    (0x1A90, 0x1A99),
    (0x1B50, 0x1B59),
    (0x1BB0, 0x1BB9),
    (0x1C40, 0x1C49),
    (0x1C50, 0x1C59),
    (0x2070, 0x2070),
    (0x2074, 0x2079),
    (0x2080, 0x2089),
    (0x2460, 0x2468),
    (0x2474, 0x247C),
    (0x2488, 0x2490),
    (0x24EA, 0x24EA),
    (0x24F5, 0x24FD),
    (0x24FF, 0x24FF),
    (0x2776, 0x277E),
    (0x2780, 0x2788),
    (0x278A, 0x2792),
    (0xA620, 0xA629),
    (0xA8D0, 0xA8D9),
    (0xA900, 0xA909),
    (0xA9D0, 0xA9D9),
    (0xA9F0, 0xA9F9),
    (0xAA50, 0xAA59),
    (0xABF0, 0xABF9),
    (0xFF10, 0xFF19),
    (0x104A0, 0x104A9),
    (0x10A40, 0x10A43),
    (0x10D30, 0x10D39),
    (0x10D40, 0x10D49),
    (0x10E60, 0x10E68),
    (0x11052, 0x1105A),
    (0x11066, 0x1106F),
    (0x110F0, 0x110F9),
    (0x11136, 0x1113F),
    (0x111D0, 0x111D9),
    (0x112F0, 0x112F9),
    (0x11450, 0x11459),
    (0x114D0, 0x114D9),
    (0x11650, 0x11659),
    (0x116C0, 0x116C9),
    (0x116D0, 0x116E3),
    (0x11730, 0x11739),
    (0x118E0, 0x118E9),
    (0x11950, 0x11959),
    (0x11BF0, 0x11BF9),
    (0x11C50, 0x11C59),
    (0x11D50, 0x11D59),
    (0x11DA0, 0x11DA9),
    (0x11F50, 0x11F59),
    (0x16130, 0x16139),
    (0x16A60, 0x16A69),
    (0x16AC0, 0x16AC9),
    (0x16B50, 0x16B59),
    (0x16D70, 0x16D79),
    (0x1CCF0, 0x1CCF9),
    (0x1D7CE, 0x1D7FF),
    (0x1E140, 0x1E149),
    (0x1E2F0, 0x1E2F9),
    (0x1E4F0, 0x1E4F9),
    (0x1E5F1, 0x1E5FA),
    (0x1E950, 0x1E959),
    (0x1F100, 0x1F10A),
    (0x1FBF0, 0x1FBF9),
];

/// Python's `str.isdigit()` for a single character.
#[inline]
pub fn is_python_digit(c: char) -> bool {
    if c.is_ascii() {
        return c.is_ascii_digit();
    }
    let cp = c as u32;
    PYTHON_DIGIT_RANGES
        .binary_search_by(|&(start, end)| {
            if end < cp {
                std::cmp::Ordering::Less
            } else if start > cp {
                std::cmp::Ordering::Greater
            } else {
                std::cmp::Ordering::Equal
            }
        })
        .is_ok()
}

/// Line-structure metrics for a document. See the module docs for definitions.
#[derive(Debug, Clone, PartialEq)]
pub struct LineStructureMetrics {
    /// Share of non-empty lines with fewer than 5 words
    pub short_line_share: f64,
    /// Share of non-empty lines ending in `. ! ? : ; " ”`
    pub end_punct_share: f64,
    /// Share of non-empty lines that repeat an earlier non-empty line
    pub dup_line_share: f64,
    /// Share of non-empty lines whose non-space characters are mostly digits / `$%.,()-/:`
    pub numeric_line_share: f64,
    /// Length (code points) of the longest stripped non-empty line
    pub longest_line: usize,
    /// Number of non-empty lines after stripping
    pub n_lines: usize,
}

/// Compute all line-structure metrics in a single pass over `text`.
pub fn line_structure_metrics(text: &str) -> LineStructureMetrics {
    let mut n_lines = 0usize;
    let mut short = 0usize;
    let mut end_punct = 0usize;
    let mut duplicates = 0usize;
    let mut numeric = 0usize;
    let mut longest_line = 0usize;
    let mut seen: HashSet<&str> = HashSet::new();

    for raw in text.split('\n') {
        let line = raw.trim_matches(is_python_whitespace);
        if line.is_empty() {
            continue;
        }
        n_lines += 1;

        let words = line
            .split(is_python_whitespace)
            .filter(|word| !word.is_empty())
            .take(SHORT_LINE_WORDS)
            .count();
        if words < SHORT_LINE_WORDS {
            short += 1;
        }

        if line.ends_with(END_PUNCTUATION) {
            end_punct += 1;
        }

        if !seen.insert(line) {
            duplicates += 1;
        }

        let mut length = 0usize;
        let mut visible = 0usize;
        let mut numeric_chars = 0usize;
        for c in line.chars() {
            length += 1;
            if !is_python_whitespace(c) {
                visible += 1;
                if is_python_digit(c) || NUMERIC_PUNCTUATION.contains(&c) {
                    numeric_chars += 1;
                }
            }
        }
        // numeric_chars / visible > 0.5, in exact integer arithmetic
        if 2 * numeric_chars > visible {
            numeric += 1;
        }
        longest_line = longest_line.max(length);
    }

    let denominator = n_lines.max(1) as f64;
    LineStructureMetrics {
        short_line_share: short as f64 / denominator,
        end_punct_share: end_punct as f64 / denominator,
        dup_line_share: duplicates as f64 / denominator,
        numeric_line_share: numeric as f64 / denominator,
        longest_line,
        n_lines,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_empty_text() {
        let m = line_structure_metrics("");
        assert_eq!(m.n_lines, 0);
        assert_eq!(m.longest_line, 0);
        assert_eq!(m.short_line_share, 0.0);
        assert_eq!(m.end_punct_share, 0.0);
        assert_eq!(m.dup_line_share, 0.0);
        assert_eq!(m.numeric_line_share, 0.0);

        let blank = line_structure_metrics(" \n\t\n\r\n");
        assert_eq!(blank.n_lines, 0);
    }

    #[test]
    fn test_basic_lines() {
        let text = "Title\nThis is a much longer line of text.\n  Title  \n$1,000.00 (5%)\n\n";
        let m = line_structure_metrics(text);
        assert_eq!(m.n_lines, 4);
        // "Title", "Title", "$1,000.00 (5%)" are short
        assert!((m.short_line_share - 0.75).abs() < 1e-12);
        // only the long sentence ends in '.'; "(5%)" ends in ')'
        assert!((m.end_punct_share - 0.25).abs() < 1e-12);
        // "Title" repeated once after stripping
        assert!((m.dup_line_share - 0.25).abs() < 1e-12);
        // "$1,000.00 (5%)": all 13 visible chars are digits or numeric punctuation
        assert!((m.numeric_line_share - 0.25).abs() < 1e-12);
        assert_eq!(
            m.longest_line,
            "This is a much longer line of text.".chars().count()
        );
    }

    #[test]
    fn test_crlf_and_unicode() {
        let m = line_structure_metrics("naïve café “quoted”\r\nnaïve café “quoted”\r\n");
        assert_eq!(m.n_lines, 2);
        assert_eq!(m.longest_line, 19);
        assert!((m.end_punct_share - 1.0).abs() < 1e-12);
        assert!((m.dup_line_share - 0.5).abs() < 1e-12);
    }

    #[test]
    fn test_numeric_threshold_is_strict() {
        // 2 numeric of 4 visible = 0.5, which is not > 0.5
        assert_eq!(line_structure_metrics("12ab").numeric_line_share, 0.0);
        assert_eq!(line_structure_metrics("123a").numeric_line_share, 1.0);
        // superscript two is a Python digit
        assert_eq!(line_structure_metrics("²²a").numeric_line_share, 1.0);
        // vulgar fraction one half is numeric but not a Python digit
        assert_eq!(line_structure_metrics("½½a").numeric_line_share, 0.0);
    }

    #[test]
    fn test_python_whitespace() {
        assert!(is_python_whitespace('\u{1C}'));
        assert!(is_python_whitespace('\u{3000}'));
        assert!(!is_python_whitespace('\u{200B}'));
        let m = line_structure_metrics("\u{1F}word\u{1F}");
        assert_eq!(m.longest_line, 4);
    }

    #[test]
    fn test_python_digit() {
        assert!(is_python_digit('7'));
        assert!(is_python_digit('\u{0663}')); // Arabic-Indic three
        assert!(is_python_digit('\u{2460}')); // circled digit one
        assert!(!is_python_digit('\u{00BD}')); // one half
        assert!(!is_python_digit('a'));
    }
}
