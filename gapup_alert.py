import pandas as pd
import requests
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQoXZndMPqOhS__q9cIaw3i9wR0ZsG8LPKQVMbUCdD3XZQgEJNtsV-xabzLl49zog21myaAWrD3fbub/pubhtml"

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
