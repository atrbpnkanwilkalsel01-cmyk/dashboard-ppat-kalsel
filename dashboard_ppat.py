import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Judul Aplikasi
st.set_page_config(page_title="Dashboard PPAT", layout="wide")
st.title("📊 Monitoring Pelaporan PPAT")

# 2. Link Google Sheets (Pastikan URL ini benar)
URL = "https://docs.google.com/spreadsheets/d/1OfPHzg74p-WKeC0WzwT931cLdVEW20mbggv-2W8X7Gw/export?format=csv"

# 3. Fungsi Ambil Data
@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(URL)
    df.columns = df.columns.str.strip()
    return df

# 4. Tampilkan Data
try:
    data = load_data()
    
    # Cari Nama Kolom Otomatis
    c_kantah = [c for c in data.columns if 'Kantor Pertanahan' in c][0]
    c_ppat = [c for c in data.columns if 'Nama' in c and 'PPAT' in c][0]

    # Sidebar Filter
    list_kantah = sorted(data[c_kantah].unique().tolist())
    pilih = st.sidebar.selectbox("Pilih Wilayah:", ["Semua"] + list_kantah)

    # Filter Data
    df_f = data[data[c_kantah] == pilih] if pilih != "Semua" else data

    # Tampilkan Angka Total
    st.metric("Total Laporan", len(df_f))

    # Grafik Batang Horizontal
    counts = df_f[c_ppat].value_counts().reset_index()
    counts.columns = ['PPAT', 'Jumlah']
    
    fig = px.bar(counts, x='Jumlah', y='PPAT', orientation='h', text='Jumlah', color_discrete_sequence=['#3498db'])
    fig.update_layout(height=max(400, len(counts)*30), yaxis={'categoryorder':'total ascending'}, xaxis_title="", yaxis_title="")
    
    st.plotly_chart(fig, use_container_width=True)
