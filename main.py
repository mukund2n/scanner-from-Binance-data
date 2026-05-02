import requests
import pandas as pd
import time
import sys


def get_ohlc(symbol="bitcoin"):
    url = f"https://api.coingecko.com/api/v3/coins/{symbol}/ohlc"

    params = {
        "vs_currency": "usd",
        "days": "1"
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code != 200:
            print(f"⚠️ HTTP error {response.status_code}")
            return None

        data = response.json()

        if not isinstance(data, list) or len(data) == 0:
            print("⚠️ Empty data")
            return None

        df = pd.DataFrame(data, columns=[
            'time','open','high','low','close'
        ])

        # Fake volume (CoinGecko OHLC doesn't include volume)
        df['volume'] = 1  

        return df

    except Exception as e:
        print(f"❌ API error: {e}")
        return None

def run():
    symbol = "BTCUSDT"

    while True:
        try:
            print("🔍 Fetching BTCUSDT 1m data (Bybit)...")
            sys.stdout.flush()

            df = get_ohlc(symbol)

            if df is None or len(df) == 0:
                print("⚠️ Skipping due to no data")
                sys.stdout.flush()
                time.sleep(10)
                continue

            last = df.iloc[-1]

            print(f"✅ {symbol} | Price: {last['close']} | Volume: {last['volume']}")
            print("-" * 40)
            sys.stdout.flush()

            time.sleep(1)

        except Exception as e:
            print(f"❌ MAIN LOOP ERROR: {e}")
            sys.stdout.flush()
            time.sleep(10)


if __name__ == "__main__":
    print("🚀 Bybit Test Started (No Binance)")
    sys.stdout.flush()
    run()
