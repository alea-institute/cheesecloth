#!/usr/bin/env python3
"""
Complete Text Analysis Workflow
==============================

This script demonstrates a comprehensive text analysis workflow using Cheesecloth,
integrating basic metrics, tokenization, advanced metrics, and comparative analysis
into a unified pipeline.

Key Features
-----------

1. Complete analysis pipeline
   - From basic character counts to advanced statistical measures
   - Consistent reporting structure across all metrics
   - Integrated results visualization

2. Multiple analysis approaches
   - Character-level analysis
   - Word/unigram analysis
   - Tokenization-based analysis
   - Compression and statistical metrics
   - Pattern detection

3. Comparative analysis
   - Cross-document comparison
   - Genre and style differentiation
   - Reference benchmarking

4. Results export
   - Structured JSON output
   - CSV report generation
   - Summary statistics

Usage
-----
```
python 4_complete_analysis_workflow.py [file1] [file2] ... [fileN]
```

Multiple files can be provided for comparative analysis.
If no files are provided, sample texts will be used for demonstration.
"""

import cheesecloth
import sys
import json
import csv
from pathlib import Path
from typing import Dict, Any


class TextAnalysisWorkflow:
    """
    Comprehensive text analysis workflow using Cheesecloth.
    """

    def __init__(self):
        """
        Initialize the analyzer with default settings.
        """
        self.hyper_analyzer = cheesecloth.HyperAnalyzer(
            include_punctuation=True, case_sensitive=True
        )
        self.results = {}

    def analyze_text(self, text: str, text_id: str) -> Dict[str, Any]:
        """
        Run comprehensive analysis on a text.

        Args:
            text: The text to analyze
            text_id: Identifier for this text

        Returns:
            Dictionary of analysis results
        """
        print(f"\n=== Analyzing: {text_id} ===\n")
        print(f"Text length: {len(text)} characters")

        # Store results with this ID
        self.results[text_id] = {}

        # Basic metrics (character, unigram, structure)
        print("\n1. Basic Metrics")
        metrics = self.hyper_analyzer.calculate_all_metrics(text)
        basic_metrics = {
            "char_count": metrics["char_count"],
            "letter_count": metrics["letter_count"],
            "digit_count": metrics["digit_count"],
            "symbol_count": metrics["symbol_count"],
            "whitespace_count": metrics["whitespace_count"],
            "non_ascii_count": metrics["non_ascii_count"],
            "ascii_ratio": metrics["ascii_ratio"],
            "uppercase_ratio": metrics["uppercase_ratio"],
            "unigram_count": metrics["unigram_count"],
            "unique_unigram_count": metrics["unique_unigram_count"],
            "unigram_type_token_ratio": metrics["unigram_type_token_ratio"],
            "line_count": metrics["line_count"],
            "paragraph_count": metrics["paragraph_count"],
            "avg_line_length": metrics["avg_line_length"],
            "avg_paragraph_length": metrics["avg_paragraph_length"],
            "avg_word_length": metrics["avg_word_length"],
        }

        self.results[text_id]["basic"] = basic_metrics

        print(f"  Characters: {basic_metrics['char_count']}")
        print(f"  Words: {basic_metrics['unigram_count']}")
        print(f"  Type-Token Ratio: {basic_metrics['unigram_type_token_ratio']:.2f}")
        print(f"  ASCII Ratio: {basic_metrics['ascii_ratio']:.2f}")

        # Tokenization analysis
        print("\n2. Tokenization Analysis")
        unigram_tokens = cheesecloth.tokenize_unigrams(text)

        # Try ML tokenization if available
        ml_token_info = {}
        try:
            gpt2_tokens = cheesecloth.tokenize_ml(text, "gpt2")
            ml_token_info["gpt2"] = {
                "token_count": len(gpt2_tokens),
                "unique_token_count": len(set(gpt2_tokens)),
            }
            print(f"  GPT-2 Tokens: {len(gpt2_tokens)}")
            print(
                f"  Compression Ratio (chars/tokens): {len(text) / len(gpt2_tokens):.2f}"
            )
        except Exception:
            print("  ML tokenization not available")

        token_analysis = {
            "unigram_tokens": len(unigram_tokens),
            "unique_unigrams": len(set(unigram_tokens)),
            "ml_tokenization": ml_token_info,
        }

        self.results[text_id]["tokenization"] = token_analysis

        # Advanced metrics
        print("\n3. Advanced Metrics")

        # Compression metrics
        compression_metrics = cheesecloth.get_compression_metrics(text)
        print(f"  Compression Ratio: {compression_metrics['compression_ratio']:.2f}")

        # Zipf analysis
        try:
            zipf_metrics = cheesecloth.get_zipf_metrics(text, False, True)
            print(f"  Zipf Fitness Score: {zipf_metrics['zipf_fitness_score']:.2f}")
            print(f"  Power Law Exponent: {zipf_metrics['power_law_exponent']:.2f}")
        except Exception as e:
            print(f"  Zipf analysis error: {e}")
            zipf_metrics = {"error": str(e)}

        # Pattern analysis
        pattern_metrics = {
            "copyright_mentions": cheesecloth.count_copyright_mentions(text),
            "section_headings": cheesecloth.count_section_strings(text),
            "questions": cheesecloth.count_question_strings(text),
            "contains_code": cheesecloth.contains_code_characters(text),
            "bullet_ellipsis_ratio": cheesecloth.bullet_or_ellipsis_lines_ratio(text),
        }

        print(f"  Contains code: {pattern_metrics['contains_code']}")
        print(f"  Questions: {pattern_metrics['questions']}")

        advanced_metrics = {
            "compression": compression_metrics,
            "zipf": zipf_metrics,
            "patterns": pattern_metrics,
        }

        self.results[text_id]["advanced"] = advanced_metrics

        return self.results[text_id]

    def analyze_file(self, filepath: str) -> Dict[str, Any]:
        """
        Analyze a text file.

        Args:
            filepath: Path to the text file

        Returns:
            Analysis results dictionary
        """
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()

            filename = Path(filepath).name
            return self.analyze_text(text, filename)

        except Exception as e:
            print(f"Error analyzing file {filepath}: {e}")
            return {"error": str(e)}

    def compare_results(self) -> None:
        """
        Compare analysis results across all texts.
        """
        if len(self.results) <= 1:
            print("\nNeed at least two texts for comparison")
            return

        print("\n=== Comparative Analysis ===\n")

        # Compare key metrics
        print(
            f"{'Text':<20} {'Chars':<10} {'Words':<10} {'TTR':<8} {'Compression':<12} {'Zipf':<8}"
        )
        print("-" * 70)

        for text_id, result in self.results.items():
            chars = result["basic"]["char_count"]
            words = result["basic"]["unigram_count"]
            ttr = result["basic"]["unigram_type_token_ratio"]

            try:
                compression = result["advanced"]["compression"]["compression_ratio"]
            except:
                compression = "N/A"

            try:
                zipf = result["advanced"]["zipf"]["zipf_fitness_score"]
            except:
                zipf = "N/A"

            print(
                f"{text_id[:19]:<20} {chars:<10} {words:<10} {ttr:<8.2f} {compression:<12.2f} {zipf:<8.2f}"
            )

    def export_results(self, output_file: str = "analysis_results.json") -> None:
        """
        Export results to a JSON file.

        Args:
            output_file: Path to save the JSON results
        """
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2)

        print(f"\nResults exported to {output_file}")

        # Also export a CSV summary
        csv_file = output_file.replace(".json", ".csv")
        with open(csv_file, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)

            # Write header
            header = [
                "Text",
                "Characters",
                "Words",
                "Type-Token Ratio",
                "Compression Ratio",
                "Zipf Fitness",
            ]
            writer.writerow(header)

            # Write data for each text
            for text_id, result in self.results.items():
                row = [
                    text_id,
                    result["basic"]["char_count"],
                    result["basic"]["unigram_count"],
                    result["basic"]["unigram_type_token_ratio"],
                    result["advanced"]["compression"]["compression_ratio"]
                    if "compression" in result["advanced"]
                    else "N/A",
                    result["advanced"]["zipf"]["zipf_fitness_score"]
                    if "zipf" in result["advanced"]
                    and "zipf_fitness_score" in result["advanced"]["zipf"]
                    else "N/A",
                ]
                writer.writerow(row)

        print(f"Summary exported to {csv_file}")


def demo_sample_texts():
    """
    Run analysis on sample texts with different characteristics.
    """
    # Create analyzer
    analyzer = TextAnalysisWorkflow()

    # Sample texts of different types
    samples = {
        "simple_english": "This is a simple example text. It has a few sentences. Nothing fancy!",
        "technical": """
        The hyperparameter optimization process leverages Bayesian methods to efficiently 
        navigate the search space. By constructing a probabilistic model of the objective 
        function and updating it with new observations, the algorithm can make informed 
        decisions about which configurations to evaluate next, balancing exploration and 
        exploitation.
        """,
        "literary": """
        The old man gazed out at the sea. Waves lapped gently against the weathered hull 
        of his small boat. Memories washed over him like the tide—days of abundance, nights 
        of struggle, years of persistence. The horizon stretched endlessly before him, a 
        canvas painted in shades of possibility and regret. He sighed, feeling the weight 
        of years in his bones.
        """,
        "code_mixed": """
        function processData(data) {
            // This function transforms input data
            let result = data.map(x => x * 2);
            console.log("Processing complete");
            return result;
        }
        
        This is an example of a JavaScript function that doubles each value in an array.
        """,
    }

    # Analyze each sample
    for name, text in samples.items():
        analyzer.analyze_text(text, name)

    # Compare results
    analyzer.compare_results()

    # Export results
    analyzer.export_results()


def main():
    """
    Main function handling command line arguments.
    """
    analyzer = TextAnalysisWorkflow()

    if len(sys.argv) > 1:
        # Analyze specific files
        for filepath in sys.argv[1:]:
            analyzer.analyze_file(filepath)

        # Compare if multiple files were provided
        if len(sys.argv) > 2:
            analyzer.compare_results()
            analyzer.export_results()
    else:
        # Run demo with sample texts
        demo_sample_texts()


if __name__ == "__main__":
    main()
