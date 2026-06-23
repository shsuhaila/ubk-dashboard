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
    # Buang baris yang benar-benar kosong berdasarkan Nama Murid / Kelompok
    if not df_live.empty:
        df_live = df_live.dropna(subset=[df_live.columns[0], df_live.columns[1]], how='all')
    return df_live

st.caption("🔄 Memuatkan data secara langsung dari tab INDIVIDU & KELOMPOK...")

try:
    df_ind = load_data(url_individu)
    df_kel = load_data(url_kelompok)
    
    # Bersihkan data Individu
    if not df_ind.empty:
        if "Tarikh Sesi" in df_ind.columns:
            df_ind["Tarikh Sesi"] = pd.to_datetime(df_ind["Tarikh Sesi"], errors='coerce')
        if "Tingkatan" in df_ind.columns:
            df_ind = df_ind.dropna(subset=["Tingkatan"])
            df_ind["Tingkatan"] = df_ind["Tingkatan"].astype(int).astype(str)

    # Bersihkan data Kelompok
    if not df_kel.empty:
        if "Tingkatan" in df_kel.columns:
            df_kel = df_kel.dropna(subset=["Tingkatan"])
            df_kel["Tingkatan"] = df_kel["Tingkatan"].astype(int).astype(str)
        if "KELOMPOK" in df_kel.columns:
            df_kel["KELOMPOK"] = df_kel["KELOMPOK"].astype(int).astype(str)

    # 3. APP HEADER SECTION
    st.markdown("<h1 class='main-title'>DASHBOARD KHIDMAT KAUNSELING MURID</h1>", unsafe_allow_html=True)
    st.markdown("<h4 class='sub-title'>Unit Bimbingan & Kaunseling (UBK)</h4>", unsafe_allow_html=True)

    # 4. SISTEM TAB UTAMA DI DALAM APP
    tab_individu, tab_kelompok = st.tabs(["👤 Sesi Individu", "👥 Sesi Kelompok / Group"])

    # ================= TAB 1: INDIVIDU =================
    with tab_individu:
        st.subheader("📊 Analisis Data Sesi Individu")
        
        # KPI Cards Individu
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Jumlah Kes Individu", len(df_ind))
        c2.metric("Bimbingan Individu", len(df_ind[df_ind["Jenis Kaunseling"].str.upper().str.contains("BIMBINGAN", na=False)]) if "Jenis Kaunseling" in df_ind.columns else 0)
        c3.metric("Kes Aktif 🟡", len(df_ind[df_ind["Status Kes"] == "Aktif"]) if "Status Kes" in df_ind.columns else 0)
        c4.metric("Kes Selesai 🟢", len(df_ind[df_ind["Status Kes"] == "Selesai"]) if "Status Kes" in df_ind.columns else 0)
        
        st.markdown("---")
        
        # Charts Individu
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Mengikut Kategori Rujukan (Individu)")
            if "Kategori Rujukan" in df_ind.columns and not df_ind.empty:
                fig1 = px.bar(df_ind, x="Kategori Rujukan", color="Kategori Rujukan")
                st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            st.subheader("Pecahan Jantina (Individu)")
            if "Jantina" in df_ind.columns and not df_ind.empty:
                fig2 = px.pie(df_ind, names="Jantina", hole=0.4, color_discrete_sequence=["#FF69B4", "#002F6C"])
                st.plotly_chart(fig2, use_container_width=True)
                
        st.markdown("---")
        st.subheader("📋 Laporan Senarai Murid (Individu)")
        st.dataframe(df_ind.reset_index(drop=True), use_container_width=True)

    # ================= TAB 2: KELOMPOK =================
    with tab_kelompok:
        st.subheader("👥 Pengurusan Sesi Kelompok")
        
        # KPI Cards Kelompok
        total_ahli = len(df_kel)
        total_kumpulan = df_kel["KELOMPOK"].nunique() if "KELOMPOK" in df_kel.columns else 0
        
        k1, k2 = st.columns(2)
        k1.metric("Jumlah Keseluruhan Kumpulan Kelompok", total_kumpulan)
        k2.metric("Jumlah Ahli Murid Terlibat", total_ahli)
        
        st.markdown("---")
        
        # Charts Kelompok
        col_k1, col_k2 = st.columns(2)
        with col_k1:
            st.subheader("Bilangan Murid Kelompok Mengikut Tingkatan")
            if "Tingkatan" in df_kel.columns and not df_kel.empty:
                # Menggunakan bar chart kategori supaya susunan mengikut teks '1', '2', '3' tanpa perpuluhan
                df_ting_count = df_kel["Tingkatan"].value_counts().reset_index()
                df_ting_count.columns = ["Tingkatan", "Bilangan Murid"]
                df_ting_count = df_ting_count.sort_values(by="Tingkatan")
                
                fig3 = px.bar(df_ting_count, x="Tingkatan", y="Bilangan Murid", color="Tingkatan")
                st.plotly_chart(fig3, use_container_width=True)
                
        with col_k2:
            st.subheader("Pecahan Jantina Ahli Kelompok")
            if "Jantina" in df_kel.columns and not df_kel.empty:
                fig4 = px.pie(df_kel, names="Jantina", hole=0.4, color_discrete_sequence=["#002F6C", "#FF69B4"])
                st.plotly_chart(fig4, use_container_width=True)

        st.markdown("---")
        st.subheader("📋 Senarai Ahli Kumpulan Kelompok")
        st.dataframe(df_kel.reset_index(drop=True), use_container_width=True)

except Exception as e:
    st.error(f"Gagal memuatkan data dari Google Sheets.")
    st.write(f"Ralat sistem: {e}")
