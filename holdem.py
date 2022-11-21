"""Algorithm for determining which player wins a hold-em hand when all 
information is available."""
from functools import lru_cache
from object_based_algorithms import identify, process
from hands import Card, Hand
from itertools import combinations

@lru_cache
def winner(*hands,flop,turn,river):
    """Given hands, a set of three flop cards, and the turn and river card,
    output the indices of the winning hands."""
    for hand in hands:
        pass
    


# cards = [Card(8,'Diamonds'),
#         Card(8,'Spades'),
#         Card(3,'Diamonds'),
#         Card(5,'Clubs'),
#         Card('Queen','Clubs'),
#         Card('Queen','Spades'),
#         Card(4,'Diamonds'),]

# print(find_best(*cards))