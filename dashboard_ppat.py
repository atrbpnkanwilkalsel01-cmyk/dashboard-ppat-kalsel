import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman Modern
st.set_page_config(page_title="Data Center PPAT Kalsel", layout="wide")

# Custom CSS untuk mempercantik tampilan
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Link Data (Mode CSV)
URL = "https://docs.google.com/spreadsheets/d/1OfPHzg74p-WKeC0WzwT931cLdVEW20mbggv-2W8X7Gw/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    # Load semua data sebagai text agar tidak ada error angka
    df = pd.read_csv(URL, dtype=str)
    # Bersihkan nama kolom
    df.columns = [str(c).strip() for c in df.columns]
    return df

# --- HEADER DASHBOARD ---
st.title("📂 Data Center Pelaporan PPAT")
st.caption("Sistem Monitoring Administrasi Real-Time")
st.markdown("---")

try:
    df = load_data()
    
    # 3. Sidebar Filter yang Bersih
    st.sidebar.header("⚙️ Kontrol Data")
    
    # Deteksi kolom secara otomatis tanpa index kaku
    col_kantah = [c for c in df.columns if 'Kantor' in c or 'Kantah' in c]
    ck = col_kantah[0] if col_kantah else df.columns[1]
    
    list_kantah = sorted(df[ck].dropna().unique().tolist())
    pilih_kantah = st.sidebar.selectbox("Filter Wilayah Kerja:", ["Semua Wilayah"] + list_kantah)

    # Logika Filter
    df_filtered = df[df[ck] == pilih_kantah] if pilih_kantah != "Semua Wilayah" else df

    # 4. Ringkasan Data (Metrics Card)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Total Laporan", f"{len(df_filtered)} Berkas")
    with c2:
        # Cari kolom Nama PPAT
        col_ppat = [c for c in df.columns if 'Nama' in c]
        cp = col_ppat[0] if col_ppat else df.columns[2]
        st.metric("PPAT Aktif", f"{df_filtered[cp].nunique()} Orang")
    with c3:
        st.metric("Wilayah", pilih_kantah if pilih_kantah != "Semua Wilayah" else "Kalsel")

    # 5. Tabel Utama (Fitur Search & Sort Bawaan)
    st.markdown("### 📑 Detail Pelaporan Lengkap")
    st.info("Gunakan tombol 'Search' di pojok kanan tabel untuk mencari nama PPAT atau nomor berkas dengan cepat.")
    
    # Menampilkan tabel interaktif yang sangat rapi
    st.dataframe(
        df_filtered, 
        use_container_width=True, 
        height=600,
        hide_index=True
    )

    # 6. Fitur Ekspor
    st.markdown("---")
    col_down, col_info = st.columns([1, 3])
    with col_down:
        csv = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Data (CSV)",
            data=csv,
            file_name=f'Data_PPAT_{pilih_kantah}.csv',
            mime='text/csv',
        )
    with col_info:
        st.write(f"Menampilkan {len(df_filtered)} baris data dari Google Sheets.")

except Exception as e:
    st.error(f"⚠️ Terjadi kendala saat memuat data: {e}")
    st.info("Pastikan Google Sheets Anda sudah di-share publik (Anyone with the link can view).")
