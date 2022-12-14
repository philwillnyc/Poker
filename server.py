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
        self.show_community_form = False
        self.show_hands_form = False
        self.show_probabilities = False
    
    def update(self):
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
        #reset the data
        holdem_data.hands.clear()
        view.num_hands = 0
        return render_template('home.html', 
                            holdem_data = holdem_data, 
                            view = view,
                            SUITS = SUITS,
                            CARD_VALUES = CARD_VALUES
                            )

    @app.route('/', methods=['POST'])
    def enter_number_hands():
        """Enter the number of hands and update page."""
        print(request.form['num_hands'])
        view.num_hands = int(request.form['num_hands'])
        view.update()
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

        #turn off hands form and turn on community form
        view.show_hands_form = False
        view.show_community_form = True
        view.show_probabilities = True

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

