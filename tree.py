import os

EXCLUDE_DIRS = {".git", "__pycache__"}   # add/remove as needed
OUTPUT_FILE = "full_tree.txt"


def write_tree(root_path, file_handle, prefix=""):
    try:
        entries = sorted(os.listdir(root_path))
    except PermissionError:
        return

    entries = [e for e in entries if e not in EXCLUDE_DIRS]

    for index, entry in enumerate(entries):
        path = os.path.join(root_path, entry)
        is_last = index == len(entries) - 1

        connector = "└── " if is_last else "├── "
        file_handle.write(prefix + connector + entry + "\n")

        if os.path.isdir(path):
            extension = "    " if is_last else "│   "
            write_tree(path, file_handle, prefix + extension)


if __name__ == "__main__":
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(".\n")
        write_tree(".", f)

    print(f"Tree exported successfully to {OUTPUT_FILE}")
