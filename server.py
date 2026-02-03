# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, abort

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

# The route() function of the Flask class is a decorator
# which tells the application which URL should call
# the associated function.
@app.route('/health')
# ‘/’ URL is bound with hello_world() function.
def healthCheck():
    return 'Flask server is up and running!'

@app.route('/analyze-stock/<ticker>')
# ‘/’ URL is bound with hello_world() function.
def analyzeStock(ticker):
    if len(ticker) > 5 or not ticker.isidentifier():
        abort(400, description="Invalid ticker symbol")
    return {'data': f'Analysis for stock {ticker} coming soon'}

# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application
    # on the local development server.
    app.run()