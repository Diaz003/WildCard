import random

class Card:
    SUITS = ["♠", "♥", "♦", "♣"]
    VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

    def __init__(self):
        self.value = random.choice(self.VALUES)
        self.suit = random.choice(self.SUITS)

    def __str__(self):
        return f"{self.value}{self.suit}"

class Deck:
    def __init__(self):
        self.cards = [Card() for _ in range(52)]
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop() if self.cards else None
