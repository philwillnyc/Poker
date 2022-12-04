"""Cython algorithms for ranking seven-card hands and computing hold-em probabilities."""

from constants import LIST_NUMERICAL_DECK
from math import comb

cdef short hand_to_matrix(short[7][2] cards, short[13][4] hand_matrix):
    """Transform an array representation of a hand into a matrix representation.
    Rows are values, columns are suits."""
    cdef short i,j

    #Clear the matrix.

    for i in range(13):
        for j in range(4):
            hand_matrix[i][j] = 0

    for i in range(7):
        hand_matrix[cards[i][0]][cards[i][1]] = 1

    return 0

cdef short rank(short[13][4] hand_matrix, short[6] results):
    """Pass a 13 by 4 matrix that represents a 7 card hand.
    For easier indexing, lowest number is highest card.
    Modify the results array in place."""

    #Clear the results.

    results[0] = 0
    results[1] = 0
    results[2] = 0
    results[3] = 0
    results[4] = 0
    results[5] = 0

    #indices to use throughout

    cdef short i, j

    #Count values and suits. These will be used to define most of the hands.

    cdef short[13] value_counts = [0]*13
    cdef short[4] suit_counts = [0]*4

    for i in range(13):
        for j in range(4):
            value_counts[i]+=hand_matrix[i][j]
            suit_counts[j]+=hand_matrix[i][j]

    #get max of value counts and suit counts
    cdef short max_repeats = 1
    cdef short suit_max = 1

    for i in range(13):
        if value_counts[i]>max_repeats:
            max_repeats = value_counts[i]
    
    for j in range(4):
        if suit_counts[j]>suit_max:
            suit_max = suit_counts[j]

    #Hand rank variable gets highest priority, plus 5 other potential ranking variables
    #based on card values. 

    cdef short hand_rank
    cdef short c1 = 0
    cdef short c2 = 0
    cdef short c3 = 0
    cdef short c4 = 0
    cdef short c5 = 0
    cdef short flush = 0
    cdef short flush_column = -1

    cdef short run = 0
    cdef short top = 0

    
    #Case of a straight flush.

    if suit_max >=5:
        flush = 1
        #Check for the straight along a column.
        for j in range(4):
            if suit_counts[j] >=5:
                flush_column = j
                for i in range(13):
                    if hand_matrix[i][j] == 1:
                        if run == 0:
                            top = i
                        run+=1
                    else:
                        run = 0
                    if run == 5:
                        break

                if run == 5 or run == 4 and hand_matrix[j][0] == 1:
                    hand_rank = 0
                    c1 = top
                    results[:2] = hand_rank, c1
                    return 0

    #Case of a four of a kind.
    
    cdef short c2flag = 0
    if max_repeats == 4:
        hand_rank = 1
        for i in range(13):
            if value_counts[i] == 4:
                c1 = i
                if c2flag:
                    break
            elif value_counts[i] != 0 and not c2flag:
                c2 = i
                c2flag = 1
        results[:3] = hand_rank,c1,c2
        return 0
    
    #Find the second most occurring value to determine repeat based hands.

    cdef short second_max_repeats = 1
    cdef short max_repeats_flag = 0

    for i in range(13):
        if value_counts[i] == max_repeats:
            if max_repeats_flag:
                second_max_repeats = max_repeats
                break
            else:
                max_repeats_flag = 1

        elif value_counts[i]>second_max_repeats:
            second_max_repeats = value_counts[i]

    #Case of a full house.

    if max_repeats == 3 and second_max_repeats >=2:
        hand_rank = 2

    #Find the best three. 

        for i in range(13):
            if value_counts[i] == 3:
                c1 = i
                break

    #Find the best two.

        for i in range(13):
            if value_counts[i] >= 2 and i != c1:
                c2 = i
                break
        results[:3] = hand_rank,c1,c2
        return 0
    
    #Check for a flush.
   
    cdef int[5] top_values
    j = 0
    if flush == 1:
        hand_rank = 3
        for j in range(4):
            if suit_counts[j] >=5:
                flush_column = j
        j = 0
        for i in range(13):
            if j == 5:
                break
            if hand_matrix[i][flush_column] == 1:
                top_values[j] = i
                j+=1
        c1,c2,c3,c4,c5 = top_values
        results[:6] = hand_rank,c1,c2,c3,c4,c5
        return 0

    #Check for the straight along value counts.

    run = 0
    top = 0
    for i in range(13):
        if value_counts[i] >= 1:
            if run == 0:
                top = i
            run+=1
        else:
            run = 0
        if run == 5:
            break

    #Case of a straight.  
    
    if run == 5 or run == 4 and value_counts[0] > 0:
        hand_rank = 4
        c1 = top
        results[:2] = hand_rank,c1
        return 0
    

    #Case of a three of a kind.

    if max_repeats == 3:
        hand_rank = 5
        #Find the best three.
        for i in range(13):
            if value_counts[i] == 3:
                c1 = i
                break
        #Find the next best two cards. 
        j = 0
        for i in range(13):
            if j == 2:
                break
            if value_counts[i] == 1:
                top_values[j] = i
                j+=1
        c2,c3,_,_,_ = top_values
        results[:4] = hand_rank,c1,c2,c3
        return 0

    #Case of a two pair.
    
    if max_repeats == 2 and second_max_repeats == 2:
        hand_rank = 6

        #Find the best two and the second best two.

        j = 0
        for i in range(13):
            if j == 2:
                break
            if value_counts[i] == 2:
                top_values[j] = i
                j+=1
        c1,c2,_,_,_ = top_values

        #Find the best single (which might be part of a different pair.)
        
        for i in range(13):
            if value_counts[i] >= 1 and i!= c1 and i!=c2:
                c3 = i
                break
        results[:4] = hand_rank,c1,c2,c3
        return 0
    
    #Case of a pair.

    if max_repeats == 2:
        hand_rank = 7

        #Find the best two.

        for i in range(13):
            if value_counts[i] == 2:
                c1 = i
                break

        #Find the next best three values.

        j = 0
        for i in range(13):
            if j == 3:
                break
            if value_counts[i] == 1:
                top_values[j] = i
                j+=1
        c2,c3,c4,_,_ = top_values
        results[:5] = hand_rank,c1,c2,c3,c4
        return 0    

    #Case of high card.

    hand_rank = 8
    j = 0
    for i in range(13):
        if j == 5:
            break
        if value_counts[i] == 1:
            top_values[j] = i
            j+=1
    c1,c2,c3,c4,c5 = top_values
    results[:6] = hand_rank,c1,c2,c3,c4,c5
    return 0

cdef short compare_array(short arr1[6], short arr2[6]):
    """Compares the ranking arrays. Returns -1 for less than, 0 for equal, 1 for greater"""
    cdef short i
    for i in range(6):
        if arr1[i]<arr2[i]:
            return -1
        if arr1[i]>arr2[i]:
            return 1
    return 0

 #Initialize the seven card hands with the holdem cards. 

cdef short update_counts(short num_hands, #How many hands are being considered (max set to ten)
                    short[5][2] com_card_comb, #the combination being used
                    short[10][2][2] hh, #holdem hands
                    short[10][7][2] fh, #store the full hand after adding a community card combination
                    short[10][13][4] fhm, #stores hands in matrix form
                    short[10][6] ranks, #stores ranks
                    short[6] results, #results from ranking
                    long[10] wins, #stores number of wins for each player
                    long[10] ties): #stores ties stores number of ties

    """For a given combination of five cards a collection of holdem hands,
    update the wins/ties record based on the rankings of the resulting hands."""

    cdef short j = 0
    for j in range(num_hands):
        fh[j][:2] = hh[j]

    #Form seven-card hands using each hold-em pair. 
    #Transform each to a matrix and pass to the rank function.

    cdef short[10] win_or_tie
    cdef short min_count 
    cdef short[6] min_rank = [9,0,0,0,0,0]  #bigger than any hand rank

    for j in range(num_hands):
        fh[j][2:] = com_card_comb
        hand_to_matrix(fh[j],fhm[j])
        rank(fhm[j],results)
        ranks[j] = results

    #Now ranks contains rankings of each hand, so we can use this data 
    #to update wins or ties.

    min_count = 0
    win_or_tie = [0]*10

    for j in range(num_hands):
        if compare_array(ranks[j],min_rank) == -1:
            min_rank = ranks[j]
    
    for j in range(num_hands):
        if compare_array(ranks[j],min_rank) == 0:
            min_count+=1
            win_or_tie[j] = 1

    #If there are multiple min ranks, update ties. Otherwise, update wins.

    if min_count > 1:
        for j in range(num_hands):
            ties[j]+=win_or_tie[j]
    else:
        for j in range(num_hands):
            wins[j]+=win_or_tie[j]

cdef short count_outcomes(short num_hands, #how many hands are being considered (max set to ten)
                    short n, #number of already determined community cards
                    short ds, #remaining deck size
                    int num_comb, #number of combinations of community cards
                    short[48][2] rd, #remaining deck
                    short[5][2] cc, #already determined community cards
                    short[10][2][2] hh, #holdem hands
                    short[10][7][2] fh, #store the full hand after adding a community card combination
                    short[10][13][4] fhm, #stores hands in matrix form
                    short[10][6] ranks, #stores ranks
                    short[6] results, #results from ranking
                    long[10] wins, #stores number of wins for each player
                    long[10] ties): #stores ties stores number of ties

    """Creates all possible hands using the remaining cards 
    with the given community cards for each holdem hand. 
    Ranks the results and based on these ranks assigns win or tie."""

    #Iterate over all the combinations cards that use the remaining cards and community cards, and apply
    #the update_counts fuction. We divide into cases: 0, 3, 4, and 5 community cards available and use simple loops. 
    #There is likely a more natural way to iterate this, which would generalize better, but this gets the job
    #done and avoids having to use itertools.combinations, a key bottleneck. An alternative is to try a numpy array. 

    cdef short i0,i1,i2,i3,i4
    cdef short[5][2] com_card_comb
    cdef short r = 5-n
    cdef long i = 0

    #Case of no community cards.

    if n == 0:
        for i0 in range(ds-4):
            for i1 in range(i0+1,ds-3):
                for i2 in range(i1+1,ds-2):
                    for i3 in range(i2+1,ds-1):
                        for i4 in range(i3+1,ds):
                            com_card_comb = rd[i0],rd[i1],rd[i2],rd[i3],rd[i4]
                            update_counts(num_hands,com_card_comb,hh,fh,fhm,ranks,results,wins,ties)


     #Case of 3 community cards.

    elif n == 3:
        for i0 in range(ds-1):
            for i1 in range(i0+1,ds):
                com_card_comb = cc[0],cc[1],cc[2],rd[i0],rd[i1]
                update_counts(num_hands,com_card_comb,hh,fh,fhm,ranks,results,wins,ties)

    #Case of 4 community cards.

    elif n == 4:
        for i0 in range(ds):
            com_card_comb = cc[0],cc[1],cc[2],cc[3],rd[i0]
            update_counts(num_hands,com_card_comb,hh,fh,fhm,ranks,results,wins,ties)

    #Case of 5 community cards.
    
    elif n == 5:
        i = 0
        com_card_comb = cc[0],cc[1],cc[2],cc[3],cc[4]
        update_counts(num_hands,com_card_comb,hh,fh,fhm,ranks,results,wins,ties)

    return 0

def get_rank(*hand):
    
    """Pass a list corresponding to a seven card hand, return numerical ranking data. 
    Smaller numbers are better."""

    #Re-index.

    reindex = lambda pair: [12-(pair[0]-2), pair[1]-1]
    hand = list(map(reindex,hand))
    
    cdef short[13][4] hand_matrix
    cdef short[6] results = [0]*6
    cdef short[7][2] cards = hand

    hand_to_matrix(cards,hand_matrix)
    rank(hand_matrix, results)
    return results

def probabilities(community_cards, *holdem_hands):
    """Pass a list of known community cards, and a sequence of pairs corresponding
    to hold-em hands. Outputs an array giving the probability of each of
    the hands being a winning hand or tying hand."""
    
    #Validate the input:
    
    if len(community_cards) not in {0,3,4,5}:
        raise Exception('Not a flop, river, or turn situation.')
    if len(holdem_hands)>10 or len(holdem_hands)<2:
        raise Exception('Algorithm only supports between 2 and 10 cards.')

    #Modify the indexing:

    reindex = lambda pair: [12-(pair[0]-2), pair[1]-1]
    community_cards = list(map(reindex, community_cards))
    holdem_hands = [list(map(reindex, hand)) for hand in holdem_hands]
    REINDEXED_NUMERICAL_DECK = list(map(reindex, LIST_NUMERICAL_DECK))

    #Build the deck of remaining cards.

    used_cards = set([tuple(card) for card in community_cards]) 
    holdem_cards = set()
    for hand in holdem_hands:
        for card in hand:
            holdem_cards.add(tuple(card))
    used_cards = used_cards.union(holdem_cards)
    remaining_cards = []
    for card in REINDEXED_NUMERICAL_DECK:
        if tuple(card) not in used_cards:
            remaining_cards.append(card)

    #Initialize all the variables that will go into the cython function to count outcomes.
    
    cdef short num_hands = len(holdem_hands)
    cdef short n = len(community_cards)
    cdef short ds = 52 - n - 2*num_hands
    cdef int num_comb = comb(ds,5-n)
    cdef short[48][2] rd
    for i in range(len(remaining_cards)):
        rd[i] = remaining_cards[i]
    cdef short[5][2] cc
    for i in range(len(community_cards)):
        cc[i] = community_cards[i]
    cdef short[10][2][2] hh
    for i in range(len(holdem_hands)):
        hh[i] = holdem_hands[i]

    #Empty arrays to process and store data. 

    cdef short[10][7][2] fh = [[[0,0]]*7]*10
    cdef short[10][13][4] fhm = [[[0,0,0,0]]*13]*10
    cdef short[10][6] ranks = [[0]*6]*10
    cdef short[6] results = [0]*6
    cdef long[10] wins = [0]*10
    cdef long[10] ties = [0]*10

    #Process.

    count_outcomes(num_hands,n,ds,num_comb,rd,cc,hh,fh,fhm,ranks,results,wins,ties)

    #Remove extra space, divide, and return the final output. 

    w = [x for x in wins[:len(holdem_hands)]]
    t = [x for x in ties[:len(holdem_hands)]]
    output = [x/num_comb for x in w+t]
    return output

