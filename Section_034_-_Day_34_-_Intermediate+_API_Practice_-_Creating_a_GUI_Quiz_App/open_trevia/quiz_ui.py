import tkinter as tk
from tkinter import messagebox
from questions import Question
from quizlogic import load_question, select_answer, submit_answer


class QuizUI:
    def __init__(self, config):
        self.config = config

        # ---------- WINDOW ----------
        self.window = tk.Tk()
        self.window.title("Quiz Challenge")
        self.window.geometry("720x720")
        self.window.resizable(False, False)
        self.window.configure(bg="#2c3e50")

        # ---------- STATE ----------
        self.qn_index = 0
        self.score = 0
        self.selected_index = None
        self.submitted = False
        self.correct_answer = None
        self.current_options = None

        # ---------- UI ----------
        self.build_ui()
        self.load_questions()

        self.window.mainloop()

    def build_ui(self):
        # ================= HEADER =================
        header = tk.Frame(self.window, bg="#34495e", pady=10)
        header.pack(fill="x")

        self.score_label = tk.Label(
            header,
            text="Score: 0",
            font=("Arial", 14, "bold"),
            bg="#34495e",
            fg="white"
        )
        self.score_label.pack(side="left", padx=20)

        self.progress_label = tk.Label(
            header,
            text="Question: 0/0",
            font=("Arial", 12),
            bg="#34495e",
            fg="#dcdcdc"
        )
        self.progress_label.pack(side="right", padx=20)

        # ================= QUESTION CARD =================
        card = tk.Frame(
            self.window,
            bg="#ecf0f1",
            padx=25,
            pady=25,
            bd=2,
            relief="ridge"
        )
        card.pack(padx=20, pady=25, fill="x")

        self.question_label = tk.Label(
            card,
            text="Loading questions...",
            font=("Arial", 16),
            bg="#ecf0f1",
            fg="#2c3e50",
            wraplength=640,
            justify="center"
        )
        self.question_label.pack()

        # ================= ANSWERS =================
        self.answers_frame = tk.Frame(self.window, bg="#2c3e50")
        self.answers_frame.pack(pady=10)

        self.answer_buttons = []
        for i in range(4):
            btn = tk.Button(
                self.answers_frame,
                text="",
                font=("Arial", 12),
                width=45,
                height=2,
                bg="#ecf0f1",
                fg="#2c3e50",
                activebackground="#bdc3c7",
                relief="raised",
                bd=2,
                cursor="hand2",
                command=lambda idx=i: self.select_answer(idx)
            )
            btn.pack(pady=6)
            self.answer_buttons.append(btn)

        # ================= CONTROLS =================
        controls = tk.Frame(self.window, bg="#2c3e50")
        controls.pack(fill="x", pady=20, padx=20)

        self.next_button = tk.Button(
            controls,
            text="Submit Answer",
            font=("Arial", 13, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            padx=25,
            pady=8,
            cursor="hand2",
            command=self.submit_answer
        )
        self.next_button.pack(side="right")

        tk.Button(
            controls,
            text="Exit Quiz",
            font=("Arial", 11),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            padx=18,
            pady=8,
            cursor="hand2",
            command=self.exit_quiz
        ).pack(side="left")

    def load_questions(self):
        try:
            self.question_data = Question(
                self.config["amount"],
                self.config["category"],
                self.config["difficulty"],
                self.config["type"],
            )

            self.qn_bank = self.question_data.question_data
            if not self.qn_bank:
                raise ValueError("No questions loaded")

            self.progress_label.config(
                text=f"Question: 1/{len(self.qn_bank)}"
            )
            self.load_question()

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.window.destroy()

    def load_question(self):
        result = load_question(
            self.qn_index,
            self.qn_bank,
            self.question_label,
            self.answer_buttons,
            self.next_button,
        )

        if result[3]:
            self.show_final_score()
            return

        self.correct_answer, self.current_options, self.submitted, _ = result
        self.selected_index = None

        self.progress_label.config(
            text=f"Question: {self.qn_index + 1}/{len(self.qn_bank)}"
        )

    def select_answer(self, index):
        self.selected_index = select_answer(
            index,
            self.submitted,
            self.answer_buttons
        )

    def submit_answer(self):
        if not self.submitted:
            self.score, self.submitted = submit_answer(
                self.selected_index,
                self.submitted,
                self.current_options,
                self.correct_answer,
                self.answer_buttons,
                self.score,
                self.score_label,
                self.next_button,
            )
        else:
            self.qn_index += 1
            if self.qn_index >= len(self.qn_bank):
                self.show_final_score()
            else:
                self.load_question()

    def show_final_score(self):
        percentage = (self.score / len(self.qn_bank)) * 100
        grade = (
            "A+" if percentage >= 90 else
            "A" if percentage >= 80 else
            "B" if percentage >= 70 else
            "C" if percentage >= 60 else
            "D" if percentage >= 50 else
            "F"
        )

        messagebox.showinfo(
            "Quiz Completed",
            f"Score: {self.score}/{len(self.qn_bank)}\n"
            f"Percentage: {percentage:.1f}%\n"
            f"Grade: {grade}"
        )
        self.window.destroy()

    def exit_quiz(self):
        if messagebox.askyesno("Exit Quiz", "Are you sure you want to exit?"):
            self.window.destroy()
