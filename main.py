import requests
import pandas as pd
import time
import sys


def get_ohlc(symbol="BTCUSDT"):
    url = "https://api.bybit.com/v5/market/kline"

    params = {
        "category": "linear",
        "symbol": symbol,
        "interval": "1",
        "limit": 50
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)

        # 🔴 FIRST check raw response
        if response.status_code != 200:
            print(f"⚠️ HTTP error {response.status_code}: {response.text}")
            return None

        try:
            data = response.json()
        except Exception:
            print(f"⚠️ Non-JSON response: {response.text[:100]}")
            return None

        if data.get("retCode") != 0:
            print(f"⚠️ API error: {data}")
            return None

        candles = data.get("result", {}).get("list", [])

        if not candles:
            print(f"⚠️ No candle data for {symbol}")
            return None

        candles.reverse()

        df = pd.DataFrame(candles, columns=[
            'time','open','high','low','close','volume','turnover'
        ])

        df['close'] = df['close'].astype(float)
        df['volume'] = df['volume'].astype(float)

        return df

    except Exception as e:
        print(f"❌ API exception: {e}")
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
