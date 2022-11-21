"""The logic for comparing hands according to hand rankings for standard poker.
Output is a tuple that allows for ties. Algorithm is written using custom objects.
Superceded by algorithm written using tuples.
"""
from collections import defaultdict
from constants import CARD_VALUES, HAND_RANKINGS
from hands import Card, Hand

#we need a mapping of the value of cards

values_dict = {}
for i,value in enumerate(CARD_VALUES):
    values_dict[value] = i+2
value_map = lambda x: values_dict[x]

#we also need a mapping of the hand rankings

hands_dict = {}
for i,hand in enumerate(reversed(HAND_RANKINGS)):
    hands_dict[hand] = i
hands_map = lambda x: hands_dict[x]

def identify(hand):
    """Return which kind of hand a given hand is, with relevant 
    value information for sorting hands of the same type."""
    #check for repeats
    values = defaultdict(int)
    for card in hand.cards:
        values[card.value]+=1

    num_unique = len(values.values())

    #only four of a kind and full house have two unique values

    if num_unique == 2:
        four, one, two, three = None, None, None, None
        for value in values:
            if values[value] == 4:
                four = value
            if values[value] == 1:
                one = value
            if values[value] == 3:
                three = value
            if values[value] ==2:
                two = value
        if four:
            return 'four of a kind', four, one
        else:
            return 'full house', three, two

    #only two pair and three of a kind have three unique values
    
    if num_unique == 3:
        singles = []
        pairs = []
        triples = []
        for value in values:
            count = values[value]
            if count == 2:
                pairs.append(value)
            elif count == 3:
                triples.append(value)
            else:
                singles.append(value)
        if len(singles) == 1:
            pair1, pair2 = sorted(pairs, key = value_map, reverse = True)
            return 'two pair', pair1, pair2, singles[0]
        else:
            single1, single2 = sorted(singles, key = value_map, reverse = True)
            return 'three of a kind', triples[0], single1, single2
    
    #only a pair has four unique values

    if num_unique == 4:
        singles = []
        for value in values:
            if values[value] == 1:
                singles.append(value)
            else:
                pair = value
        single1,single2,single3 = sorted(singles, key = value_map, reverse = True)
        return 'pair', pair, single1, single2, single3 

    #Now we have all unique value cards so we must check for straight and flush

    straight,flush = False,False

    #determine straight, remember ace can be low!

    ace_low = False
    NUMERICAL_VALUES = [value_map(value) for value in values]
    if max(NUMERICAL_VALUES) - min(NUMERICAL_VALUES) == 4:
        straight = True

    #ace low straight case

    elif max(NUMERICAL_VALUES) == 14:
        if all([x in NUMERICAL_VALUES for x in [2,3,4,5]]):
            straight = True
            ace_low = True

    #determine flush

    flush = len(set(card.suit for card in hand.cards)) == 1

    #determine high card

    sorted_values = sorted(values.keys(), key = value_map, reverse = True)
    high_card = sorted_values[0]

    if straight and flush:
        return 'straight flush', high_card if not ace_low else 5
    if straight:
        return 'straight', high_card if not ace_low else 5
    if flush:
        return ('flush',) + tuple(sorted_values)

    return ('high card',) + tuple(sorted_values)    

def process(hand):
    """Transform the output of identify into sortable tuples that correspond to the ranking of poker hands."""
    hand_type, *high_cards = identify(hand)
    return (hands_map(hand_type),)+tuple(map(value_map,high_cards))

def compare(*hands):
    """Return a list of which hands won, indexed by input order."""
    #save the input order and then sort them according to the output of process
    enumerated_hands = enumerate(hands)
    hand_ranks = sorted([(i,process(hand)) for (i,hand) in enumerated_hands], 
                        key = lambda x: x[1], 
                        reverse = True)
    winning_index, winning_rank = hand_ranks[0]
    indices = [winning_index]
    for i, rank in hand_ranks[1:]:
        if rank == winning_rank:
            indices.append(i)
        else:
            break
    return sorted(indices)



