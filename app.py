import streamlit as st
import requests

def get_funding_rate(symbol="BTCUSDT"):
    url = f"https://fapi.binance.com/fapi/v1/fundingRate?symbol={symbol}&limit=1"
    res = requests.get(url).json()
    return float(res[0]['fundingRate']) * 100

def get_open_interest(symbol="BTCUSDT"):
    url = f"https://fapi.binance.com/fapi/v1/openInterest?symbol={symbol}"
    res = requests.get(url).json()
    return float(res['openInterest'])

def get_price(symbol="BTCUSDT"):
    url = f"https://fapi.binance.com/fapi/v1/ticker/price?symbol={symbol}"
    res = requests.get(url).json()
    return float(res['price'])

st.set_page_config(page_title="BTC Market Radar", layout="centered")
st.title("📡 BTC Market Manipulation Radar")

if 'baseline_oi' not in st.session_state:
    st.session_state['baseline_oi'] = get_open_interest()

price = get_price()
funding = get_funding_rate()
oi = get_open_interest()
oi_change = ((oi - st.session_state['baseline_oi']) / st.session_state['baseline_oi']) * 100

st.metric("BTC Price", f"${price:,.2f}")
st.metric("Funding Rate", f"{funding:.4f} %")
st.metric("Open Interest Change", f"{oi_change:.2f} %")

if funding > 0.08 and oi_change > 5:
    st.error("🚨 Potential LONG Squeeze Detected!")
elif funding < -0.08 and oi_change > 5:
    st.success("🚀 Potential SHORT Squeeze Detected!")

if st.button("🔄 Refresh Data"):
    st.experimental_rerun()