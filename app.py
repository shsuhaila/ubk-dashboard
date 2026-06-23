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

if not df_ind.empty and "Nama Murid" in df_ind.columns:
    df_ind = df_ind.dropna(subset=["Nama Murid"])
if not df_kel.empty and "Nama" in df_kel.columns:
    df_kel = df_kel.dropna(subset=["Nama"])

# 3. TAJUK UTAMA
st.title("DASHBOARD KHIDMAT KAUNSELING MURID (UBK)")

# 4. SISTEM TAB
tab_ind, tab_kel = st.tabs(["Sesi Individu", "Sesi Kelompok"])

# ================= TAB 1 =================
with tab_ind:
    st.header("Analisis Sesi Individu")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Jumlah Kes Individu", len(df_ind))
    
    bil_bimb = len(df_ind[df_ind["Jenis Kaunseling"].str.upper().str.contains("BIMBINGAN", na=False)]) if "Jenis Kaunseling" in df_ind.columns else 0
    c2.metric("Bimbingan Individu", bil_bimb)
    
    kes_aktif = len(df_ind[df_ind["Status Kes"] == "Aktif"]) if "Status Kes" in df_ind.columns else 0
    kes_selesai = len(df_ind[df_ind["Status Kes"] == "Selesai"]) if "Status Kes" in df_ind.columns else 0
    c3.metric("Kes Aktif", kes_aktif)
    c4.metric("Kes Selesai", kes_selesai)
    
    col1, col2 = st.columns(2)
    with col1:
        if "Kategori Rujukan" in df_ind.columns and not df_ind.empty:
            fig1 = px.bar(df_ind, x="Kategori Rujukan", title="Kategori Rujukan")
            st.plotly_chart(fig1, use_container_width=True)
    with col2:
        if "Jantina" in df_ind.columns and not df_ind.empty:
            fig2 = px.pie(df_ind, names="Jantina", title="Pecahan Jantina", hole=0.4)
            st.plotly_chart(fig2, use_container_width=True)
            
    st.subheader("Senarai Murid Individu")
    st.dataframe(df_ind.reset_index(drop=True), use_container_width=True)

# ================= TAB 2 =================
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
