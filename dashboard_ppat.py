import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Setting Halaman
st.set_page_config(page_title="Dashboard PPAT Lengkap", layout="wide")

# 2. Link Google Sheets
URL = "https://docs.google.com/spreadsheets/d/1OfPHzg74p-WKeC0WzwT931cLdVEW20mbggv-2W8X7Gw/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(URL, dtype=str)
    df.columns = [str(c).strip() for c in df.columns]
    return df

try:
    df = load_data()
    st.title("📊 Monitoring Seluruh PPAT")

    # Identifikasi Kolom secara otomatis
    col_kantah = [c for c in df.columns if 'Kantor' in c or 'Kantah' in c][0]
    col_ppat = [c for c in df.columns if 'Nama' in c and 'PPAT' in c][0]

    # Sidebar Filter
    list_kantah = sorted(df[col_kantah].dropna().unique().tolist())
    pilih = st.sidebar.selectbox("Filter Wilayah:", ["Semua Wilayah"] + list_kantah)
    
    # Proses Data Filter
    df_f = df[df[col_kantah] == pilih] if pilih != "Semua Wilayah" else df

    # Hitung Statistik PPAT
    counts = df_f[col_ppat].value_counts().reset_index()
    counts.columns = ['Nama PPAT', 'Jumlah']
    
    # --- RAHASIA AGAR SEMUA NAMA TAMPIL ---
    # Kita hitung berapa jumlah PPAT unik. 
    # Lalu kita kalikan dengan 25 pixel per baris agar grafik memanjang ke bawah.
    jumlah_nama = len(counts)
    tinggi_grafik = max(500, jumlah_nama * 25) 

    st.metric("Total Laporan Terdeteksi", len(df_f))

    # Tampilkan Grafik
    st.subheader(f"Daftar Aktivitas Seluruh PPAT ({pilih})")
    
    if jumlah_nama > 0:
        fig = px.bar(
            counts, 
            x='Jumlah', 
            y='Nama PPAT', 
            orientation='h', 
            text='Jumlah',
            color='Jumlah',
            color_continuous_scale='Blues'
        )
        
        fig.update_layout(
            height=tinggi_grafik, # Mengikuti jumlah nama yang ada
            yaxis={'categoryorder':'total ascending'},
            margin=dict(l=200), # Memberi ruang agar nama panjang tidak terpotong
            xaxis_title="Jumlah Laporan",
            yaxis_title=""
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Tidak ada data untuk ditampilkan.")

    # --- TAMPILKAN SEMUA KOLOM & SHEET ---
    st.markdown("---")
    st.subheader("📑 Tabel Data Transaksi Lengkap")
    st.dataframe(df_f, use_container_width=True)

except Exception as e:
    st.error(f"Gagal memuat grafik: {e}")
