import streamlit as st
import pandas as pd

# 1. Judul & Konfigurasi Halaman Dasar
st.set_page_config(page_title="Monitoring PPAT Kalsel", layout="wide")
st.title("📂 Data Monitoring Pelaporan PPAT")

# 2. Link Google Sheets (Pastikan URL ini benar)
URL = "https://docs.google.com/spreadsheets/d/1OfPHzg74p-WKeC0WzwT931cLdVEW20mbggv-2W8X7Gw/export?format=csv"

@st.cache_data(ttl=10)
def load_data():
    # Membaca data sebagai string agar tidak ada baris yang hilang
    df = pd.read_csv(URL, dtype=str)
    # Bersihkan nama kolom dari spasi
    df.columns = [str(c).strip() for c in df.columns]
    return df

try:
    df = load_data()
    
    if df.empty:
        st.warning("Data tidak terbaca atau Google Sheets kosong.")
    else:
        # --- FILTER PER KANTAH ---
        st.sidebar.header("🔍 Filter Wilayah")
        
        # Mengambil kolom Kantor Pertanahan (Kolom kedua)
        col_kantah = df.columns[1] 
        
        list_kantah = sorted(df[col_kantah].dropna().unique().tolist())
        pilih_kantah = st.sidebar.selectbox(
            "Pilih Kantor Pertanahan:", 
            ["SEMUA DATA"] + list_kantah
        )

        # Logika Filter
        if pilih_kantah == "SEMUA DATA":
            df_final = df
        else:
            df_final = df[df[col_kantah] == pilih_kantah]

        # --- RINGKASAN & TABEL ---
        st.metric("Total Laporan Terdeteksi", len(df_final))
        st.markdown(f"Menampilkan data untuk: **{pilih_kantah}**")
        
        # Menampilkan tabel lengkap (Semua Kolom & Semua Nama PPAT)
        st.dataframe(
            df_final, 
            use_container_width=True, 
            height=700,
            hide_index=True
        )

        # Tombol Download
        csv = df_final.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Data CSV", data=csv, file_name='data_ppat.csv')

except Exception as e:
    st.error(f"Sistem gagal: {e}")
