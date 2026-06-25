import os
import pandas as pd
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# Published Google Sheet CSV URL
sheet_url = "PASTE_YOUR_PUBLISHED_CSV_URL_HERE"

# Read Google Sheet
df = pd.read_csv(sheet_url)

# Remove blank stock names
df = df[df["STOCK"].notna()]

# Fill date downward
df["STOCK ON RADAR DATE"] = df["STOCK ON RADAR DATE"].ffill()

# Latest date
latest_date = df["STOCK ON RADAR DATE"].dropna().iloc[-1]

# Stocks for latest date
stocks = df[df["STOCK ON RADAR DATE"] == latest_date]["STOCK"].tolist()

message = f"🚀 MSI Radar Stocks ({latest_date})\n\n"

for s in stocks:
    message += f"• {s}\n"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    url,
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)

print(message)
