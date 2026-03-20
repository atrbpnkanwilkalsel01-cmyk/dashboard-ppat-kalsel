import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard PPAT Kalsel", layout="wide")

# Link Google Sheets (Format CSV Export)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1QPeMTsbhho_YNS8nEq4gtz3WHk925Zb_gtYXpUvXkH0/export?format=csv"

@st.cache_data
def load_data():
    df = pd.read_csv(SHEET_URL)
    # Pastikan nama kolom sesuai dengan header di Google Sheets Anda
    # Berdasarkan link: 'Bulan', 'Kantor Pertanahan (Wilayah kerja)', 'Kantah Kotabaru' (Nama PPAT)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], dayfirst=True)
    return df

try:
    df = load_data()

    st.title("📊 Analisis Pelaporan PPAT - Kanwil Kalsel")

    # --- SIDEBAR FILTER ---
    st.sidebar.header("Filter Data")
    list_kantah = ["Semua"] + sorted(df['Kantor Pertanahan (Wilayah kerja)'].unique().tolist())
    selected_kantah = st.sidebar.selectbox("Pilih Kantah", list_kantah)

    if selected_kantah != "Semua":
        df_filtered = df[df['Kantor Pertanahan (Wilayah kerja)'] == selected_kantah]
    else:
        df_filtered = df

    # --- BAGIAN 1: GRAFIK TREN PER BULAN ---
    st.subheader("📈 Tren Pelaporan per Bulan")
    # Mengurutkan bulan agar tidak acak (Jan, Feb, Mar...)
    order_bulan = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 
                   'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
    
    df_bulan = df_filtered.groupby('Bulan').size().reindex(order_bulan).reset_index(name='Jumlah Laporan')
    fig_bulan = px.line(df_bulan, x='Bulan', y='Jumlah Laporan', markers=True, 
                        title="Jumlah Laporan Masuk Tiap Bulan",
                        line_shape="spline", color_discrete_sequence=['#3498db'])
    st.plotly_chart(fig_bulan, use_container_width=True)

    col1, col2 = st.columns(2)

    # --- BAGIAN 2: GRAFIK PER KANTAH ---
    with col1:
        st.subheader("🏢 Perbandingan antar Kantah")
        df_kantah = df_filtered['Kantor Pertanahan (Wilayah kerja)'].value_counts().reset_index()
        fig_kantah = px.bar(df_kantah, x='count', y='Kantor Pertanahan (Wilayah kerja)', 
                            orientation='h', title="Produktivitas per Wilayah Kerja",
                            labels={'count': 'Total Laporan', 'Kantor Pertanahan (Wilayah kerja)': 'Kantah'},
                            color='count', color_continuous_scale='Blues')
        st.plotly_chart(fig_kantah, use_container_width=True)

    # --- BAGIAN 3: GRAFIK PER PPAT ---
    with col2:
        st.subheader("👤 Top 10 PPAT Teraktif")
        # Menggunakan kolom 'Kantah Kotabaru' yang berisi Nama PPAT
        df_ppat = df_filtered['Kantah Kotabaru'].value_counts().head(10).reset_index()
        fig_ppat = px.bar(df_ppat, x='count', y='Kantah Kotabaru', 
                           orientation='h', title="10 PPAT dengan Laporan Terbanyak",
                           labels={'count': 'Jumlah Laporan', 'Kantah Kotabaru': 'Nama PPAT'},
                           color='count', color_continuous_scale='Reds')
        st.plotly_chart(fig_ppat, use_container_width=True)

    # --- TABEL DATA ---
    with st.expander("Lihat Data Mentah"):
        st.write(df_filtered)

except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
    st.info("Pastikan kolom 'Bulan', 'Kantor Pertanahan (Wilayah kerja)', dan 'Kantah Kotabaru' tersedia di Sheets Anda.")