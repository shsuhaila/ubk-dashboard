import streamlit as st
import pandas as pd
import plotly.express as px

# 1. TETAPAN HALAMAN
st.set_page_config(page_title="Dashboard UBK", layout="wide")

# 2. PAUTAN DATA GOOGLE SHEETS
base_url = "https://docs.google.com/spreadsheets/d/1bVA4HXnygPpWyjOnYqTFZfgXCJngFRojFVeK4mZ3Vq0/gviz/tq?tqx=out:csv"
url_individu = f"{base_url}&sheet=INDIVIDU"
url_kelompok = f"{base_url}&sheet=KELOMPOK"

@st.cache_data(ttl=5)
def load_data(url):
    df_live = pd.read_csv(url)
    df_live.columns = df_live.columns.str.strip()
    return df_live

# Membaca data
df_ind = load_data(url_individu)
df_kel = load_data(url_kelompok)

# Pembersihan data & Penyeragaman Huruf Besar
if not df_ind.empty and "Nama Murid" in df_ind.columns:
    df_ind = df_ind.dropna(subset=["Nama Murid"])
    # Seragamkan lajur penting menjadi HURUF BESAR untuk elak ralat pengiraan
    if "Kategori Rujukan" in df_ind.columns:
        df_ind["Kategori Rujukan"] = df_ind["Kategori Rujukan"].astype(str).str.strip().str.upper()
    if "Status Kes" in df_ind.columns:
        df_ind["Status Kes"] = df_ind["Status Kes"].astype(str).str.strip().str.upper()

if not df_kel.empty and "Nama" in df_kel.columns:
    df_kel = df_kel.dropna(subset=["Nama"])

# 3. TAJUK UTAMA
st.title("📊 DASHBOARD KHIDMAT KAUNSELING MURID (UBK)")

# 4. SISTEM TAB
tab_ind, tab_kel = st.tabs(["👤 Sesi Individu", "👥 Sesi Kelompok"])

# ================= TAB 1: INDIVIDU =================
with tab_ind:
    st.header("Analisis Sesi Individu")
    
    # Pengiraan KPI yang tepat menggunakan teks huruf besar
    total_kes = len(df_ind)
    
    bil_bimb = 0
    if "Jenis Kaunseling" in df_ind.columns:
        bil_bimb = len(df_ind[df_ind["Jenis Kaunseling"].str.upper().str.contains("BIMBINGAN", na=False)])
        
    # Mengira rujukan guru secara selamat (HURUF BESAR)
    rujukan_guru = 0
    if "Kategori Rujukan" in df_ind.columns:
        rujukan_guru = len(df_ind[df_ind["Kategori Rujukan"] == "RUJUKAN GURU"])
        
    kes_selesai = len(df_ind[df_ind["Status Kes"] == "SELESAI"]) if "Status Kes" in df_ind.columns else 0
    
    # Paparan baris kad nombor
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Jumlah Kes Individu", total_kes)
    c2.metric("Rujukan Guru 👥", rujukan_guru)
    c3.metric("Bimbingan Individu", bil_bimb)
    c4.metric("Kes Selesai 🟢", kes_selesai)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Mengikut Kategori Rujukan")
        if "Kategori Rujukan" in df_ind.columns and not df_ind.empty:
            # Membuat graf bar susunan mengikut bilangan tertinggi
            df_count = df_ind["Kategori Rujukan"].value_counts().reset_index()
            df_count.columns = ["Kategori Rujukan", "Bilangan Kes"]
            fig1 = px.bar(df_count, x="Kategori Rujukan", y="Bilangan Kes", color="Kategori Rujukan")
            st.plotly_chart(fig1, use_container_width=True)
            
    with col2:
        st.subheader("Pecahan Jantina")
        if "Jantina" in df_ind.columns and not df_ind.empty:
            fig2 = px.pie(df_ind, names="Jantina", hole=0.4, color_discrete_sequence=["#FF69B4", "#002F6C"])
            st.plotly_chart(fig2, use_container_width=True)
                
    st.markdown("---")
    st.subheader("📋 Senarai Murid Individu")
    st.dataframe(df_ind.reset_index(drop=True), use_container_width=True)

# ================= TAB 2: KELOMPOK =================
with tab_kel:
    st.header("Pengurusan Sesi Kelompok")
    total_ahli = len(df_kel)
    total_kumpulan = df_kel["KELOMPOK"].nunique() if "KELOMPOK" in df_kel.columns else 0
    
    k1, k2 = st.columns(2)
    k1.metric("Jumlah Kumpulan", total_kumpulan)
    k2.metric("Jumlah Ahli Terlibat", total_ahli)
    
    col_k1, col_k2 = st.columns(2)
    with col_k1:
        if "Tingkatan" in df_kel.columns and not df_kel.empty:
            df_ting = df_kel.dropna(subset=["Tingkatan"]).copy()
            df_ting["Tingkatan"] = df_ting["Tingkatan"].astype(str).str.replace(r'\.0$', '', regex=True)
            fig3 = px.histogram(df_ting, x="Tingkatan", title="Bilangan Murid Mengikut Tingkatan")
            st.plotly_chart(fig3, use_container_width=True)
    with col_k2:
        if "Jantina" in df_kel.columns and not df_kel.empty:
            fig4 = px.pie(df_kel, names="Jantina", title="Pecahan Jantina Ahli Kelompok", hole=0.4)
            st.plotly_chart(fig4, use_container_width=True)

    st.subheader("Semakan Ahli Mengikut Kumpulan")
    if "KELOMPOK" in df_kel.columns and not df_kel.empty:
        df_kel["KELOMPOK"] = df_kel["KELOMPOK"].astype(str).str.replace(r'\.0$', '', regex=True)
        senarai_kumpulan = sorted(df_kel["KELOMPOK"].unique(), key=lambda x: int(x) if x.isdigit() else 999)
        
        kumpulan_dipilih = st.selectbox("Pilih nombor Kumpulan Kelompok:", options=senarai_kumpulan, index=0)
        df_filtered = df_kel[df_kel["KELOMPOK"] == kumpulan_dipilih].copy()
        
        if "Tingkatan" in df_filtered.columns:
            df_filtered["Tingkatan"] = df_filtered["Tingkatan"].astype(str).str.replace(r'\.0$', '', regex=True)
            
        st.write(f"Senarai ahli untuk KUMPULAN {kumpulan_dipilih}:")
        st.dataframe(df_filtered.reset_index(drop=True), use_container_width=True)
