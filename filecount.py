"""
filecount.py

Purpose:
    Count only meaningful project files by type, ignoring
    git internals, Python caches, and tooling artifacts.

Design Principle:
    If a human did not intentionally write or maintain it,
    it should not be counted.
"""

from pathlib import Path
from collections import defaultdict
from rich.console import Console
from rich.table import Table
from rich import box


# Directories that should be ignored entirely
IGNORE_DIRS = {
    ".git",
    "__pycache__",
    ".cache",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "node_modules",
    ".idea",
    ".vscode",
}

# File extensions that should be ignored
IGNORE_EXTENSIONS = {
    "pyc",
    "pyo",
    "log",
    "lock",
}


def should_ignore(path: Path) -> bool:
    """
    Determines whether a file should be excluded
    based on its parent directories or extension.
    """

    # Ignore based on directory ancestry
    if any(part in IGNORE_DIRS for part in path.parts):
        return True

    # Ignore based on extension
    if path.suffix:
        if path.suffix.lstrip(".").lower() in IGNORE_EXTENSIONS:
            return True

    return False


def collect_file_counts(base_path: Path) -> dict:
    """
    Walks the project tree and counts files by extension,
    excluding irrelevant infrastructure and cache files.
    """

    counts = defaultdict(int)

    for item in base_path.rglob("*"):
        if not item.is_file():
            continue

        if should_ignore(item):
            continue

        extension = item.suffix.lower().lstrip(".")
        extension = extension if extension else "no_extension"

        counts[extension] += 1

    return counts


def render_table(counts: dict) -> None:
    """
    Renders the filtered file counts using Rich.
    """

    console = Console()

    table = Table(
        title="Project File Composition (Author Files Only)",
        box=box.DOUBLE,
        show_lines=True,
        header_style="bold cyan",
    )

    table.add_column("File Type", style="magenta")
    table.add_column("Count", justify="right", style="green")

    for file_type, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
        table.add_row(file_type, str(count))

    console.print(table)


def main():
    """
    Entry point.
    """

    project_root = Path(".").resolve()
    counts = collect_file_counts(project_root)
    render_table(counts)


if __name__ == "__main__":
    main()
