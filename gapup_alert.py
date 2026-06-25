import os
import pandas as pd
import requests

# -----------------------------
# Telegram Secrets from GitHub
# -----------------------------
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# -----------------------------
# Google Sheet Published CSV URL
# -----------------------------
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQoXZndMPqOhS__q9claw3i9wR0ZsG8LPKQVMbUCdD3XZQgEJNtsV-xabzLI49zog21myaAWrD3fbub/pub?output=csv"

print("Reading Google Sheet...")

# Read Google Sheet
df = pd.read_csv(sheet_url)

print("Google Sheet Read Successfully")

# Remove blank stock names
df = df[df["STOCK"].notna()]

# Fill blank dates downward
df["STOCK ON RADAR DATE"] = df["STOCK ON RADAR DATE"].ffill()

# Latest radar date
latest_date = df["STOCK ON RADAR DATE"].dropna().iloc[-1]

# Stocks of latest date
stocks = df[df["STOCK ON RADAR DATE"] == latest_date]["STOCK"].tolist()

# Telegram Message
message = f"🚀 MSI Radar Stocks ({latest_date})\n\n"

for stock in stocks:
    message += f"✅ {stock}\n"

print(message)

# Telegram API URL
telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# Send Telegram Message
response = requests.post(
    telegram_url,
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)

print(response.text)

if response.status_code == 200:
    print("Telegram Message Sent Successfully")
else:
    print("Telegram Error")
