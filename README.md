# binance-python

Python app med flask og ccxt som kobler seg opp mot binance.

### Funksjoner

Har endepunkter for å kjøpe/selge en krypto, samt hente prisen for et par.

### Bruk

Se [config.json](config.json) for eksempel på konfigurasjon. Hvis isSandbox == true så er vi i testmodus. apiKey og secret kan genereres på [binance](https://testnet.binance.vision/). Om den er false så er man live og nøkler genereres inne på din bruker på [Binance.com](https://binance.com)
#### Bruk av endepunkter

Standard port som blir satt er port 5000

> /get_price/{symbol}

Returnerer prisen på et gitt par.

> /buy

Body må være på formen:

```json
{
  symbol: String
  amount: 0.1
}
```

> /sell

Body må være på formen:

```json
{
  symbol: String
  amount: Float
}
```

Begge to vil opprette en *market* order
