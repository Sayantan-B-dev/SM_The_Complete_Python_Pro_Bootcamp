import random
from tkinter import messagebox


def load_question(
    qn_index,
    qn_bank,
    question_label,
    answer_buttons,
    next_button,
):
    # Quiz finished
    if qn_index >= len(qn_bank):
        return None, None, True, True

    q = qn_bank[qn_index]
    correct_answer = q["correct_answer"]

    options = q["incorrect_answers"] + [correct_answer]
    random.shuffle(options)

    # Update question text
    question_label.config(
        text=f"Q{qn_index + 1}: {q['question']}"
    )

    # Reset buttons
    for btn in answer_buttons:
        btn.config(
            bg="SystemButtonFace",
            fg="black",
            state="normal"
        )

    # Fill options
    for btn, option in zip(answer_buttons, options):
        btn.config(text=option)

    next_button.config(text="Submit")

    return correct_answer, options, False, False


def select_answer(index, submitted, answer_buttons):
    if submitted:
        return index

    for btn in answer_buttons:
        btn.config(bg="SystemButtonFace")

    answer_buttons[index].config(bg="lightblue")
    return index


def submit_answer(
    selected_index,
    submitted,
    current_options,
    correct_answer,
    answer_buttons,
    score,
    score_label,
    next_button,
):
    if submitted:
        return score, submitted

    if selected_index is None:
        messagebox.showwarning("No Answer", "Please select an answer.")
        return score, submitted

    # Disable buttons
    for btn in answer_buttons:
        btn.config(state="disabled")

    correct_idx = current_options.index(correct_answer)

    # Highlight correct
    answer_buttons[correct_idx].config(bg="lightgreen")

    if current_options[selected_index] == correct_answer:
        score += 1
    else:
        answer_buttons[selected_index].config(bg="tomato")

    score_label.config(text=f"Score: {score}")
    next_button.config(text="Next")

    return score, True
