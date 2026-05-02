import requests
import pandas as pd
import time
import sys


def get_ohlc(symbol="BTCUSDT"):
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": "1m",
        "limit": 50
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        # Validate response
        if not isinstance(data, list) or len(data) == 0:
            print(f"⚠️ Invalid/empty response for {symbol}: {data}")
            return None

        df = pd.DataFrame(data, columns=[
            'time','open','high','low','close','volume',
            'close_time','qav','trades','tbbav','tbqav','ignore'
        ])

        if df.empty:
            print(f"⚠️ DataFrame empty for {symbol}")
            return None

        df['close'] = df['close'].astype(float)
        df['volume'] = df['volume'].astype(float)

        return df

    except Exception as e:
        print(f"❌ API error for {symbol}: {e}")
        return None


def run():
    symbol = "BTCUSDT"

    while True:
        try:
            print("🔍 Fetching BTCUSDT 1m data...")
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

            time.sleep(20)

        except Exception as e:
            print(f"❌ MAIN LOOP ERROR: {e}")
            sys.stdout.flush()
            time.sleep(10)


if __name__ == "__main__":
    print("🚀 Binance Test Started")
    sys.stdout.flush()
    run()
