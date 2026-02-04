# ============================================================
# SAFE BULK RENAME SCRIPT (PYTHON) — FIXED
# ============================================================

import os
import sys

# ---------------- CONFIG ----------------
ROOT_DIR = "."
EXCLUDE_DIRS = {
    ".git",
    "__pycache__",
    ".idea",
    ".vscode",
    ".DS_Store"
}

REPLACE_DASH = "_-_"   # replaces " - "
REPLACE_SPACE = "_"   # replaces " "
BAR_WIDTH = 50

# ---------------- HELPERS ----------------
def sanitize_name(name: str) -> str:
    name = name.replace(" - ", REPLACE_DASH)
    name = name.replace(" ", REPLACE_SPACE)
    return name

def progress_bar(current, total):
    percent = int((current / total) * 100)
    filled = int((percent / 100) * BAR_WIDTH)
    bar = "#" * filled + "-" * (BAR_WIDTH - filled)
    sys.stdout.write(f"\r[{bar}] {percent:3d}% ({current}/{total})")
    sys.stdout.flush()

# ---------------- COLLECT PATHS (BOTTOM-UP) ----------------
paths = []

for root, dirs, files in os.walk(ROOT_DIR, topdown=False):
    # remove excluded + hidden directories
    dirs[:] = [
        d for d in dirs
        if d not in EXCLUDE_DIRS and not d.startswith(".")
    ]

    for name in files + dirs:
        if name.startswith("."):
            continue
        paths.append(os.path.join(root, name))

TOTAL = len(paths)
COUNT = 0

# ---------------- RENAME LOOP ----------------
for path in paths:
    COUNT += 1
    parent = os.path.dirname(path)
    old_name = os.path.basename(path)

    new_name = sanitize_name(old_name)

    if new_name != old_name:
        new_path = os.path.join(parent, new_name)

        if not os.path.exists(new_path):
            try:
                os.rename(path, new_path)
            except Exception as e:
                pass  # skip safely

    progress_bar(COUNT, TOTAL)

print("\nRename completed safely.")
