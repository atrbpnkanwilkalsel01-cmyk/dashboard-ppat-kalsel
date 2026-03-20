import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Judul & Konfigurasi Halaman
st.set_page_config(page_title="Dashboard PPAT Kalsel", layout="wide")
st.title("📊 Monitoring Pelaporan PPAT (Data Lengkap)")

# 2. Link Google Sheets (Format CSV)
URL = "https://docs.google.com/spreadsheets/d/1OfPHzg74p-WKeC0WzwT931cLdVEW20mbggv-2W8X7Gw/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    # Load data sebagai string agar aman dari error tipe data
    df = pd.read_csv(URL, dtype=str)
    # Bersihkan spasi di nama kolom
    df.columns = [str(c).strip() for c in df.columns]
    return df

try:
    df = load_data()
    
    # Deteksi kolom secara dinamis
    c_kantah = [c for c in df.columns if 'Kantor' in c or 'Kantah' in c][0]
    c_ppat = [c for c in df.columns if 'Nama' in c and 'PPAT' in c][0]

    # --- SIDEBAR FILTER ---
    st.sidebar.header("Filter Wilayah")
    list_kantah = sorted(df[c_kantah].dropna().unique().tolist())
    pilih = st.sidebar.selectbox("Pilih Kantor Pertanahan:", ["Semua"] + list_kantah)

    # Filter Data
    df_f = df[df[c_kantah] == pilih] if pilih != "Semua" else df

    # --- RINGKASAN ---
    st.metric("Total Laporan Masuk", len(df_f))
    st.markdown("---")

    # --- GRAFIK SEMUA NAMA PPAT ---
    st.subheader(f"📈 Grafik Aktivitas PPAT ({pilih})")
    
    # Hitung jumlah laporan per nama
    counts = df_f[c_ppat].value_counts().reset_index()
    counts.columns = ['Nama PPAT', 'Jumlah']
    
    # Trik agar SEMUA nama muncul: Tinggi grafik dibuat dinamis
    # Setiap 1 nama PPAT diberi ruang 30 pixel
    tinggi_dinamis = max(500, len(counts) * 30)

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
        height=tinggi_dinamis, 
        yaxis={'categoryorder':'total ascending'},
        xaxis_title="Total Laporan",
        yaxis_title=""
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # --- TABEL DATA LENGKAP (SEMUA KOLOM) ---
    st.markdown("---")
    st.subheader("📑 Tabel Data Lengkap (Semua Kolom)")
    st.write("Menampilkan semua detail dari Google Sheets:")
    st.dataframe(df_f, use_container_width=True)

    # Tombol Download
    csv = df_f.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Data CSV", data=csv, file_name='data_ppat.csv', mime='text/csv')

except Exception as e:
    st.error(f"Terjadi kesalahan teknis: {e}")
