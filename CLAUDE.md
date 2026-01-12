# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Orai is a Python project (version 0.1.0) currently in early development stage. The project uses Python 3.12+ and is managed with uv package manager.

## Development Environment

The project uses:
- Python 3.12 (specified in `.python-version`)
- uv for dependency management (indicated by `pyproject.toml`)
- Virtual environment in `.venv/`

### Setup Commands

Activate the virtual environment:
```bash
source .venv/bin/activate
```

Run the main application:
```bash
python main.py
```

Install dependencies (when added):
```bash
uv pip install -e .
```

## Project Structure

Currently minimal structure:
- `main.py` - Entry point with a `main()` function
- `pyproject.toml` - Project metadata and dependencies
- `.venv/` - Virtual environment

## Architecture Notes

The project is in its initial state. As it grows, architectural patterns and conventions should be documented here.
