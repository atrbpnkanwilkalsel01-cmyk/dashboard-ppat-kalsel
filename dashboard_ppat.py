import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Judul dan Layout
st.set_page_config(page_title="Monitoring PPAT Kalsel", layout="wide")

# 2. Link Data (Google Sheets CSV Export)
URL_SHEET = "https://docs.google.com/spreadsheets/d/1OfPHzg74p-WKeC0WzwT931cLdVEW20mbggv-2W8X7Gw/export?format=csv"

@st.cache_data(ttl=60)
def ambil_data():
    df = pd.read_csv(URL_SHEET)
    # Bersihkan nama kolom dari spasi gaib
    df.columns = df.columns.str.strip()
    return df

# 3. Proses Tampilan
try:
    data = ambil_data()
    
    # Deteksi kolom secara otomatis berdasarkan kata kunci
    kolom_kantah = [c for c in data.columns if 'Kantor Pertanahan' in c][0]
    kolom_ppat = [c for c in data.columns if 'Nama' in c and 'PPAT' in c][0]

    st.title("📊 Monitoring Pelaporan PPAT")
    st.markdown("---")

    # Sidebar untuk Filter
    st.sidebar.header("Filter Wilayah")
    pilihan_kantah = st.sidebar.selectbox(
        "Pilih Kantor Pertanahan:", 
        ["Semua Wilayah"] + sorted(data[kolom_kantah].unique().tolist())
    )

    # Logika Filter Data
    if pilihan_kantah != "Semua Wilayah":
        df_final = data[data[kolom_kantah] == pilihan_kantah]
    else:
        df_final = data

    # Tampilan Statistik Singkat
    c1, c2 = st.columns(2)
    c1.metric("Total Laporan Masuk", len(df_final))
    c2.metric("Jumlah PPAT Melapor", df_final[kolom_ppat].nunique())

    # Grafik Nama-Nama PPAT
    st.subheader(f"Daftar Aktivitas PPAT: {pilihan_kantah}")
    
    # Hitung jumlah laporan per PPAT
    hitung_ppat = df_final[kolom_ppat].value_counts().reset_index()
    hitung_ppat.columns = ['Nama PPAT', 'Jumlah']
    
    # Buat Grafik Batang
    fig = px.bar(
        hitung_ppat, 
        x='Jumlah', 
        y='Nama PPAT', 
        orientation='h',
        text='Jumlah',
        color='Jumlah',
        color_continuous_scale='Blues'
    )
    
    # Atur tinggi grafik agar tidak bertumpuk
    fig.update_layout(
        yaxis={'categoryorder':'total ascending'}, 
        height=max(400, len(hitung_ppat) * 30),
        margin=dict(l=200)
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # Tabel Detail (Opsional di bagian bawah)
    with st.expander("Lihat Detail Tabel"):
        st.dataframe(df_final[[kolom_kantah, kolom_ppat, 'Timestamp']], use_container_width=True)

except Exception as e:
    st.error("Gagal memuat data. Periksa apakah kolom 'Kantor Pertanahan' dan 'Nama PPAT' sudah benar di Google Sheets.")
