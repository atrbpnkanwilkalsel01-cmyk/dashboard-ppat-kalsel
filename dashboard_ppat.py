import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman Luas
st.set_page_config(page_title="Monitoring PPAT Kalsel", layout="wide")

# 2. Link Google Sheets (Pastikan URL ini benar-benar mengarah ke CSV export)
URL = "https://docs.google.com/spreadsheets/d/1OfPHzg74p-WKeC0WzwT931cLdVEW20mbggv-2W8X7Gw/export?format=csv"

@st.cache_data(ttl=10) # Update sangat cepat setiap 10 detik
def load_data():
    # Membaca data tanpa batasan, semua diperlakukan sebagai teks agar tidak hilang
    df = pd.read_csv(URL, dtype=str)
    # Menghapus spasi di awal/akhir nama kolom
    df.columns = [str(c).strip() for c in df.columns]
    return df

st.title("📂 Data Lengkap Pelaporan PPAT")
st.markdown("---")

try:
    df = load_data()
    
    if df.empty:
        st.error("Data tidak ditemukan di Google Sheets. Pastikan sheet tidak kosong.")
    else:
        # 3. Sidebar untuk Filter Wilayah
        # Kita ambil kolom Kantor Pertanahan (biasanya kolom ke-2)
        col_kantah = df.columns[1] 
        # Kita ambil kolom Nama PPAT (biasanya kolom ke-3)
        col_ppat = df.columns[2]

        st.sidebar.header("Pilih Filter")
        list_kantah = sorted(df[col_kantah].dropna().unique().tolist())
        pilih_kantah = st.sidebar.selectbox("Tampilkan Wilayah:", ["SEMUA KANTAH"] + list_kantah)

        # Logika Filter
        if pilih_kantah == "SEMUA KANTAH":
            df_final = df
        else:
            df_final = df[df[col_kantah] == pilih_kantah]

        # 4. Ringkasan (Metrics)
        # Di sini kita akan hitung berdasarkan data asli di sheet
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Total Seluruh Laporan", len(df_final))
        with c2:
            st.metric("Jumlah PPAT Terdata", df_final[col_ppat].nunique())
        with c3:
            st.metric("Jumlah Kantah", df_final[col_kantah].nunique())

        st.markdown("---")
        
        # 5. Tabel Utama (Menampilkan SEMUA Kolom dan SEMUA Baris)
        st.subheader(f"📑 Tabel Transaksi: {pilih_kantah}")
        st.write("Berikut adalah seluruh data yang terbaca dari Google Sheets:")
        
        # Menampilkan tabel yang bisa di-scroll dan dicari
        st.dataframe(
            df_final, 
            use_container_width=True, 
            height=700 # Tabel dibuat tinggi agar banyak baris terlihat sekaligus
        )

        # 6. Fitur Download untuk backup
        csv = df_final.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Data Ini ke Excel (CSV)",
            data=csv,
            file_name=f'data_ppat_{pilih_kantah}.csv',
            mime='text/csv',
        )

except Exception as e:
    st.error(f"Terjadi kesalahan saat menarik data: {e}")
    st.info("Pastikan Google Sheets sudah di-set 'Anyone with the link can view'.")import streamlit as st
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
