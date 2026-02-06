from html import unescape

# ----------- HTML CLEANING -----------

def clean_html_text(text):
    return unescape(text)


# ----------- QUIZ OPTIONS -----------

ALL_CATEGORIES = {
    "General Knowledge": 9,
    "Books": 10,
    "Film & TV": 11,
    "Music": 12,
    "Science & Nature": 17,
    "Computers": 18,
    "Mathematics": 19,
    "Sports": 21,
    "Geography": 22,
    "History": 23,
}

ALL_DIFFICULTY = {
    "Easy": "easy",
    "Medium": "medium",
    "Hard": "hard",
}

ALL_TYPES = {
    "Multiple Choice": "multiple",
    "True/False": "boolean",
}

MIN_QUESTIONS = 1
MAX_QUESTIONS = 50
DEFAULT_QUESTIONS = 10
