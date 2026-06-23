import streamlit as st
import pandas as pd
import plotly.express as px

# 1. TETAPAN HALAMAN
st.set_page_config(
    page_title="Dashboard UBK",
    page_icon="📊",
    layout="wide"
)

# 2. PAUTAN DATA GOOGLE SHEETS
base_url = "https://docs.google.com/spreadsheets/d/1bVA4HXnygPpWyjOnYqTFZfgXCJngFRojFVeK4mZ3Vq0/gviz/tq?tqx=out:csv"
url_individu = f"{base_url}&sheet=INDIVIDU"
url_kelompok = f"{base_url}&sheet=KELOMPOK"

@st.cache_data(ttl=5)
def load_data(url):
    df_live = pd.read_csv(url)
    df_live.columns = df_live.columns.str.strip()
    return df_live

st.caption("🔄 Memuatkan data secara langsung dari Google Sheets...")

# Membaca data mentah
df_ind = load_data(url_individu)
df_kel = load_data(url_kelompok)

# Bersihkan baris kosong berdasarkan Lajur Nama
if not df_ind.empty and "Nama Murid" in df_ind.columns:
    df_ind = df_ind.dropna(subset=["Nama Murid"])
if not df_kel.empty and "Nama" in df_kel.columns:
    df_kel = df_kel.dropna(subset=["Nama"])

# 3. TAJUK UTAMA APP
st.title("📊 DASHBOARD KHIDMAT KAUNSELING MURID (UBK)")

# 4. SISTEM TAB UTAMA
tab_ind, tab_kel = st.tabs(["👤 Sesi Individu", "👥 Sesi Kelompok"])

# ================= TAB 1: INDIVIDU =================
with tab_ind:
    st.subheader("📊 Analisis Data Sesi Individu")
    
    # Ringkasan KPI metric
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Jumlah Kes Individu", len(df_ind))
    
    bil_bimb = len(df_ind[df_ind["Jenis Kaunseling"].str.upper().str.contains("BIMBINGAN", na=False)]) if "Jenis Kaunseling" in df_ind.columns else 0
    c2.metric("Bimbingan Individu", bil_bimb)
    
    kes_aktif = len(df_ind[df_ind["Status Kes"] == "Aktif"]) if "Status Kes" in df_ind.columns else 0
    kes_selesai = len(df_ind[df_ind["Status Kes"] == "Selesai"]) if "Status Kes" in df_ind.columns else 0
    c3.metric("Kes Aktif 🟡", kes_aktif)
    c4.metric("Kes Selesai 🟢", kes_selesai)
    
    st.markdown("
