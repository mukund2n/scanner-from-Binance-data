def get_ohlc(symbol="BTCUSDT"):
    url = "https://api.bybit.com/v5/market/kline"
    
    params = {
        "category": "linear",
        "symbol": symbol,
        "interval": "1",
        "limit": 50
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get("retCode") != 0:
            print(f"⚠️ API error: {data}")
            return None

        candles = data["result"]["list"]

        if not candles:
            print(f"⚠️ No candle data for {symbol}")
            return None

        # Bybit returns newest first → reverse it
        candles.reverse()

        df = pd.DataFrame(candles, columns=[
            'time','open','high','low','close','volume','turnover'
        ])

        df['close'] = df['close'].astype(float)
        df['volume'] = df['volume'].astype(float)

        return df

    except Exception as e:
        print(f"❌ API error: {e}")
        return None
