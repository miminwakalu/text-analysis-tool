var express = require('express');
var app = express();

const quotes = [
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

app.get('/quotes/random', function (req, res) {
    randomQuote = quotes[Math.floor(Math.random() * quotes.length)];
    res.json(randomQuote);
})

app.listen(5000, function () {
    console.log('Express App running at http://127.0.0.1:5000');
})

