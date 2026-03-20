import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Halaman Dasar
st.set_page_config(page_title="Dashboard Lengkap PPAT Kalsel", layout="wide")

# 2. Link Google Sheets (Format CSV Export)
URL_SHEET = "https://docs.google.com/spreadsheets/d/1OfPHzg74p-WKeC0WzwT931cLdVEW20mbggv-2W8X7Gw/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    # Membaca semua kolom tanpa kecuali
    df = pd.read_csv(URL_SHEET)
    # Membersihkan spasi di nama kolom
    df.columns = [str(c).strip() for c in df.columns]
    return df

try:
    df = load_data()
    
    st.title("📊 Monitoring Pelaporan PPAT (Data Lengkap)")
    st.markdown("---")

    # --- BAGIAN FILTER DINAMIS ---
    # Mencari kolom Kantor Pertanahan secara otomatis untuk filter
    col_kantah = [c for c in df.columns if 'Kantor' in c or 'Kantah' in c]
    
    if col_kantah:
        ck = col_kantah[0]
        list_kantah = sorted(df[ck].dropna().unique().tolist())
        pilih = st.sidebar.selectbox("Pilih Wilayah (Filter):", ["Semua Wilayah"] + list_kantah)
        
        if pilih != "Semua Wilayah":
            df_display = df[df[ck] == pilih]
        else:
            df_display = df
    else:
        df_display = df
        st.warning("Kolom wilayah tidak ditemukan, menampilkan semua data.")

    # --- RINGKASAN DATA ---
    st.subheader("📌 Ringkasan")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Laporan", len(df_display))
    
    # Cari kolom Nama PPAT untuk hitung jumlah orang
    col_ppat = [c for c in df.columns if 'Nama' in c and 'PPAT' in c]
    if col_ppat:
        c2.metric("Jumlah PPAT Melapor", df_display[col_ppat[0]].nunique())
    
    c3.info("Data diperbarui setiap 60 detik")

    # --- GRAFIK AKTIVITAS ---
    if col_ppat:
        st.subheader("📈 Grafik Aktivitas PPAT")
        cp = col_ppat[0]
        counts = df_display[cp].value_counts().reset_index()
        counts.columns = ['Nama PPAT', 'Jumlah']
        
        fig = px.bar(counts, x='Jumlah', y='Nama PPAT', orientation='h', 
                     text='Jumlah', color='Jumlah', color_continuous_scale='Viridis')
        fig.update_layout(height=max(400, len(counts)*25), yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

    # --- TAMPILKAN SEMUA KOLOM (TABEL LENGKAP) ---
    st.markdown("---")
    st.subheader("📑 Tabel Data Lengkap (Semua Kolom)")
    st.write("Gunakan fitur *search* di tabel bawah ini untuk mencari data spesifik.")
    
    # Menampilkan seluruh dataframe (semua kolom dari sheet)
    st.dataframe(df_display, use_container_width=True)

    # Fitur Download Data
    csv = df_display.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Data ke Excel/CSV",
        data=csv,
        file_name='data_lengkap_ppat.csv',
        mime='text/csv',
    )

except Exception as e:
    st.error(f"Terjadi Kendala: {e}")
    st.info("Pastikan link Google Sheets dapat diakses publik (Anyone with the link).")
