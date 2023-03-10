"""Flask for the web interface."""
from flask import Flask, render_template, request, session
from flask_session import Session
from constants import SUITS, CARD_VALUES
from holdem import Card, Holdem

class View():
    """Class for storing viewing details of the page."""
    def __init__(self):
        self.num_hands = 0
        self.hand_numbers = []
        self.hand_numbers_pairs = []
        #settings for which page elements display
        self.start_button = "Begin"
        self.show_hands_form = False
        self.show_flop_form = False
        self.show_turn_form = False
        self.show_river_form = False
        self.show_probabilities = False
        self.show_community_info = False
        #keep track of which cards are in play to avoid duplicates

        self.cards = set()
    
    def update_hand_numbers(self):
        """Generates hand number data to use in display."""
        self.hand_numbers = [str(i+1) for i in range(self.num_hands)]
        self.hand_numbers_pairs = [(i,str(i+1)) for i in range(self.num_hands)]
    
    def clear(self):
        """Clears the view data."""
        self.num_hands = 0
        self.hand_numbers.clear()
        self.hand_numbers_pairs.clear()
        self.start_button = "Begin"
        self.show_hands_form = False
        self.show_flop_form = False
        self.show_turn_form = False
        self.show_river_form = False
        self.show_probabilities = False
        self.show_community_info = False
        self.cards.clear()

#Create the flask app and a holdem object to store hand data, and a view
#object to keep track of the various viewing components.

app = Flask(__name__)

#Set up individual sessions so multiple users don't conflict. 

app.secret_key = '123456789'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
server_session = (Session(app))

#When something goes wrong with the input, restart. This could be made to do a lot more.

def restart():
    """Restart everything."""

    session['holdem_data'] = Holdem()
    session['view'] = View()

    return render_template(
            'home.html', 
            holdem_data = session['holdem_data'],
            view =  session['view'], 
            SUITS = SUITS,
            CARD_VALUES = CARD_VALUES,
                )

@app.route('/', methods=['GET'])
def home():
    """Initial appearance of page."""
    return restart()

@app.route('/', methods=['POST'])
def enter_number_hands():
    """Enter the number of hands and update page."""
    holdem_data = session['holdem_data']
    view =  session['view']

    view.num_hands = int(request.form['num_hands'])
    view.update_hand_numbers()
    view.start_button = "Restart"

    #clear data
    holdem_data.clear()
    view.show_flop_form = False
    view.show_turn_form = False
    view.show_river_form = False
    view.show_probabilities = False
    view.show_community_info = False
    
    #turn on hands form
    view.show_hands_form = True
    return render_template(
                        'home.html', 
                        holdem_data = holdem_data,
                        view = view,
                        SUITS = SUITS,
                        CARD_VALUES = CARD_VALUES
                            )

@app.route('/hands', methods=['POST'])
def enter_hands():
    """Enter hands and update page."""
    holdem_data = session['holdem_data']
    view =  session['view']
    for i in range(view.num_hands):
        #look up the suits and values of each of the cards
        r = request.form
        if 'NULL' in r.values():
            return restart()
        hand = []
        for card_num in ['first','second']:
            value_key,suit_key = f'{card_num}_value{i+1}', f'{card_num}_suit{i+1}'
            value, suit = r[value_key], r[suit_key]
            card = Card(value,suit)
            if card in view.cards:
                return restart()  
            else:
                hand.append(Card(value,suit))
                view.cards.add(card)

        holdem_data.add_hand(*hand)
    
    #turn on flop form, turn off hands form, turn on community display and probabilities

    view.show_hands_form = False
    view.show_flop_form = True
    view.show_probabilities = True
    view.show_community_info = True

    #update the probabilities

    holdem_data.update_probabilities()

    return render_template(
                        'home.html', 
                        holdem_data = holdem_data,
                        view = view, 
                        SUITS = SUITS,
                        CARD_VALUES = CARD_VALUES,
                            )

@app.route('/flop', methods = ['POST'])
def flop():
        """Enter the flop and update the page."""
        holdem_data = session['holdem_data']
        view =  session['view']
        r = request.form
        if 'NULL' in r.values():
            return restart()
        flop = []
        for card_num in ['first','second','third']:
            value_key,suit_key = f'{card_num}_value', f'{card_num}_suit'
            value, suit = r[value_key], r[suit_key]
            card = Card(value,suit)
            if card in view.cards:
                return restart()  
            else:
                flop.append(card)
                view.cards.add(card)

        holdem_data.set_flop(*flop)
        
        #turn on turn form, turn off flop form
        view.show_turn_form = True
        view.show_flop_form = False

        #update the probabilities
        holdem_data.update_probabilities()

        return render_template(
                        'home.html', 
                        holdem_data = holdem_data,
                        view = view, 
                        SUITS = SUITS,
                        CARD_VALUES = CARD_VALUES,

                            )
@app.route('/turn', methods = ['POST'])
def turn():
    """Enter the turn and update the page."""
    holdem_data = session['holdem_data']
    view =  session['view']
    r = request.form
    if 'NULL' in r.values():
        return restart()
    value, suit = r['value'], r['suit']
    card = Card(value,suit)
    if card in view.cards:
        return restart()  
    else:
        holdem_data.set_turn(card)
    
    #turn on river form, turn off turn form
    view.show_river_form = True
    view.show_turn_form = False

    #update the probabilities
    holdem_data.update_probabilities()

    return render_template(
                    'home.html', 
                    holdem_data = holdem_data,
                    view = view, 
                    SUITS = SUITS,
                    CARD_VALUES = CARD_VALUES,
                        )

@app.route('/river', methods = ['POST'])
def river():
    holdem_data = session['holdem_data']
    view =  session['view']
    """Enter the river and update the page."""
    r = request.form
    if 'NULL' in r.values():
        return restart()
    value, suit = r['value'], r['suit']
    card = Card(value,suit)
    if card in view.cards:
        return restart()  
    else:
        holdem_data.set_river(card)
    

    #update the probabilities
    holdem_data.update_probabilities()

    #turn off river form
    view.show_river_form = False

    return render_template(
                    'home.html', 
                    holdem_data = holdem_data,
                    view = view, 
                    SUITS = SUITS,
                    CARD_VALUES = CARD_VALUES,
                        )
app.run(debug = True)


