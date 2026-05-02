import requests
import pandas as pd
import time
import sys

# CoinGecko coin IDs (not symbols)
COINS = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "XRP": "ripple",
    "BNB": "binancecoin"
}


def get_ohlc(coin_id):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc"

    params = {
        "vs_currency": "usd",
        "days": "1"
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code != 200:
            print(f"⚠️ HTTP error {response.status_code} for {coin_id}")
            return None

        data = response.json()

        if not isinstance(data, list) or len(data) == 0:
            print(f"⚠️ Empty data for {coin_id}")
            return None

        df = pd.DataFrame(data, columns=[
            'time','open','high','low','close'
        ])

        # CoinGecko OHLC does not include volume → placeholder
        df['volume'] = 1  

        return df

    except Exception as e:
        print(f"❌ API error for {coin_id}: {e}")
        return None


def run():
    while True:
        try:
            print("🔍 Scanning coins (CoinGecko)...")
            sys.stdout.flush()

            for symbol, coin_id in COINS.items():
                try:
                    time.sleep(1)  # avoid rate limit

                    df = get_ohlc(coin_id)

                    if df is None or len(df) == 0:
                        print(f"⚠️ Skipping {symbol}")
                        continue

                    last = df.iloc[-1]

                    print(f"✅ {symbol} | Price: {last['close']}")
                    sys.stdout.flush()

                except Exception as e:
                    print(f"❌ {symbol} error: {e}")
                    sys.stdout.flush()

            print("=" * 50)
            sys.stdout.flush()

            time.sleep(30)

        except Exception as e:
            print(f"❌ MAIN LOOP ERROR: {e}")
            sys.stdout.flush()
            time.sleep(10)


if __name__ == "__main__":
    print("🚀 CoinGecko Scanner Started (Railway Safe)")
    sys.stdout.flush()
    run()
