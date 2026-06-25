import os
import pandas as pd
import requests
import yfinance as yf

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# Google Sheet CSV URL
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQoXZndMPqOhS__q9cIaw3i9wR0ZsG8LPKQVMbUCdD3XZQgEJNtsV-xabzLl49zog21myaAWrD3fbub/pub?output=csv"

print("=" * 60)
print("Reading Google Sheet...")
print(sheet_url)
print("=" * 60)

# Check URL
response = requests.get(sheet_url)

print("HTTP Status :", response.status_code)
print("First 300 characters of response:")
print(response.text[:300])
print("=" * 60)

# Stop if URL is invalid
if response.status_code != 200:
    raise Exception(f"Google Sheet URL not accessible. HTTP Status = {response.status_code}")

# Read CSV
df = pd.read_csv(sheet_url)

print("Columns found:")
print(df.columns.tolist())

# Remove blank rows
df = df[df["STOCK"].notna()].copy()

# Fill dates downward
df["STOCK ON RADAR DATE"] = df["STOCK ON RADAR DATE"].ffill()

# Latest date
latest_date = df["STOCK ON RADAR DATE"].dropna().iloc[-1]

print("Latest Date :", latest_date)

# Stocks for latest date
stocks = df[df["STOCK ON RADAR DATE"] == latest_date]["STOCK"].tolist()

print("Stocks :", stocks)

message = f"🚀 GAP UP ALERT\n\nDate : {latest_date}\n\n"

count = 0

for stock in stocks:

    symbol = stock.upper() + ".NS"

    print(f"Checking {symbol}")

    try:

        data = yf.download(
            symbol,
            period="5d",
            progress=False,
            auto_adjust=False
        )

        if len(data) < 2:
            print("Not enough data")
            continue

        prev_close = float(data["Close"].iloc[-2])
        today_open = float(data["Open"].iloc[-1])

        gap = ((today_open - prev_close) / prev_close) * 100

        print(f"{stock} Gap = {gap:.2f}%")

        if 1 <= gap <= 3:

            count += 1
            message += f"✅ {stock.upper()}   {gap:.2f}%\n"

    except Exception as e:
        print(stock, e)

if count == 0:
    message += "No Gap-Up Stocks (1%-3%)"

print("=" * 60)
print(message)
print("=" * 60)

response = requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)

print("Telegram Response :", response.status_code)
print(response.text)
