import random
from flask import Flask, request

app = Flask(__name__)

quotes = [
    {
        'text': 'An eye for an eye only ends up making the whole world blind.',
        'author': 'Mahatma Gandhi'
    },
    {
        'text': 'When in doubt, tell the truth.',
        'author': 'Mark Twain'
    },
    {
        'text': 'You are who you choose to be.',
        'author': 'Iron Giant'
    }
]

@app.route('/quotes/random', methods=['GET'])
def get_random_quote():
    return random.choice(quotes)

if __name__ == '__main__':
    app.run(port=5000)
