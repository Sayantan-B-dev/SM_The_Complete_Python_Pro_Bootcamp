import tkinter as tk
from tkinter import ttk


class HabitForm(tk.Frame):
    def __init__(self, parent, on_add, on_update, on_delete):
        super().__init__(parent)
        self.on_add = on_add
        self.on_update = on_update
        self.on_delete = on_delete
        self._build()

    def _build(self):
        ttk.Label(self, text="Quantity").pack(anchor="w")

        self.entry = ttk.Entry(self)
        self.entry.pack(fill="x", pady=(0, 10))

        row = ttk.Frame(self)
        row.pack(fill="x")

        self.add_btn = ttk.Button(row, text="Add", command=self._add)
        self.add_btn.pack(side="left", expand=True, fill="x", padx=3)

        self.update_btn = ttk.Button(row, text="Update", command=self._update)
        self.update_btn.pack(side="left", expand=True, fill="x", padx=3)

        self.delete_btn = ttk.Button(row, text="Delete Today", command=self._delete)
        self.delete_btn.pack(side="left", expand=True, fill="x", padx=3)

    def set_enabled(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        self.add_btn.config(state=state)
        self.update_btn.config(state=state)
        self.delete_btn.config(state=state)

    def _add(self):
        v = self.entry.get().strip()
        if v:
            self.on_add(v)

    def _update(self):
        v = self.entry.get().strip()
        if v:
            self.on_update(v)

    def _delete(self):
        self.on_delete()
