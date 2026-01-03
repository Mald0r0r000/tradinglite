import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime
# Import de la lib spécifique
from streamlit_lightweight_charts import renderLightweightCharts

st.set_page_config(layout="wide")
st.title("🕯️ Mon TradingView (Moteur Lightweight)")

# --- 1. Gestion des données (Simulées) ---
if "data_list" not in st.session_state:
    # On initialise avec 50 bougies
    initial_price = 100
    data = []
    current_time = int(time.time()) - 50*60 # Commencer il y a 50 min
    
    for i in range(50):
        open_p = initial_price
        close_p = open_p + np.random.uniform(-1, 1)
        high_p = max(open_p, close_p) + np.random.uniform(0, 0.5)
        low_p = min(open_p, close_p) - np.random.uniform(0, 0.5)
        
        # Format spécifique exigé par Lightweight Charts
        candle = {
            "time": current_time + (i * 60), # Timestamp UNIX
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
    new_time = last_candle["time"] + 60
    prev_close = last_candle["close"]
    
    change = np.random.uniform(-1, 1)
    new_close = prev_close + change
    new_high = max(prev_close, new_close) + np.random.uniform(0, 0.5)
    new_low = min(prev_close, new_close) - np.random.uniform(0, 0.5)
    
    new_candle = {
        "time": new_time,
        "open": prev_close,
        "high": new_high,
        "low": new_low,
        "close": new_close
    }
    
    st.session_state.data_list.append(new_candle)
    # On garde l'historique propre (ex: 100 dernières)
    if len(st.session_state.data_list) > 100:
        st.session_state.data_list.pop(0)

# --- 2. Configuration du Graphique (Le JSON de config) ---
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
    "crosshair": {
        "mode": 0 # Mode normal
    },
    "priceScale": {
        "borderColor": "rgba(197, 203, 206, 0.8)"
    },
    "timeScale": {
        "borderColor": "rgba(197, 203, 206, 0.8)",
        "timeVisible": True,
        "secondsVisible": False
    }
}

# --- 3. Boucle de rendu ---
# Utilisation de st.fragment pour ne recharger que cette partie (Streamlit 1.37+)
@st.fragment(run_every=2) # Mise à jour toutes les 2 secondes
def draw_chart():
    update_data() # Génère la nouvelle donnée
    
    # Préparation de la série de données
    seriesCandlestickChart = [
        {
            "type": 'Candlestick',
            "data": st.session_state.data_list,
            "options": {
                "upColor": '#26a69a',      # Le vert TradingView
                "downColor": '#ef5350',    # Le rouge TradingView
                "borderVisible": False,
                "wickUpColor": '#26a69a',
                "wickDownColor": '#ef5350'
            }
        }
    ]
    
    # Affichage du prix actuel
    last_price = st.session_state.data_list[-1]["close"]
    st.metric(label="Live Price", value=f"{last_price:.2f}")

    # Rendu du graphique
    # La clé est la data_list : si elle change, le chart se met à jour
    renderLightweightCharts(
        options=chartOptions, 
        series=seriesCandlestickChart, 
        height=500
    )

# Appel de la fonction fragment
draw_chart()
