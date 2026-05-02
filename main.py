import requests
import pandas as pd
import time
import sys

COINS = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "XRP": "ripple",
    "BNB": "binancecoin"
}


def get_price(coin_id):
    url = f"https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids": coin_id,
        "vs_currencies": "usd"
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 429:
            print("⚠️ Rate limit hit. Sleeping 60 sec...")
            time.sleep(60)
            return None

        if response.status_code != 200:
            print(f"⚠️ HTTP error {response.status_code}")
            return None

        data = response.json()

        return data[coin_id]["usd"]

    except Exception as e:
        print(f"❌ API error: {e}")
        return None


def run():
    while True:
        try:
            print("🔍 Scanning coins (SAFE MODE)...")
            sys.stdout.flush()

            for symbol, coin_id in COINS.items():
                try:
                    time.sleep(3)  # 🔥 VERY IMPORTANT (avoid 429)

                    price = get_price(coin_id)

                    if price is None:
                        print(f"⚠️ Skipping {symbol}")
                        continue

                    print(f"✅ {symbol} | Price: {price}")
                    sys.stdout.flush()

                except Exception as e:
                    print(f"❌ {symbol} error: {e}")
                    sys.stdout.flush()

            print("=" * 50)
            sys.stdout.flush()

            time.sleep(60)  # slower loop = stable

        except Exception as e:
            print(f"❌ MAIN LOOP ERROR: {e}")
            sys.stdout.flush()
            time.sleep(30)


if __name__ == "__main__":
    print("🚀 CoinGecko Stable Scanner Started")
    sys.stdout.flush()
    run()
