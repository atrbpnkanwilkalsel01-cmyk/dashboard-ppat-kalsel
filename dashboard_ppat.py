import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman Dasar
st.set_page_config(page_title="Data Center PPAT Kalsel", layout="wide")

# 2. Link Google Sheets (Mode CSV)
URL = "https://docs.google.com/spreadsheets/d/1OfPHzg74p-WKeC0WzwT931cLdVEW20mbggv-2W8X7Gw/export?format=csv"

@st.cache_data(ttl=30)
def load_data():
    # Load data sebagai string agar aman dari error tipe data
    df = pd.read_csv(URL, dtype=str)
    # Bersihkan nama kolom dari spasi tidak terlihat
    df.columns = [str(c).strip() for c in df.columns]
    return df

st.title("📂 Data Monitoring Pelaporan PPAT")
st.markdown("---")

try:
    df = load_data()
    
    if df.empty:
        st.warning("Data di Google Sheets kosong atau tidak terbaca.")
    else:
        # --- SISTEM FILTER DINAMIS (SIDEBAR) ---
        st.sidebar.header("🔍 Menu Filter")
        st.sidebar.info("Gunakan filter di bawah untuk menyaring data pada tabel.")

        # Identifikasi kolom secara otomatis berdasarkan urutan/nama
        # Kolom B (Index 1) biasanya Kantah, Kolom C (Index 2) Nama PPAT, Kolom D (Index 3) Status
        col_kantah = df.columns[1]
        col_ppat = df.columns[2]
        col_status = df.columns[3] if len(df.columns) > 3 else None

        # 1. Filter Kantor Pertanahan
        list_kantah = sorted(df[col_kantah].dropna().unique().tolist())
        pilih_kantah = st.sidebar.multiselect("Pilih Kantor Pertanahan:", list_kantah, default=[])

        # 2. Filter Nama PPAT (Dinamis berdasarkan Kantah yang dipilih)
        if pilih_kantah:
            df_temp = df[df[col_kantah].isin(pilih_kantah)]
        else:
            df_temp = df
            
        list_ppat = sorted(df_temp[col_ppat].dropna().unique().tolist())
        pilih_ppat = st.sidebar.multiselect("Pilih Nama PPAT:", list_ppat, default=[])

        # 3. Filter Status (Jika ada kolomnya)
        if col_status:
            list_status = sorted(df[col_status].dropna().unique().tolist())
            pilih_status = st.sidebar.multiselect("Pilih Status Pelaporan:", list_status, default=[])

        # --- LOGIKA PENYARINGAN DATA ---
        df_filtered = df.copy()

        if pilih_kantah:
            df_filtered = df_filtered[df_filtered[col_kantah].isin(pilih_kantah)]
        
        if pilih_ppat:
            df_filtered = df_filtered[df_filtered[col_ppat].isin(pilih_ppat)]
            
        if col_status and pilih_status:
            df_filtered = df_filtered[df_filtered[col_status].isin(pilih_status)]

        # --- TAMPILAN RINGKASAN ---
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Total Baris Ditemukan", f"{len(df_filtered)}")
        with c2:
            st.metric("Jumlah PPAT Terfilter", f"{df_filtered[col_ppat].nunique()}")
        with c3:
            st.metric("Wilayah Terfilter", f"{df_filtered[col_kantah].nunique()}")

        # --- TABEL UTAMA ---
        st.markdown("### 📑 Tabel Detail Data")
        st.write("Data di bawah ini berubah otomatis mengikuti filter di samping kiri.")
        
        st.dataframe(
            df_filtered, 
            use_container_width=True, 
            height=650,
            hide_index=True
        )

        # Tombol Download
        st.markdown("---")
        csv = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Hasil Filter (CSV)",
            data=csv,
            file_name='data_ppat_terfilter.csv',
            mime='text/csv',
        )

except Exception as e:
    st.error(f"Sistem gagal membaca data: {e}")
    st.info("Pastikan link Google Sheets sudah di-share publik (Anyone with the link can view).")
