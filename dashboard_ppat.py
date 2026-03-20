import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Judul dan Layout
st.set_page_config(page_title="Monitoring PPAT Kalsel", layout="wide")

# 2. Link Data (Google Sheets CSV Eimport streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard", layout="wide")

# Link Data
URL = "https://docs.google.com/spreadsheets/d/1OfPHzg74p-WKeC0WzwT931cLdVEW20mbggv-2W8X7Gw/export?format=csv"

@st.cache_data(ttl=60)
def load():
    df = pd.read_csv(URL)
    df.columns = df.columns.str.strip()
    return df

try:
    data = load()
    
    # Mencari kolom secara otomatis (ini harus ada di kode tapi bisa disembunyikan di tampilan)
    c_kantah = [c for c in data.columns if 'Kantor Pertanahan' in c][0]
    c_ppat = [c for c in data.columns if 'Nama' in c and 'PPAT' in c][0]

    st.title("📊 Monitoring Pelaporan")

    # Filter Sidebar (Tanpa teks instruksi yang panjang)
    pilih = st.sidebar.selectbox("Wilayah:", ["Semua"] + sorted(data[c_kantah].unique().tolist()))

    # Filter data
    df_f = data[data[c_kantah] == pilih] if pilih != "Semua" else data

    # Tampilkan angka saja
    st.metric("Total Laporan", len(df_f))

    # Grafik (Nama PPAT tetap ada di grafik agar bisa dibaca, tapi judul atasnya dihapus)
    counts = df_f[c_ppat].value_counts().reset_index()
    counts.columns = ['P', 'J'] # Nama kolom disingkat agar tidak ada kata "Nama PPAT"
    
    fig = px.bar(counts, x='J', y='P', orientation='h', text='J', color_discrete_sequence=['#3498db'])
    
    # Menghapus judul sumbu X dan Y agar bersih
    fig.update_layout(
        xaxis_title="", 
        yaxis_title="", 
        height=max(400, len(counts) * 30),
        margin=dict(l=150, r=20, t=20, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)

except Exception:
    st.error("Pastikan koneksi internet stabil atau kolom Google Sheets tidak kosong.")xport)
URL_SHEET = "https://docs.google.com/spreadsheets/d/1OfPHzg74p-WKeC0WzwT931cLdVEW20mbggv-2W8X7Gw/export?format=csv"

@st.cache_data(ttl=60)
def ambil_data():
    df = pd.read_csv(URL_SHEET)
    df.columns = df.columns.str.strip()
    return df

# 3. Proses Tampilan
try:
    data = ambil_data()
    
    # Deteksi kolom (mencari kolom yang relevan secara otomatis)
    kol_kantah = [c for c in data.columns if 'Kantor Pertanahan' in c][0]
    kol_ppat = [c for c in data.columns if 'Nama' in c and 'PPAT' in c][0]

    st.title("📊 Monitoring Pelaporan")

    # Sidebar Filter
    pilihan_kantah = st.sidebar.selectbox(
        "Pilih Wilayah:", 
        ["Semua"] + sorted(data[kol_kantah].unique().tolist())
    )

    # Filter Data
    df_f = data[data[kol_kantah] == pilihan_kantah] if pilihan_kantah != "Semua" else data

    # Menampilkan total laporan saja (Nama PPAT & Kantah di judul dihapus)
    st.metric("Total Laporan", len(df_f))

    # Grafik Utama
    counts = df_f[kol_ppat].value_counts().reset_index()
    counts.columns = ['PPAT', 'Jumlah']
    
    fig = px.bar(
        counts, 
        x='Jumlah', 
        y='PPAT', 
        orientation='h',
        text='Jumlah',
        color_discrete_sequence=['#3498db']
    )
    
    fig.update_layout(
        yaxis={'categoryorder':'total ascending', 'title': ''}, # Judul sumbu Y dihapus
        xaxis={'title': 'Jumlah Laporan'},
        height=max(400, len(counts) * 30),
        margin=dict(l=200)
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # Tabel Detail (Hanya menampilkan Timestamp)
    with st.expander("Lihat Detail Waktu"):
        st.dataframe(df_f[['Timestamp']], use_container_width=True)
