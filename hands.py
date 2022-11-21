
from constants import SUIT_RANKING_DICT as sr
from constants import CARD_RANKING_DICT as cr

class Card:
    """A card is determined by it's suit and value."""

    def __init__(self,value,suit):
        self.suit = suit
        self.value = value

    #Define eq and hash methods so that cards can be used in hands which must be cached as function inputs.

    def __eq__(self,other):
        return self.suit == other.suit and self.value == other.value

    def __hash__(self):
        return hash((self.suit, self.value))
    
    def __str__(self):
        return f'{self.value} of {self.suit}'

    def __repr__(self):
        return f'{self.value} of {self.suit}'

    def to_tuple(self):
        return (cr[self.value], sr[self.suit])

class Hand:
    """A hand is made up of cards."""

    def __init__(self,*cards):
        self.cards = frozenset(cards)

    #Define eq and hash methods so that hands can be cached as function inputs.

    def __eq__(self,other):
        return self.cards == other.cards

    def __hash__(self):
        return hash(self.cards)

    def __str__(self):
        return ', '.join([str(card) for card in self.cards])
    
    def __repr__(self):
        return ', '.join([str(card) for card in self.cards])

    def to_tuples(self):
        """Returns the tuple representation of the hand: a tuple of tuple pairs, sorted"""
        return tuple(sorted([card.to_tuple() for card in self.cards], reverse = True))

    @classmethod
    def make(cls,*vs_seq):
        """Make a hand by specifying an alternating sequence of values and SUITS."""
        cards = []
        for i in range(0,len(vs_seq),2):
            cards.append(Card(vs_seq[i],vs_seq[i+1]))
        return Hand(*cards)

