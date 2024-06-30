import random
from typing import List, Tuple, Dict

suits = ['hearts', 'diamonds', 'clubs', 'spades']
ranks = ['6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']

class Card:
    def __init__(self, suit: str, rank: str):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]
        random.shuffle(self.cards)

    def draw(self) -> Card:
        return self.cards.pop()

    def __len__(self):
        return len(self.cards)

def deal_cards(num_players) -> Tuple[Dict[int, List[Card]], Card, List[Card]]:
    if num_players < 2 or num_players > 6:
        raise ValueError("Number of players must be between 2 and 6")
    deck = Deck()
    
    players_hands = {player: [deck.draw() for _ in range(6)] for player in range(num_players)}

    trump_card = deck.draw()

    remaining_deck = deck.cards

    return players_hands, trump_card, remaining_deck