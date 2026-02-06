import tkinter as tk
from tkinter import ttk, messagebox

from quiz_ui import QuizUI
from quiz_constants import (
    ALL_CATEGORIES,
    ALL_DIFFICULTY,
    ALL_TYPES,
    DEFAULT_QUESTIONS,
    MIN_QUESTIONS,
    MAX_QUESTIONS,
)


class SetupApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Quiz Setup")
        self.root.geometry("300x260")
        self.root.resizable(False, False)

        # ---------- VARIABLES ----------
        self.amount_var = tk.IntVar(value=DEFAULT_QUESTIONS)
        self.category_var = tk.StringVar(value="General Knowledge")
        self.difficulty_var = tk.StringVar(value="Easy")
        self.type_var = tk.StringVar(value="Multiple Choice")

        # ---------- UI ----------
        tk.Label(self.root, text="Quiz Setup", font=("Arial", 14, "bold")).pack(pady=10)

        form = tk.Frame(self.root)
        form.pack(padx=10, pady=5, fill="x")

        # Amount
        tk.Label(form, text="Questions").grid(row=0, column=0, sticky="w", pady=5)
        tk.Spinbox(
            form,
            from_=MIN_QUESTIONS,
            to=MAX_QUESTIONS,
            textvariable=self.amount_var,
            width=8
        ).grid(row=0, column=1, sticky="e")

        # Category
        tk.Label(form, text="Category").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Combobox(
            form,
            textvariable=self.category_var,
            values=list(ALL_CATEGORIES.keys()),
            state="readonly",
            width=18
        ).grid(row=1, column=1, sticky="e")

        # Difficulty
        tk.Label(form, text="Difficulty").grid(row=2, column=0, sticky="w", pady=5)
        ttk.Combobox(
            form,
            textvariable=self.difficulty_var,
            values=list(ALL_DIFFICULTY.keys()),
            state="readonly",
            width=18
        ).grid(row=2, column=1, sticky="e")

        # Type
        tk.Label(form, text="Type").grid(row=3, column=0, sticky="w", pady=5)
        ttk.Combobox(
            form,
            textvariable=self.type_var,
            values=list(ALL_TYPES.keys()),
            state="readonly",
            width=18
        ).grid(row=3, column=1, sticky="e")

        # Start button
        tk.Button(
            self.root,
            text="Start Quiz",
            font=("Arial", 11, "bold"),
            command=self.start_quiz
        ).pack(pady=15)

        self.root.bind("<Return>", lambda e: self.start_quiz())
        self.root.mainloop()

    def start_quiz(self):
        try:
            amount = int(self.amount_var.get())
            if amount < MIN_QUESTIONS or amount > MAX_QUESTIONS:
                raise ValueError

            config = {
                "amount": amount,
                "category": ALL_CATEGORIES[self.category_var.get()],
                "difficulty": ALL_DIFFICULTY[self.difficulty_var.get()],
                "type": ALL_TYPES[self.type_var.get()],
            }

            self.root.destroy()
            QuizUI(config)

        except Exception:
            messagebox.showerror("Error", "Invalid setup values")


if __name__ == "__main__":
    SetupApp()
