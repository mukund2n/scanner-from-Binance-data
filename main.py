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
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 429:
            print("⚠️ Rate limit hit → Cooling down 90 sec...")
            sys.stdout.flush()
            time.sleep(90)
            return None

        if response.status_code != 200:
            print(f"⚠️ HTTP error {response.status_code}")
            return None

        return response.json()

    except Exception as e:
        print(f"❌ API error: {e}")
        return None


def run():
    while True:
        try:
            print("🔍 Scanning coins (Optimized)...")
            sys.stdout.flush()

            data = get_prices()

            if data is None:
                print("⚠️ Skipping cycle due to API issue")
                sys.stdout.flush()
                time.sleep(30)
                continue

            for coin in COINS:
                try:
                    price = data.get(coin, {}).get("usd")

                    if price is None:
                        print(f"⚠️ Missing price for {coin}")
                        continue

                    print(f"✅ {coin.upper()} | Price: {price}")

                except Exception as e:
                    print(f"❌ Error for {coin}: {e}")

            print("=" * 50)
            sys.stdout.flush()

            # 🔥 IMPORTANT: keep this slow
            time.sleep(60)

        except Exception as e:
            print(f"❌ MAIN LOOP ERROR: {e}")
            sys.stdout.flush()
            time.sleep(30)


if __name__ == "__main__":
    print("🚀 CoinGecko Optimized Scanner Started")
    sys.stdout.flush()
    run()
