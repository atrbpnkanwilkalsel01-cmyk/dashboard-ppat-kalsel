import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard PPAT Kalsel", layout="wide")

# Link Google Sheets
SHEET_URL = "https://docs.google.com/spreadsheets/d/1QPeMTsbhho_YNS8nEq4gtz3WHk925Zb_gtYXpUvXkH0/export?format=csv"

@st.cache_data(ttl=600) # Data akan refresh setiap 10 menit
def load_data():
    df = pd.read_csv(SHEET_URL)
    # Menghapus baris yang benar-benar kosong jika ada
    df = df.dropna(subset=['Bulan', 'Kantor Pertanahan (Wilayah kerja)'])
    # Memastikan semua data di kolom kunci berupa teks agar tidak error 'float vs str'
    df['Bulan'] = df['Bulan'].astype(str)
    df['Kantor Pertanahan (Wilayah kerja)'] = df['Kantor Pertanahan (Wilayah kerja)'].astype(str)
    df['Kantah Kotabaru'] = df['Kantah Kotabaru'].astype(str)
    return df

try:
    df = load_data()

    st.title("📊 Analisis Pelaporan PPAT - Kanwil Kalsel")
    st.info(f"Total Laporan Terdata: {len(df)} entri")

    # 1. GRAFIK PER KANTAH (Wilayah Kerja)
    st.subheader("🏢 Jumlah Laporan per Kantor Pertanahan")
    df_kantah = df['Kantor Pertanahan (Wilayah kerja)'].value_counts().reset_index()
    fig_kantah = px.bar(df_kantah, x='count', y='Kantor Pertanahan (Wilayah kerja)', 
                        orientation='h', color='count', color_continuous_scale='Blues',
                        labels={'count':'Jumlah Laporan', 'Kantor Pertanahan (Wilayah kerja)':'Kantah'})
    st.plotly_chart(fig_kantah, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        # 2. GRAFIK PER BULAN
        st.subheader("📅 Laporan per Bulan")
        df_bulan = df['Bulan'].value_counts().reset_index()
        fig_bulan = px.pie(df_bulan, values='count', names='Bulan', hole=0.4)
        st.plotly_chart(fig_bulan, use_container_width=True)

    with col2:
        # 3. GRAFIK PER PPAT (Top 10)
        st.subheader("👤 Top 10 PPAT Teraktif")
        df_ppat = df['Kantah Kotabaru'].value_counts().head(10).reset_index()
        fig_ppat = px.bar(df_ppat, x='count', y='Kantah Kotabaru', orientation='h',
                          color_discrete_sequence=['#FF4B4B'])
        st.plotly_chart(fig_ppat, use_container_width=True)

    # Tabel Data Mentah
    with st.expander("Klik untuk lihat detail tabel data"):
        st.write(df)

except Exception as e:
    st.error(f"Data sedang diproses atau ada kolom yang tidak sesuai. Error: {e}")
