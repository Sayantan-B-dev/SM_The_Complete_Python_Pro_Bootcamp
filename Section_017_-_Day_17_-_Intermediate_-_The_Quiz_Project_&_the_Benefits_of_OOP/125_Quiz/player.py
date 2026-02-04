class Player:
    def __init__(self, name):
        """
        Stores player identity and score.
        """
        self.name = name
        self.score = 0

    def increment_score(self):
        """
        Increases score by one.
        """
        self.score += 1

    def reset_score(self):
        """
        Resets score to zero.
        """
        self.score = 0

    def get_score(self):
        """
        Returns current score.
        """
        return self.score
