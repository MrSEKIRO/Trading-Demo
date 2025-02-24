min_crypto_amount = {
    "ABAN": 10
}

def get_min_amount(crypto_name):
    min_amount = min_crypto_amount.get(crypto_name)
    return min_amount