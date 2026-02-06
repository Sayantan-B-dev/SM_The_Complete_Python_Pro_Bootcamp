import requests
from quiz_constants import clean_html_text, MAX_QUESTIONS

OPEN_TRIVIA_URL = "https://opentdb.com/api.php"


class Question:
    def __init__(self, amount, category, difficulty, q_type):
        self.amount = min(amount, MAX_QUESTIONS)
        self.category = category
        self.difficulty = difficulty
        self.q_type = q_type
        self.question_data = []

        self.get_questions()

    def get_questions(self):
        params = {
            "amount": self.amount,
            "category": self.category,
            "difficulty": self.difficulty,
            "type": self.q_type,
        }

        response = requests.get(OPEN_TRIVIA_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data["response_code"] != 0 or not data["results"]:
            raise ValueError("No questions found for selected options")

        self.question_data = self.clean_data(data["results"])

    def clean_data(self, data):
        cleaned = []
        for q in data:
            cleaned.append({
                "question": clean_html_text(q["question"]),
                "correct_answer": clean_html_text(q["correct_answer"]),
                "incorrect_answers": [
                    clean_html_text(a) for a in q["incorrect_answers"]
                ],
            })
        return cleaned
