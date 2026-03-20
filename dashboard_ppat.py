import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Judul dan Layout
st.set_page_config(page_title="Monitoring PPAT Kalsel", layout="wide")

# 2. Link Data (Google Sheets CSV Eimpoimport streamlit as st
import pandas as pd
import plotly.express as px
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard PPAT", layout="wide")

# Mengambil Data dari Google Sheets
URL = "https://docs.google.com/spreadsheets/d/1OfPHzg74p-WKeC0WzwT931cLdVEW20mbggv-2W8X7Gw/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(URL)
    df.columns = df.columns.str.strip()
    return df

try:
    df = load_data()
    # Deteksi kolom secara otomatis
    col_kantah = [c for c in df.columns if 'Kantor Pertanahan' in c][0]
    col_ppat = [c for c in df.columns if 'Nama' in c and 'PPAT' in c][0]

    st.title("📊 Monitoring Pelaporan PPAT")

    # Filter Sidebar
    pilihan = st.sidebar.selectbox("Pilih Wilayah:", ["Semua"] + sorted(df[col_kantah].unique().tolist()))
    
    # Filter Data
    df_f = df[df[col_kantah] == pilihan] if pilihan != "Semua" else df

    # Tampilan Angka
    st.metric("Total Laporan Masuk", len(df_f))

    # Grafik Nama PPAT
    st.subheader(f"Daftar PPAT - {pilihan}")
    counts = df_f[col_ppat].value_counts().reset_index()
    counts.columns = ['Nama PPAT', 'Jumlah']
    
    fig = px.bar(counts, x='Jumlah', y='Nama PPAT', orientation='h', text='Jumlah', color_discrete_sequence=['#3498db'])
    fig.update_layout(height=max(400, len(counts)*30), yaxis={'categoryorder':'total ascending'}, xaxis_title="", yaxis_title="")
    
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error("Gagal memuat data. Periksa koneksi atau kolom Google Sheets.")
st.set_page_config(page_title="Dashboard PPAT", layout="wide")

# Ambil Data
URL = "https://docs.google.com/spreadsheets/d/1OfPHzg74p-WKeC0WzwT931cLdVEW20mbggv-2W8X7Gw/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(URL)
    df.columns = df.columns.str.strip()
    return df

try:
    df = load_data()
    # Deteksi kolom Nama PPAT & Kantah secara otomatis
    col_kantah = [c for c in df.columns if 'Kantor Pertanahan' in c][0]
    col_ppat = [c for c in df.columns if 'Nama' in c and 'PPAT' in c][0]

    st.title("📊 Monitoring Pelaporan")

    # Filter Sidebar
    pilihan = st.sidebar.selectbox("Wilayah:", ["Semua"] + sorted(df[col_kantah].unique().tolist()))
    df_f = df[df[col_kantah] == pilihan] if pilihan != "Semua" else df

    st.metric("Total Laporan", len(df_f))

    # Grafik Nama PPAT
    counts = df_f[col_ppat].value_counts().reset_index()
    counts.columns = ['PPAT', 'Jumlah']
    
    fig = px.bar(counts, x='Jumlah', y='PPAT', orientation='h', text='Jumlah')
    fig.update_layout(height=max(400, len(counts)*30), yaxis={'categoryorder':'total ascending'}, xaxis_title="", yaxis_title="")
    
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
