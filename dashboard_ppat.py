import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Awal
st.set_page_config(page_title="Dashboard PPAT Kalsel", layout="wide")

# 2. Link Data (Mode CSV)
URL = "https://docs.google.com/spreadsheets/d/1OfPHzg74p-WKeC0WzwT931cLdVEW20mbggv-2W8X7Gw/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    # Load data dan bersihkan nama kolom
    df = pd.read_csv(URL, dtype=str)
    df.columns = [str(c).strip() for c in df.columns]
    return df

st.title("📊 Monitoring Pelaporan PPAT")

try:
    df = load_data()
    
    if df.empty:
        st.warning("Data di Google Sheets kosong atau tidak terbaca.")
    else:
        # --- DETEKSI KOLOM SECARA CERDAS (PENGGANTI INDEX) ---
        # Mencari kolom wilayah (Kantor Pertanahan)
        col_kantah = [c for c in df.columns if 'Kantor' in c or 'Kantah' in c]
        # Mencari kolom Nama PPAT
        col_ppat = [c for c in df.columns if 'Nama' in c]
        
        # Jika tidak ketemu, pakai kolom yang tersedia secara default
        ck = col_kantah[0] if col_kantah else df.columns[min(1, len(df.columns)-1)]
        cp = col_ppat[0] if col_ppat else df.columns[min(2, len(df.columns)-1)]

        # --- SIDEBAR & FILTER ---
        list_kantah = sorted(df[ck].dropna().unique().tolist())
        pilih = st.sidebar.selectbox("Filter Wilayah:", ["Semua"] + list_kantah)
        df_f = df[df[ck] == pilih] if pilih != "Semua" else df

        # --- TAMPILAN DASHBOARD ---
        st.metric("Total Laporan Masuk", len(df_f))

        # Grafik Batang (Tampilkan SEMUA Nama PPAT)
        st.subheader(f"📈 Grafik Aktivitas PPAT ({pilih})")
        counts = df_f[cp].value_counts().reset_index()
        counts.columns = ['Nama PPAT', 'Jumlah']
        counts['Jumlah'] = pd.to_numeric(counts['Jumlah'], errors='coerce').fillna(0)
        
        # Tinggi dinamis agar semua nama muncul (30 pixel per nama)
        tinggi_grafik = max(500, len(counts) * 30)
        
        fig = px.bar(counts, x='Jumlah', y='Nama PPAT', orientation='h', 
                     text='Jumlah', color='Jumlah', color_continuous_scale='Blues')
        fig.update_layout(height=tinggi_grafik, yaxis={'categoryorder':'total ascending'}, yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

        # --- TABEL DATA LENGKAP (Tampilkan Semua Kolom & Sheet) ---
        st.markdown("---")
        st.subheader("📑 Tabel Data Lengkap (Semua Kolom)")
        st.dataframe(df_f, use_container_width=True)

except Exception as e:
    st.error(f"Terjadi kesalahan teknis: {e}")
    st.info("Catatan: Pastikan link Google Sheets Anda sudah di-share 'Anyone with the link can view'.")
