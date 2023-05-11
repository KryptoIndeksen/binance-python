import ccxt
from flask import Flask, jsonify, request
import json

app = Flask(__name__)

def open_config():
    with open('./config.json', 'r') as f:
        data = json.loads(f.read())

    return data

CONFIG = open_config()

exchange = ccxt.binance({
    'apiKey': CONFIG['apiKey'],
    'secret': CONFIG['secret'],
    'enableRateLimit': True,
})

@app.route('/get_price/<symbol>')
def get_price(symbol):
    ticker = ccxt.binance().fetch_ticker(symbol)
    latestPrice = {
        'symbol': ticker['symbol'],
        'price': ticker['last']
    }
    return jsonify(latestPrice)

@app.route('/buy', methods=['POST'])
def buy():
    symbol = request.json['symbol']
    amount = request.json['amount']

    market_order = exchange.create_market_buy_order(symbol, amount)

    return jsonify(market_order)

@app.route('/sell', methods=['POST'])
def sell():
    symbol = request.json['symbol']
    amount = request.json['amount']

    market_order = exchange.create_market_sell_order(symbol, amount)

    return jsonify(market_order)

if __name__ == '__main__':
    app.run(debug=true)
