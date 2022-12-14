from constants import SUIT_RANKING_DICT as SR
from constants import CARD_RANKING_DICT as CR
from algorithms import probabilities

class Card:
    def __init__(self,value,suit):
        """values and suits should be entered as strings as they are in constants.py."""
        self.value = value
        self.suit = suit
    
    def to_numerical(self):
        """returns a numerical array based on the card."""
        return [CR[self.value],SR[self.suit]]

class Holdem:
    """Class for data on a hold-em game."""
    def __init__(self, *hands, flop = [], turn = None, river = None):

        self.flop = flop
        self.turn = turn
        self.river = river
        self.hands = []
        self.probabilities = []

        for hand in hands:
            self.hands.append(hand)
        
        if len(self.hands)>1:
            self.update_probabilities()
        
    def add_hand(self,card1, card2):
        """Adds a hand and updates the probabilities."""
        self.hands.append([card1,card2])
        if len(self.hands) >= 2:
            self.update_probabilities()
    
    def set_flop(self,card1,card2,card3):
        """Sets the flop and updates probabilities."""
        self.flop.clear()
        self.flop+=[card1,card2,card3]
        self.update_probabilities()

    def set_turn(self,card):
        """Sets the turn and updates probabilities."""
        self.turn = card
        self.update_probabilities()
    
    def set_river(self,card):
        """Sets the river and updates probabilities."""
        self.river = card
        self.update_probabilities()

    def update_probabilities(self):
        """Computes the probabilities and stores the result."""
        community_cards = []
        if self.flop:
            for card in self.flop:
                community_cards.append(card.to_numerical())
        if self.turn:
            community_cards.append(self.turn.to_numerical())
        if self.river:
            community_cards.append(self.river.to_numerical())
        hands = [[card.to_numerical() for card in hand] for hand in self.hands]
        self.probabilities.clear()
        self.probabilities = probabilities(community_cards,*hands)

    def percentages(self, percentage = True, rounding = 2):
        """returns probabilities as percentages (or proportions), rounded
        divided into wins and ties."""
        if not self.probabilities:
            return

        if percentage:
            mult = 100
        else:
            mult = 1

        output = list(map(lambda x: round(mult*x,rounding),self.probabilities))
        return output[:len(self.hands)//2+1], output[len(self.hands)//2+1:]
        
h = Holdem([Card('Nine','Hearts'),Card('Nine','Diamonds')],
        [Card('Two','Hearts'),Card('Three','Spades')])


print(h.percentages())