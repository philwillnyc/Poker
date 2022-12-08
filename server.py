"""Flask server for the web interface."""
from flask import Flask, render_template, request
from constants import SUITS, CARD_VALUES

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    """Initial appearance of page."""
    num_hands = 0
    return render_template('home.html', num_hands = num_hands)

@app.route('/', methods=['POST'])
def enter_number_hands():
    num_hands = int(request.form['num_hands'])
    hand_numbers = [str(i) for i in range(1,num_hands+1)]
    return render_template(
                        'home.html', 
                        num_hands = num_hands,
                        hand_numbers = hand_numbers, 
                        SUITS = SUITS,
                        CARD_VALUES = CARD_VALUES
                            )


@app.route('/compute', methods=['POST'])
def compute():
    request

def main():
    hands = []
    flop = []
    turn = None
    river = None
    app.run()

if __name__ == '__main__':
    main()