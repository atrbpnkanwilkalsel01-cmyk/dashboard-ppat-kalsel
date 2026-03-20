import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Judul dan Konfigurasi
st.set_page_config(page_title="Dashboard PPAT", layout="wide")
st.title("📊 Monitoring Pelaporan PPAT Kalsel")

# 2. Link Data Google Sheets
URL = "https://docs.google.com/spreadsheets/d/1OfPHzg74p-WKeC0WzwT931cLdVEW20mbggv-2W8X7Gw/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(URL, dtype=str)
    # Bersihkan spasi di nama kolom
    df.columns = [str(c).strip() for c in df.columns]
    return df

try:
    df = load_data()
    
    # Deteksi otomatis nama kolom penting
    cols_kantah = [c for c in df.columns if 'Kantor' in c or 'Kantah' in c]
    cols_ppat = [c for c in df.columns if 'Nama' in c]
    
    # Ambil kolom pertama yang cocok sebagai cadangan
    ck = cols_kantah[0] if cols_kantah else df.columns[1]
    cp = cols_ppat[0] if cols_ppat else df.columns[2]

    # --- SIDEBAR FILTER (Sidebar) ---
    st.sidebar.header("Filter Data")
    list_kantah = sorted(df[ck].dropna().unique().tolist())
    pilih = st.sidebar.selectbox("Pilih Wilayah (Filter):", ["Semua"] + list_kantah)

    # Filter Data
    df_f = df[df[ck] == pilih] if pilih != "Semua" else df

    # --- RINGKASAN DATA (Metric) ---
    st.subheader("📌 Ringkasan Data")
    st.metric("Total Laporan Masuk", len(df_f))
    st.markdown("---")

    # --- TAMPILAN GRAFIK ---
    st.subheader(f"📈 Grafik Aktivitas PPAT - {pilih}")
    
    # Menghitung jumlah laporan per PPAT
    c_ppat = df_f[cp].value_counts().reset_index()
    c_ppat.columns = ['Nama PPAT', 'Jumlah']
    
    # Hitung jumlah total PPAT unik untuk mengatur tinggi grafik
    total_ppat = len(c_ppat)
    
    # Logika: Jika PPAT sedikit (kurang dari 20), tinggi grafik minimal 400.
    # Jika banyak, setiap PPAT diberi ruang 25 pixel (misal 100 PPAT = 2500px).
    tinggi_grafik = max(400, total_ppat * 25)

    if total_ppat > 0:
        # Buat Grafik Batang Horizontal
        fig1 = px.bar(
            c_ppat, 
            x='Jumlah', 
            y='Nama PPAT', 
            orientation='h', 
            text='Jumlah',
            color='Jumlah', 
            color_continuous_scale='Blues'
        )
        
        # Konfigurasi Tampilan Grafik
        fig1.update_layout(
            height=tinggi_grafik, # Menggunakan tinggi dinamis yang sudah dihitung
            yaxis={'categoryorder':'total ascending'}, # Urutkan dari yang paling banyak
            xaxis_title="Jumlah Laporan",
            yaxis_title="" # Hapus judul sumbu Y agar nama terlihat
        )
        
        # Atur teks agar muncul di luar batang dan label sumbu Y tidak terpotong
        fig1.update_traces(textposition='outside')
        
        # Tampilkan Grafik di Streamlit
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.warning(f"Tidak ada data pelaporan ditemukan untuk wilayah {pilih}.")

    # --- TABEL DATA LENGKAP ---
    st.markdown("---")
    st.subheader("📑 Tabel Data Lengkap (Semua Kolom)")
    # Tampilkan seluruh dataframe (semua kolom)
    st.dataframe(df
