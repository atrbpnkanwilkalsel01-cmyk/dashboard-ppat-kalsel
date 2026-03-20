import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman Dasar
st.set_page_config(page_title="Monitoring PPAT Kalsel", layout="wide")

# 2. Link Google Sheets (Pastikan URL ini benar)
URL = "https://docs.google.com/spreadsheets/d/1OfPHzg74p-WKeC0WzwT931cLdVEW20mbggv-2W8X7Gw/export?format=csv"

@st.cache_data(ttl=10) # Update data setiap 10 detik
def load_data():
    # Membaca seluruh data sebagai teks (string) agar tidak ada baris yang hilang
    df = pd.read_csv(URL, dtype=str)
    # Membersihkan spasi di nama kolom
    df.columns = [str(c).strip() for c in df.columns]
    return df

st.title("📂 Data Monitoring Pelaporan PPAT")
st.markdown("---")

try:
    df = load_data()
    
    if df.empty:
        st.warning("Data tidak terbaca atau Google Sheets kosong.")
    else:
        # --- MENU FILTER PER KANTAH SAJA ---
        st.sidebar.header("🔍 Filter Wilayah")
        
        # Mengambil kolom Kantor Pertanahan (Biasanya kolom kedua/Index 1)
        col_kantah = df.columns[1] 
        
        # Mengambil daftar unik Kantah yang ada di Sheets
        list_kantah = sorted(df[col_kantah].dropna().unique().tolist())
        
        # Pilihan Filter
        pilih_kantah = st.sidebar.selectbox(
            "Pilih Kantor Pertanahan:", 
            ["TAMPILKAN SEMUA DATA"] + list_kantah
        )

        # Logika Penyaringan
        if pilih_kantah == "TAMPILKAN SEMUA DATA":
            df_final = df
        else:
            df_final = df[df[col_kantah] == pilih_kantah]

        # --- RINGKASAN ---
        st.metric("Jumlah Laporan yang Muncul", len(df_final))
        st.info(f"Menampilkan data untuk: **{pilih_kantah}**")

        # --- TABEL DATA LENGKAP ---
        # Menampilkan SEMUA KOLOM dan SEMUA BARIS sesuai filter
        st.dataframe(
            df_final, 
            use_container_width=True, 
            height=700, # Tabel dibuat tinggi agar semua data terlihat
            hide_index=True
        )

        # Tombol Download Hasil Filter
        csv = df_final.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Data Ini (CSV)",
            data=csv,
            file_name=f'data_ppat_{pilih_kantah}.csv',
            mime='text/csv',
        )

except Exception as e:
    st.error(f"Sistem gagal memuat data: {e}")
    st.info("Pastikan link Google Sheets Anda sudah di-set 'Anyone with the link can view'.")import streamlit as st
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
