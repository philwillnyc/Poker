"""Python based computational algorithms for ranking 7 card hands and computing
Hold-em probabilities. Very slow compared to the Cython based algorithms."""

import numpy as np
from math import comb
from itertools import combinations
from collections import defaultdict
from functools import lru_cache
from constants import NUMERICAL_DECK


@lru_cache(maxsize = None)
#There are 133,784,560 possible hands. We could reduce this by combining equivalent suit cases.
#how much memory would it take to save all of this, and how quickly would it load and be accessed?
def rank(*hand):
    """Pass seven cards, assumed to be sorted. 
    Returns a tuple based ranking of the best possible hand. 
    Format: (numerical_hand_rank,*comparison_card_values)."""


    #count the number of times each value and each suit occurs. 

    number_counts, suit_counts = defaultdict(int),defaultdict(int)
    for number, suit in hand:
        number_counts[number]+=1
        suit_counts[suit]+=1

    #first, look for flush based on suit counts:

    flush_suit = None
    for suit in suit_counts:
        suit_freq = suit_counts[suit]
        if  suit_freq >= 5:
            flush_suit = suit
            break

    #case A: 5 or more of one suit: flush or straight flush.
    if flush_suit:
        #Get the cards of the flush suit and look for a straight flush
        suited_numbers = [card[0] for card in filter(lambda card: card[1] == flush_suit, hand)]
        #Tack on an ace low at the end if the ace is there
        if 14 in suited_numbers:
            suited_numbers.append(1)
        sf_count = 1
        top_value = suited_numbers[0]
        for i,value in enumerate(suited_numbers[1:]):
            if value == suited_numbers[i] - 1:
                sf_count+=1
                if sf_count == 5: 
                    #We've found the best straight flush.
                    return (8,top_value)
            else:
                #Reset the counts
                sf_count = 1
                top_value = value

        #we didn't find a straight flush. Just return the values of the top flush cards
        return (5,)+tuple(suited_numbers[:5])

    #Case B: 4 or less of every suit. Flush and straight flush are ruled out above.

    #Divide into cases based on value counts.

    counts_items = sorted(number_counts.items(), 
                            key = lambda item: item[1],
                            reverse = True)
    counts_pattern = [x[1] for x in counts_items]
    numbers_set = set(number_counts.keys())
    

    leading_val,leading_count = counts_items[0]

    #Case 1: 4, _, ... Will be 4 of a kind.

    if  leading_count == 4:
        high_card = max(numbers_set-{leading_val})
        return (7,leading_val, high_card)

    #Case 2: 3,3,1. Will be full house.

    if counts_pattern == [3,3,1]:
        next_val = counts_items[1][0]
        if next_val>leading_val:
            return (6,next_val,leading_val)
        else:
            return (6,leading_val,next_val)

    #Case 3: 3,2,2: Will be full house.

    if counts_pattern == [3,2,2]:
        pairs = {counts_items[0][0],counts_items[1][0]}
        return (6, leading_val, max(pairs))
        
    #Case 4: 3,2,1,1. Will be full house.

    if counts_pattern == [3,2,1,1]:
        next_val = counts_items[1][0]
        return (6,leading_val,next_val)

    #At this point look for a straight to make the remaining cases, all lower hands, easier.

    numbers = [card[0] for card in hand]
    augmented_numbers = numbers + [1]*number_counts[14]

    #Walk through the augmented numbers and increment the straight count if appropriate.

    straight_count = 1
    top_number = augmented_numbers[0]
    for i, number in enumerate(augmented_numbers[1:]):
        prev_number = augmented_numbers[i]
        if number == prev_number:
            continue
        if number == prev_number - 1:
            straight_count += 1
            if straight_count >= 5:
                return (4,top_number)
        else:
            straight_count = 1
            top_number = number
    
    #Now that we've ruled out straights, we can handle the patterns for the lower hands.

        #Case 5: 3,1,1,1,1. Three of a kind.
    
    if counts_pattern == [3,1,1,1,1]:
        remaining_numbers = sorted(list(numbers_set-{leading_val}), reverse = True)
        second, third, *_ = remaining_numbers
        return (3,second,third)

        #Case 6: 2,2,2,1. Two pair.
    
    if counts_pattern == [2,2,2,1]:
        pairs = {counts_items[0][0],counts_items[1][0],counts_items[2][0]}
        worst_pair = min(pairs)
        pairs = pairs-{worst_pair}
        other_card = counts_items[-1][0]
        return (2,max(pairs),min(pairs),max(other_card,worst_pair))
        
        #Case 7: 2,2,1,1,1. Two pair. 

    if counts_pattern == [2,2,1,1,1]:
        pairs = {counts_items[0][0],counts_items[1][0]}
        top_pair = max(pairs)
        other_pair = min(pairs)
        other_card = max(numbers_set-{top_pair,other_pair})
        return (2,top_pair,other_pair,other_card)

        #Case 8: 2,1,1,1,1,1. Pair. 

    if counts_pattern == [2,1,1,1,1,1]:
        pair = counts_items[0][0]
        remaining_numbers = sorted(list(numbers_set-{pair}), reverse = True)
        return (1,pair)+tuple(remaining_numbers[:3])

        #Case 9: #1,1,1,1,1,1,1. High card.

    if counts_pattern == [1,1,1,1,1,1,1]:
        return (0,)+tuple(sorted(list(numbers_set))[:5])

    raise(Exception('Something went wrong with the input.'))

@lru_cache(maxsize = None)
def compare(*hands):
    """Pass sorted tuple representations of 7 card hands, output will be a numpy array
    of winning and tying indices (1 for win or tie, 0 for loss; all wins come first then ties)."""
    ranks = [rank(*hand) for hand in hands]
    max_rank = max(ranks)
    results = []
    tie = False
    repeat_flag = False
    for r in ranks:
        if r == max_rank:
            if repeat_flag:
                tie = True
            results.append(1)
            if not repeat_flag:
                repeat_flag = True
        else:
            results.append(0)
    
    if tie:
        return np.array([0]*len(hands)+results)
    else:
        return np.array(results+[0]*len(hands))

@lru_cache(maxsize = None)
def probabilities(community_cards, *holdem_hands):
    """Pass a tuple of known community cards, and a sequence of pairs corresponding
    to hold-em hands. Outputs a numpy array giving the probability of each of the hands being a winning hand."""

    holdem_cards = set()
    for hand in holdem_hands:
        for card in hand:
            holdem_cards.add(card)
    remaining_cards = NUMERICAL_DECK-holdem_cards.union(community_cards)
    num_unknown = 5-len(community_cards)
    possible_rem_cards = (cards for cards in combinations(remaining_cards,num_unknown))
    m = comb(len(remaining_cards),num_unknown)
   
    #numpy array with a row for each combination
    output = np.zeros((m,2*len(holdem_hands)))

    for i,cards in enumerate(possible_rem_cards):
        hands = [tuple(sorted(cards+community_cards+hand)) for hand in holdem_hands]
        output[i] += compare(*hands)
    #add all the rows of the numpy array, divided by size of sample space
    return np.sum(output,axis = 0)/m

test_hands = [((5,1),(6,4)),
            ((14,2),(14,3)),
            ((14,1),(13,1))]

#print(compare(((2, 2), (2, 3), (3, 4), (4, 3), (12, 1), (12, 4), (14, 4)),
#((3, 4), (4, 3), (5, 2), (6, 2), (12, 1), (12, 4), (14, 4))))
print(probabilities(tuple(),*test_hands))


# print(probabilities(frozenset([(14,3),
#                                 (13,4),
#                                 (9,4),
#                                 (10,3),
#                                 (8,1)]),

#                                 ((14,1),
#                                 (14,2)),
#                                 ((5,3),
#                                 (6,4))))


    
    









    

