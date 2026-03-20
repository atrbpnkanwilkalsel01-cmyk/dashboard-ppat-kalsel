import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Halaman
st.set_page_config(page_title="PPAT Kalsel", layout="wide")

# 2. Ambil Data (Gunakan Link Sheets Terbaru Anda)
URL = "https://docs.google.com/spreadsheets/d/1OfPHzg74p-WKeC0WzwT931cLdVEW20mbggv-2W8X7Gw/export?format=csv"

def load_data():
    df = pd.read_csv(URL)
    df.columns = df.columns.str.strip()
    return df

# 3. Jalankan Aplikasi
try:
    df = load_data()
    
    # Identifikasi kolom otomatis
    col_kantah = [c for c in df.columns if 'Kantor Pertanahan' in c][0]
    col_ppat = [c for c in df.columns if 'Nama' in c and 'PPAT' in c][0]

    st.title("📊 Monitoring PPAT")

    # Filter di samping
    list_kantah = sorted(df[col_kantah].unique().tolist())
    pilihan = st.sidebar.selectbox("Pilih Kantah:", ["Semua"] + list_kantah)

    # Filter data
    df_f = df[df[col_kantah] == pilihan] if pilihan != "Semua" else df

    # Tampilkan Angka Total
    st.metric("Total Laporan", len(df_f))

    # Grafik Nama PPAT
    st.subheader(f"Daftar PPAT - {pilihan}")
    counts = df_f[col_ppat].value_counts().reset_index()
    counts.columns = ['Nama PPAT', 'Jumlah']
    
    fig = px.bar(counts, x='Jumlah', y='Nama PPAT', orientation='h', text='Jumlah')
    fig.update_layout(height=max(400, len(counts)*30), yaxis={'categoryorder':'total ascending'})
    
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error("Gagal memuat data. Pastikan kolom di Sheets sudah benar.")
