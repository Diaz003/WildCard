import random
from cards import Card

class Deck:
    def __init__(self):
        self.cards = []
        self.discard_pile = []
        self.create_hearts_deck()
        self.shuffle()
    
    def create_hearts_deck(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        for rank in ranks:
            self.cards.append(Card('hearts', rank))
    
    def shuffle(self):  # Método añadido
        random.shuffle(self.cards)
    
    def draw_card(self):
        if not self.cards:
            self.refill_deck_from_discard()
        return self.cards.pop()