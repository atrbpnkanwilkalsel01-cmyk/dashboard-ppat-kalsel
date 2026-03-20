import streamlit as st
import pandas as pd

# 1. Setting Halaman
st.set_page_config(page_title="Data Check PPAT", layout="wide")

# 2. Link CSV (Pastikan Anyone with the link can VIEW di Google Sheets)
URL = "https://docs.google.com/spreadsheets/d/1OfPHzg74p-WKeC0WzwT931cLdVEW20mbggv-2W8X7Gw/export?format=csv"

st.title("🔍 Pengecekan Data Real-Time")

@st.cache_data(ttl=5) # Update setiap 5 detik
def load_raw_data():
    # Memaksa pembacaan seluruh file tanpa batasan
    df = pd.read_csv(URL, dtype=str, on_bad_lines='skip')
    return df

try:
    df = load_raw_data()
    
    # --- DIAGNOSTIK DATA (Untuk tahu kenapa cuma muncul sedikit) ---
    st.sidebar.header("📊 Statistik Sistem")
    st.sidebar.write(f"Total Baris Terbaca: **{len(df)}**")
    st.sidebar.write(f"Total Kolom Terbaca: **{len(df.columns)}**")
    
    if len(df) <= 2:
        st.error("⚠️ PERINGATAN: Sistem hanya mendeteksi 2 baris data.")
        st.info("Penyebabnya kemungkinan: Link Google Sheets Anda mengarah ke Tab yang salah atau akses terbatas.")
    
    # --- MENU FILTER (Dibuat sangat sederhana agar tidak error) ---
    st.sidebar.header("🔍 Filter")
    
    # Ambil kolom ke-2 (Kantah) dan ke-3 (PPAT) secara paksa
    col_A = df.columns[0] # Timestamp
    col_B = df.columns[1] # Kantah
    col_C = df.columns[2] # Nama PPAT

    # Filter Nama PPAT - Mengambil SEMUA yang unik di kolom tersebut
    semua_nama = sorted(df[col_C].dropna().unique().tolist())
    pilih_ppat = st.sidebar.multiselect("Pilih Nama PPAT (Cek Daftar Ini):", semua_nama)

    # Logika Filter
    if pilih_ppat:
        df_tampil = df[df[col_C].isin(pilih_ppat)]
    else:
        df_tampil = df

    # --- TAMPILAN UTAMA ---
    st.subheader("📑 Tabel Data Mentah (Hasil Google Sheets)")
    st.write("Jika di sini tetap muncul 2 nama, silakan cek Tab/Sheet di Google Sheets Anda.")
    
    # Menampilkan data apa adanya
    st.dataframe(df_tampil, use_container_width=True, height=800)

    # Fitur Download
    csv = df_tampil.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Data", csv, "data_ppat.csv", "text/csv")

except Exception as e:
    st.error(f"Koneksi Gagal: {e}")
