class Game:
    def __init__(self, quiz, player):
        """
        Coordinates quiz flow, input, and scoring.
        """
        self.quiz = quiz
        self.player = player

    def start(self):
        """
        Main entry point for the game.
        """
        self._clear_screen()
        print("=" * 60)
        print(f"           QUIZ GAME — Welcome {self.player.name}")
        print("=" * 60)

        while self.quiz.has_more_questions():
            self._play_round()

        self._show_final_score()

    def _play_round(self):
        """
        Executes one full question cycle.
        """
        question = self.quiz.get_current_question()
        question.display()

        user_choice = self._get_user_input(question)

        if question.is_correct(user_choice):
            print("\n✔ Correct!")
            self.player.increment_score()
        else:
            print("\n✘ Wrong!")
            print(f"The correct answer was: {question.options[question.correct_index - 1]}")

        self.quiz.next_question()
        self._show_progress()

        input("\nPress ENTER to continue...")
        self._clear_screen()

    def _get_user_input(self, question):
        """
        Safely handles numeric input.
        """
        while True:
            try:
                choice = int(input("Your answer (number): "))
                if question.is_valid_choice(choice):
                    return choice
                print("Invalid option number.")
            except ValueError:
                print("Please enter a valid number.")

    def _show_progress(self):
        """
        Displays running score in score/total format.
        """
        answered = self.quiz.current_index
        total = self.quiz.total_questions()
        score = self.player.get_score()

        print("\n" + "-" * 60)
        print(f"Score: {score}/{answered}    Progress: {answered}/{total}")
        print("-" * 60)

    def _show_final_score(self):
        """
        Displays final result summary.
        """
        print("\n" + "=" * 60)
        print("                 QUIZ COMPLETED")
        print("=" * 60)
        print(f"Final Score: {self.player.get_score()}/{self.quiz.total_questions()}")
        print("=" * 60)

    def _clear_screen(self):
        """
        Clears terminal screen (cross-platform).
        """
        import os
        os.system("cls" if os.name == "nt" else "clear")
