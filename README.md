# 📈 Binance Telegram Bot 🚀  
*A real-time crypto price alert bot for Binance, integrated with Telegram.*

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/) 
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Binance API](https://img.shields.io/badge/API-Binance-yellow.svg)](https://binance-docs.github.io/apidocs/spot/en/)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://core.telegram.org/bots)

## 📌 Features
✅ **Fetches real-time OHLCV (Open, High, Low, Close, Volume) data from Binance**  
✅ **Calculates support & resistance levels across multiple timeframes**  
✅ **Sends alerts to Telegram when price approaches key levels**  
✅ **Prevents duplicate alerts to avoid spam**  
✅ **Uses scheduled tasks for efficient execution**  
✅ **Error handling for API failures and rate limits**  

---

## 🛠️ Installation & Setup

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/semihengin/binance-telegram-bot.git
cd binance-telegram-bot
```

### **2️⃣ Create & Configure `.env` File**
Create a `.env` file in the project root and add the following:
```env
TELEGRAM_BOT_TOKEN = "your_bot_token_here"
CHAT_ID = "your_chat_id_here"
```
🔹 **`TELEGRAM_BOT_TOKEN`** → Your Telegram bot token ([Get it from @BotFather](https://t.me/botfather))  
🔹 **`CHAT_ID`** → Your Telegram chat ID ([Find it using @userinfobot](https://t.me/useridinfobot))  

### **3️⃣ Run the Bot**
```sh
python bot.py
```
💡 The bot will start fetching Binance price data and sending alerts to Telegram.

---

## 📊 How It Works

1. Fetches **real-time price data** from Binance  
2. Calculates **support & resistance** levels for multiple timeframes  
3. Compares the **current price** with support & resistance  
4. Sends a **Telegram alert** if price is **within 0.2%** of key levels  
5. Prevents **duplicate alerts** unless price moves away and returns  

### **Example Alert Message 📩**
```
🚀 BTC/USDT (1h) is approaching RESISTANCE level! 🚀
💰 Current Price: 63,450.00 USDT
📈 Resistance: 63,600.00 USDT
📊 Resistance Proximity: 0.24%
```

---

## ⚙️ Configuration
Modify these settings in `bot.py`:
```python
COINS = ["BNB/USDT", "XRP/USDT", "ETH/USDT", "SOL/USDT", "BTC/USDT"]  # Coins to monitor
TIMEFRAMES = ["15m", "1h", "4h", "1d"]  # Timeframes for analysis
ALERT_THRESHOLD = 0.002  # 0.2% proximity threshold for alerts
```

---

## 🛠️ Error Handling & Debugging
- **Handles Binance API failures** with exception management  
- **Prevents Telegram API rate limits** by introducing delays  
- **Logs errors** in the terminal for easy debugging  

---
