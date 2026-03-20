import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Dashboard PPAT Kalsel", layout="wide")

# 2. Link Google Sheets (Export CSV)
URL = "https://docs.google.com/spreadsheets/d/1OfPHzg74p-WKeC0WzwT931cLdVEW20mbggv-2W8X7Gw/export?format=csv"

@st.cache_data(ttl=30)
def load_data():
    # Mengambil data mentah (semua kolom dan baris)
    df = pd.read_csv(URL, dtype=str)
    df.columns = [str(c).strip() for c in df.columns]
    return df

st.title("📊 Monitoring Pelaporan PPAT (Data Lengkap)")
st.markdown("---")

try:
    df = load_data()
    
    if df.empty:
        st.warning("Data kosong atau tidak dapat diakses.")
    else:
        # Identifikasi Kolom (Berdasarkan posisi agar tidak error nama)
        col_kantah = df.columns[1] # Kolom B
        col_ppat = df.columns[2]   # Kolom C
        
        # --- MENU FILTER (Independen) ---
        st.sidebar.header("🔍 Filter Pencarian")
        
        # Filter Kantah (Bisa pilih banyak)
        list_kantah = sorted(df[col_kantah].dropna().unique().tolist())
        pilih_kantah = st.sidebar.multiselect("Filter Kantor Pertanahan:", list_kantah)

        # Filter Nama PPAT (MENAMPILKAN SEMUA NAMA DARI AWAL)
        list_ppat_semua = sorted(df[col_ppat].dropna().unique().tolist())
        pilih_ppat = st.sidebar.multiselect("Filter Nama PPAT (Cari Semua Nama di Sini):", list_ppat_semua)

        # --- LOGIKA FILTERING ---
        df_filtered = df.copy()
        
        if pilih_kantah:
            df_filtered = df_filtered[df_filtered[col_kantah].isin(pilih_kantah)]
        
        if pilih_ppat:
            df_filtered = df_filtered[df_filtered[col_ppat].isin(pilih_ppat)]

        # --- TAMPILAN DATA ---
        c1, c2 = st.columns(2)
        c1.metric("Total Laporan Terpilih", len(df_filtered))
        c2.metric("Total PPAT Unik Terpilih", df_filtered[col_ppat].nunique())

        st.markdown("### 📑 Tabel Seluruh Baris Data")
        # Menampilkan SEMUA baris dan SEMUA kolom yang ada di Sheet
        st.dataframe(df_filtered, use_container_width=True, height=700)

        # Tombol Download Data Terfilter
        csv = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Hasil Filter ke CSV", data=csv, file_name='data_ppat.csv')

except Exception as e:
    st.error(f"Terjadi kesalahan teknis: {e}")
    st.info("Saran: Pastikan Google Sheets sudah disetel 'Anyone with the link can view'.")
