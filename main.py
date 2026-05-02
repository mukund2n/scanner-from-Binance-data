import requests
import time
import sys

COINS = ["bitcoin", "ethereum", "solana", "ripple", "binancecoin"]

def get_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids": ",".join(COINS),
        "vs_currencies": "usd"
    }

    try:
        response = requests.get(url, params=params, timeout=5)

        if response.status_code == 429:
            print("⚠️ Rate limit hit")
            return None

        if response.status_code != 200:
            print(f"⚠️ HTTP error {response.status_code}")
            return None

        return response.json()

    except Exception as e:
        print(f"❌ API error: {e}")
        return None


def run():
    last_prices = {}
    heartbeat = 0

    while True:
        try:
            print(f"💓 Alive tick {heartbeat}")
            sys.stdout.flush()

            data = get_prices()

            if data:
                for coin in COINS:
                    price = data.get(coin, {}).get("usd")

                    if price:
                        prev = last_prices.get(coin)

                        # Print only if changed (reduces spam)
                        if prev != price:
                            print(f"📊 {coin.upper()} → {price}")
                            last_prices[coin] = price

            else:
                print("⚠️ API skipped")

            heartbeat += 1
            sys.stdout.flush()

            # 🔥 KEY: small continuous activity
            time.sleep(5)

        except Exception as e:
            print(f"❌ LOOP ERROR: {e}")
            sys.stdout.flush()
            time.sleep(3)


if __name__ == "__main__":
    print("🚀 Stable Scanner LIVE")
    sys.stdout.flush()
    run()
