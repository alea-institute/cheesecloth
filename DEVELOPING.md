
# Initial Setup

```bash
$ maturin new --mixed --bindings pyo3 cheesecloth
$ cd cheesecloth
$ uv venv --seed
$ maturin develop
```

# Running

## Build

```bash
maturin develop --uv
```


## Tests

```bash
uv run pytest
```

## Checks (as run in CI)

```bash
export PYO3_PYTHON=$PWD/.venv/bin/python   # lets `cargo test` link against Python
cargo fmt --all -- --check
cargo clippy --all-targets -- -D warnings
cargo test --release
ruff check python examples
ruff format --check python examples
mypy python/cheesecloth/__init__.pyi
uv run pytest python/tests --benchmark-disable
```

Network tests (Hugging Face Hub downloads) are skipped unless
`CHEESECLOTH_NETWORK_TESTS=1` is set.

## Wheels

The extension is built against the stable ABI (`abi3-py310`), so
`maturin build --release` produces a single `cp310-abi3` wheel per platform that
installs on CPython 3.10 through 3.14.
