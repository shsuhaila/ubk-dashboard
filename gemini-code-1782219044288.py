import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

# 1. PAGE CONFIGURATION (KPM Theme / Responsive A4 Landscape Friendly)
st.set_page_config(
    page_title="Dashboard Khidmat Kaunseling Murid",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for KPM Green & Blue Theme styling
st.markdown("""
    <style>
    :root {
        --kpm-blue: #002F6C;
        --kpm-green: #006B3E;
    }
    .main-title {
        color: var(--kpm-blue);
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: bold;
        padding-bottom: 2px;
        margin-bottom: 0px;
    }
    .sub-title {
        color: var(--kpm-green);
        font-family: Arial, sans-serif;
        font-weight: 600;
        margin-top: 0px;
        padding-bottom: 20px;
    }
    div[data-testid="stMetric"] {
        background-color: #f8f9fa;
        border-left: 5px solid var(--kpm-green);
        padding: 10px;
        border-radius: 4px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    div[data-testid="stMetric"] label {
        color: var(--kpm-blue) !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_index=True)

# 2. GENERATE SAMPLE DATA (Minimum 30 Records)
@st.cache_data
def load_sample_data():
    data = [
        {"ID Murid": f"M{i:03d}", 
         "Nama Murid": nama, "Tingkatan": ting, "Kelas": kel, "Jantina": jan,
         "Tarikh Sesi": pd.to_datetime(tarikh), "Jenis Kaunseling": jns, 
         "Kategori Rujukan": ruj, "Isu": isu, "Tindakan Susulan": tindakan, "Status Kes": stat}
        for i, (nama, ting, kel, jan, tarikh, jns, ruj, isu, tindakan, stat) in enumerate([
            ("Ahmad Danial", "Tingkatan 5", "Sidiq", "Lelaki", "2026-01-10", "Individu", "SSDM", "Disiplin lewat ke sekolah", "Sesi kaunseling & amaran", "Selesai"),
            ("Siti Nurhaliza", "Tingkatan 4", "Amanah", "Perempuan", "2026-01-15", "Individu", "Minda Sihat", "Anxiety peperiksaan", "Latihan pernafasan", "Aktif"),
            ("Muhammad Ali", "Tingkatan 3", "Tabligh", "Lelaki", "2026-01-22", "Kelompok", "Rujukan Guru", "Kurang motivasi kelas", "Bimbingan kelompok", "Selesai"),
            ("Chong Wei", "Tingkatan 5", "Fatonah", "Lelaki", "2026-02-05", "Individu", "Psikometrik", "Pemilihan kerjaya", "Ujian Minat Kerjaya", "Selesai"),
            ("Nur Aisha", "Tingkatan 2", "Sidiq", "Perempuan", "2026-02-12", "Individu", "SSDM", "Bully siber", "Sesi mediasi", "Aktif"),
            ("Arvin Raj", "Tingkatan 1", "Amanah", "Lelaki", "2026-02-18", "Kelompok", "Minda Sihat", "Stress penyesuaian diri", "Sesi suai kenal", "Selesai"),
            ("Fatima Zahra", "Tingkatan 4", "Tabligh", "Perempuan", "2026-03-01", "Individu", "Rujukan Guru", "Masalah keluarga", "Sesi sokongan emosi", "Aktif"),
            ("Lim Jia Khang", "Tingkatan 3", "Fatonah", "Lelaki", "2026-03-14", "Individu", "SSDM", "Merokok", "Rujukan PK HEM", "Selesai"),
            ("Saraswathy", "Tingkatan 5", "Sidiq", "Perempuan", "2026-03-20", "Kelompok", "Psikometrik", "Persediaan SPM", "Teknik belajar", "Selesai"),
            ("Muhammad Haziq", "Tingkatan 2", "Amanah", "Lelaki", "2026-04-02", "Individu", "Minda Sihat", "Kemurungan ringan", "Pemantauan berkala", "Aktif"),
            ("Puteri Balqis", "Tingkatan 1", "Tabligh", "Perempuan", "2026-04-11", "Kelompok", "Rujukan Guru", "Kerap ponteng", "Ziarah Cakna", "Aktif"),
            ("Ravi Kumar", "Tingkatan 4", "Fatonah", "Lelaki", "2026-04-25", "Individu", "SSDM", "Biadab dengan guru", "Sesi sahsiah", "Selesai"),
            ("Nurul Izzah", "Tingkatan 3", "Sidiq", "Perempuan", "2026-05-03", "Individu", "Minda Sihat", "Stress akademik", "Terapi relaksasi", "Selesai"),
            ("Daniel Jacobs", "Tingkatan 5", "Amanah", "Lelaki", "2026-05-19", "Kelompok", "Psikometrik", "Hala tuju matrikulasi", "Taklimat IPTA", "Selesai"),
            ("Anis Sofea", "Tingkatan 2", "Tabligh", "Perempuan", "2026-05-28", "Individu", "Rujukan Guru", "Perselisihan faham rakan", "Sesi rundingan", "Selesai"),
            ("Syed Ammar", "Tingkatan 1", "Fatonah", "Lelaki", "2026-06-02", "Individu", "SSDM", "Vaping", "Sesi kesedaran kesihatan", "Aktif"),
            ("Tan Mei Ling", "Tingkatan 5", "Tabligh", "Perempuan", "2026-06-08", "Kelompok", "Minda Sihat", "Anxiety kerjaya", "Ujian personality", "Selesai"),
            ("Muaz Zulkifli", "Tingkatan 4", "Sidiq", "Lelaki", "2026-06-15", "Individu", "Rujukan Guru", "Kurang fokus", "Latihan tumpuan", "Selesai"),
            ("Khairul Anwar", "Tingkatan 3", "Amanah", "Lelaki", "2026-07-01", "Kelompok", "SSDM", "Datang lambat", "Sesi disiplin diri", "Selesai"),
            ("Nadia Mustafa", "Tingkatan 2", "Fatonah", "Perempuan", "2026-07-12", "Individu", "Psikometrik", "Interpretasi skor ITP", "Perbincangan profil", "Selesai"),
            ("Michelle Wong", "Tingkatan 1", "Sidiq", "Perempuan", "2026-07-22", "Individu", "Minda Sihat", "Harga diri rendah", "Sesi membina keyakinan", "Selesai"),
            ("Haris Safwan", "Tingkatan 4", "Tabligh", "Lelaki", "2026-08-05", "Kelompok", "Rujukan Guru", "Konflik interpersonal", "Sesi dinamika", "Selesai"),
            ("Farah Diana", "Tingkatan 3", "Amanah", "Perempuan", "2026-08-19", "Individu", "SSDM", "Bergaduh", "Kontrak tingkah laku", "Selesai"),
            ("Adam Malik", "Tingkatan 5", "Fatonah", "Lelaki", "2026-08-25", "Individu", "Psikometrik", "Kerjaya Kejuruteraan", "Analisis subjek", "Selesai"),
            ("Sarah Jasmin", "Tingkatan 2", "Sidiq", "Perempuan", "2026-09-02", "Kelompok", "Minda Sihat", "Gementar di khalayak", "Latihan ucapan", "Selesai"),
            ("Alif Iskandar", "Tingkatan 1", "Tabligh", "Lelaki", "2026-09-11", "Individu", "Rujukan Guru", "Kesunyian", "Sesi ramah mesra", "Selesai"),
            ("Wong Kar Wai", "Tingkatan 4", "Amanah", "Lelaki", "2026-09-28", "Individu", "SSDM", "Siber jenayah ringan", "Advokasi undang-undang", "Selesai"),
            ("Zara Batrisya", "Tingkatan 3", "Fatonah", "Perempuan", "2026-10-05", "Kelompok", "Psikometrik", "Inventori Nilai Kerja", "Pemetaan minat", "Selesai"),
            ("Eshwar Rao", "Tingkatan 5", "Sidiq", "Lelaki", "2026-10-15", "Individu", "Minda Sihat", "Stress melampau", "Rujukan klinik kesihatan", "Selesai"),
            ("Siti Aminah", "Tingkatan 2", "Amanah", "Perempuan", "2026-10-22", "Individu", "Rujukan Guru", "Sering menangis", "Sokongan emosi berterusan", "Selesai")
        ], start=1)
    ]
    return pd.DataFrame(data)

df_all = load_sample_data()

# 3. SIDEBAR / FILTERS PANEL
st.sidebar.image("https://www.moe.gov.my/images/pemberitahuan/2023/KPM_Logo.png", use_container_width=True)
st.sidebar.header("Tapis Data Dashboard")

# Filters setup
filter_ting = st.sidebar.multiselect("Tingkatan", options=sorted(df_all["Tingkatan"].unique()), default=sorted(df_all["Tingkatan"].unique()))
filter_kelas = st.sidebar.multiselect("Kelas", options=sorted(df_all["Kelas"].unique()), default=sorted(df_all["Kelas"].unique()))
filter_jenis = st.sidebar.multiselect("Jenis Kaunseling", options=df_all["Jenis Kaunseling"].unique(), default=df_all["Jenis Kaunseling"].unique())
filter_rujukan = st.sidebar.multiselect("Kategori Rujukan", options=df_all["Kategori Rujukan"].unique(), default=df_all["Kategori Rujukan"].unique())
filter_jantina = st.sidebar.multiselect("Jantina", options=df_all["Jantina"].unique(), default=df_all["Jantina"].unique())

# Timeline Date Filter
min_date = df_all["Tarikh Sesi"].min().date()
max_date = df_all["Tarikh Sesi"].max().date()
date_range = st.sidebar.date_input("Timeline Tarikh Sesi", [min_date, max_date], min_value=min_date, max_value=max_date)

# Apply dynamic filtering
df = df_all[
    (df_all["Tingkatan"].isin(filter_ting)) &
    (df_all["Kelas"].isin(filter_kelas)) &
    (df_all["Jenis Kaunseling"].isin(filter_jenis)) &
    (df_all["Kategori Rujukan"].isin(filter_rujukan)) &
    (df_all["Jantina"].isin(filter_jantina))
]

if len(date_range) == 2:
    df = df[(df["Tarikh Sesi"].dt.date >= date_range[0]) & (df["Tarikh Sesi"].dt.date <= date_range[1])]

# Prepare date formatting for month/year filtering trend
df["Bulan-Tahun"] = df["Tarikh Sesi"].dt.strftime('%b %Y')
df = df.sort_values("Tarikh Sesi")

# 4. APP HEADER SECTION
st.markdown("<h1 class='main-title'>DASHBOARD KHIDMAT KAUNSELING MURID</h1>", unsafe_index=True)
st.markdown("<h4 class='sub-title'>Unit Bimbingan & Kaunseling (UBK)</h4>", unsafe_index=True)

# 5. TOP KPI CARDS (Formula Driven)
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Jumlah Keseluruhan Murid", len(df))
col2.metric("Kaunseling Individu", len(df[df["Jenis Kaunseling"] == "Individu"]))
col3.metric("Kaunseling Kelompok", len(df[df["Jenis Kaunseling"] == "Kelompok"]))
col4.metric("Kes Aktif 🟡", len(df[df["Status Kes"] == "Aktif"]))
col5.metric("Kes Selesai 🟢", len(df[df["Status Kes"] == "Selesai"]))

st.markdown("---")

col6, col7, col8, col9 = st.columns(4)
col6.metric("Rujukan SSDM", len(df[df["Kategori Rujukan"] == "SSDM"]))
col7.metric("Rujukan Minda Sihat", len(df[df["Kategori Rujukan"] == "Minda Sihat"]))
col8.metric("Rujukan Guru", len(df[df["Kategori Rujukan"] == "Rujukan Guru"]))
col9.metric("Rujukan Psikometrik", len(df[df["Kategori Rujukan"] == "Psikometrik"]))

st.markdown("---")

# 6. CHARTS LAYOUT SECTION
# Row 1: Kategori Rujukan (Bar) & Perbandingan Kaunseling (Pie)
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("Bilangan Murid Mengikut Kategori Rujukan")
    fig_bar = px.bar(df, x="Kategori Rujukan", color="Kategori Rujukan", 
                     color_discrete_sequence=px.colors.qualitative.Prism, barmode="group")
    fig_bar.update_layout(height=320, showlegend=False, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig_bar, use_container_width=True)

with row1_col2:
    st.subheader("Perbandingan Kaunseling Individu & Kelompok")
    fig_pie = px.pie(df, names="Jenis Kaunseling", hole=0.4,
                     color_discrete_sequence=["#002F6C", "#006B3E"])
    fig_pie.update_layout(height=320, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig_pie, use_container_width=True)

# Row 2: Tingkatan (Column) & Kelas (Column)
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.subheader("Bilangan Murid Mengikut Tingkatan")
    fig_ting = px.histogram(df, x="Tingkatan", category_orders={"Tingkatan": sorted(df_all["Tingkatan"].unique())},
                            color_discrete_sequence=["#002F6C"])
    fig_ting.update_layout(height=320, yaxis_title="Bilangan", margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig_ting, use_container_width=True)

with row2_col2:
    st.subheader("Bilangan Murid Mengikut Kelas")
    fig_kelas = px.histogram(df, x="Kelas", category_orders={"Kelas": ["Sidiq", "Amanah", "Tabligh", "Fatonah"]},
                             color_discrete_sequence=["#006B3E"])
    fig_kelas.update_layout(height=320, yaxis_title="Bilangan", margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig_kelas, use_container_width=True)

# Row 3: Trend (Line) & Stacked Breakdown
row3_col1, row3_col2 = st.columns(2)

with row3_col1:
    st.subheader("Trend Khidmat Kaunseling Mengikut Bulan")
    trend_df = df.groupby("Bulan-Tahun").size().reset_index(name="Jumlah Kes")
    fig_line = px.line(trend_df, x="Bulan-Tahun", y="Jumlah Kes", markers=True,
                       color_discrete_sequence=["#002F6C"])
    fig_line.update_layout(height=320, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig_line, use_container_width=True)

with row3_col2:
    st.subheader("Kategori Rujukan Mengikut Tingkatan")
    fig_stack = px.histogram(df, x="Tingkatan", color="Kategori Rujukan",
                             category_orders={"Tingkatan": sorted(df_all["Tingkatan"].unique())},
                             color_discrete_sequence=px.colors.qualitative.Safe)
    fig_stack.update_layout(height=320, yaxis_title="Bilangan", margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig_stack, use_container_width=True)

st.markdown("---")

# 7. SEARCHABLE TABLE REPORT SECTION
st.subheader("📋 Laporan Senarai Murid")

# Dynamic text search input box
search_query = st.text_input("🔍 Cari Nama Murid:", "")

# Inject data search
if search_query:
    df_final = df[df["Nama Murid"].str.contains(search_query, case=False, na=False)]
else:
    df_final = df

# Selective columns formatting for standard output view
display_cols = ["ID Murid", "Nama Murid", "Tingkatan", "Kelas", "Tarikh Sesi", "Jenis Kaunseling", "Kategori Rujukan", "Isu", "Status Kes"]
st.dataframe(df_final[display_cols].reset_index(drop=True), use_container_width=True)

# Printable footprint reminder
st.caption("💡 *Nota Cetakan: Guna fungsi cetak pelayar web (Ctrl+P / Cmd+P) dan tetapkan orientasi kepada 'Landscape' untuk cetakan susun atur kad A4 yang kemas.*")