import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi
st.set_page_config(page_title="Dashboard PPAT", layout="wide")
st.title("📊 Monitoring Pelaporan PPAT")

# 2. Link Data
URL = "https://docs.google.com/spreadsheets/d/1OfPHzg74p-WKeC0WzwT931cLdVEW20mbggv-2W8X7Gw/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    # Baca data sebagai string
    df = pd.read_csv(URL, dtype=str)
    # Bersihkan nama kolom dari spasi gaib
    df.columns = [str(c).strip() for c in df.columns]
    return df

try:
    df = load_data()
    
    if len(df.columns) < 3:
        st.error(f"Data ditemukan tapi kolom kurang. Kolom yang ada: {list(df.columns)}")
    else:
        # PAKAI URUTAN (INDEX), BUKAN NAMA. 
        # Index 1 = Kolom B (Kantah), Index 2 = Kolom C (Nama PPAT)
        col_kantah = df.columns[1]
        col_ppat = df.columns[2]

        # Sidebar
        list_kantah = sorted(df[col_kantah].dropna().unique().tolist())
        pilih = st.sidebar.selectbox("Filter Wilayah:", ["Semua"] + list_kantah)
        
        # Filter Data
        df_f = df[df[col_kantah] == pilih] if pilih != "Semua" else df

        # Hitung Data untuk Grafik
        counts = df_f[col_ppat].value_counts().reset_index()
        counts.columns = ['Nama', 'Jumlah']
        counts['Jumlah'] = pd.to_numeric(counts['Jumlah'], errors='coerce').fillna(0)

        # Tampilkan Total
        st.metric("Total Laporan", len(df_f))

        # Tampilkan Grafik SEMUA Nama (Tinggi Dinamis)
        # 35 pixel per nama agar semua terbaca
        tinggi_grafik = max(500, len(counts) * 35)
        
        fig = px.bar(
            counts, 
            x='Jumlah', 
            y='Nama', 
            orientation='h', 
            text='Jumlah',
            color='Jumlah',
            color_continuous_scale='Blues'
        )
        
        fig.update_layout(
            height=tinggi_grafik,
            yaxis={'categoryorder':'total ascending'},
            margin=dict(l=250), # Ruang luas untuk nama PPAT yang panjang
            xaxis_title="Jumlah Laporan",
            yaxis_title=""
        )
        st.plotly_chart(fig, use_container_width=True)

        # TAMPILKAN SEMUA KOLOM (Tabel Lengkap)
        st.markdown("---")
        st.subheader("📑 Tabel Data Lengkap (Semua Kolom)")
        st.dataframe(df_f, use_container_width=True)

except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
