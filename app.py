import streamlit as st
import pandas as pd
import numpy as np
import time
from streamlit_lightweight_charts import renderLightweightCharts

st.set_page_config(layout="wide")
st.title("🕯️ Mon TradingView (Moteur Lightweight)")

# --- 1. Gestion des données (Simulées) ---
if "data_list" not in st.session_state:
    initial_price = 100.0
    data = []
    # On force un timestamp entier (int)
    current_time = int(time.time()) - 50*60 
    
    for i in range(50):
        open_p = float(initial_price)
        close_p = float(open_p + np.random.uniform(-1, 1))
        high_p = float(max(open_p, close_p) + np.random.uniform(0, 0.5))
        low_p = float(min(open_p, close_p) - np.random.uniform(0, 0.5))
        
        candle = {
            "time": int(current_time + (i * 60)), 
            "open": open_p,
            "high": high_p,
            "low": low_p,
            "close": close_p
        }
        data.append(candle)
        initial_price = close_p
        
    st.session_state.data_list = data

# Fonction pour ajouter une bougie
def update_data():
    last_candle = st.session_state.data_list[-1]
    new_time = int(last_candle["time"] + 60)
    prev_close = float(last_candle["close"])
    
    change = np.random.uniform(-1, 1)
    new_close = float(prev_close + change)
    new_high = float(max(prev_close, new_close) + np.random.uniform(0, 0.5))
    new_low = float(min(prev_close, new_close) - np.random.uniform(0, 0.5))
    
    new_candle = {
        "time": new_time,
        "open": prev_close,
        "high": new_high,
        "low": new_low,
        "close": new_close
    }
    
    st.session_state.data_list.append(new_candle)
    if len(st.session_state.data_list) > 100:
        st.session_state.data_list.pop(0)

# --- 2. Configuration du Graphique ---
chartOptions = {
    "layout": {
        "textColor": 'black',
        "background": {
            "type": 'solid',
            "color": 'white'
        }
    },
    "grid": {
        "vertLines": {"color": "rgba(197, 203, 206, 0.5)"},
        "horzLines": {"color": "rgba(197, 203, 206, 0.5)"}
    },
    "timeScale": {
        "timeVisible": True,
        "secondsVisible": False
    }
}

# --- 3. Boucle de rendu ---
@st.fragment(run_every=2)
def draw_chart():
    update_data() 
    
    # FIX: Structure correcte pour renderLightweightCharts
    # Le paramètre est 'charts' (liste de dictionnaires de graphiques)
    # Chaque graphique contient 'chart' (options) et 'series' (séries de données)
    charts = [
        {
            "chart": chartOptions,
            "series": [
                {
                    "type": 'Candlestick',
                    "data": st.session_state.data_list,
                    "options": {
                        "upColor": '#26a69a',
                        "downColor": '#ef5350',
                        "borderVisible": False,
                        "wickUpColor": '#26a69a',
                        "wickDownColor": '#ef5350'
                    }
                }
            ]
        }
    ]
    
    last_price = st.session_state.data_list[-1]["close"]
    st.metric(label="Live Price", value=f"{last_price:.2f}")

    # Utilisation correcte de l'API
    renderLightweightCharts(
        charts=charts,
        key="live_chart"
    )

draw_chart()
