//! # Unicode Character Categories
//!
//! This module provides comprehensive Unicode character categorization functionality,
//! allowing for detailed analysis of text based on the standard Unicode character
//! categories and category groups.
//!
//! ## Key Features
//!
//! * Full Unicode character categorization (Ll, Lu, Nd, etc.)
//! * Unicode category grouping (L, N, P, S, Z, etc.)
//! * Efficient category counting and frequency analysis
//! * Parallelized processing for large texts
//! * Optimized caching for common ASCII characters
//!
//! The module implements the full Unicode General Category system with extensions
//! for efficient text analysis, providing insights into script composition and
//! character distribution patterns.

use icu_properties::{maps, GeneralCategory};
use std::cell::RefCell;
use std::collections::HashMap;
use std::sync::OnceLock;

/// Unicode character category enum
#[derive(Hash, Eq, PartialEq, Clone, Copy, Debug)]
pub enum UnicodeCategory {
    Ll, // Lowercase Letter
    Lu, // Uppercase Letter
    Lt, // Titlecase Letter
    Lm, // Modifier Letter
    Lo, // Other Letter
    Mn, // Non-spacing Mark
    Mc, // Spacing Mark
    Me, // Enclosing Mark
    Nd, // Decimal Number
    Nl, // Letter Number
    No, // Other Number
    Pc, // Connector Punctuation
    Pd, // Dash Punctuation
    Ps, // Open Punctuation
    Pe, // Close Punctuation
    Pi, // Initial Punctuation
    Pf, // Final Punctuation
    Po, // Other Punctuation
    Sm, // Math Symbol
    Sc, // Currency Symbol
    Sk, // Modifier Symbol
    So, // Other Symbol
    Zs, // Space Separator
    Zl, // Line Separator
    Zp, // Paragraph Separator
    Cc, // Control
    Cf, // Format
    Cs, // Surrogate
    Co, // Private Use
    Cn, // Unassigned
}

/// Unicode character category group enum
#[derive(Hash, Eq, PartialEq, Clone, Copy, Debug)]
pub enum UnicodeCategoryGroup {
    L, // Letter
    M, // Mark
    N, // Number
    P, // Punctuation
    S, // Symbol
    Z, // Separator
    C, // Other
}

/// Number of distinct Unicode general categories ([`UnicodeCategory`] variants).
pub const NUM_CATEGORIES: usize = 30;

/// Number of distinct Unicode category groups ([`UnicodeCategoryGroup`] variants).
pub const NUM_GROUPS: usize = 7;

/// All categories in enum-discriminant order (`ALL_CATEGORIES[c as usize] == c`).
pub const ALL_CATEGORIES: [UnicodeCategory; NUM_CATEGORIES] = [
    UnicodeCategory::Ll,
    UnicodeCategory::Lu,
    UnicodeCategory::Lt,
    UnicodeCategory::Lm,
    UnicodeCategory::Lo,
    UnicodeCategory::Mn,
    UnicodeCategory::Mc,
    UnicodeCategory::Me,
    UnicodeCategory::Nd,
    UnicodeCategory::Nl,
    UnicodeCategory::No,
    UnicodeCategory::Pc,
    UnicodeCategory::Pd,
    UnicodeCategory::Ps,
    UnicodeCategory::Pe,
    UnicodeCategory::Pi,
    UnicodeCategory::Pf,
    UnicodeCategory::Po,
    UnicodeCategory::Sm,
    UnicodeCategory::Sc,
    UnicodeCategory::Sk,
    UnicodeCategory::So,
    UnicodeCategory::Zs,
    UnicodeCategory::Zl,
    UnicodeCategory::Zp,
    UnicodeCategory::Cc,
    UnicodeCategory::Cf,
    UnicodeCategory::Cs,
    UnicodeCategory::Co,
    UnicodeCategory::Cn,
];

/// All category groups in enum-discriminant order.
pub const ALL_GROUPS: [UnicodeCategoryGroup; NUM_GROUPS] = [
    UnicodeCategoryGroup::L,
    UnicodeCategoryGroup::M,
    UnicodeCategoryGroup::N,
    UnicodeCategoryGroup::P,
    UnicodeCategoryGroup::S,
    UnicodeCategoryGroup::Z,
    UnicodeCategoryGroup::C,
];

/// Map an ICU general category onto our enum.
fn from_icu(category: GeneralCategory) -> UnicodeCategory {
    match category {
        GeneralCategory::LowercaseLetter => UnicodeCategory::Ll,
        GeneralCategory::UppercaseLetter => UnicodeCategory::Lu,
        GeneralCategory::TitlecaseLetter => UnicodeCategory::Lt,
        GeneralCategory::ModifierLetter => UnicodeCategory::Lm,
        GeneralCategory::OtherLetter => UnicodeCategory::Lo,
        GeneralCategory::NonspacingMark => UnicodeCategory::Mn,
        GeneralCategory::SpacingMark => UnicodeCategory::Mc,
        GeneralCategory::EnclosingMark => UnicodeCategory::Me,
        GeneralCategory::DecimalNumber => UnicodeCategory::Nd,
        GeneralCategory::LetterNumber => UnicodeCategory::Nl,
        GeneralCategory::OtherNumber => UnicodeCategory::No,
        GeneralCategory::ConnectorPunctuation => UnicodeCategory::Pc,
        GeneralCategory::DashPunctuation => UnicodeCategory::Pd,
        GeneralCategory::OpenPunctuation => UnicodeCategory::Ps,
        GeneralCategory::ClosePunctuation => UnicodeCategory::Pe,
        GeneralCategory::InitialPunctuation => UnicodeCategory::Pi,
        GeneralCategory::FinalPunctuation => UnicodeCategory::Pf,
        GeneralCategory::OtherPunctuation => UnicodeCategory::Po,
        GeneralCategory::MathSymbol => UnicodeCategory::Sm,
        GeneralCategory::CurrencySymbol => UnicodeCategory::Sc,
        GeneralCategory::ModifierSymbol => UnicodeCategory::Sk,
        GeneralCategory::OtherSymbol => UnicodeCategory::So,
        GeneralCategory::SpaceSeparator => UnicodeCategory::Zs,
        GeneralCategory::LineSeparator => UnicodeCategory::Zl,
        GeneralCategory::ParagraphSeparator => UnicodeCategory::Zp,
        GeneralCategory::Control => UnicodeCategory::Cc,
        GeneralCategory::Format => UnicodeCategory::Cf,
        GeneralCategory::Surrogate => UnicodeCategory::Cs,
        GeneralCategory::PrivateUse => UnicodeCategory::Co,
        GeneralCategory::Unassigned => UnicodeCategory::Cn,
    }
}

/// Lookup table for the Latin-1 range (U+0000..=U+00FF), built once from ICU data.
fn latin1_table() -> &'static [UnicodeCategory; 256] {
    static TABLE: OnceLock<[UnicodeCategory; 256]> = OnceLock::new();
    TABLE.get_or_init(|| {
        let map = maps::general_category();
        let mut table = [UnicodeCategory::Cn; 256];
        for (i, slot) in table.iter_mut().enumerate() {
            // Every value in 0..=255 is a valid scalar value
            let ch = char::from_u32(i as u32).unwrap_or('\0');
            *slot = from_icu(map.get(ch));
        }
        table
    })
}

/// Convert a character to its Unicode general category.
///
/// The result always agrees with the Unicode Character Database (as shipped with
/// ICU4X), e.g. `'\n'`, `'\t'` and `'\r'` are `Cc` (control), `'-'` is `Pd`, and
/// `'^'` is `Sk`. Latin-1 characters use a precomputed table; other characters
/// use ICU's code point trie, which is a constant-time lookup.
#[inline]
pub fn char_to_category(ch: char) -> UnicodeCategory {
    let cp = ch as u32;
    if cp < 256 {
        latin1_table()[cp as usize]
    } else {
        from_icu(maps::general_category().get(ch))
    }
}

/// Convert a Unicode category to its group - optimized with a direct lookup table
pub fn category_to_group(category: UnicodeCategory) -> UnicodeCategoryGroup {
    // Using a lookup table for better performance than a match statement
    static GROUPS: [UnicodeCategoryGroup; 30] = [
        // Ll, Lu, Lt, Lm, Lo
        UnicodeCategoryGroup::L,
        UnicodeCategoryGroup::L,
        UnicodeCategoryGroup::L,
        UnicodeCategoryGroup::L,
        UnicodeCategoryGroup::L,
        // Mn, Mc, Me
        UnicodeCategoryGroup::M,
        UnicodeCategoryGroup::M,
        UnicodeCategoryGroup::M,
        // Nd, Nl, No
        UnicodeCategoryGroup::N,
        UnicodeCategoryGroup::N,
        UnicodeCategoryGroup::N,
        // Pc, Pd, Ps, Pe, Pi, Pf, Po
        UnicodeCategoryGroup::P,
        UnicodeCategoryGroup::P,
        UnicodeCategoryGroup::P,
        UnicodeCategoryGroup::P,
        UnicodeCategoryGroup::P,
        UnicodeCategoryGroup::P,
        UnicodeCategoryGroup::P,
        // Sm, Sc, Sk, So
        UnicodeCategoryGroup::S,
        UnicodeCategoryGroup::S,
        UnicodeCategoryGroup::S,
        UnicodeCategoryGroup::S,
        // Zs, Zl, Zp
        UnicodeCategoryGroup::Z,
        UnicodeCategoryGroup::Z,
        UnicodeCategoryGroup::Z,
        // Cc, Cf, Cs, Co, Cn
        UnicodeCategoryGroup::C,
        UnicodeCategoryGroup::C,
        UnicodeCategoryGroup::C,
        UnicodeCategoryGroup::C,
        UnicodeCategoryGroup::C,
    ];

    // Use the enum discriminant as an index into the lookup table
    GROUPS[category as usize]
}

/// Get the string representation of a Unicode category
pub fn category_to_string(category: UnicodeCategory) -> &'static str {
    match category {
        UnicodeCategory::Ll => "Ll",
        UnicodeCategory::Lu => "Lu",
        UnicodeCategory::Lt => "Lt",
        UnicodeCategory::Lm => "Lm",
        UnicodeCategory::Lo => "Lo",
        UnicodeCategory::Mn => "Mn",
        UnicodeCategory::Mc => "Mc",
        UnicodeCategory::Me => "Me",
        UnicodeCategory::Nd => "Nd",
        UnicodeCategory::Nl => "Nl",
        UnicodeCategory::No => "No",
        UnicodeCategory::Pc => "Pc",
        UnicodeCategory::Pd => "Pd",
        UnicodeCategory::Ps => "Ps",
        UnicodeCategory::Pe => "Pe",
        UnicodeCategory::Pi => "Pi",
        UnicodeCategory::Pf => "Pf",
        UnicodeCategory::Po => "Po",
        UnicodeCategory::Sm => "Sm",
        UnicodeCategory::Sc => "Sc",
        UnicodeCategory::Sk => "Sk",
        UnicodeCategory::So => "So",
        UnicodeCategory::Zs => "Zs",
        UnicodeCategory::Zl => "Zl",
        UnicodeCategory::Zp => "Zp",
        UnicodeCategory::Cc => "Cc",
        UnicodeCategory::Cf => "Cf",
        UnicodeCategory::Cs => "Cs",
        UnicodeCategory::Co => "Co",
        UnicodeCategory::Cn => "Cn",
    }
}

/// Get the string representation of a Unicode category group
pub fn category_group_to_string(group: UnicodeCategoryGroup) -> &'static str {
    match group {
        UnicodeCategoryGroup::L => "L",
        UnicodeCategoryGroup::M => "M",
        UnicodeCategoryGroup::N => "N",
        UnicodeCategoryGroup::P => "P",
        UnicodeCategoryGroup::S => "S",
        UnicodeCategoryGroup::Z => "Z",
        UnicodeCategoryGroup::C => "C",
    }
}

/// Convert a character directly to its Unicode category group
#[inline]
pub fn char_to_category_group(ch: char) -> UnicodeCategoryGroup {
    category_to_group(char_to_category(ch))
}

/// Convert a string to a vector of Unicode categories
pub fn to_category_vector(text: &str) -> Vec<UnicodeCategory> {
    text.chars().map(char_to_category).collect()
}

/// Convert a string to a vector of Unicode category groups
pub fn to_category_group_vector(text: &str) -> Vec<UnicodeCategoryGroup> {
    text.chars().map(char_to_category_group).collect()
}

/// Category index (enum discriminant) of every character in `text`.
fn category_index_sequence(text: &str) -> Vec<u8> {
    text.chars().map(|c| char_to_category(c) as u8).collect()
}

/// Map a category index sequence onto group indices.
fn group_index_sequence(categories: &[u8]) -> Vec<u8> {
    categories
        .iter()
        .map(|&c| category_to_group(ALL_CATEGORIES[c as usize]) as u8)
        .collect()
}

/// Dense per-category counts for `text`.
fn category_count_array(text: &str) -> ([usize; NUM_CATEGORIES], usize) {
    let mut counts = [0usize; NUM_CATEGORIES];
    let mut total = 0usize;
    for c in text.chars() {
        counts[char_to_category(c) as usize] += 1;
        total += 1;
    }
    (counts, total)
}

/// Collapse dense category counts into dense group counts.
fn group_counts_from_categories(counts: &[usize; NUM_CATEGORIES]) -> [usize; NUM_GROUPS] {
    let mut groups = [0usize; NUM_GROUPS];
    for (i, &count) in counts.iter().enumerate() {
        groups[category_to_group(ALL_CATEGORIES[i]) as usize] += count;
    }
    groups
}

// Scratch space for sparse n-gram counting. Category trigrams have 31^3 possible
// keys (30 categories plus the START/END edge marker); allocating and scanning a
// table that size for every document would dominate the cost for short texts, so
// a per-thread table is reused and only the touched slots are reset.
thread_local! {
    static NGRAM_SCRATCH: RefCell<Vec<usize>> = const { RefCell::new(Vec::new()) };
}

/// Count bigrams (with START/END edges) or trigrams over an index sequence whose
/// values are all `< edge`. The value `edge` marks the START/END position. Returns
/// the non-zero entries as (packed key, count) in first-seen order.
fn sparse_ngram_counts(seq: &[u8], edge: usize, order: usize) -> Vec<(usize, usize)> {
    let n = seq.len();
    if n == 0 {
        return Vec::new();
    }
    let slots = edge + 1;
    let size = slots.pow(order as u32);
    NGRAM_SCRATCH.with(|cell| {
        let mut counts = cell.borrow_mut();
        if counts.len() < size {
            counts.resize(size, 0);
        }
        let counts: &mut [usize] = &mut counts[..];
        let mut touched: Vec<usize> = Vec::new();
        let mut bump = |idx: usize| {
            if counts[idx] == 0 {
                touched.push(idx);
            }
            counts[idx] += 1;
        };
        if order == 2 {
            // (START, c0), (c0, c1), ..., (c_{n-1}, END)
            bump(edge * slots + seq[0] as usize);
            for w in seq.windows(2) {
                bump(w[0] as usize * slots + w[1] as usize);
            }
            bump(seq[n - 1] as usize * slots + edge);
        } else {
            // One trigram per character: (prev or START, current, next or END)
            for i in 0..n {
                let prev = if i == 0 { edge } else { seq[i - 1] as usize };
                let next = if i + 1 == n {
                    edge
                } else {
                    seq[i + 1] as usize
                };
                bump((prev * slots + seq[i] as usize) * slots + next);
            }
        }
        touched
            .into_iter()
            .map(|idx| {
                let count = counts[idx];
                counts[idx] = 0;
                (idx, count)
            })
            .collect()
    })
}

/// A category bigram key; `None` marks the START (first) or END (second) edge.
pub type CategoryBigram = (Option<&'static str>, Option<&'static str>);

/// A category trigram key; `None` marks the START (first) or END (third) edge.
pub type CategoryTrigram = (Option<&'static str>, &'static str, Option<&'static str>);

fn category_name(idx: usize) -> Option<&'static str> {
    ALL_CATEGORIES.get(idx).map(|&c| category_to_string(c))
}

fn group_name(idx: usize) -> Option<&'static str> {
    ALL_GROUPS.get(idx).map(|&g| category_group_to_string(g))
}

fn decode_bigrams(
    counts: Vec<(usize, usize)>,
    edge: usize,
    name: fn(usize) -> Option<&'static str>,
) -> Vec<(CategoryBigram, usize)> {
    let slots = edge + 1;
    counts
        .into_iter()
        .map(|(idx, count)| ((name(idx / slots), name(idx % slots)), count))
        .collect()
}

fn decode_trigrams(
    counts: Vec<(usize, usize)>,
    edge: usize,
    name: fn(usize) -> Option<&'static str>,
) -> Vec<(CategoryTrigram, usize)> {
    let slots = edge + 1;
    counts
        .into_iter()
        .map(|(idx, count)| {
            let next = idx % slots;
            let current = (idx / slots) % slots;
            let prev = idx / (slots * slots);
            // The middle position is always a real character, never an edge
            let current_name = name(current).unwrap_or("");
            ((name(prev), current_name, name(next)), count)
        })
        .collect()
}

/// All Unicode category statistics for a text, computed from a single
/// classification pass: per-category and per-group counts plus the non-zero
/// category / group bigrams and trigrams (with START/END edges).
pub struct CategoryProfile {
    pub total_chars: usize,
    pub category_counts: [usize; NUM_CATEGORIES],
    pub group_counts: [usize; NUM_GROUPS],
    pub category_bigrams: Vec<(CategoryBigram, usize)>,
    pub group_bigrams: Vec<(CategoryBigram, usize)>,
    pub category_trigrams: Vec<(CategoryTrigram, usize)>,
    pub group_trigrams: Vec<(CategoryTrigram, usize)>,
}

impl CategoryProfile {
    /// Total number of bigrams (`n + 1` for a non-empty text of `n` chars).
    pub fn bigram_total(&self) -> usize {
        if self.total_chars == 0 {
            0
        } else {
            self.total_chars + 1
        }
    }

    /// Total number of trigrams (one per character).
    pub fn trigram_total(&self) -> usize {
        self.total_chars
    }
}

/// Compute a [`CategoryProfile`] for `text`.
pub fn category_profile(text: &str) -> CategoryProfile {
    let cats = category_index_sequence(text);
    let groups = group_index_sequence(&cats);
    let mut category_counts = [0usize; NUM_CATEGORIES];
    for &c in &cats {
        category_counts[c as usize] += 1;
    }
    let group_counts = group_counts_from_categories(&category_counts);
    CategoryProfile {
        total_chars: cats.len(),
        category_counts,
        group_counts,
        category_bigrams: decode_bigrams(
            sparse_ngram_counts(&cats, NUM_CATEGORIES, 2),
            NUM_CATEGORIES,
            category_name,
        ),
        group_bigrams: decode_bigrams(
            sparse_ngram_counts(&groups, NUM_GROUPS, 2),
            NUM_GROUPS,
            group_name,
        ),
        category_trigrams: decode_trigrams(
            sparse_ngram_counts(&cats, NUM_CATEGORIES, 3),
            NUM_CATEGORIES,
            category_name,
        ),
        group_trigrams: decode_trigrams(
            sparse_ngram_counts(&groups, NUM_GROUPS, 3),
            NUM_GROUPS,
            group_name,
        ),
    }
}

/// Count the occurrences of each Unicode category in a string (non-zero entries only)
pub fn count_categories(text: &str) -> HashMap<UnicodeCategory, usize> {
    let (counts, _) = category_count_array(text);
    counts
        .iter()
        .enumerate()
        .filter(|(_, &count)| count > 0)
        .map(|(i, &count)| (ALL_CATEGORIES[i], count))
        .collect()
}

/// Count the occurrences of each Unicode category group in a string (non-zero entries only)
pub fn count_category_groups(text: &str) -> HashMap<UnicodeCategoryGroup, usize> {
    let (counts, _) = category_count_array(text);
    group_counts_from_categories(&counts)
        .iter()
        .enumerate()
        .filter(|(_, &count)| count > 0)
        .map(|(i, &count)| (ALL_GROUPS[i], count))
        .collect()
}

/// Get efficient string-based frequency counts of Unicode categories
pub fn category_string_frequency(text: &str) -> HashMap<String, usize> {
    count_categories(text)
        .into_iter()
        .map(|(category, count)| (category_to_string(category).to_string(), count))
        .collect()
}

/// Get efficient string-based frequency counts of Unicode category groups
pub fn category_group_string_frequency(text: &str) -> HashMap<String, usize> {
    count_category_groups(text)
        .into_iter()
        .map(|(group, count)| (category_group_to_string(group).to_string(), count))
        .collect()
}

/// Count the ratio of each Unicode category in a string
pub fn category_ratios(text: &str) -> HashMap<UnicodeCategory, f64> {
    let (counts, total) = category_count_array(text);
    if total == 0 {
        return HashMap::new();
    }
    let total = total as f64;
    counts
        .iter()
        .enumerate()
        .filter(|(_, &count)| count > 0)
        .map(|(i, &count)| (ALL_CATEGORIES[i], count as f64 / total))
        .collect()
}

/// Count the ratio of each Unicode category group in a string
pub fn category_group_ratios(text: &str) -> HashMap<UnicodeCategoryGroup, f64> {
    let (counts, total) = category_count_array(text);
    if total == 0 {
        return HashMap::new();
    }
    let total = total as f64;
    group_counts_from_categories(&counts)
        .iter()
        .enumerate()
        .filter(|(_, &count)| count > 0)
        .map(|(i, &count)| (ALL_GROUPS[i], count as f64 / total))
        .collect()
}

/// Calculate bigrams of Unicode categories in a text
/// Each bigram is a tuple of (optional preceding category, optional following category)
/// For the first character, the preceding category is None
/// For the last character, the following category is None
pub fn calculate_category_bigrams(
    text: &str,
) -> Vec<(Option<UnicodeCategory>, Option<UnicodeCategory>)> {
    let categories = to_category_vector(text);
    if categories.is_empty() {
        return Vec::new();
    }
    let mut bigrams = Vec::with_capacity(categories.len() + 1);
    bigrams.push((None, Some(categories[0])));
    for window in categories.windows(2) {
        bigrams.push((Some(window[0]), Some(window[1])));
    }
    bigrams.push((Some(categories[categories.len() - 1]), None));
    bigrams
}

/// Calculate bigrams of Unicode category groups in a text
pub fn calculate_category_group_bigrams(
    text: &str,
) -> Vec<(Option<UnicodeCategoryGroup>, Option<UnicodeCategoryGroup>)> {
    let groups = to_category_group_vector(text);
    if groups.is_empty() {
        return Vec::new();
    }
    let mut bigrams = Vec::with_capacity(groups.len() + 1);
    bigrams.push((None, Some(groups[0])));
    for window in groups.windows(2) {
        bigrams.push((Some(window[0]), Some(window[1])));
    }
    bigrams.push((Some(groups[groups.len() - 1]), None));
    bigrams
}

/// Calculate trigrams of Unicode categories in a text
/// Each trigram is a tuple of (prev category, current category, next category)
/// For the first character, prev is None; for the last character, next is None
pub fn calculate_category_trigrams(
    text: &str,
) -> Vec<(
    Option<UnicodeCategory>,
    UnicodeCategory,
    Option<UnicodeCategory>,
)> {
    let categories = to_category_vector(text);
    let n = categories.len();
    (0..n)
        .map(|i| {
            let prev = if i == 0 {
                None
            } else {
                Some(categories[i - 1])
            };
            let next = if i + 1 == n {
                None
            } else {
                Some(categories[i + 1])
            };
            (prev, categories[i], next)
        })
        .collect()
}

/// Calculate trigrams of Unicode category groups in a text
pub fn calculate_category_group_trigrams(
    text: &str,
) -> Vec<(
    Option<UnicodeCategoryGroup>,
    UnicodeCategoryGroup,
    Option<UnicodeCategoryGroup>,
)> {
    let groups = to_category_group_vector(text);
    let n = groups.len();
    (0..n)
        .map(|i| {
            let prev = if i == 0 { None } else { Some(groups[i - 1]) };
            let next = if i + 1 == n {
                None
            } else {
                Some(groups[i + 1])
            };
            (prev, groups[i], next)
        })
        .collect()
}

fn owned_bigram((a, b): CategoryBigram) -> (Option<String>, Option<String>) {
    (a.map(str::to_string), b.map(str::to_string))
}

fn owned_trigram((a, b, c): CategoryTrigram) -> (Option<String>, String, Option<String>) {
    (a.map(str::to_string), b.to_string(), c.map(str::to_string))
}

fn bigram_counts_for(
    seq: &[u8],
    edge: usize,
    name: fn(usize) -> Option<&'static str>,
) -> HashMap<(Option<String>, Option<String>), usize> {
    decode_bigrams(sparse_ngram_counts(seq, edge, 2), edge, name)
        .into_iter()
        .map(|(key, count)| (owned_bigram(key), count))
        .collect()
}

fn trigram_counts_for(
    seq: &[u8],
    edge: usize,
    name: fn(usize) -> Option<&'static str>,
) -> HashMap<(Option<String>, String, Option<String>), usize> {
    decode_trigrams(sparse_ngram_counts(seq, edge, 3), edge, name)
        .into_iter()
        .map(|(key, count)| (owned_trigram(key), count))
        .collect()
}

fn to_ratios<K: std::hash::Hash + Eq>(counts: HashMap<K, usize>) -> HashMap<K, f64> {
    let total: usize = counts.values().sum();
    if total == 0 {
        return HashMap::new();
    }
    counts
        .into_iter()
        .map(|(k, v)| (k, v as f64 / total as f64))
        .collect()
}

/// Count the frequencies of Unicode category bigrams in a text
pub fn count_category_bigrams(text: &str) -> HashMap<(Option<String>, Option<String>), usize> {
    bigram_counts_for(
        &category_index_sequence(text),
        NUM_CATEGORIES,
        category_name,
    )
}

/// Calculate the ratios of Unicode category bigrams in a text
pub fn category_bigram_ratios(text: &str) -> HashMap<(Option<String>, Option<String>), f64> {
    to_ratios(count_category_bigrams(text))
}

/// Count the frequencies of Unicode category group bigrams in a text
pub fn count_category_group_bigrams(
    text: &str,
) -> HashMap<(Option<String>, Option<String>), usize> {
    let groups = group_index_sequence(&category_index_sequence(text));
    bigram_counts_for(&groups, NUM_GROUPS, group_name)
}

/// Calculate the ratios of Unicode category group bigrams in a text
pub fn category_group_bigram_ratios(text: &str) -> HashMap<(Option<String>, Option<String>), f64> {
    to_ratios(count_category_group_bigrams(text))
}

/// Count the frequencies of Unicode category trigrams in a text
pub fn count_category_trigrams(
    text: &str,
) -> HashMap<(Option<String>, String, Option<String>), usize> {
    trigram_counts_for(
        &category_index_sequence(text),
        NUM_CATEGORIES,
        category_name,
    )
}

/// Calculate the ratios of Unicode category trigrams in a text
pub fn category_trigram_ratios(
    text: &str,
) -> HashMap<(Option<String>, String, Option<String>), f64> {
    to_ratios(count_category_trigrams(text))
}

/// Count the frequencies of Unicode category group trigrams in a text
pub fn count_category_group_trigrams(
    text: &str,
) -> HashMap<(Option<String>, String, Option<String>), usize> {
    let groups = group_index_sequence(&category_index_sequence(text));
    trigram_counts_for(&groups, NUM_GROUPS, group_name)
}

/// Calculate the ratios of Unicode category group trigrams in a text
pub fn category_group_trigram_ratios(
    text: &str,
) -> HashMap<(Option<String>, String, Option<String>), f64> {
    to_ratios(count_category_group_trigrams(text))
}

#[cfg(test)]
mod tests {
    // Importing everything since most of the module's functions are tested
    #[allow(unused_imports)]
    use super::*;

    #[test]
    fn test_char_to_category() {
        assert_eq!(char_to_category('a'), UnicodeCategory::Ll);
        assert_eq!(char_to_category('A'), UnicodeCategory::Lu);
        assert_eq!(char_to_category('1'), UnicodeCategory::Nd);
        assert_eq!(char_to_category('!'), UnicodeCategory::Po);
        assert_eq!(char_to_category(' '), UnicodeCategory::Zs);
    }

    #[test]
    fn test_category_to_group() {
        assert_eq!(
            category_to_group(UnicodeCategory::Ll),
            UnicodeCategoryGroup::L
        );
        assert_eq!(
            category_to_group(UnicodeCategory::Mn),
            UnicodeCategoryGroup::M
        );
        assert_eq!(
            category_to_group(UnicodeCategory::Nd),
            UnicodeCategoryGroup::N
        );
        assert_eq!(
            category_to_group(UnicodeCategory::Po),
            UnicodeCategoryGroup::P
        );
        assert_eq!(
            category_to_group(UnicodeCategory::Sm),
            UnicodeCategoryGroup::S
        );
        assert_eq!(
            category_to_group(UnicodeCategory::Zs),
            UnicodeCategoryGroup::Z
        );
        assert_eq!(
            category_to_group(UnicodeCategory::Cc),
            UnicodeCategoryGroup::C
        );
    }

    #[test]
    fn test_char_to_category_group() {
        assert_eq!(char_to_category_group('a'), UnicodeCategoryGroup::L);
        assert_eq!(char_to_category_group('A'), UnicodeCategoryGroup::L);
        assert_eq!(char_to_category_group('1'), UnicodeCategoryGroup::N);
        assert_eq!(char_to_category_group('!'), UnicodeCategoryGroup::P);
        assert_eq!(char_to_category_group(' '), UnicodeCategoryGroup::Z);
    }

    #[test]
    fn test_to_category_vector() {
        let text = "Hello, world!";
        let categories = to_category_vector(text);
        assert_eq!(categories.len(), text.len());
        assert_eq!(categories[0], UnicodeCategory::Lu);
        assert_eq!(categories[1], UnicodeCategory::Ll);
        assert_eq!(categories[5], UnicodeCategory::Po);
        assert_eq!(categories[12], UnicodeCategory::Po);
    }

    #[test]
    fn test_to_category_group_vector() {
        let text = "Hello, world!";
        let categories = to_category_group_vector(text);
        assert_eq!(categories.len(), text.len());
        assert_eq!(categories[0], UnicodeCategoryGroup::L);
        assert_eq!(categories[1], UnicodeCategoryGroup::L);
        assert_eq!(categories[5], UnicodeCategoryGroup::P);
        assert_eq!(categories[12], UnicodeCategoryGroup::P);
    }

    #[test]
    fn test_count_categories() {
        let text = "Hello, world!";
        let counts = count_categories(text);
        assert_eq!(counts[&UnicodeCategory::Lu], 1);
        assert_eq!(counts[&UnicodeCategory::Ll], 9);
        assert_eq!(counts[&UnicodeCategory::Po], 2);
        assert_eq!(counts[&UnicodeCategory::Zs], 1);
    }

    #[test]
    fn test_count_category_groups() {
        let text = "Hello, world!";
        let counts = count_category_groups(text);
        assert_eq!(counts[&UnicodeCategoryGroup::L], 10);
        assert_eq!(counts[&UnicodeCategoryGroup::P], 2);
        assert_eq!(counts[&UnicodeCategoryGroup::Z], 1);
    }

    #[test]
    fn test_category_ratios() {
        let text = "Hello, world!";
        let ratios = category_ratios(text);

        assert!((ratios[&UnicodeCategory::Lu] - 1.0 / 13.0).abs() < 1e-10);
        assert!((ratios[&UnicodeCategory::Ll] - 9.0 / 13.0).abs() < 1e-10);
        assert!((ratios[&UnicodeCategory::Po] - 2.0 / 13.0).abs() < 1e-10);
        assert!((ratios[&UnicodeCategory::Zs] - 1.0 / 13.0).abs() < 1e-10);
    }

    #[test]
    fn test_category_group_ratios() {
        let text = "Hello, world!";
        let ratios = category_group_ratios(text);

        assert!((ratios[&UnicodeCategoryGroup::L] - 10.0 / 13.0).abs() < 1e-10);
        assert!((ratios[&UnicodeCategoryGroup::P] - 2.0 / 13.0).abs() < 1e-10);
        assert!((ratios[&UnicodeCategoryGroup::Z] - 1.0 / 13.0).abs() < 1e-10);
    }

    #[test]
    fn test_calculate_category_bigrams() {
        let text = "Hi";
        let bigrams = calculate_category_bigrams(text);

        assert_eq!(bigrams.len(), 3);
        assert_eq!(bigrams[0], (None, Some(UnicodeCategory::Lu))); // H: (None, H)
        assert_eq!(
            bigrams[1],
            (Some(UnicodeCategory::Lu), Some(UnicodeCategory::Ll))
        ); // H→i
        assert_eq!(bigrams[2], (Some(UnicodeCategory::Ll), None)); // i: (i, None)

        let text = "A1";
        let bigrams = calculate_category_bigrams(text);

        assert_eq!(bigrams.len(), 3);
        assert_eq!(bigrams[0], (None, Some(UnicodeCategory::Lu))); // A: (None, A)
        assert_eq!(
            bigrams[1],
            (Some(UnicodeCategory::Lu), Some(UnicodeCategory::Nd))
        ); // A→1
        assert_eq!(bigrams[2], (Some(UnicodeCategory::Nd), None)); // 1: (1, None)
    }

    #[test]
    fn test_count_category_bigrams() {
        let text = "Hi";
        let counts = count_category_bigrams(text);

        assert_eq!(counts.len(), 3);
        assert_eq!(counts[&(None, Some("Lu".to_string()))], 1); // Start→H
        assert_eq!(counts[&(Some("Lu".to_string()), Some("Ll".to_string()))], 1); // H→i
        assert_eq!(counts[&(Some("Ll".to_string()), None)], 1); // i→End

        let text = "HiHi"; // Test counts with duplicated bigrams
        let counts = count_category_bigrams(text);

        assert_eq!(counts.len(), 4);
        assert_eq!(counts[&(None, Some("Lu".to_string()))], 1); // Start→H
        assert_eq!(counts[&(Some("Lu".to_string()), Some("Ll".to_string()))], 2); // H→i (twice)
        assert_eq!(counts[&(Some("Ll".to_string()), Some("Lu".to_string()))], 1); // i→H
        assert_eq!(counts[&(Some("Ll".to_string()), None)], 1); // i→End
    }

    #[test]
    fn test_category_bigram_ratios() {
        let text = "Hi";
        let ratios = category_bigram_ratios(text);

        assert_eq!(ratios.len(), 3);
        assert!((ratios[&(None, Some("Lu".to_string()))] - 1.0 / 3.0).abs() < 1e-10); // Start→H
        assert!(
            (ratios[&(Some("Lu".to_string()), Some("Ll".to_string()))] - 1.0 / 3.0).abs() < 1e-10
        ); // H→i
        assert!((ratios[&(Some("Ll".to_string()), None)] - 1.0 / 3.0).abs() < 1e-10);
        // i→End
    }

    #[test]
    fn test_calculate_category_group_bigrams() {
        let text = "Hi";
        let bigrams = calculate_category_group_bigrams(text);

        assert_eq!(bigrams.len(), 3);
        assert_eq!(bigrams[0], (None, Some(UnicodeCategoryGroup::L))); // Start→H
        assert_eq!(
            bigrams[1],
            (Some(UnicodeCategoryGroup::L), Some(UnicodeCategoryGroup::L))
        ); // H→i
        assert_eq!(bigrams[2], (Some(UnicodeCategoryGroup::L), None)); // i→End

        let text = "A1";
        let bigrams = calculate_category_group_bigrams(text);

        assert_eq!(bigrams.len(), 3);
        assert_eq!(bigrams[0], (None, Some(UnicodeCategoryGroup::L))); // Start→A
        assert_eq!(
            bigrams[1],
            (Some(UnicodeCategoryGroup::L), Some(UnicodeCategoryGroup::N))
        ); // A→1
        assert_eq!(bigrams[2], (Some(UnicodeCategoryGroup::N), None)); // 1→End
    }

    #[test]
    fn test_count_category_group_bigrams() {
        let text = "Hi";
        let counts = count_category_group_bigrams(text);

        assert_eq!(counts.len(), 3);
        assert_eq!(counts[&(None, Some("L".to_string()))], 1); // Start→L
        assert_eq!(counts[&(Some("L".to_string()), Some("L".to_string()))], 1); // L→L
        assert_eq!(counts[&(Some("L".to_string()), None)], 1); // L→End

        let text = "A1";
        let counts = count_category_group_bigrams(text);

        assert_eq!(counts.len(), 3);
        assert_eq!(counts[&(None, Some("L".to_string()))], 1); // Start→L
        assert_eq!(counts[&(Some("L".to_string()), Some("N".to_string()))], 1); // L→N
        assert_eq!(counts[&(Some("N".to_string()), None)], 1); // N→End
    }

    #[test]
    fn test_category_group_bigram_ratios() {
        let text = "Hi";
        let ratios = category_group_bigram_ratios(text);

        assert_eq!(ratios.len(), 3);
        assert!((ratios[&(None, Some("L".to_string()))] - 1.0 / 3.0).abs() < 1e-10); // Start→L
        assert!(
            (ratios[&(Some("L".to_string()), Some("L".to_string()))] - 1.0 / 3.0).abs() < 1e-10
        ); // L→L
        assert!((ratios[&(Some("L".to_string()), None)] - 1.0 / 3.0).abs() < 1e-10); // L→End

        let text = "A1";
        let ratios = category_group_bigram_ratios(text);

        assert_eq!(ratios.len(), 3);
        assert!((ratios[&(None, Some("L".to_string()))] - 1.0 / 3.0).abs() < 1e-10); // Start→L
        assert!(
            (ratios[&(Some("L".to_string()), Some("N".to_string()))] - 1.0 / 3.0).abs() < 1e-10
        ); // L→N
        assert!((ratios[&(Some("N".to_string()), None)] - 1.0 / 3.0).abs() < 1e-10);
        // N→End
    }

    #[test]
    fn test_calculate_category_trigrams() {
        let text = "Hi!";
        let trigrams = calculate_category_trigrams(text);

        assert_eq!(trigrams.len(), 3);
        assert_eq!(
            trigrams[0],
            (None, UnicodeCategory::Lu, Some(UnicodeCategory::Ll))
        ); // Start→H→i
        assert_eq!(
            trigrams[1],
            (
                Some(UnicodeCategory::Lu),
                UnicodeCategory::Ll,
                Some(UnicodeCategory::Po)
            )
        ); // H→i→!
        assert_eq!(
            trigrams[2],
            (Some(UnicodeCategory::Ll), UnicodeCategory::Po, None)
        ); // i→!→End
    }

    #[test]
    fn test_count_category_trigrams() {
        let text = "Hi!";
        let counts = count_category_trigrams(text);

        assert_eq!(counts.len(), 3);
        assert_eq!(counts[&(None, "Lu".to_string(), Some("Ll".to_string()))], 1); // Start→H→i
        assert_eq!(
            counts[&(
                Some("Lu".to_string()),
                "Ll".to_string(),
                Some("Po".to_string())
            )],
            1
        ); // H→i→!
        assert_eq!(counts[&(Some("Ll".to_string()), "Po".to_string(), None)], 1);
        // i→!→End
    }

    #[test]
    fn test_category_trigram_ratios() {
        let text = "Hi!";
        let ratios = category_trigram_ratios(text);

        assert_eq!(ratios.len(), 3);
        assert!(
            (ratios[&(None, "Lu".to_string(), Some("Ll".to_string()))] - 1.0 / 3.0).abs() < 1e-10
        ); // Start→H→i
        assert!(
            (ratios[&(
                Some("Lu".to_string()),
                "Ll".to_string(),
                Some("Po".to_string())
            )] - 1.0 / 3.0)
                .abs()
                < 1e-10
        ); // H→i→!
        assert!(
            (ratios[&(Some("Ll".to_string()), "Po".to_string(), None)] - 1.0 / 3.0).abs() < 1e-10
        ); // i→!→End
    }

    #[test]
    fn test_calculate_category_group_trigrams() {
        let text = "Hi!";
        let trigrams = calculate_category_group_trigrams(text);

        assert_eq!(trigrams.len(), 3);
        assert_eq!(
            trigrams[0],
            (None, UnicodeCategoryGroup::L, Some(UnicodeCategoryGroup::L))
        ); // Start→H→i
        assert_eq!(
            trigrams[1],
            (
                Some(UnicodeCategoryGroup::L),
                UnicodeCategoryGroup::L,
                Some(UnicodeCategoryGroup::P)
            )
        ); // H→i→!
        assert_eq!(
            trigrams[2],
            (Some(UnicodeCategoryGroup::L), UnicodeCategoryGroup::P, None)
        ); // i→!→End
    }

    #[test]
    fn test_count_category_group_trigrams() {
        let text = "Hi!";
        let counts = count_category_group_trigrams(text);

        assert_eq!(counts.len(), 3);
        assert_eq!(counts[&(None, "L".to_string(), Some("L".to_string()))], 1); // Start→H→i
        assert_eq!(
            counts[&(
                Some("L".to_string()),
                "L".to_string(),
                Some("P".to_string())
            )],
            1
        ); // H→i→!
        assert_eq!(counts[&(Some("L".to_string()), "P".to_string(), None)], 1); // i→!→End
    }

    #[test]
    fn test_category_group_trigram_ratios() {
        let text = "Hi!";
        let ratios = category_group_trigram_ratios(text);

        assert_eq!(ratios.len(), 3);
        assert!(
            (ratios[&(None, "L".to_string(), Some("L".to_string()))] - 1.0 / 3.0).abs() < 1e-10
        ); // Start→H→i
        assert!(
            (ratios[&(
                Some("L".to_string()),
                "L".to_string(),
                Some("P".to_string())
            )] - 1.0 / 3.0)
                .abs()
                < 1e-10
        ); // H→i→!
        assert!(
            (ratios[&(Some("L".to_string()), "P".to_string(), None)] - 1.0 / 3.0).abs() < 1e-10
        ); // i→!→End
    }

    #[test]
    fn test_trigram_empty_string() {
        let text = "";
        assert_eq!(calculate_category_trigrams(text).len(), 0);
        assert_eq!(calculate_category_group_trigrams(text).len(), 0);
        assert_eq!(count_category_trigrams(text).len(), 0);
        assert_eq!(count_category_group_trigrams(text).len(), 0);
        assert_eq!(category_trigram_ratios(text).len(), 0);
        assert_eq!(category_group_trigram_ratios(text).len(), 0);
    }

    #[test]
    fn test_trigram_single_character() {
        let text = "A";
        let cat_trigrams = calculate_category_trigrams(text);
        assert_eq!(cat_trigrams.len(), 1);
        assert_eq!(cat_trigrams[0], (None, UnicodeCategory::Lu, None));

        let group_trigrams = calculate_category_group_trigrams(text);
        assert_eq!(group_trigrams.len(), 1);
        assert_eq!(group_trigrams[0], (None, UnicodeCategoryGroup::L, None));
    }

    #[test]
    fn test_trigram_two_characters() {
        let text = "A1";
        let cat_trigrams = calculate_category_trigrams(text);
        assert_eq!(cat_trigrams.len(), 2);
        assert_eq!(
            cat_trigrams[0],
            (None, UnicodeCategory::Lu, Some(UnicodeCategory::Nd))
        );
        assert_eq!(
            cat_trigrams[1],
            (Some(UnicodeCategory::Lu), UnicodeCategory::Nd, None)
        );

        let group_trigrams = calculate_category_group_trigrams(text);
        assert_eq!(group_trigrams.len(), 2);
        assert_eq!(
            group_trigrams[0],
            (None, UnicodeCategoryGroup::L, Some(UnicodeCategoryGroup::N))
        );
        assert_eq!(
            group_trigrams[1],
            (Some(UnicodeCategoryGroup::L), UnicodeCategoryGroup::N, None)
        );
    }

    #[test]
    fn test_trigram_ratio_sums() {
        let text = "Hello!";
        let cat_ratios = category_trigram_ratios(text);
        let total = cat_ratios.values().sum::<f64>();
        assert!((total - 1.0).abs() < 1e-10);

        let group_ratios = category_group_trigram_ratios(text);
        let total = group_ratios.values().sum::<f64>();
        assert!((total - 1.0).abs() < 1e-10);
    }

    #[test]
    fn test_cache_hit() {
        // Test the cache by calling the function twice with the same character
        let non_ascii_char = 'ñ';

        // First call should cache the result
        let first_result = char_to_category(non_ascii_char);

        // Second call should hit the cache
        let second_result = char_to_category(non_ascii_char);

        // Results should be the same
        assert_eq!(first_result, second_result);

        // Same for category group
        let first_group = char_to_category_group(non_ascii_char);
        let second_group = char_to_category_group(non_ascii_char);
        assert_eq!(first_group, second_group);
    }
}
