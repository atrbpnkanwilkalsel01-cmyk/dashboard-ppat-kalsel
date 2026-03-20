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
    df.columns = df.columns.str.strip()
    return df

# 3. Proses Tampilan
try:
    data = ambil_data()
    
    # Deteksi kolom (mencari kolom yang relevan secara otomatis)
    kol_kantah = [c for c in data.columns if 'Kantor Pertanahan' in c][0]
    kol_ppat = [c for c in data.columns if 'Nama' in c and 'PPAT' in c][0]

    st.title("📊 Monitoring Pelaporan")

    # Sidebar Filter
    pilihan_kantah = st.sidebar.selectbox(
        "Pilih Wilayah:", 
        ["Semua"] + sorted(data[kol_kantah].unique().tolist())
    )

    # Filter Data
    df_f = data[data[kol_kantah] == pilihan_kantah] if pilihan_kantah != "Semua" else data

    # Menampilkan total laporan saja (Nama PPAT & Kantah di judul dihapus)
    st.metric("Total Laporan", len(df_f))

    # Grafik Utama
    counts = df_f[kol_ppat].value_counts().reset_index()
    counts.columns = ['PPAT', 'Jumlah']
    
    fig = px.bar(
        counts, 
        x='Jumlah', 
        y='PPAT', 
        orientation='h',
        text='Jumlah',
        color_discrete_sequence=['#3498db']
    )
    
    fig.update_layout(
        yaxis={'categoryorder':'total ascending', 'title': ''}, # Judul sumbu Y dihapus
        xaxis={'title': 'Jumlah Laporan'},
        height=max(400, len(counts) * 30),
        margin=dict(l=200)
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # Tabel Detail (Hanya menampilkan Timestamp)
    with st.expander("Lihat Detail Waktu"):
        st.dataframe(df_f[['Timestamp']], use_container_width=True)
