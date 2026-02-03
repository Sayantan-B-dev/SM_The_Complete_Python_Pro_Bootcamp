class Quiz:
    def __init__(self, questions):
        """
        Controls question order and progression.
        """
        if not questions:
            raise ValueError("Quiz must contain at least one question.")

        self.questions = questions
        self.current_index = 0

    def has_more_questions(self):
        """
        Checks if questions remain.
        """
        return self.current_index < len(self.questions)

    def get_current_question(self):
        """
        Returns the active Question object.
        """
        return self.questions[self.current_index]

    def next_question(self):
        """
        Advances to the next question.
        """
        self.current_index += 1

    def reset(self):
        """
        Resets quiz progression.
        """
        self.current_index = 0

    def total_questions(self):
        """
        Returns total number of questions.
        """
        return len(self.questions)
