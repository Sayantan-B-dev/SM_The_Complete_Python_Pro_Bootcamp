import tkinter as tk
from tkinter import filedialog, scrolledtext
import threading
import queue
import os
from pathlib import Path
import main  # our logic module

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Folder Organizer")
        self.root.geometry("700x500")
        self.root.resizable(True, True)

        # Variables
        self.folder_path = tk.StringVar()
        self.monitor_active = False
        self.monitor = None
        self.log_queue = queue.Queue()
        self.config = main.load_config()  # load once

        # Build UI
        self.create_widgets()

        # Start periodic queue check
        self.poll_log_queue()

    def create_widgets(self):
        # Top frame: folder selection
        top_frame = tk.Frame(self.root, padx=10, pady=10)
        top_frame.pack(fill=tk.X)

        tk.Label(top_frame, text="Folder:").pack(side=tk.LEFT)
        entry = tk.Entry(top_frame, textvariable=self.folder_path, width=50)
        entry.pack(side=tk.LEFT, padx=5)
        tk.Button(top_frame, text="Browse", command=self.browse_folder).pack(side=tk.LEFT)

        # Button frame
        btn_frame = tk.Frame(self.root, padx=10, pady=5)
        btn_frame.pack(fill=tk.X)

        self.sort_btn = tk.Button(btn_frame, text="Sort Now", command=self.sort_now, width=15)
        self.sort_btn.pack(side=tk.LEFT, padx=5)

        self.monitor_btn = tk.Button(btn_frame, text="Start Monitoring", command=self.toggle_monitor, width=18)
        self.monitor_btn.pack(side=tk.LEFT, padx=5)

        # Log area
        log_frame = tk.Frame(self.root, padx=10, pady=10)
        log_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(log_frame, text="Activity Log:").pack(anchor=tk.W)
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, state='normal')
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)

    def log_message(self, message):
        """Add message to log area (thread‑safe via queue)."""
        self.log_queue.put(message)

    def poll_log_queue(self):
        """Check queue for new log messages and update UI."""
        try:
            while True:
                msg = self.log_queue.get_nowait()
                self.log_text.insert(tk.END, msg + "\n")
                self.log_text.see(tk.END)
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.poll_log_queue)

    def sort_now(self):
        """Perform a one‑time sort of the selected folder."""
        folder = self.folder_path.get()
        if not folder:
            self.log_message("Please select a folder first.")
            return
        if not os.path.isdir(folder):
            self.log_message("Selected path is not a valid directory.")
            return

        self.log_message(f"Starting one‑time sort of {folder}")
        self.status_var.set("Sorting...")
        # Run sort in a thread to keep UI responsive
        threading.Thread(target=self._run_sort, args=(folder,), daemon=True).start()

    def _run_sort(self, folder):
        # skip_stability_check=True to move all files immediately
        moved = main.organize_folder(folder, self.config, skip_stability_check=True)
        self.log_message(f"One‑time sort completed. Moved {moved} files.")
        self.status_var.set("Ready")

    def toggle_monitor(self):
        if not self.monitor_active:
            # Start monitoring
            folder = self.folder_path.get()
            if not folder:
                self.log_message("Please select a folder first.")
                return
            if not os.path.isdir(folder):
                self.log_message("Selected path is not a valid directory.")
                return

            # First, do an initial sort (skip stability check to catch existing files)
            self.log_message(f"Initial sort of {folder}")
            moved = main.organize_folder(folder, self.config, skip_stability_check=True)
            self.log_message(f"Initial sort moved {moved} files.")

            # Create and start monitor
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

    def on_closing(self):
        """Ensure monitor stops when window is closed."""
        if self.monitor_active and self.monitor:
            self.monitor.stop()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()