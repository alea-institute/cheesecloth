# Changelog

## v0.3.0 (unreleased)

### Features
- Readability is now part of the Python API (implemented in Rust):
  `calculate_readability_score()`, `get_readability_level()` and
  `get_readability_factors()`, each taking
  `(text, include_punctuation=False, case_sensitive=True, average_sentence_length=None)`.
  They compute the same values as `AllMetrics.calculate_readability_score()` /
  `get_readability_level()` / `get_readability_assessment()` without building the
  full `get_all_metrics()` dictionary. `average_sentence_length` lets callers
  supply their own sentence statistics instead of the built-in estimate.
- New line-structure metrics (single pass, Rust): `short_line_share()`,
  `end_punct_share()`, `dup_line_share()`, `numeric_line_share()`,
  `longest_line_length()`, `count_nonempty_lines()` and the combined
  `get_line_structure_metrics()` (keys `short_line_share`, `end_punct_share`,
  `dup_line_share`, `numeric_line_share`, `longest_line`, `n_lines`). Semantics
  match the documented Python reference exactly (`str.strip`/`str.split`
  whitespace, `str.isdigit` digits, code-point lengths).
- `get_all_char_metrics()` adds `control_chars_excluding_whitespace` and
  `ratio_control_chars_excluding_whitespace`: Unicode `Cc` characters other than
  whitespace (`\t \n \v \f \r`, U+0085), a cleaner binary/garbage signal than
  the raw `Cc` ratio.

### Packaging
- Wheels are now built against the stable ABI (`abi3-py310`): one wheel per
  platform supports CPython 3.10 through 3.14. `requires-python` is now `>=3.10`.
- Added GitHub Actions CI: rustfmt, clippy, ruff, mypy, Rust and Python tests
  (3.10, 3.14), abi3 wheels for Linux x86_64/aarch64 (manylinux_2_28), macOS
  arm64/x86_64 and Windows x64, an sdist, and a smoke test that installs the
  built wheel on Python 3.10-3.14. Nothing is published automatically.

### Fixes
- Unicode categories now match the Unicode Character Database for all
  characters. The previous ASCII fast path labelled `\t \n \r \f` as `Zs`
  (they are `Cc`), `- * / %` as `Sm` (they are `Pd`, `Po`, `Po`, `Po`) and `^`
  as `Po` (it is `Sk`). This changes `unicode_category_*` ratios, category
  bigrams/trigrams and `category_entropy` for text containing those characters.
- Unigram `average_token_length`, `short_token_ratio` and `long_token_ratio`
  measure token length in code points rather than UTF-8 bytes (affects
  non-ASCII text; `get_all_metrics()` previously disagreed with
  `get_all_unigram_metrics()` here).
- `cheesecloth.cli` failed to import on Python < 3.12 (backslash inside an
  f-string expression).
- Type stubs now cover every function exported by the extension module.
- Hugging Face network tests use `stanfordnlp/imdb` and only run when
  `CHEESECLOTH_NETWORK_TESTS=1`.

### Performance
- `get_all_char_metrics()` is ~20x faster (2.2 -> ~48 Mchar/s single core on
  short documents): all Unicode category statistics come from one
  classification pass with dense/sparse array counting instead of per-character
  `String` keys, category lookups use a Latin-1 table plus ICU's code point trie
  instead of a locked LRU cache, and character frequencies are reused for the
  entropy and `char_frequency` outputs.
- `get_all_unigram_metrics()` is ~10x faster (6.6 -> ~66 Mchar/s): tokens are
  counted without copying, and the Python wrapper that recomputed four metrics
  the Rust function already returns was removed.
- Category bigram/trigram functions no longer allocate a `String` per character.
- ML tokenizer functions share cached tokenizers via `Arc` instead of cloning
  the whole tokenizer on every call (~3.5 ms -> ~2 us per short text).

## v0.2.2 (2025-04-19)

### Features
- Added Unicode category trigram analysis for deeper text structure insights
- Implemented advanced character type transition metrics
- Enhanced `CharMetrics` class with trigram support and new convenience properties
- Improved batch processing with parallel execution capabilities
- Added comprehensive README with clear examples, badges, and navigation links

### Improvements
- Added type stubs for missing trigram functions in `__init__.pyi`
- Optimized unigram frequency analysis and improved bigram handling
- Enhanced pattern matching with more efficient regex implementations
- Expanded test coverage for Unicode category trigrams

### Documentation
- Reorganized README.md for better clarity, usability and PyPI presentation
- Added badges for PyPI version and license information
- Improved examples with verified, working code snippets and expected outputs
- Enhanced code documentation with better type annotations

## v0.2.1 (2025-04-15)

### Improvements
- Added package configuration to exclude test files and example data from distributions
- Created MANIFEST.in to control Python package contents
- Added Cargo package exclusions for cleaner builds

## v0.2.0 (2025-04-15)

### Features
- Reorganized metric groups in CLI to align with Rust library structure
- Added readability metrics group with comprehensive readability assessment
- Added typed wrapper classes with convenience methods for better IDE support
- Added optimized metrics calculation mode with `--use-optimized-metrics` flag
- Enhanced pattern matching with pre-compiled regex patterns

### Documentation
- Added comprehensive metrics documentation in IMPLEMENTED_METRICS.md
- Updated README with new functionality examples
- Added extensive Python type annotations for better developer experience

### Performance
- Excluded slow pattern group from "all" option by default
- Improved metric group detection logic
- Enhanced JSON serialization handling for complex metrics

## v0.1.0 (2025-04-14)

### Features
- Initial release with comprehensive text metrics implementation
- High-performance Rust core with Python bindings
- CLI tools for dataset analysis
- Support for character, unigram, and token-level metrics
- Integration with machine learning tokenizers