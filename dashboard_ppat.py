import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Judul dan Konfigurasi
st.set_page_config(page_title="Dashboard PPAT", layout="wide")
st.title("📊 Monitoring Pelaporan PPAT")

# 2. Link Data Google Sheets Anda
URL = "https://docs.google.com/spreadsheets/d/1OfPHzg74p-WKeC0WzwT931cLdVEW20mbggv-2W8X7Gw/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(URL)
    # Membersihkan nama kolom dari spasi yang tidak terlihat
    df.columns = [str(c).strip() for c in df.columns]
    return df

try:
    df = load_data()
    
    # Mengambil kolom berdasarkan urutan posisi agar tidak error nama
    # Kolom 1 biasanya 'Kantor Pertanahan', Kolom 2 biasanya 'Nama PPAT'
    col_kantah = df.columns[1]
    col_ppat = df.columns[2]

    # Sidebar Filter
    list_kantah = sorted(df[col_kantah].dropna().unique().tolist())
    pilih = st.sidebar.selectbox("Pilih Wilayah:", ["Semua"] + list_kantah)

    # Filter Data
    if pilih != "Semua":
        df_f = df[df[col_kantah] == pilih]
    else:
        df_f = df

    # Menampilkan Statistik Sederhana
    st.metric("Total Laporan Masuk", len(df_f))

    # Membuat Grafik Nama PPAT
    counts = df_f[col_ppat].value_counts().reset_index()
    counts.columns = ['Nama PPAT', 'Jumlah']
    
    fig = px.bar(
        counts, 
        x='Jumlah', 
        y='Nama PPAT', 
        orientation='h', 
        text='Jumlah',
        color_discrete_sequence=['#3498db']
    )
    
    fig.update_layout(
        height=max(400, len(counts) * 30),
        yaxis={'categoryorder':'total ascending'},
        xaxis_title="Jumlah Laporan",
        yaxis_title=""
    )
    
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Terjadi kesalahan teknis: {e}")
