SUITS = ['h',
'd',
's',
'c']
NUMERICAL_SUITS = [1,2,3,4]
SUIT_RANKING_PAIRS = list(zip(NUMERICAL_SUITS,SUITS))
SUIT_RANKING_DICT = dict(zip(SUITS,NUMERICAL_SUITS))

CARD_VALUES = [str(i) for i in range(2,11)]+['J','Q','K','A']
NUMERICAL_VALUES = [i for i in range(2,15)]
CARD_RANKING_PAIRS = list(zip(NUMERICAL_VALUES,CARD_VALUES))
CARD_RANKING_DICT = dict(zip(CARD_VALUES,NUMERICAL_VALUES))

DECK = [(value,suit) for value in CARD_VALUES for suit in SUITS]

NUMERICAL_DECK = frozenset([(value,suit) for value in NUMERICAL_VALUES for suit in NUMERICAL_SUITS])
LIST_NUMERICAL_DECK = [[value,suit] for value in NUMERICAL_VALUES for suit in NUMERICAL_SUITS]

HAND_RANKINGS = reversed([
    'straight flush', 
    'four of a kind',
    'full house',
    'flush',
    'straight',
    'three of a kind',
    'two pair',
    'pair',
    'high card'
                ])
NUMERICAL_HAND_RANKINGS = [i for i in range(9)]
HAND_RANKING_PAIRS = list(zip(NUMERICAL_HAND_RANKINGS,HAND_RANKINGS))