SUITS = ['Hearts',
'Diamonds',
'Spades',
'Clubs']
CARD_VALUES = ['Two','Three','Four','Five','Six','Seven',
                'Eight','Nine','Ten','Jack','Queen','King','Ace']


NUMERICAL_SUITS = [1,2,3,4]
NUMERICAL_VALUES = [i for i in range(2,15)]

SUIT_RANKING_DICT = dict(zip(SUITS,NUMERICAL_SUITS))
CARD_RANKING_DICT = dict(zip(CARD_VALUES,NUMERICAL_VALUES))

DECK = [(value,suit) for value in CARD_VALUES for suit in SUITS]
NUMERICAL_DECK = frozenset([(value,suit) for value in NUMERICAL_VALUES for suit in NUMERICAL_SUITS])
LIST_NUMERICAL_DECK = [[value,suit] for value in NUMERICAL_VALUES for suit in NUMERICAL_SUITS]
