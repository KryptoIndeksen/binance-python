# binance-python

Python app using flask and ccxt to connect to the binance exchange.

### Functionality

This app has endpoints to look up the price for a given trading pair and to buy/sell crypto with market orders.

## Installation

Clone or fork this repo. Install and run this app with

```shell
pip3 install requirements.txt
python3 -m   flask run
```

or build a docker image with

```shell
docker build --tag python-binance .
```

and start the image with
```shell
docker run -p 127.0.0.1:3000:5000/tcp python-binance
```

### Usage

Look at [config.json](config.json) for examples of configurating this app. if isSandbox is set to true then the app is in test mode. Then you will look at real prices, but all buy and sell orders are not actually made. apiKey and secret can be generated at [binance testnet](https://testnet.binance.vision/).

If it is set to false then buy/sell orders will be excecuted. keys can be generated for your user at [Binance.com](https://binance.com)

#### Usage of endpoints

This app uses port 5000 and available endpoints are:

> /get_price/{symbol}

which returns the price for the given symbol pair.

> /buy

Will place a market buy order on binance for a given amount and symbol pair.

Body needs to be as follows:

```json
{
  symbol: String
  amount: 0.1
}
```

> /sell

Will place a market sell order on binance for a given amount and symbol pair.

Body needs to be as follows:

```json
{
  symbol: String
  amount: Float
}
```
