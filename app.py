import streamlit as st
import requests
import socket

def get_price():
    try:
        res = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd", timeout=5)
        if res.ok:
            return float(res.json().get("bitcoin", {}).get("usd", 0.0))
    except Exception as e:
        st.warning(f"⚠️ Error fetching BTC price: {e}")
    return 0.0

def get_funding_rate(symbol="BTCUSDT"):
    url = f"https://fapi.binance.com/fapi/v1/fundingRate?symbol={symbol}&limit=1"
    try:
        res = requests.get(url, timeout=5)
        if res.ok:
            data = res.json()
            if data and isinstance(data, list):
                return float(data[0].get('fundingRate', 0.0)) * 100
    except Exception as e:
        st.warning(f"⚠️ Error getting Funding Rate: {e}")
    return 0.0

def get_open_interest(symbol="BTCUSDT"):
    url = f"https://fapi.binance.com/fapi/v1/openInterest?symbol={symbol}"
    try:
        res = requests.get(url, timeout=5)
        if res.ok:
            data = res.json()
            return float(data.get('openInterest', 0.0))
    except Exception as e:
        st.warning(f"⚠️ Error getting Open Interest: {e}")
    return 0.0

st.set_page_config(page_title="BTC Market Radar", layout="centered")
st.title("📡 BTC Market Manipulation Radar")

try:
    socket.create_connection(("api.coingecko.com", 443), timeout=5)
    st.success("✅ Bisa connect ke CoinGecko!")
except Exception as e:
    st.error(f"❌ Gagal connect ke CoinGecko: {e}")

if 'baseline_oi' not in st.session_state:
    st.session_state['baseline_oi'] = get_open_interest()

price = get_price()
funding = get_funding_rate()
oi = get_open_interest()
oi_change = ((oi - st.session_state['baseline_oi']) / st.session_state['baseline_oi']) * 100 if st.session_state['baseline_oi'] else 0

st.metric("BTC Price", f"${price:,.2f}")
st.metric("Funding Rate", f"{funding:.4f} %")
st.metric("Open Interest Change", f"{oi_change:.2f} %")

if funding > 0.08 and oi_change > 5:
    st.error("🚨 Potential LONG Squeeze Detected!")
elif funding < -0.08 and oi_change > 5:
    st.success("🚀 Potential SHORT Squeeze Detected!")

if st.button("🔄 Refresh Data"):
    st.experimental_rerun()
