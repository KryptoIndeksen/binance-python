# binance-python
Python app med flask og ccxt som kobler seg opp mot binance.

### Funksjoner

Har endepunkter for å kjøpe/selge en krypto, samt hente prisen for et par.

### Bruk av endepunkter
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
