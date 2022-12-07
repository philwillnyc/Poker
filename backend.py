from flask import Flask, render_template, request
from constants import SUITS, CARD_VALUES

app = Flask(__name__)



@app.route('/', methods=['GET'])
def home():
    num_hands = 0
    return render_template('home.html', num_hands = num_hands)

@app.route('/', methods=['POST'])
def hands():
    num_hands = int(request.form['num_hands'])
    hand_numbers = [str(i) for i in range(1,num_hands+1)]
    return render_template('home.html', 
    num_hands = num_hands,
    hand_numbers = hand_numbers, 
    SUITS = SUITS,
    CARD_VALUES = CARD_VALUES
    )

@app.route('/compute', methods=['GET', 'POST'])
def compute():
    pass

app.run()