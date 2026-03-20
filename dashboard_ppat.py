import streamlit as st
import pandas as pd

# 1. Konfigurasi Dasar
st.set_page_config(page_title="Data Monitoring PPAT", layout="wide")

# URL CSV Langsung
URL = "https://docs.google.com/spreadsheets/d/1OfPHzg74p-WKeC0WzwT931cLdVEW20mbggv-2W8X7Gw/export?format=csv"

@st.cache_data(ttl=1) # Cek data setiap detik
def load_full_data():
    # Memaksa Google mengirimkan data terbaru tanpa limit
    return pd.read_csv(URL, dtype=str, on_bad_lines='skip')

st.title("📂 Pusat Data Monitoring PPAT")
st.markdown("---")

try:
    df = load_full_data()
    df.columns = [str(c).strip() for c in df.columns]

    # --- BAGIAN DIAGNOSTIK (Cek kenapa data cuma sedikit) ---
    st.sidebar.header("🔍 Diagnostik Sistem")
    st.sidebar.write(f"Baris Terbaca: **{len(df)}**")
    
    if len(df) <= 2:
        st.sidebar.error("⚠️ DATA TERBATAS")
        st.sidebar.write("Google Sheets hanya mengirim 2 baris. Kemungkinan data Anda ada di **Tab/Sheet lain**, bukan di Sheet pertama.")

    # --- FILTER OTOMATIS ---
    # Mengambil kolom manapun yang mengandung kata 'Nama' atau 'Kantor'
    col_kantah = [c for c in df.columns if 'Kantor' in c or 'Kantah' in c]
    col_ppat = [c for c in df.columns if 'Nama' in c]

    if col_kantah and col_ppat:
        ck = col_kantah[0]
        cp = col_ppat[0]

        # Multi-filter
        st.sidebar.header("⚙️ Filter")
        all_ppat = sorted(df[cp].dropna().unique().tolist())
        pilih_ppat = st.sidebar.multiselect("Pilih/Cari Nama PPAT:", all_ppat)

        # Logika Filter
        df_filtered = df[df[cp].isin(pilih_ppat)] if pilih_ppat else df
    else:
        df_filtered = df

    # --- TAMPILAN UTAMA ---
    st.subheader("📑 Tabel Informasi Lengkap")
    st.caption("Gunakan kotak pencarian di dalam tabel (pojok kanan atas tabel) untuk mencari data.")
    
    # Menampilkan tabel yang bisa dicari, diurutkan, dan difilter manual
    st.dataframe(df_filtered, use_container_width=True, height=600)

    # Info Kolom
    with st.expander("Lihat Struktur Kolom Terbaca"):
        st.write(list(df.columns))

except Exception as e:
    st.error(f"Koneksi ke Sheets Gagal: {e}")

st.markdown("---")
st.warning("Jika data tetap hanya 2, silakan pindahkan data Anda di Google Sheets ke **Tab paling kiri (Sheet1)**.")
