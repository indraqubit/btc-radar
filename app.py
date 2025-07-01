import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# ----------------------
# Function to get BTC price from CoinGecko
# ----------------------
def get_price():
    try:
        res = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
        return res.json()['bitcoin']['usd']
    except:
        return 0

# ----------------------
# Save price + timestamp to CSV
# ----------------------
def log_price(price):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file = "btc_price_log.csv"
    with open(file, "a") as f:
        f.write(f"{now},{price}\n")

# ----------------------
# Load price history
# ----------------------
def load_data():
    file = "btc_price_log.csv"
    if not os.path.exists(file):
        return pd.DataFrame(columns=["time", "price"])
    df = pd.read_csv(file, names=["time", "price"], parse_dates=["time"])
    return df.tail(100)  # show last 100 records

# ----------------------
# Streamlit UI
# ----------------------
st.set_page_config(page_title="BTC Radar", layout="centered")
st.title("📡 BTC Price Tracker")

price = get_price()
if price > 0:
    st.success(f"Current BTC Price: ${price:,.2f}")
    log_price(price)
else:
    st.error("⚠️ Failed to fetch price")

# Load & plot
st.subheader("📈 BTC Price History")
data = load_data()
if not data.empty:
    fig, ax = plt.subplots()
    ax.plot(data["time"], data["price"], color='orange', marker='o')
    ax.set_xlabel("Time")
    ax.set_ylabel("Price (USD)")
    ax.grid(True)
    st.pyplot(fig)
else:
    st.warning("No data to display yet.")

if st.button("🔄 Refresh Now"):
    st.rerun()
