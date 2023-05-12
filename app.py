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
exchange.set_sandbox_mode(CONFIG['isSandbox'])

@app.route('/get_price/<symbol>')
def get_price(symbol):
    ticker = ccxt.binance().fetch_ticker(symbol)
    latestPrice = {
        'symbol': ticker['symbol'],
        'price': ticker['last']
    }
    return jsonify(latestPrice)

@app.route('/buy', methods=['POST']) # amount er i base currency. for BTC/USDT er det BTC
def buy():
    symbol = request.json['symbol']
    amount = request.json['amount']
    
    return place_order(symbol, amount, 'buy')

@app.route('/sell', methods=['POST']) # amount er i base currency. for BTC/USDT er det BTC
def sell():
    symbol = request.json['symbol']
    amount = request.json['amount']
    
    return place_order(symbol, amount, 'sell')

def place_order(symbol, amount, side):
    order = exchange.create_order(symbol, "market", side, amount, None)
    return jsonify(order)

if __name__ == '__main__':
    app.run(debug=true)
