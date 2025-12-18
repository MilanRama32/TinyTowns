from Cards import Card

class Building:
    def __init__(self, card: Card, position: tuple):
        self.card = card
        self.position = position
        self.score = 0

    def score(self, board):
        self.score = self.card.scoreSelf(self.position, board)
        return self.score