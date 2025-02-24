import time

def buy_from_exchange(crypto_symbol, amount):
    print(f"Wait buy {amount} {crypto_symbol} from exchange")
    time.sleep(1)
    print("Buyed successfully.")