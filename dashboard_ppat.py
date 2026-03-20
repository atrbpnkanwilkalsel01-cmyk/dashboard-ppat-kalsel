import streamlit as st
import pandas as pd

# 1. Konfigurasi Dasar
st.set_page_config(page_title="Monitoring PPAT Kalsel", layout="wide")

# 2. Link Data Direct CSV
URL = "https://docs.google.com/spreadsheets/d/1OfPHzg74p-WKeC0WzwT931cLdVEW20mbggv-2W8X7Gw/export?format=csv"

@st.cache_data(ttl=30)
def load_data():
    # Membaca data apa adanya (semua sebagai string agar tidak ada data hilang/corrupt)
    df = pd.read_csv(URL, dtype=str)
    # Bersihkan hanya spasi di judul kolom saja
    df.columns = [str(c).strip() for c in df.columns]
    return df

st.title("📂 Data Monitoring Pelaporan PPAT")
st.caption("Menampilkan data real-time sesuai dengan isi Google Sheets")
st.markdown("---")

try:
    df = load_data()
    
    if df.empty:
        st.warning("Data di Google Sheets kosong atau tidak terbaca.")
    else:
        # --- SIDEBAR UNTUK FILTER ---
        # Mengambil kolom ke-2 (Kantor Pertanahan) secara otomatis berdasarkan urutan posisi
        col_kantah = df.columns[1] 
        
        st.sidebar.header("Filter Tampilan")
        list_kantah = sorted(df[col_kantah].dropna().unique().tolist())
        pilih_kantah = st.sidebar.selectbox("Pilih Kantor Pertanahan:", ["TAMPILKAN SEMUA"] + list_kantah)

        # Filter Data
        if pilih_kantah == "TAMPILKAN SEMUA":
            df_final = df
        else:
            df_final = df[df[col_kantah] == pilih_kantah]

        # --- RINGKASAN SEDERHANA ---
        st.metric("Total Baris Data", len(df_final))

        # --- TABEL UTAMA ---
        # Menampilkan SEMUA kolom yang ada di Sheet tanpa terkecuali
        st.dataframe(
            df_final, 
            use_container_width=True, 
            height=600,
            hide_index=True
        )

        # Tombol Download untuk arsip
        st.markdown("---")
        csv = df_final.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Data CSV",
            data=csv,
            file_name=f'data_ppat_{pilih_kantah}.csv',
            mime='text/csv',
        )

except Exception as e:
    st.error(f"Sistem gagal membaca data: {e}")
    st.info("Pastikan akses Google Sheets adalah 'Anyone with the link can view'.")
