import streamlit as st
import requests

st.set_page_config(page_title="BTC Market Manipulation Radar")

# --- Kraken Futures API ---
def get_kraken_funding_oi(symbol="PI_XBTUSD"):
    url = "https://futures.kraken.com/derivatives/api/v3/tickers"
    try:
        res = requests.get(url, timeout=5)
        if res.ok:
            tickers = res.json().get("tickers", [])
            row = next((x for x in tickers if x.get("symbol") == symbol), None)
            if row:
                return float(row.get("fundingRate", 0.0)) * 100, float(row.get("openInterest", 0.0))
    except Exception as e:
        st.warning(f"⚠️ Kraken API error: {e}")
    return 0.0, 0.0

def get_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    try:
        res = requests.get(url, timeout=5)
        if res.ok:
            return res.json().get("bitcoin", {}).get("usd", 0.0)
    except Exception as e:
        st.warning(f"⚠️ CoinGecko error: {e}")
    return 0.0

# --- UI Layout ---
st.title("📡 BTC Market Manipulation Radar")
st.success("✅ Bisa connect ke CoinGecko!")

# --- Pull Data ---
funding, oi = get_kraken_funding_oi()
price = get_price()

# --- State Management ---
if 'baseline_oi' not in st.session_state:
    st.session_state['baseline_oi'] = oi

oi_change = 100 * ((oi - st.session_state['baseline_oi']) / st.session_state['baseline_oi']) if st.session_state['baseline_oi'] > 0 else 0.0

# --- Display Metrics ---
st.markdown("### BTC Price")
st.markdown(f"<h1 style='font-size: 3.5rem;'>${price:,.2f}</h1>", unsafe_allow_html=True)

st.markdown("### Funding Rate")
st.markdown(f"<h1 style='font-size: 2.5rem;'>{funding:.4f} %</h1>", unsafe_allow_html=True)

st.markdown("### Open Interest Change")
st.markdown(f"<h1 style='font-size: 2.5rem;'>{oi_change:.2f} %</h1>", unsafe_allow_html=True)

# --- Manipulation Warning ---
if funding > 0.08 and oi_change > 3:
    st.error("🚨 Potential LONG Squeeze Detected")
elif funding < -0.08 and oi_change > 3:
    st.error("🚨 Potential SHORT Squeeze Detected")

# --- Refresh Button ---
if st.button("🔄 Refresh Data"):
    st.session_state['baseline_oi'] = oi
    st.experimental_rerun()
