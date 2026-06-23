import streamlit as st
import pandas as pd
import datetime
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

# 2. GENERATE SAMPLE DATA
@st.cache_data
def load_sample_data():
    data = [
        {"ID Murid": f"M{i:03d}", "Nama Murid": nama, "Tingkatan": ting, "Kelas": kel, "Jantina": jan,
         "Tarikh Sesi": pd.to_datetime(tarikh), "Jenis Kaunseling": jns, "Kategori Rujukan": ruj, 
         "Isu": isu, "Tindakan Susulan": tindakan, "Status Kes": stat}
        for i, (nama, ting, kel, jan, tarikh, jns, ruj, isu, tindakan, stat) in enumerate([
            ("Ahmad Danial", "Tingkatan 5", "Sidiq", "Lelaki", "2026-01-10", "Individu", "SSDM", "Disiplin lewat ke sekolah", "Sesi amaran", "Selesai"),
            ("Siti Nurhaliza", "Tingkatan 4", "Amanah", "Perempuan", "2026-01-15", "Individu", "Minda Sihat", "Anxiety peperiksaan", "Latihan pernafasan", "Aktif"),
            ("Muhammad Ali", "Tingkatan 3", "Tabligh", "Lelaki", "2026-01-22", "Kelompok", "Rujukan Guru", "Kurang motivasi", "Bimbingan kelompok", "Selesai"),
            ("Chong Wei", "Tingkatan 5", "Fatonah", "Lelaki", "2026-02-05", "Individu", "Psikometrik", "Pemilihan kerjaya", "Ujian Minat", "Selesai"),
            ("Nur Aisha", "Tingkatan 2", "Sidiq", "Perempuan", "2026-02-12", "Individu", "SSDM", "Bully siber", "Sesi mediasi", "Aktif"),
            ("Arvin Raj", "Tingkatan 1", "Amanah", "Lelaki", "2026-02-18", "Kelompok", "Minda Sihat", "Stress penyesuaian", "Sesi suai kenal", "Selesai"),
            ("Fatima Zahra", "Tingkatan 4", "Tabligh", "Perempuan", "2026-03-01", "Individu", "Rujukan Guru", "Masalah keluarga", "Sokongan emosi", "Aktif"),
            ("Lim Jia Khang", "Tingkatan 3", "Fatonah", "Lelaki", "2026-03-14", "Individu", "SSDM", "Merokok", "Rujukan PK HEM", "Selesai"),
            ("Saraswathy", "Tingkatan 5", "Sidiq", "Perempuan", "2026-03-20", "Kelompok", "Psikometrik", "Persediaan SPM", "Teknik belajar", "Selesai"),
            ("Muhammad Haziq", "Tingkatan 2", "Amanah", "Lelaki", "2026-04-02", "Individu", "Minda Sihat", "Kemurungan ringan", "Pemantauan", "Aktif")
        ] * 3, start=1) # Loops data to make 30 items easily
    ]
    return pd.DataFrame(data)

df_all = load_sample_data()

# 3. SIDEBAR / FILTERS
st.sidebar.header("Tapis Data Dashboard")
filter_ting = st.sidebar.multiselect("Tingkatan", options=sorted(df_all["Tingkatan"].unique()), default=sorted(df_all["Tingkatan"].unique()))
filter_kelas = st.sidebar.multiselect("Kelas", options=sorted(df_all["Kelas"].unique()), default=sorted(df_all["Kelas"].unique()))
filter_jenis = st.sidebar.multiselect("Jenis Kaunseling", options=df_all["Jenis Kaunseling"].unique(), default=df_all["Jenis Kaunseling"].unique())
filter_rujukan = st.sidebar.multiselect("Kategori Rujukan", options=df_all["Kategori Rujukan"].unique(), default=df_all["Kategori Rujukan"].unique())

df = df_all[
    (df_all["Tingkatan"].isin(filter_ting)) & (df_all["Kelas"].isin(filter_kelas)) &
    (df_all["Jenis Kaunseling"].isin(filter_jenis)) & (df_all["Kategori Rujukan"].isin(filter_rujukan))
]

df["Bulan-Tahun"] = df["Tarikh Sesi"].dt.strftime('%b %Y')
df = df.sort_values("Tarikh Sesi")

# 4. APP HEADER SECTION
st.markdown("<h1 class='main-title'>DASHBOARD KHIDMAT KAUNSELING MURID</h1>", unsafe_allow_html=True)
st.markdown("<h4 class='sub-title'>Unit Bimbingan & Kaunseling (UBK)</h4>", unsafe_allow_html=True)

# 5. TOP KPI CARDS
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Jumlah Keseluruhan", len(df))
col2.metric("Individu", len(df[df["Jenis Kaunseling"] == "Individu"]))
col3.metric("Kelompok", len(df[df["Jenis Kaunseling"] == "Kelompok"]))
col4.metric("Kes Aktif 🟡", len(df[df["Status Kes"] == "Aktif"]))
col5.metric("Kes Selesai 🟢", len(df[df["Status Kes"] == "Selesai"]))

st.markdown("---")

# 6. CHARTS LAYOUT SECTION
row1_col1, row1_col2 = st.columns(2)
with row1_col1:
    st.subheader("Bilangan Murid Mengikut Kategori Rujukan")
    fig_bar = px.bar(df, x="Kategori Rujukan", color="Kategori Rujukan")
    st.plotly_chart(fig_bar, use_container_width=True)

with row1_col2:
    st.subheader("Perbandingan Kaunseling Individu & Kelompok")
    fig_pie = px.pie(df, names="Jenis Kaunseling", hole=0.4, color_discrete_sequence=["#002F6C", "#006B3E"])
    st.plotly_chart(fig_pie, use_container_width=True)

row2_col1, row2_col2 = st.columns(2)
with row2_col1:
    st.subheader("Bilangan Murid Mengikut Tingkatan")
    fig_ting = px.histogram(df, x="Tingkatan")
    st.plotly_chart(fig_ting, use_container_width=True)

with row2_col2:
    st.subheader("Bilangan Murid Mengikut Kelas")
    fig_kelas = px.histogram(df, x="Kelas")
    st.plotly_chart(fig_kelas, use_container_width=True)

st.markdown("---")
st.subheader("📋 Laporan Senarai Murid")
st.dataframe(df.reset_index(drop=True), use_container_width=True)
