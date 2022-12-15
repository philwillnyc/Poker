"""Flask for the web interface."""
from flask import Flask, render_template, request
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
    
    def update_hand_numbers(self):
        self.hand_numbers = [str(i+1) for i in range(self.num_hands)]
        self.hand_numbers_pairs = [(i,str(i+1)) for i in range(self.num_hands)]


def main():

    #create the flask app and a holdem object to store hand data, and a view
    #object to keep track of the various viewing components.
    app = Flask(__name__)
    holdem_data = Holdem()
    view = View()

    @app.route('/', methods=['GET'])
    def home():
        """Initial appearance of page."""

        return render_template('home.html', 
                            holdem_data = holdem_data, 
                            view = view,
                            SUITS = SUITS,
                            CARD_VALUES = CARD_VALUES
                            )

    @app.route('/', methods=['POST'])
    def enter_number_hands():
        """Enter the number of hands and update page."""
        view.num_hands = int(request.form['num_hands'])
        view.update_hand_numbers()
        view.start_button = "Restart"

        #clear data
        holdem_data.hands.clear()
        holdem_data.flop.clear()
        holdem_data.turn = None
        holdem_data.river = None

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
        for i in range(view.num_hands):
            #look up the suits and values of each of the cards
            r = request.form
            hand = []
            for card_num in ['first','second']:
                value_key,suit_key = f'{card_num}_value{i+1}', f'{card_num}_suit{i+1}'
                value, suit = r[value_key], r[suit_key]
                hand.append(Card(value,suit))
            holdem_data.add_hand(*hand)
        
        #turn on flop form, off hand form

        view.show_hands_form = False
        view.show_flop_form = True
        view.show_probabilities = True

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
            r = request.form
            flop = []
            for card_num in ['first','second','third']:
                value_key,suit_key = f'{card_num}_value', f'{card_num}_suit'
                value, suit = r[value_key], r[suit_key]
                flop.append(Card(value,suit))
            holdem_data.set_flop(*flop)
            
            #turn on turn form, community card info, turn off flop form
            view.show_turn_form = True
            view.show_community_info = True
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
        r = request.form
        value, suit = r['value'], r['suit']
        card = Card(value,suit)
        holdem_data.set_turn(card)
        
        #turn on river form, turn form off
        view.show_turn_form = False
        view.show_river_form = True

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
        """Enter the river and update the page."""
        r = request.form
        value, suit = r['value'], r['suit']
        card = Card(value,suit)
        holdem_data.set_river(card)
        
        #turn off river form
        view.show_river_form = False

        #update the probabilities
        holdem_data.update_probabilities()

        return render_template(
                        'home.html', 
                        holdem_data = holdem_data,
                        view = view, 
                        SUITS = SUITS,
                        CARD_VALUES = CARD_VALUES,
                            )
    app.run()

if __name__ == '__main__':
    main()

