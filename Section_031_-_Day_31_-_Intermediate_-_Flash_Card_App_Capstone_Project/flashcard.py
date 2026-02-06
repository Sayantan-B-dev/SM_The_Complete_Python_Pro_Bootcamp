import tkinter as tk
from tkinter import messagebox
import pandas as pd

# ----------------------------
# DATA SETUP (Dummy MCQ Data)
# ----------------------------

data = {
    "question": [
        "What is the output of print(2 ** 3)?",
        "Which data type is immutable?",
        "Which keyword defines a function in Python?",
        "What does pandas primarily work with?",
        "Which loop is best when iterations are unknown?"
    ],
    "options": [
        ["5", "6", "8", "9"],
        ["List", "Dictionary", "Set", "Tuple"],
        ["func", "define", "def", "lambda"],
        ["Lists", "Arrays", "DataFrames", "Strings"],
        ["for", "while", "do-while", "repeat"]
    ],
    "answer": [
        "8",
        "Tuple",
        "def",
        "DataFrames",
        "while"
    ]
}

df = pd.DataFrame(data)

# ----------------------------
# APPLICATION STATE
# ----------------------------

current_index = 0
attempted = 0
correct = 0

# ----------------------------
# UI SETUP
# ----------------------------

root = tk.Tk()
root.title("Flashcard MCQ")
root.geometry("700x450")
root.configure(bg="#f2f2f2")

# Center card frame
card = tk.Frame(
    root,
    bg="white",
    padx=30,
    pady=30,
    relief="flat"
)
card.place(relx=0.5, rely=0.5, anchor="center")

# Question text
question_label = tk.Label(
    card,
    text="",
    font=("Segoe UI", 16, "bold"),
    bg="white",
    wraplength=550,
    justify="center"
)
question_label.pack(pady=(0, 20))

# Option buttons container
options_frame = tk.Frame(card, bg="white")
options_frame.pack(pady=10)

option_buttons = []

# Progress label
progress_label = tk.Label(
    card,
    text="",
    font=("Segoe UI", 10),
    bg="white",
    fg="#666"
)
progress_label.pack(pady=(15, 5))

# Skip button
skip_button = tk.Button(
    card,
    text="Skip",
    font=("Segoe UI", 10),
    bg="#eeeeee",
    relief="flat",
    command=lambda: handle_skip()
)
skip_button.pack(pady=10)

# ----------------------------
# LOGIC FUNCTIONS
# ----------------------------

def load_question():
    """
    Loads the current question into the UI.
    Handles end-of-quiz condition safely.
    """
    global current_index

    # Clear old option buttons
    for btn in option_buttons:
        btn.destroy()
    option_buttons.clear()

    # End condition
    if current_index >= len(df):
        end_quiz()
        return

    # Set question text
    question_label.config(text=df.loc[current_index, "question"])

    # Create option buttons dynamically
    for option in df.loc[current_index, "options"]:
        btn = tk.Button(
            options_frame,
            text=option,
            font=("Segoe UI", 12),
            bg="#f7f7f7",
            relief="flat",
            width=30,
            command=lambda opt=option: handle_answer(opt)
        )
        btn.pack(pady=5)
        option_buttons.append(btn)

    update_progress()


def handle_answer(selected_option):
    """
    Handles answer selection.
    Updates score and moves forward.
    """
    global current_index, attempted, correct

    attempted += 1

    # Check correctness
    if selected_option == df.loc[current_index, "answer"]:
        correct += 1

    current_index += 1
    load_question()


def handle_skip():
    """
    Handles skipped questions.
    Skip counts as attempted but not correct.
    """
    global current_index, attempted

    attempted += 1
    current_index += 1
    load_question()


def update_progress():
    """
    Updates progress indicator text.
    """
    progress_label.config(
        text=f"Question {current_index + 1} of {len(df)}"
    )


def end_quiz():
    """
    Handles quiz completion safely.
    """
    question_label.config(
        text=f"Result: {correct} / {attempted} correct"
    )

    for btn in option_buttons:
        btn.destroy()

    skip_button.config(state="disabled")

# ----------------------------
# START APPLICATION
# ----------------------------

load_question()
root.mainloop()
