#!/usr/bin/env python3
"""
Tests for the data loading and processing module.
"""

import json
import os
import tempfile

from cheesecloth.data import (
    TextDataLoader,
    TextBatchProcessor,
    process_text_file,
    process_jsonl_file,
    process_huggingface_dataset,
)
import cheesecloth


def create_test_text_file():
    """Create a temporary text file for testing."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("This is a test.\nThis is another test.\n")
    return f.name


def create_test_jsonl_file():
    """Create a temporary JSONL file for testing."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".jsonl") as f:
        f.write(json.dumps({"text": "This is a test."}) + "\n")
        f.write(json.dumps({"text": "This is another test."}) + "\n")
    return f.name


def test_text_data_loader_raw_text():
    """Test loading raw text."""
    loader = TextDataLoader()
    text = "This is a test."
    result = list(loader.load_text_from_source(text, "text"))
    assert len(result) == 1
    assert result[0] == text


def test_text_data_loader_text_file():
    """Test loading text from a file."""
    file_path = create_test_text_file()
    try:
        loader = TextDataLoader()
        result = list(loader.load_text_from_source(file_path, "file"))
        assert len(result) == 1
        assert "This is a test.\nThis is another test.\n" in result[0]
    finally:
        os.unlink(file_path)


def test_text_data_loader_text_file_batches():
    """Test loading text from a file in batches."""
    file_path = create_test_text_file()
    try:
        loader = TextDataLoader(
            batch_size=10
        )  # Small batch size to force multiple batches
        result = list(loader.load_text_from_source(file_path, "file"))
        assert len(result) > 1  # Should be split into multiple batches
        joined = "".join(result)
        assert "This is a test." in joined
        assert "This is another test." in joined
    finally:
        os.unlink(file_path)


def test_text_data_loader_jsonl():
    """Test loading text from a JSONL file."""
    file_path = create_test_jsonl_file()
    try:
        loader = TextDataLoader()
        result = list(loader.load_text_from_source(file_path, "jsonl"))
        assert len(result) == 2
        assert "This is a test." in result
        assert "This is another test." in result
    finally:
        os.unlink(file_path)


def test_text_data_loader_huggingface():
    """Test loading text from a Hugging Face dataset."""
    loader = TextDataLoader()
    # Use a small dataset for testing
    result = list(loader.load_huggingface_dataset("imdb", split="train[:10]"))
    assert len(result) == 10


def test_text_batch_processor():
    """Test batch processing of texts."""
    # Create an analyzer (BatchProcessor in this case)
    metrics = ["char_count", "word_count"]
    analyzer = cheesecloth.BatchProcessor(
        metrics, include_punctuation=False, case_sensitive=True
    )

    # Create a batch processor
    processor = TextBatchProcessor(analyzer, batch_size=2)

    # Process a list of texts
    texts = ["This is a test.", "This is another test."]
    results = processor.process_texts(texts)

    assert len(results) == 2
    assert "char_count" in results[0]
    assert "word_count" in results[0]


def test_process_text_file():
    """Test the convenience function for processing a text file."""
    file_path = create_test_text_file()
    try:
        metrics = ["char_count", "word_count"]
        analyzer = cheesecloth.BatchProcessor(
            metrics, include_punctuation=False, case_sensitive=True
        )

        results = process_text_file(file_path, analyzer)
        assert len(results) == 1  # One result for the whole file
        assert "char_count" in results[0]
        assert "word_count" in results[0]
    finally:
        os.unlink(file_path)


def test_process_jsonl_file():
    """Test the convenience function for processing a JSONL file."""
    file_path = create_test_jsonl_file()
    try:
        metrics = ["char_count", "word_count"]
        analyzer = cheesecloth.BatchProcessor(
            metrics, include_punctuation=False, case_sensitive=True
        )

        results = process_jsonl_file(file_path, analyzer)
        assert len(results) == 2  # One result per JSON object
        assert "char_count" in results[0]
        assert "word_count" in results[0]
    finally:
        os.unlink(file_path)


def test_process_huggingface_dataset():
    """Test the convenience function for processing a Hugging Face dataset."""
    metrics = ["char_count", "word_count"]
    analyzer = cheesecloth.BatchProcessor(
        metrics, include_punctuation=False, case_sensitive=True
    )

    # Use a small dataset for testing
    results = process_huggingface_dataset("imdb", analyzer, split="train[:10]")
    assert len(results) == 10
    assert "char_count" in results[0]
    assert "word_count" in results[0]
