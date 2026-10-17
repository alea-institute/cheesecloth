"""Every public function/class of the compiled extension must have a type stub."""

import re
from pathlib import Path

import cheesecloth
import cheesecloth.cheesecloth as native

STUB = Path(cheesecloth.__file__).with_name("__init__.pyi")


def test_stub_covers_native_module():
    stubbed = set(re.findall(r"^(?:def|class) (\w+)", STUB.read_text(), re.M))
    public = {name for name in dir(native) if not name.startswith("_")}
    missing = sorted(public - stubbed)
    assert not missing, f"missing from __init__.pyi: {missing}"


def test_new_functions_exported_from_package():
    for name in (
        "calculate_readability_score",
        "get_readability_level",
        "get_readability_factors",
        "get_line_structure_metrics",
        "short_line_share",
        "end_punct_share",
        "dup_line_share",
        "numeric_line_share",
        "longest_line_length",
        "count_nonempty_lines",
    ):
        assert callable(getattr(cheesecloth, name)), name
