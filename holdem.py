class Card:
    def __init__(self,value,suit):
        """values and suits should be entered as strings as they are in constants.py."""
        self.value = value
        self.suit = suit

class Holdem:
    """Class for data on a hold-em game."""
    def __init__(self, flop = None, turn = None, river = None, *hands):

        self.flop = flop
        self.turn = turn
        self.river = river
        self.hands = hands 

    def percentages():
        """Passes card data to the probabilities algorithm. Returns formatted text on the percentages
        of wins and ties."""
