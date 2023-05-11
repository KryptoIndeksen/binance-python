import ccxt
from flask import Flask, jsonify, request

app = Flask(__name__)

exchange = ccxt.binance({
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_SECRET_KEY',
    'enableRateLimit': True,
})

@app.route('/get_price/<symbol>')
def get_price(symbol):
    ticker = ccxt.binance().fetch_ticker(symbol)
    return jsonify(ticker['last'])

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
    app.run(host='0.0.0.0')
