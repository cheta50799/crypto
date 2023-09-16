import os
import time
import asyncio
from datetime import datetime, timedelta  # Import datetime and timedelta
from binance.client import Client
from telegram import Bot

# Initialize the Binance client with your API key and secret
binance_api_key = "kyOYXvSIhXZtSvQaWOnfnHfiKB0wYn2WNIo7AhGZo5aXfjxSgFBBfh0i9Hm0L2Wx"
binance_api_secret = "ikNwTqWSHou8M6MLqP4UVq5aKDIlvFZP3MMGviYkMkBCG6kPLWXYwXjGmtEQNegj"
client = Client(binance_api_key, binance_api_secret)

# Initialize the Telegram bot with your API token
telegram_bot_token = "6513600654:AAF4b8iSoMD6qSjWBfLXGMXvfk0RXhaxjzk"
bot = Bot(token=telegram_bot_token)

def calculate_percentage_change(last_price, current_price):
    return ((current_price - last_price) / last_price) * 100

async def send_telegram_notification(chat_id, message):
    await bot.send_message(chat_id=chat_id, text=message)

def get_last_24_hours_closing_price(crypto_pair):
    # Get the klines (candlestick data) for the past 24 hours
    klines = client.futures_klines(symbol=crypto_pair, interval=Client.KLINE_INTERVAL_1HOUR, limit=24)
    
    # Extract the closing prices from the klines
    closing_prices = [float(kline[4]) for kline in klines]
    
    # Return the closing price from 24 hours ago
    return closing_prices[-2]  # The second-to-last closing price

def check_price_change(crypto_pair):
    last_price = get_last_24_hours_closing_price(crypto_pair)  # Set last_price to the closing price from 24 hours ago
    
    while True:
        ticker = client.get_symbol_ticker(symbol=crypto_pair)
        current_price = float(ticker['price'])
        
        if last_price is not None:
            percentage_change = calculate_percentage_change(last_price, current_price)
            
            if abs(percentage_change) > 0.001:
                message = f"{crypto_pair} has {'increased' if percentage_change > 0 else 'decreased'} by {abs(percentage_change):.2f}%."
                asyncio.run(send_telegram_notification("5236098786", message))  # Replace with your chat ID
        
        last_price = current_price
        time.sleep(600)  # Sleep for 10 minutes to avoid spamming

if __name__ == "__main__":
    crypto_pair = input("Enter the cryptocurrency pair to monitor (e.g., BTCUSDT): ")
    check_price_change(crypto_pair)
