from trivia_api import fetch_questions
from quiz import Quiz
from player import Player
from game import Game


def main():
    """
    Application entry point.
    """
    name = input("Enter your name: ").strip()
    if not name:
        name = "Player"

    questions = fetch_questions(amount=5, difficulty="medium")

    quiz = Quiz(questions)
    player = Player(name)
    game = Game(quiz, player)

    game.start()


if __name__ == "__main__":
    main()
