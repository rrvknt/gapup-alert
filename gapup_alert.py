import pandas as pd
import requests
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

sheet_url = "https://docs.google.com/spreadsheets/d/1q25b6xI1hMAALiGYA_YYR9rcP2vQ6XNtvQTlqGoN_ic/gviz/tq?tqx=out:csv&sheet=Sheet1"

df = pd.read_csv(sheet_url)

# Keep only rows having stock name
df = df[df["STOCK"].notna()]

# Fill date downward
df["STOCK ON RADAR DATE"] = df["STOCK ON RADAR DATE"].fillna(method="ffill")

# Latest date in sheet
latest_date = df["STOCK ON RADAR DATE"].dropna().iloc[-1]

# Stocks for latest date
stocks = df[df["STOCK ON RADAR DATE"] == latest_date]["STOCK"]

message = f"🚀 MSI Radar Stocks ({latest_date})\n\n"

for stock in stocks:
    message += f"{stock}\n"

print(message)

response = requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)

print("Telegram Response:")
print(response.text)
