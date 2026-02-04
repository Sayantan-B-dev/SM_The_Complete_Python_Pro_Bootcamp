class Question:
    def __init__(self, text, options, correct_index):
        """
        Represents a single quiz question.

        text          : Question string
        options       : List of answer options
        correct_index : 1-based index of the correct option
        """
        self.text = text
        self.options = options
        self.correct_index = correct_index

    def display(self):
        """
        Displays the question and options
        in a clean, readable terminal format.
        """
        print("\n" + "=" * 60)
        print(self.text)
        print("-" * 60)

        for i, option in enumerate(self.options, start=1):
            print(f"  {i}. {option}")

        print("=" * 60)

    def is_valid_choice(self, choice):
        """
        Ensures the user input is within valid range.
        """
        return 1 <= choice <= len(self.options)

    def is_correct(self, choice):
        """
        Checks if the chosen option is correct.
        """
        return choice == self.correct_index
