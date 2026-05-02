import requests
import pandas as pd
import time
import sys

def get_ohlc(symbol="BTCUSDT"):
    url = f"https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": "1m",
        "limit": 50
    }

    response = requests.get(url, params=params, timeout=10)
    data = response.json()

    df = pd.DataFrame(data, columns=[
        'time','open','high','low','close','volume',
        'close_time','qav','trades','tbbav','tbqav','ignore'
    ])

    df['close'] = df['close'].astype(float)
    df['volume'] = df['volume'].astype(float)

    return df


def run():
    while True:
        try:
            print("🔍 Fetching BTCUSDT 1m data...")
            sys.stdout.flush()

            df = get_ohlc("BTCUSDT")

            last = df.iloc[-1]

            print(f"Price: {last['close']} | Volume: {last['volume']}")
            print("-" * 40)
            sys.stdout.flush()

            time.sleep(20)

        except Exception as e:
            print(f"❌ Error: {e}")
            sys.stdout.flush()
            time.sleep(10)


if __name__ == "__main__":
    print("🚀 Binance Test Started")
    sys.stdout.flush()
    run()