import requests
import html
import random

from question import Question


TRIVIA_API_URL = "https://opentdb.com/api.php"


def fetch_questions(amount=5, difficulty="medium"):
    """
    Fetches questions from Open Trivia Database
    and converts them into Question objects.
    """
    params = {
        "amount": amount,
        "type": "multiple",
        "difficulty": difficulty
    }

    response = requests.get(TRIVIA_API_URL, params=params)
    data = response.json()

    questions = []

    for item in data["results"]:
        question_text = html.unescape(item["question"])
        correct_answer = html.unescape(item["correct_answer"])
        incorrect_answers = [
            html.unescape(ans) for ans in item["incorrect_answers"]
        ]

        options = incorrect_answers + [correct_answer]
        random.shuffle(options)

        correct_index = options.index(correct_answer) + 1

        questions.append(
            Question(
                question_text,
                options,
                correct_index
            )
        )

    return questions
