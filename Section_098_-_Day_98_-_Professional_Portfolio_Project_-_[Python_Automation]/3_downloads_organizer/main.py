import os
import shutil
import json
import time
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Path.home() / 'folder_organizer.log'),
        logging.StreamHandler()
    ]
)

def load_config(config_path='config.json'):
    """Load extension-to-folder mapping from JSON file."""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        logging.error(f"Config file {config_path} not found. Using default mapping.")
        return {
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
            "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".odt"],
            "Archives": [".zip", ".tar", ".gz", ".rar", ".7z"],
            "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
            "Video": [".mp4", ".mkv", ".avi", ".mov", ".wmv"],
            "Programs": [".exe", ".msi", ".sh", ".bat", ".app", ".dmg"],
            "Others": []
        }
    except json.JSONDecodeError:
        logging.error("Invalid JSON in config file. Using default mapping.")
        return {}

def build_extension_map(category_map):
    """Convert {folder: [extensions]} to {extension: folder}."""
    ext_map = {}
    for folder, extensions in category_map.items():
        for ext in extensions:
            ext_map[ext.lower()] = folder
    return ext_map

def ensure_folder(folder_path):
    """Create folder if it doesn't exist."""
    folder_path.mkdir(parents=True, exist_ok=True)

def is_file_stable(file_path, wait_seconds=60):
    """Check if file is likely fully downloaded (older than wait_seconds)."""
    if not os.path.exists(file_path):
        return False
    return time.time() - os.path.getmtime(file_path) >= wait_seconds

def get_unique_filename(destination_folder, filename):
    """Generate unique filename if original already exists."""
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    while (destination_folder / new_filename).exists():
        new_filename = f"{base}_{counter}{ext}"
        counter += 1
    return new_filename

def organize_file(file_path, ext_map, root_folder, skip_stability_check=False):
    """
    Move a single file to its appropriate subfolder based on extension.
    Returns (success, target_path) or (False, None) if skipped/error.
    """
    file_path = Path(file_path)
    if not file_path.is_file():
        return False, None

    # Skip if file is already inside a category subfolder
    if file_path.parent.name in set(ext_map.values()):
        return False, None

    # Stability check (optional)
    if not skip_stability_check and not is_file_stable(file_path):
        logging.info(f"Skipping {file_path.name} (possibly still downloading)")
        return False, None

    ext = file_path.suffix.lower()
    target_folder_name = ext_map.get(ext, "Others")
    target_folder = root_folder / target_folder_name
    ensure_folder(target_folder)

    new_filename = get_unique_filename(target_folder, file_path.name)
    destination = target_folder / new_filename

    try:
        shutil.move(str(file_path), str(destination))
        logging.info(f"Moved {file_path.name} -> {target_folder_name}/{new_filename}")
        return True, destination
    except (shutil.Error, PermissionError, OSError) as e:
        logging.error(f"Failed to move {file_path.name}: {e}")
        return False, None

def organize_folder(folder_path, category_map, skip_stability_check=False):
    """
    Scan the folder (non‑recursive) and move every file to its category subfolder.
    Returns number of files moved.
    """
    folder_path = Path(folder_path)
    ext_map = build_extension_map(category_map)
    moved_count = 0
    for item in folder_path.iterdir():
        if not item.is_file():
            continue
        success, _ = organize_file(item, ext_map, folder_path, skip_stability_check)
        if success:
            moved_count += 1
    return moved_count


class FolderMonitor:
    """
    Monitors a folder for new/modified files and sorts them in real time.
    Uses watchdog in a separate thread.
    """
    def __init__(self, root_folder, category_map, callback=None):
        self.root_folder = Path(root_folder)
        self.category_map = category_map
        self.ext_map = build_extension_map(category_map)   # build once
        self.callback = callback
        self.observer = None
        self.event_handler = None
        self._stop_event = threading.Event()

    def start(self):
        """Start monitoring (non‑blocking)."""
        if self.observer and self.observer.is_alive():
            return

        self.event_handler = Handler(self.root_folder, self.ext_map, self.callback)
        self.observer = Observer()
        self.observer.schedule(self.event_handler, str(self.root_folder), recursive=False)
        self.observer.start()
        logging.info(f"Started monitoring {self.root_folder}")

    def stop(self):
        """Stop monitoring."""
        if self.observer and self.observer.is_alive():
            self.observer.stop()
            self.observer.join()
            logging.info(f"Stopped monitoring {self.root_folder}")

    def is_active(self):
        return self.observer is not None and self.observer.is_alive()


class Handler(FileSystemEventHandler):
    """
    Watchdog event handler: on file creation or modification, sort that file.
    Ignores events inside category subfolders.
    """
    def __init__(self, root_folder, ext_map, callback):
        super().__init__()
        self.root_folder = Path(root_folder)
        self.ext_map = ext_map
        self.callback = callback

    def on_created(self, event):
        self._handle_event(event)

    def on_modified(self, event):
        self._handle_event(event)

    def _handle_event(self, event):
        if event.is_directory:
            return
        file_path = Path(event.src_path)
        # Ignore if file is already in a category subfolder
        if file_path.parent.name in self.ext_map.values():
            return
        # Small delay to ensure file is completely written
        time.sleep(1)
        if self.callback:
            self.callback(f"New file detected: {file_path.name}")
        organize_file(file_path, self.ext_map, self.root_folder, skip_stability_check=False)