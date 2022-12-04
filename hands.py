from constants import SUIT_RANKING_DICT as sr
from constants import CARD_RANKING_DICT as cr

class Card:
    """A card is determined by it's suit and value, integer based. 
    For making and displaying cards, use the simple string notation, e.g. JC for jack of clubs."""

    def __init__(self,value,suit):
        self.suit = suit
        self.value = value
    
    def __str__(self):
        return f'{self.value} of {self.suit}'

    def __repr__(self):
        return f'{self.value} of {self.suit}'

    def to_list(self):
        return [cr[self.value], sr[self.suit]]

    @classmethod()
    def make(cls,value: str, suit: str):
        pass

class Hand:
    """A hand is made up of Cards."""

    def __init__(self,*cards):

        self.cards = cards

    def __str__(self):
        return ', '.join([str(card) for card in self.cards])
    
    def __repr__(self):
        return ', '.join([str(card) for card in self.cards])

    def to_list(self):
        """Returns the list representation of the hand: a list of pairs, sorted."""
        return list(sorted([card.to_list() for card in self.cards], reverse = True))


