import ccxt
import telebot
import pandas as pd
import time
import os
from dotenv import load_dotenv  

# Load environment variables from .env file
load_dotenv()

# 🔹 Telegram Bot Settings
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# 🔹 Binance API Setup
exchange = ccxt.binance()

# 🔹 Coins and Timeframes to Monitor
COINS = ["BNB/USDT", "ETH/USDT", "SOL/USDT", "BTC/USDT"]
TIMEFRAMES = ["15m", "1h", "4h", "1d"]

# 🔹 Alert Threshold (e.g., alerts when price is within 0.2% of support/resistance)
ALERT_THRESHOLD = 0.002  # 0.2%

# 🔹 Track previously sent signals
previous_signals = {}

# 🔹 Support & Resistance Calculation
def calculate_support_resistance(df, lookback=50):
    """Determines support & resistance levels based on the highest and lowest points of the last X candles."""
    return df['low'].rolling(window=lookback).min().iloc[-1], df['high'].rolling(window=lookback).max().iloc[-1]

# 🔹 Fetch Price Data from Binance
def fetch_data(symbol, timeframe, limit=100):
    """Fetches OHLCV data from Binance."""
    bars = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    return df

# 🔹 Send Support & Resistance Levels to Telegram
def send_support_resistance_levels():
    """Updates and sends support & resistance levels to Telegram (Runs every 1 hour)."""
    message = "📊 *Latest Support & Resistance Levels* 📊\n"
    proximity_list = []  

    for symbol in COINS:
        for timeframe in TIMEFRAMES:
            df = fetch_data(symbol, timeframe)
            support, resistance = calculate_support_resistance(df)

            ticker = exchange.fetch_ticker(symbol)
            price = ticker['last']

            # Calculate percentage distance
            support_proximity = abs((price - support) / support) * 100
            resistance_proximity = abs((resistance - price) / resistance) * 100

            # Add to list
            proximity_list.append((symbol, timeframe, price, support, resistance, support_proximity, resistance_proximity))
            
            # Initialize signal tracking
            previous_signals[f"{symbol}_{timeframe}_support"] = False
            previous_signals[f"{symbol}_{timeframe}_resistance"] = False

    # Order coins for structured display
    coin_order = {coin: i for i, coin in enumerate(COINS)}
    sorted_proximity = sorted(proximity_list, key=lambda x: (coin_order[x[0]], min(x[5], x[6])))

    for symbol, timeframe, price, support, resistance, support_proximity, resistance_proximity in sorted_proximity:
        message += f"\n🔹 *{symbol} ({timeframe})* 🔹\n"
        message += f"💰 Current Price: `{price:.4f} USDT`\n"
        message += f"📉 Support: `{support:.4f} USDT` (📏 %{support_proximity:.2f} away)\n"
        message += f"📈 Resistance: `{resistance:.4f} USDT` (📏 %{resistance_proximity:.2f} away)\n"

    bot.send_message(CHAT_ID, message, parse_mode="Markdown")

# 🔹 Signal Check & Alert Function
def check_and_send_signals():
    """Sends alerts when price approaches support/resistance levels."""
    last_update_time = time.time()

    while True:
        if time.time() - last_update_time >= 3600:
            send_support_resistance_levels()
            last_update_time = time.time()

        for symbol in COINS:
            for timeframe in TIMEFRAMES:
                try:
                    df = fetch_data(symbol, timeframe)
                    support, resistance = calculate_support_resistance(df)
                    ticker = exchange.fetch_ticker(symbol)
                    price = ticker['last']

                    key_support = f"{symbol}_{timeframe}_support"
                    key_resistance = f"{symbol}_{timeframe}_resistance"

                    support_diff = ((price - support) / support) * 100
                    resistance_diff = ((resistance - price) / resistance) * 100

                    message = None
                    send_multiple_times = timeframe in ["1h", "4h", "1d"]

                    # Approaching Support Level
                    if (price > support) and (price <= support * (1 + ALERT_THRESHOLD)):
                        if not previous_signals.get(key_support, False):
                            message = (f"⚠️ *{symbol} ({timeframe}) is approaching SUPPORT level!* ⚠️\n"
                                       f"💰 Current Price: `{price:.4f} USDT`\n"
                                       f"📉 Support: `{support:.4f} USDT`\n"
                                       f"📊 Support Proximity: `%{support_diff:.2f}`")
                            send_alert(message, send_multiple_times)
                            previous_signals[key_support] = True

                    # Approaching Resistance Level
                    elif (price < resistance) and (price >= resistance * (1 - ALERT_THRESHOLD)):
                        if not previous_signals.get(key_resistance, False):
                            message = (f"🚀 *{symbol} ({timeframe}) is approaching RESISTANCE level!* 🚀\n"
                                       f"💰 Current Price: `{price:.4f} USDT`\n"
                                       f"📈 Resistance: `{resistance:.4f} USDT`\n"
                                       f"📊 Resistance Proximity: `%{resistance_diff:.2f}`")
                            send_alert(message, send_multiple_times)
                            previous_signals[key_resistance] = True

                    # Reset signal status if price moves away from support/resistance
                    if price > support * (1 + ALERT_THRESHOLD):
                        previous_signals[key_support] = False
                    if price < resistance * (1 - ALERT_THRESHOLD):
                        previous_signals[key_resistance] = False

                except Exception as e:
                    print(f"Error: {e}")

        time.sleep(60)

# 🔹 Telegram Alert Sending Function
def send_alert(message, multiple=False):
    """Sends the alert message to Telegram, optionally multiple times."""
    if multiple:
        for _ in range(3):
            bot.send_message(CHAT_ID, message, parse_mode="Markdown")
            print(f"Message Sent: {message}")
            time.sleep(5)
    else:
        bot.send_message(CHAT_ID, message, parse_mode="Markdown")
        print(f"Message Sent: {message}")

if __name__ == "__main__":
    send_support_resistance_levels()  
    check_and_send_signals()
