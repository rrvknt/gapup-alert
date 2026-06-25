import os
import pandas as pd
import requests
import yfinance as yf

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQoXZndMPqOhS__q9cIaw3i9wR0ZsG8LPKQVMbUCdD3XZQgEJNtsV-xabzLl49zog21myaAWrD3fbub/pub?output=csv"

print("Reading Google Sheet...")

df = pd.read_csv(sheet_url)

df = df[df["STOCK"].notna()].copy()
df["STOCK ON RADAR DATE"] = df["STOCK ON RADAR DATE"].ffill()

latest_date = df["STOCK ON RADAR DATE"].dropna().iloc[-1]

stocks = df[df["STOCK ON RADAR DATE"] == latest_date]["STOCK"].tolist()

message = f"🚀 GAP UP ALERT\n\nDate : {latest_date}\n\n"

count = 0

for stock in stocks:

    symbol = stock.upper() + ".NS"

    try:

        data = yf.download(
            symbol,
            period="5d",
            progress=False,
            auto_adjust=False
        )

        if len(data) < 2:
            continue

        prev_close = float(data["Close"].iloc[-2])
        today_open = float(data["Open"].iloc[-1])

        gap = ((today_open - prev_close) / prev_close) * 100

        if 1 <= gap <= 3:

            count += 1

            message += f"✅ {stock.upper()}   {gap:.2f}%\n"

    except Exception as e:
        print(stock, e)

if count == 0:
    message += "No Gap-Up Stocks (1%-3%)"

requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)

print(message)
