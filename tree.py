import os

EXCLUDE_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "venv"
}

EXCLUDE_EXTENSIONS = {
    ".md",
    # ".log",
    # ".pyc"
}


FILENAME={
    "full":"full_folder_tree.txt",
    "python":"python_folder_tree.txt",
}

FULL_LENGTH = True
OUTPUT_FILE = FILENAME["python"]
LENGTH=11

NORMALIZED_EXCLUDE_DIRS = {d.lower() for d in EXCLUDE_DIRS}


def should_exclude_file(filename):
    _, ext = os.path.splitext(filename)
    return ext.lower() in EXCLUDE_EXTENSIONS


def format_folder_name(name):
    if FULL_LENGTH and len(name) > LENGTH:
        return name[:LENGTH] + "..."
    return name


def write_tree(root_path, file_handle, prefix=""):
    try:
        entries = sorted(os.listdir(root_path))
    except PermissionError:
        return

    filtered = []

    for entry in entries:
        full_path = os.path.join(root_path, entry)
        entry_normalized = entry.strip().lower()

        if os.path.isdir(full_path) and entry_normalized in NORMALIZED_EXCLUDE_DIRS:
            continue

        if os.path.isfile(full_path) and should_exclude_file(entry):
            continue

        filtered.append(entry)

    for index, entry in enumerate(filtered):
        full_path = os.path.join(root_path, entry)
        is_last = index == len(filtered) - 1

        connector = "└── " if is_last else "├── "
        display_name = format_folder_name(entry) if os.path.isdir(full_path) else entry

        file_handle.write(prefix + connector + display_name + "\n")

        if os.path.isdir(full_path):
            extension_prefix = "    " if is_last else "│   "
            write_tree(full_path, file_handle, prefix + extension_prefix)


if __name__ == "__main__":
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(".\n")
        write_tree(".", f)

    print(f"Tree exported successfully to {OUTPUT_FILE}")