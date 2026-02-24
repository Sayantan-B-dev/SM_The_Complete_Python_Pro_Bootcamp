# Folder Organizer – Complete Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Folder Structure](#folder-structure)
3. [Installation and Environment](#installation-and-environment)
4. [Running the Application](#running-the-application)
5. [Configuration File (`config.json`)](#configuration-file-configjson)
6. [Detailed Explanation of `main.py`](#detailed-explanation-of-mainpy)
   - 6.1 [Imports and Logging](#imports-and-logging)
   - 6.2 [Function `load_config`](#function-load_config)
   - 6.3 [Function `build_extension_map`](#function-build_extension_map)
   - 6.4 [Function `ensure_folder`](#function-ensure_folder)
   - 6.5 [Function `is_file_stable`](#function-is_file_stable)
   - 6.6 [Function `get_unique_filename`](#function-get_unique_filename)
   - 6.7 [Function `organize_file`](#function-organize_file)
   - 6.8 [Function `organize_folder`](#function-organize_folder)
   - 6.9 [Class `FolderMonitor`](#class-folderMonitor)
   - 6.10 [Class `Handler`](#class-handler)
7. [Detailed Explanation of `ui.py`](#detailed-explanation-of-uipy)
   - 7.1 [Imports and Global](#imports-and-global)
   - 7.2 [Class `App`](#class-app)
   - 7.3 [Method `__init__`](#method-__init__)
   - 7.4 [Method `create_widgets`](#method-create_widgets)
   - 7.5 [Method `browse_folder`](#method-browse_folder)
   - 7.6 [Method `log_message`](#method-log_message)
   - 7.7 [Method `poll_log_queue`](#method-poll_log_queue)
   - 7.8 [Method `sort_now`](#method-sort_now)
   - 7.9 [Method `_run_sort`](#method-_run_sort)
   - 7.10 [Method `toggle_monitor`](#method-toggle_monitor)
   - 7.11 [Method `on_closing`](#method-on_closing)
8. [How Everything Works Together](#how-everything-works-together)
9. [Troubleshooting and Tips](#troubleshooting-and-tips)
10. [Customization and Extending](#customization-and-extending)

---

## 1. Project Overview

The **Folder Organizer** is a desktop application built with Python that helps you automatically sort files in a chosen folder into subfolders based on their file extensions. It provides two modes:

- **One‑time sort:** Moves all existing files in a folder into categorized subfolders.
- **Real‑time monitoring:** Watches a folder for new or modified files and sorts them immediately as they appear.

The application uses a graphical user interface (GUI) built with Tkinter. The logic for file operations and monitoring is separated into `main.py`, and the UI is in `ui.py`. Configuration (which extensions go into which folder) is stored in `config.json`.

---

## 2. Folder Structure

```
folder_organizer/
│
├── main.py               # Core logic: file sorting, monitoring, watchdog integration
├── ui.py                 # Tkinter GUI, user interaction
├── config.json           # File extension to folder name mapping
├── requirements.txt      # Python dependencies (only watchdog)
└── README.md             # Basic usage instructions (this file is more detailed)
```

After running, a log file `folder_organizer.log` may appear in your home directory.

---

## 3. Installation and Environment

### Prerequisites
- **Python 3.6 or higher** (Tkinter is included in standard Python installations on Windows and macOS; on Linux you may need to install `python3-tk` separately).
- **pip** (Python package installer).

### Steps

1. **Create a project folder** and place all the files as shown above.
2. **Install the required dependency** (watchdog) by running:
   ```bash
   pip install -r requirements.txt
   ```
   *Note:* `watchdog` is used for real‑time file monitoring. If you only plan to use the one‑time sort, you could skip this, but the monitoring feature requires it.
3. **Verify Tkinter** is available:
   ```bash
   python -m tkinter
   ```
   A small window should appear. If not, install Tkinter for your OS.

---

## 4. Running the Application

To start the application, open a terminal in the project folder and run:

```bash
python ui.py
```

The GUI window will appear. From there you can:

- Click **Browse** to select a folder you want to organize.
- Click **Sort Now** to perform a one‑time sort of all files in that folder.
- Click **Start Monitoring** to first sort the folder once and then continuously watch for new/modified files. The button toggles to **Stop Monitoring** when active.

All actions are logged in the text area and also saved to `~/folder_organizer.log`.

---

## 5. Configuration File (`config.json`)

The `config.json` file defines how files are categorized. It contains a JSON object where each key is a folder name (the target subfolder), and the value is a list of file extensions (including the dot). For example:

```json
{
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".odt", ".rtf", ".md"],
    "Archives": [".zip", ".tar", ".gz", ".rar", ".7z", ".bz2"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
    "Video": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"],
    "Programs": [".exe", ".msi", ".sh", ".bat", ".app", ".dmg", ".deb", ".rpm"],
    "Others": []
}
```

- Any file with an extension not listed in any category will be placed into the folder named `"Others"`.
- You can add, remove, or change folder names and extensions as you like. Just make sure the JSON syntax is valid.
- The folder names will be created inside the folder you are organizing (if they don't already exist).

**Important:** The folder names in `config.json` are also used to decide whether a file is already inside a category subfolder – the application will not move files that are already in such a folder to avoid loops.

---

## 6. Detailed Explanation of `main.py`

`main.py` contains all the core logic: reading configuration, moving files, and monitoring a folder. Let's go through it section by section.

### 6.1 Imports and Logging

```python
import os
import shutil
import json
import time
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
```

- **os, shutil, json, time, pathlib** – standard library modules for file operations, JSON parsing, time delays, and cross‑platform path handling.
- **logging** – for writing log messages to both a file and the console.
- **watchdog.observers.Observer** – the main class that watches a directory for changes.
- **watchdog.events.FileSystemEventHandler** – base class to handle file system events.
- **threading** – used internally by the `FolderMonitor` to run the observer in a separate thread.

Logging is configured to write to `~/folder_organizer.log` and also print to the console (StreamHandler). The format includes timestamp, log level, and message.

### 6.2 Function `load_config`

```python
def load_config(config_path='config.json'):
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        logging.error("Config file not found. Using default mapping.")
        return { ... }   # default mapping
    except json.JSONDecodeError:
        logging.error("Invalid JSON. Using default mapping.")
        return {}
```

**Purpose:** Loads the JSON configuration file and returns it as a Python dictionary. If the file is missing or contains invalid JSON, it logs an error and returns a hard‑coded default mapping (the same as the example above). This ensures the program can still run without a config file.

**Return value:** A dictionary like `{"Images": [".jpg", ...], "Documents": [...], ...}`.

### 6.3 Function `build_extension_map`

```python
def build_extension_map(category_map):
    ext_map = {}
    for folder, extensions in category_map.items():
        for ext in extensions:
            ext_map[ext.lower()] = folder
    return ext_map
```

**Purpose:** Converts the configuration dictionary (folder → list of extensions) into a reverse lookup dictionary (extension → folder). This makes it faster to determine the target folder for a given file extension.

**Example:** If `category_map` is `{"Images": [".jpg", ".png"]}`, `ext_map` becomes `{".jpg": "Images", ".png": "Images"}`. Extensions are stored in lowercase for case‑insensitive matching.

### 6.4 Function `ensure_folder`

```python
def ensure_folder(folder_path):
    folder_path.mkdir(parents=True, exist_ok=True)
```

**Purpose:** Creates a folder (and any necessary parent folders) if it does not already exist. Uses `pathlib.Path.mkdir()` with `parents=True` and `exist_ok=True` to avoid errors if the folder already exists.

### 6.5 Function `is_file_stable`

```python
def is_file_stable(file_path, wait_seconds=60):
    if not os.path.exists(file_path):
        return False
    return time.time() - os.path.getmtime(file_path) >= wait_seconds
```

**Purpose:** Checks whether a file is likely to be fully written and not still being downloaded or modified. It compares the file's last modification time with the current time; if the file was modified more than `wait_seconds` ago, it is considered stable. This helps avoid moving partially downloaded files.

**Parameters:**
- `file_path` – the file to check.
- `wait_seconds` – how many seconds must have passed since the last modification to consider the file stable. Default 60.

**Returns:** `True` if the file is older than `wait_seconds`, `False` otherwise (or if the file doesn't exist).

### 6.6 Function `get_unique_filename`

```python
def get_unique_filename(destination_folder, filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    while (destination_folder / new_filename).exists():
        new_filename = f"{base}_{counter}{ext}"
        counter += 1
    return new_filename
```

**Purpose:** When moving a file, if a file with the same name already exists in the destination folder, this function generates a new unique name by appending `_1`, `_2`, etc., until a name is available.

**Parameters:**
- `destination_folder` – a `Path` object of the target folder.
- `filename` – the original filename (string).

**Returns:** A new filename (string) that does not exist in the destination folder.

### 6.7 Function `organize_file`

```python
def organize_file(file_path, ext_map, root_folder, skip_stability_check=False):
    file_path = Path(file_path)
    if not file_path.is_file():
        return False, None

    # Skip if file is already inside a category subfolder
    if file_path.parent.name in set(ext_map.values()):
        return False, None

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
```

**Purpose:** Moves a single file to its appropriate subfolder. This is the core function that performs the actual file move.

**Parameters:**
- `file_path` – the file to move (string or Path).
- `ext_map` – the extension‑to‑folder dictionary from `build_extension_map`.
- `root_folder` – the top‑level folder being organized (e.g., the Downloads folder). Subfolders will be created inside this.
- `skip_stability_check` – if `True`, the stability check is bypassed (used for manual sorting to move everything immediately).

**Steps:**
1. Convert `file_path` to a `Path` object.
2. If it's not a file, return `False`.
3. Check if the file's parent folder name is one of the category names (e.g., "Images", "Documents") – if so, it's already in a sorted subfolder, so we skip it to avoid moving files back and forth.
4. Optionally check file stability.
5. Determine the target folder name using `ext_map.get(ext, "Others")`. If the extension is not found, it goes to "Others".
6. Create the target folder if needed.
7. Generate a unique filename.
8. Attempt to move the file with `shutil.move`. If successful, log the action and return `True, destination`.
9. If an error occurs (permission, file in use, etc.), log the error and return `False, None`.

**Returns:** A tuple `(success, destination)` where `success` is a boolean and `destination` is the new path (or `None`).

### 6.8 Function `organize_folder`

```python
def organize_folder(folder_path, category_map, skip_stability_check=False):
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
```

**Purpose:** Scans the given folder (non‑recursively) and attempts to move every file into its category subfolder. It counts how many files were successfully moved.

**Parameters:**
- `folder_path` – the folder to organize.
- `category_map` – the configuration dictionary from `load_config`.
- `skip_stability_check` – passed to `organize_file`.

**Steps:**
1. Convert `folder_path` to `Path`.
2. Build the extension map.
3. Iterate over all items in the folder.
4. For each file, call `organize_file`.
5. Increment `moved_count` if successful.
6. Return the total count.

This function is called both for the one‑time sort and for the initial sort when starting monitoring.

### 6.9 Class `FolderMonitor`

```python
class FolderMonitor:
    def __init__(self, root_folder, category_map, callback=None):
        self.root_folder = Path(root_folder)
        self.category_map = category_map
        self.ext_map = build_extension_map(category_map)
        self.callback = callback
        self.observer = None
        self.event_handler = None
        self._stop_event = threading.Event()

    def start(self):
        if self.observer and self.observer.is_alive():
            return
        self.event_handler = Handler(self.root_folder, self.ext_map, self.callback)
        self.observer = Observer()
        self.observer.schedule(self.event_handler, str(self.root_folder), recursive=False)
        self.observer.start()
        logging.info(f"Started monitoring {self.root_folder}")

    def stop(self):
        if self.observer and self.observer.is_alive():
            self.observer.stop()
            self.observer.join()
            logging.info(f"Stopped monitoring {self.root_folder}")

    def is_active(self):
        return self.observer is not None and self.observer.is_alive()
```

**Purpose:** Encapsulates the watchdog observer and provides a clean interface to start and stop monitoring a folder. It is designed to be used from the UI thread without blocking.

**Attributes:**
- `root_folder` – the folder being monitored.
- `category_map` – the configuration dictionary.
- `ext_map` – pre‑built extension map for efficiency.
- `callback` – an optional function that will be called with status messages (used to update the UI log).
- `observer` – the watchdog `Observer` instance.
- `event_handler` – an instance of our custom `Handler` class.
- `_stop_event` – not currently used but could be extended.

**Methods:**
- `start()`: Creates a `Handler`, schedules it with the observer, and starts the observer in a background thread.
- `stop()`: Stops the observer and waits for the thread to finish.
- `is_active()`: Returns whether the observer is alive.

### 6.10 Class `Handler`

```python
class Handler(FileSystemEventHandler):
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
        if file_path.parent.name in self.ext_map.values():
            return
        time.sleep(1)
        if self.callback:
            self.callback(f"New file detected: {file_path.name}")
        organize_file(file_path, self.ext_map, self.root_folder, skip_stability_check=False)
```

**Purpose:** This class inherits from `watchdog.events.FileSystemEventHandler` and overrides `on_created` and `on_modified` to react when a file is created or modified in the monitored folder.

**Methods:**
- `on_created(event)`: Called when a file or directory is created.
- `on_modified(event)`: Called when a file or directory is modified.
- `_handle_event(event)`: Common logic for both events.

**Logic:**
1. If the event is for a directory, ignore it.
2. Get the file path.
3. If the file is already inside a category subfolder (its parent name is one of the folder names), ignore it to avoid re‑sorting.
4. Wait 1 second (to give the file time to be completely written, especially for downloads).
5. If a callback is provided, call it with a message (this will appear in the UI log).
6. Call `organize_file` with `skip_stability_check=False` to respect the stability check even during monitoring (so partially downloaded files aren't moved immediately).

Note that monitoring is non‑recursive – it only watches the top‑level folder, not subfolders. This prevents reacting to files being moved into the category folders.

---

## 7. Detailed Explanation of `ui.py`

`ui.py` contains the Tkinter GUI and user interaction logic. It imports functions and classes from `main.py`.

### 7.1 Imports and Global

```python
import tkinter as tk
from tkinter import filedialog, scrolledtext
import threading
import queue
import os
from pathlib import Path
import main
```

- **tkinter** – standard GUI library.
- **filedialog, scrolledtext** – Tkinter widgets for folder selection and scrolling text area.
- **threading** – to run long tasks (like sorting or monitoring) without freezing the UI.
- **queue** – a thread‑safe queue to pass log messages from background threads to the main UI thread.
- **os, pathlib** – for path operations.
- **main** – our core logic module.

### 7.2 Class `App`

The `App` class encapsulates the entire GUI.

### 7.3 Method `__init__`

```python
def __init__(self, root):
    self.root = root
    self.root.title("Folder Organizer")
    self.root.geometry("700x500")
    self.root.resizable(True, True)

    self.folder_path = tk.StringVar()
    self.monitor_active = False
    self.monitor = None
    self.log_queue = queue.Queue()
    self.config = main.load_config()

    self.create_widgets()
    self.poll_log_queue()
```

**Purpose:** Initializes the application.

**Attributes:**
- `root` – the Tkinter root window.
- `folder_path` – a `StringVar` that holds the selected folder path (bound to an Entry widget).
- `monitor_active` – boolean indicating whether monitoring is currently running.
- `monitor` – an instance of `main.FolderMonitor` (or `None`).
- `log_queue` – a `queue.Queue` used to safely pass log messages from background threads to the main thread.
- `config` – the configuration dictionary loaded once at startup.
- Then it builds the UI and starts polling the log queue.

### 7.4 Method `create_widgets`

This method creates all the GUI elements:

- **Top frame:** Label "Folder:", Entry bound to `folder_path`, Browse button.
- **Button frame:** "Sort Now" and "Start Monitoring" buttons.
- **Log frame:** Label "Activity Log:" and a `ScrolledText` widget.
- **Status bar:** A Label at the bottom bound to `status_var`.

Buttons are assigned commands: `sort_now` and `toggle_monitor`.

### 7.5 Method `browse_folder`

```python
def browse_folder(self):
    folder = filedialog.askdirectory()
    if folder:
        self.folder_path.set(folder)
```

Opens a directory selection dialog and updates the `folder_path` variable.

### 7.6 Method `log_message`

```python
def log_message(self, message):
    self.log_queue.put(message)
```

Adds a message to the queue. This is called from background threads (e.g., from the `callback` in `FolderMonitor`) to avoid direct UI updates from other threads.

### 7.7 Method `poll_log_queue`

```python
def poll_log_queue(self):
    try:
        while True:
            msg = self.log_queue.get_nowait()
            self.log_text.insert(tk.END, msg + "\n")
            self.log_text.see(tk.END)
    except queue.Empty:
        pass
    finally:
        self.root.after(100, self.poll_log_queue)
```

This method is called repeatedly (every 100 ms) via `after()`. It checks the queue for any new messages and inserts them into the log text widget. This is the standard Tkinter pattern for thread‑safe UI updates.

### 7.8 Method `sort_now`

```python
def sort_now(self):
    folder = self.folder_path.get()
    if not folder:
        self.log_message("Please select a folder first.")
        return
    if not os.path.isdir(folder):
        self.log_message("Selected path is not a valid directory.")
        return

    self.log_message(f"Starting one‑time sort of {folder}")
    self.status_var.set("Sorting...")
    threading.Thread(target=self._run_sort, args=(folder,), daemon=True).start()
```

**Purpose:** Triggered by the "Sort Now" button. It validates the selected folder, logs the start, updates status, and launches a background thread to run `_run_sort`. This keeps the UI responsive.

### 7.9 Method `_run_sort`

```python
def _run_sort(self, folder):
    moved = main.organize_folder(folder, self.config, skip_stability_check=True)
    self.log_message(f"One‑time sort completed. Moved {moved} files.")
    self.status_var.set("Ready")
```

Runs in a background thread. Calls `organize_folder` from `main` with `skip_stability_check=True` so that all files are moved regardless of their age. After completion, it logs the result and resets the status. Note: it does **not** directly update UI widgets except via `log_message` (which puts a message in the queue) and `status_var.set` (which is thread‑safe because `StringVar` is designed to be updated from any thread, but it's safer to use `after`; however, `status_var.set` is generally safe in Tkinter). We use a queue for log messages to be extra safe.

### 7.10 Method `toggle_monitor`

```python
def toggle_monitor(self):
    if not self.monitor_active:
        # Start monitoring
        folder = self.folder_path.get()
        if not folder or not os.path.isdir(folder):
            self.log_message("Please select a valid folder first.")
            return

        self.log_message(f"Initial sort of {folder}")
        moved = main.organize_folder(folder, self.config, skip_stability_check=True)
        self.log_message(f"Initial sort moved {moved} files.")

        self.monitor = main.FolderMonitor(folder, self.config, callback=self.log_message)
        self.monitor.start()
        self.monitor_active = True
        self.monitor_btn.config(text="Stop Monitoring")
        self.status_var.set(f"Monitoring {folder} ...")
        self.log_message(f"Started real‑time monitoring of {folder}")
    else:
        # Stop monitoring
        if self.monitor:
            self.monitor.stop()
            self.monitor = None
        self.monitor_active = False
        self.monitor_btn.config(text="Start Monitoring")
        self.status_var.set("Ready")
        self.log_message("Monitoring stopped.")
```

**Purpose:** Handles toggling monitoring on/off.

**Start branch:**
- Validates folder.
- Performs an initial sort (with `skip_stability_check=True`) to clean up any existing files.
- Creates a `FolderMonitor` instance, passing the folder, config, and the `log_message` method as callback.
- Calls `start()` on the monitor (which starts the watchdog observer in a background thread).
- Updates UI: button text, status, and logs.

**Stop branch:**
- Calls `stop()` on the monitor.
- Resets the monitor attribute and UI state.

### 7.11 Method `on_closing`

```python
def on_closing(self):
    if self.monitor_active and self.monitor:
        self.monitor.stop()
    self.root.destroy()
```

Called when the user closes the window. It ensures the monitoring thread is stopped before the application exits.

Finally, the `if __name__ == "__main__":` block creates the Tk root, instantiates the App, and starts the main loop.

---

## 8. How Everything Works Together

1. **Startup:** The user runs `python ui.py`. The `App` class loads the configuration and displays the main window.

2. **User selects a folder** using the Browse button. The path is stored in `folder_path`.

3. **Sort Now:**
   - The user clicks "Sort Now".
   - `sort_now` validates the folder and starts a background thread.
   - In the background, `_run_sort` calls `main.organize_folder` with `skip_stability_check=True`.
   - `organize_folder` builds the extension map, iterates over all files, and for each file calls `organize_file`.
   - `organize_file` determines the target folder, creates it if necessary, resolves name conflicts, and moves the file. It logs each move via the Python `logging` module (which writes to file and console). The background thread also calls `log_message` to send the final summary to the UI via the queue.
   - The UI’s `poll_log_queue` picks up the summary and displays it in the log area.

4. **Start Monitoring:**
   - The user clicks "Start Monitoring".
   - `toggle_monitor` performs an initial sort (same as above) to clean up existing files.
   - It then creates a `FolderMonitor` object, passing `log_message` as the callback.
   - `monitor.start()` creates a watchdog `Observer` and a `Handler`, and starts the observer in a separate thread.
   - From now on, whenever a file is created or modified in the monitored folder (and not inside a category subfolder), `Handler._handle_event` is called.
   - The handler waits 1 second, then calls `organize_file` (with stability check enabled). It also sends a message via the callback, which puts the message into the queue and eventually appears in the UI log.
   - The monitoring continues until the user clicks "Stop Monitoring" or closes the application.

5. **Stopping:**
   - The user clicks "Stop Monitoring" → `monitor.stop()` stops the observer thread.
   - If the user closes the window, `on_closing` stops the monitor and destroys the window.

---

## 9. Troubleshooting and Tips

- **Nothing happens when I click Sort Now:**  
  Check the console or log file (`~/folder_organizer.log`) for error messages. Common issues:
  - The selected folder doesn't exist.
  - Permission errors (can't read files or write to subfolders).
  - The config file is missing or malformed (the app will fall back to defaults, but you may not see the categories you expect).

- **Files are not moving during monitoring:**  
  - Ensure the file is not already inside a category subfolder (the app skips those).  
  - Check if the file is being modified frequently (e.g., a download in progress). The stability check (60 seconds) will skip it until it's stable. You can reduce the `wait_seconds` in `is_file_stable` if needed.  
  - Make sure watchdog is installed (`pip install watchdog`).  
  - On some systems, watchdog may need additional permissions or may not detect certain file events (e.g., on network drives). Test by creating a simple text file in the monitored folder – you should see a log entry.

- **The UI freezes:**  
  This should not happen because long tasks are run in threads. If it does, check for errors in the background thread (they will appear in the console/log). Ensure you are not directly updating the UI from a background thread (we use the queue for that).

- **Duplicate filenames are handled correctly:**  
  The app appends `_1`, `_2`, etc. If you see files with unexpected names, it means a conflict occurred and was resolved.

- **How do I change the wait time for partially downloaded files?**  
  Edit the `wait_seconds` parameter in the call to `is_file_stable` inside `organize_file` (in `main.py`). For monitoring, the handler also waits 1 second before processing – you can adjust that as well.

- **Can I monitor multiple folders at once?**  
  Currently the app supports monitoring only one folder at a time. You could extend it by creating multiple `FolderMonitor` instances, but the UI would need to manage them.

---

## 10. Customization and Extending

- **Adding new file types:** Simply edit `config.json`. Add a new key with a list of extensions, or add extensions to existing categories.
- **Changing folder names:** Change the keys in `config.json`. The app will create folders with those names.
- **Recursive sorting:** The current version only sorts the top‑level folder, not subfolders. To add recursion, modify `organize_folder` to use `os.walk` or `Path.rglob`, but be careful to avoid moving files from already‑sorted subfolders.
- **Different stability check:** You could implement a more robust check (e.g., compare file size over a few seconds) by modifying `is_file_stable`.
- **Adding a pause/resume feature for monitoring:** The `FolderMonitor` class could be extended with a pause flag that the handler checks before acting.
- **Using a configuration GUI:** You could add a settings window to edit `config.json` directly from the app.
- **Logging level:** You can change the logging level in `main.py` to DEBUG to see more details.

---

This documentation should give you a deep understanding of every component of the Folder Organizer. Feel free to experiment and adapt it to your needs!