import ccxt
from flask import Flask, jsonify, request
import json
import requests

app = Flask(__name__)

def open_config():
    with open('./config/config.json', 'r') as f:
        data = json.loads(f.read())

    return data

CONFIG = open_config()

exchange = ccxt.binance({
    'apiKey': CONFIG['apiKey'],
    'secret': CONFIG['secret'],
    'enableRateLimit': True,
})
exchange.set_sandbox_mode(CONFIG['isSandbox'])

@app.route("/market_cap/<quote>")
def calculate_market_cap(quote): 
    response = requests.get('https://www.binance.com/exchange-api/v2/public/asset-service/product/get-products')
    if response.status_code == 200:
        data = response.json()
        
        ret = {}
        test = {}
        for element in data:
            if element == "data":
                for d in data[element]:
                    if d["q"] == quote:
                        c = float(d["c"])
                        cs = int(d["cs"] or 0)
                        ret[d["s"]] = {
                            'symbol': d["b"],
                            'c': c,
                            'cs': cs,
                            'market_cap': c*cs
                        }
        
        return sorted([value for value in ret.values()], key=lambda x:x['market_cap'], reverse=True)


@app.route('/price/<symbol>')
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
