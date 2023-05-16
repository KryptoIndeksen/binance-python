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
        responseJson = response.json()
        
        market_cap = {}
        close = 'c'
        cirulating= 'cs'
        symbol = 's'
        base = 'b'
        for element in responseJson:
            if element == "data":
                for data in responseJson[element]:#get data field in response
                    if data["q"] == quote:
                        #if trading pair has correct quote currency, then calculate market cap for that pair
                        c = float(data[close])
                        cs = int(data[cirulating] or 0)
                        market_cap[data[symbol]] = {
                            'pair': market_cap[data[symbol]],
                            'symbol': data[base],
                            'close': c,
                            'inCirculation': cs,
                            'marketCap': c*cs
                        }
        
        return sorted([value for value in market_cap.values()], key=lambda x:x['marketCap'], reverse=True)


@app.route('/price/<symbol>')
def get_price(symbol):
    ticker = exchange.fetch_ticker(symbol)
    latestPrice = {
        'symbol': ticker['symbol'],
        'price': ticker['last']
    }
    return jsonify(latestPrice)

@app.route('/buy', methods=['POST']) # amount is base currency. for BTC/USDT that is BTC
def buy():
    symbol = request.json['symbol']
    amount = request.json['amount']
    
    return place_order(symbol, amount, 'buy')

@app.route('/sell', methods=['POST']) # amount is base currency. For BTC/USDT that is BTC
def sell():
    symbol = request.json['symbol']
    amount = request.json['amount']
    
    return place_order(symbol, amount, 'sell')

def place_order(symbol, amount, side):
    order = exchange.create_order(symbol, "market", side, amount, None)
    return jsonify(order)

if __name__ == '__main__':
    app.run(debug=true)
