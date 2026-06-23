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
df_ind = load_data(url_individu)
df_kel = load_data(url_kelompok)

# Pastikan tiada baris kosong pada data utama
if not df_ind.empty and "Nama Murid" in df_ind.columns:
    df_ind = df_ind.dropna(subset=["Nama Murid"])
if not df_kel.empty and "Nama" in df_kel.columns:
    df_kel = df_kel.dropna(subset=["Nama"])

# 3. APP HEADER SECTION
st.markdown("<h1 class='main-title'>DASHBOARD KHIDMAT KAUNSELING MURID</h1>", unsafe_allow_html=True)
st.markdown("<h4 class='sub-title'>Unit Bimbingan & Kaunseling (UBK)</h4>", unsafe_allow_html=True)

# 4. SISTEM TAB UTAMA DI DALAM APP
tab_individu, tab_kelompok = st.tabs(["👤 Sesi Individu", "👥 Sesi Kelompok / Group"])

# ================= TAB 1: INDIVIDU =================
with tab_individu:
    st.subheader("📊 Analisis Data Sesi Individu")
    
    c1, c2, c3, c4 = st.columns(4)
    # Pembetulan kurungan lengkap di sini
    c1.metric("Jumlah Kes Individu", len(df_ind))
    
    # Kira bimbingan
    bil_bimbingan = 0
    if "Jenis Kaunseling" in df_ind.columns:
        bil_bimbingan = len(df_ind[df_ind["Jenis Kaunseling"].str.upper().str.contains("BIMBINGAN", na=False)])
    c2.metric("Bimbingan Individu", bil_bimbingan)
    
    # Kira Status Kes
    kes_aktif = len(df_ind[df_ind["Status Kes"] == "Aktif"]) if "Status Kes" in df_ind.columns else 0
    kes_selesai = len(df_ind[df_ind["Status Kes"] == "Selesai"]) if "Status Kes" in df_ind.columns else 0
    c3.metric("Kes Aktif 🟡", kes_aktif)
    c4.metric("Kes Selesai 🟢", kes_selesai)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Mengikut Kategori
