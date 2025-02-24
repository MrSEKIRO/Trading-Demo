prices = {
    "ABAN": 4
}

def get_crypto_price(crypto_symbol):
    price = prices.get(crypto_symbol)
    return price