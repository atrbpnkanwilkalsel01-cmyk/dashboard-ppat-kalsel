import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman Luas
st.set_page_config(page_title="Data Center PPAT Kalsel", layout="wide")

# 2. Link Google Sheets (Pastikan URL ini benar)
URL = "https://docs.google.com/spreadsheets/d/1OfPHzg74p-WKeC0WzwT931cLdVEW20mbggv-2W8X7Gw/export?format=csv"

@st.cache_data(ttl=10) # Update sangat cepat
def load_data():
    # Membaca seluruh file tanpa batasan baris (Low Memory False)
    # Ini memastikan ribuan baris pun akan terbaca semua
    df = pd.read_csv(URL, dtype=str, low_memory=False)
    
    # Bersihkan nama kolom dari spasi atau karakter aneh
    df.columns = [str(c).strip() for c in df.columns]
    
    # Hapus baris yang benar-benar kosong (jika ada baris hantu di tengah sheet)
    df = df.dropna(how='all')
    
    return df

st.title("📑 Monitoring Pelaporan PPAT (Full Data Mode)")
st.info("Sistem ini sekarang membaca SELURUH baris data dari Google Sheets Anda.")

try:
    df = load_data()
    
    # --- PENENTUAN KOLOM (Sangat Penting) ---
    # Kita tidak menebak nama, kita ambil urutannya:
    # Index 1 = Kantor Pertanahan, Index 2 = Nama PPAT
    col_kantah = df.columns[1]
    col_ppat = df.columns[2]

    # --- MENU FILTER (Dibuat Independen Agar Semua Nama Muncul) ---
    st.sidebar.header("🔍 Filter Pencarian")

    # Ambil SEMUA daftar unik dari seluruh kolom di sheet
    all_kantah = sorted(df[col_kantah].unique().astype(str))
    all_ppat = sorted(df[col_ppat].unique().astype(str))

    # Tampilkan Filter Multiselect
    pilih_kantah = st.sidebar.multiselect(
        f"Pilih Wilayah ({len(all_kantah)} Wilayah Terdeteksi):", 
        options=all_kantah
    )

    pilih_ppat = st.sidebar.multiselect(
        f"Pilih Nama PPAT ({len(all_ppat)} Nama Terdeteksi):", 
        options=all_ppat
    )

    # --- LOGIKA FILTERING ---
    df_filtered = df.copy()
    
    if pilih_kantah:
        df_filtered = df_filtered[df_filtered[col_kantah].isin(pilih_kantah)]
    
    if pilih_ppat:
        df_filtered = df_filtered[df_filtered[col_ppat].isin(pilih_ppat)]

    # --- TAMPILAN RINGKASAN ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Laporan Terbaca", len(df))
    c2.metric("Data Setelah Filter", len(df_filtered))
    c3.metric("Total Nama PPAT di Sheet", len(all_ppat))

    # --- TABEL UTAMA ---
    st.markdown("---")
    st.subheader("Data Hasil Filter")
    
    # Menampilkan tabel dengan tinggi yang sangat luas (800 pixel)
    st.dataframe(
        df_filtered, 
        use_container_width=True, 
        height=800,
        hide_index=True
    )

    # Tombol Download
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Data ke CSV", data=csv, file_name='data_lengkap_ppat.csv')

except Exception as e:
    st.error(f"⚠️ Terjadi Masalah Pembacaan: {e}")
    st.info("Pastikan Google Sheets Anda sudah di-share 'Anyone with the link can view'.")
