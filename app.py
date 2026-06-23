import streamlit as st
import pandas as pd
import plotly.express as px

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="Dashboard Khidmat Kaunseling Murid",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for KPM Theme
st.markdown("""
    <style>
    :root {
        --kpm-blue: #002F6C;
        --kpm-green: #006B3E;
    }
    .main-title { color: var(--kpm-blue); font-family: sans-serif; font-weight: bold; }
    .sub-title { color: var(--kpm-green); font-family: sans-serif; font-weight: 600; padding-bottom: 20px; }
    div[data-testid="stMetric"] {
        background-color: #f8f9fa;
        border-left: 5px solid var(--kpm-green);
        padding: 10px;
        border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. PAUTAN UTK BACA DUA TAB BERBEZA
base_url = "https://docs.google.com/spreadsheets/d/1bVA4HXnygPpWyjOnYqTFZfgXCJngFRojFVeK4mZ3Vq0/gviz/tq?tqx=out:csv"
url_individu = f"{base_url}&sheet=INDIVIDU"
url_kelompok = f"{base_url}&sheet=KELOMPOK"

@st.cache_data(ttl=5)
def load_data(url):
    df_live = pd.read_csv(url)
    df_live.columns = df_live.columns.str.strip()
    return df_live

st.caption("🔄 Memuatkan data secara langsung dari tab INDIVIDU & KELOMPOK...")

# Membaca data mentah
df_ind_raw = load_data(url_individu)
df_kel_raw = load_data(url_kelompok)

# Bersihkan data Individu
if not df_ind_raw.empty and "Nama Murid" in df_ind_raw.columns:
    df_ind = df_ind_raw.dropna(subset=["Nama Murid"]).copy()
    if "Tarikh Sesi" in df_ind.columns:
        df_ind["Tarikh Sesi"] = pd.to_datetime(df_ind["Tarikh Sesi"], errors='coerce')
    if "Tingkatan" in df_ind.columns:
        df_ind = df_ind.dropna(subset=["Tingkatan"])
        df_ind["Tingkatan"] = df_ind["Tingkatan"].astype(int).astype(str)
else:
    df_ind = df_ind_raw.copy()

# Bersihkan data Kelompok
if not df_kel_raw.empty and "Nama" in df_kel_raw.columns:
    df_kel = df_kel_raw.dropna(subset=["Nama"]).copy()
    if "KELOMPOK" in df_kel.columns:
        df_kel["KELOMPOK"] = df_kel["KELOMPOK"].astype(int).astype(str)
else:
