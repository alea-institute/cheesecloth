# Changelog

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