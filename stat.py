# ============================================================
# File: stat.py
# Purpose:
#   Analyze current directory size excluding common gitignore
#   patterns (including .git), group by file extension,
#   display statistics using Rich, and list all NO_EXT files.
# ============================================================

import os
from collections import defaultdict
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.progress import track

# ----------------------------
# Configuration Section
# ----------------------------

EXCLUDED_DIRECTORIES = {
    "__pycache__", ".git", "venv", ".venv", "env", "ENV", "virtualenv",
    "pip-wheel-metadata", ".vscode", ".idea", "logs", "log",
    "instance", "build", "dist", ".eggs", "htmlcov",
    ".pytest_cache", ".tox", ".nox", ".ipynb_checkpoints",
    ".cache", ".tmp", "temp", "tmp"
}

EXCLUDED_FILE_EXTENSIONS = {
    ".pyc", ".pyo", ".pyd", ".db", ".sqlite3", ".log", ".iml"
}

EXCLUDED_FILE_NAMES = {
    ".DS_Store", "Thumbs.db", "desktop.ini", ".coverage"
}

# ----------------------------
# Utility Functions
# ----------------------------

def human_readable_size(size_in_bytes: int) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024
    return f"{size_in_bytes:.2f} PB"


def should_exclude(path: Path) -> bool:
    if any(part in EXCLUDED_DIRECTORIES for part in path.parts):
        return True
    if path.name in EXCLUDED_FILE_NAMES:
        return True
    if path.suffix in EXCLUDED_FILE_EXTENSIONS:
        return True
    return False


# ----------------------------
# Main Analysis Logic
# ----------------------------

def analyze_directory(root_directory: Path):
    extension_sizes = defaultdict(int)
    extension_counts = defaultdict(int)
    no_extension_files = []
    total_size = 0

    all_files = list(root_directory.rglob("*"))

    for path in track(all_files, description="Analyzing files..."):
        if path.is_file() and not should_exclude(path):
            try:
                file_size = path.stat().st_size
                extension = path.suffix.lower() if path.suffix else "NO_EXT"

                extension_sizes[extension] += file_size
                extension_counts[extension] += 1
                total_size += file_size

                if extension == "NO_EXT":
                    no_extension_files.append(path.relative_to(root_directory))

            except (PermissionError, OSError):
                continue

    return extension_sizes, extension_counts, no_extension_files, total_size


# ----------------------------
# Display Results Using Rich
# ----------------------------

def display_results(extension_sizes, extension_counts, no_extension_files, total_size):
    console = Console()

    summary_table = Table(title="File Type Storage Statistics")
    summary_table.add_column("Extension", justify="left", style="cyan")
    summary_table.add_column("File Count", justify="right", style="magenta")
    summary_table.add_column("Total Size", justify="right", style="green")

    sorted_extensions = sorted(
        extension_sizes.items(),
        key=lambda item: item[1],
        reverse=True
    )

    for ext, size in sorted_extensions:
        summary_table.add_row(
            ext,
            str(extension_counts[ext]),
            human_readable_size(size)
        )

    console.print(summary_table)
    console.print(f"\n[bold yellow]Total Storage Used:[/bold yellow] {human_readable_size(total_size)}\n")

    if no_extension_files:
        no_ext_table = Table(title="Files Without Extension (NO_EXT)")
        no_ext_table.add_column("File Path", style="white")

        for file_path in sorted(no_extension_files):
            no_ext_table.add_row(str(file_path))

        console.print(no_ext_table)


# ----------------------------
# Entry Point
# ----------------------------

if __name__ == "__main__":
    current_directory = Path(".").resolve()
    sizes, counts, no_ext_files, total = analyze_directory(current_directory)
    display_results(sizes, counts, no_ext_files, total)


# ============================================================
# Expected Output (Example)
# ============================================================
#
#  File Type Storage Statistics
#  ┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
#  ┃ Extension     ┃ File Count   ┃ Total Size   ┃
#  ┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
#  │ NO_EXT        │ 2049         │ 27.36 MB     │
#  │ .py           │ 42           │ 1.85 MB      │
#  └───────────────┴──────────────┴──────────────┘
#
#  Total Storage Used: 31.02 MB
#
#  Files Without Extension (NO_EXT)
#  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#  ┃ File Path                            ┃
#  ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
#  │ README                                │
#  │ Dockerfile                            │
#  │ Makefile                              │
#  └──────────────────────────────────────┘
#
# ============================================================