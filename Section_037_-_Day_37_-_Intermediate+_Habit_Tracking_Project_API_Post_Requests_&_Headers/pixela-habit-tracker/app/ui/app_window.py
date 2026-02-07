import tkinter as tk
from tkinter import messagebox

from app.ui.habit_form import HabitForm
from app.ui.graph_view import GraphView
from app.utils.exceptions import HabitTrackerError, PixelaAPIError


class AppWindow:
    def __init__(self, habit_manager):
        self.habit_manager = habit_manager
        self._blocked = False
        self._rate_warned = False

        self.root = tk.Tk()
        self.root.title("Pixela Habit Tracker")
        self.root.geometry("420x380")
        self.root.resizable(False, False)

        self._build()

    def _build(self):
        box = tk.Frame(self.root, padx=20, pady=20)
        box.pack(fill="both", expand=True)

        tk.Label(
            box,
            text="Habit Tracker",
            font=("Segoe UI", 16, "bold"),
        ).pack(pady=(0, 10))

        self.status = tk.Label(
            box,
            text="Ready",
            anchor="w",
            fg="gray",
        )
        self.status.pack(fill="x", pady=(0, 10))

        self.form = HabitForm(
            box,
            on_add=self._add,
            on_update=self._update,
            on_delete=self._delete,
        )
        self.form.pack(fill="x")

        self.graph = GraphView(box)
        self.graph.pack(pady=15)

        url = (
            f"{self.habit_manager.client.base_url}"
            f"/users/{self.habit_manager.client.username}"
            f"/graphs/{self.habit_manager.graph_id}.html"
        )
        self.graph.set_graph_url(url)

    # --------------------
    # CORE UX GUARD
    # --------------------

    def _run(self, action, success_msg):
        if self._blocked:
            return

        self._blocked = True
        self.form.set_enabled(False)
        self.status.config(text="Processing...")

        try:
            action()
            self.status.config(text=success_msg)
            messagebox.showinfo("Success", success_msg)

        except PixelaAPIError as e:
            if e.status_code == 503 and not self._rate_warned:
                self._rate_warned = True
                messagebox.showwarning(
                    "Pixela Rate Limit",
                    "Pixela rejected this request due to free-tier throttling.\n\n"
                    "Please wait a few seconds before clicking again.\n\n"
                    "This may happen randomly (≈25% of requests).",
                )
            else:
                messagebox.showerror("Pixela Error", str(e))

            self.status.config(text="Error")

        except HabitTrackerError as e:
            messagebox.showerror("Error", str(e))
            self.status.config(text="Error")

        finally:
            self.root.after(1200, self._unblock)

    def _unblock(self):
        self._blocked = False
        self.form.set_enabled(True)
        self.status.config(text="Ready")

    # --------------------
    # ACTIONS
    # --------------------

    def _add(self, q):
        self._run(
            lambda: self.habit_manager.add_habit(q),
            "Habit entry added for today.",
        )

    def _update(self, q):
        self._run(
            lambda: self.habit_manager.update_habit(q),
            "Habit entry updated for today.",
        )

    def _delete(self):
        self._run(
            lambda: self.habit_manager.delete_habit(),
            "Today's habit entry deleted (if it existed).",
        )

    def run(self):
        self.root.mainloop()
