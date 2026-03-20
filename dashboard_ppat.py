import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard PPAT Kalsel", layout="wide")

# Link Google Sheets
SHEET_URL = "https://docs.google.com/spreadsheets/d/1QPeMTsbhho_YNS8nEq4gtz3WHk925Zb_gtYXpUvXkH0/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(SHEET_URL)
    df.columns = df.columns.str.strip() # Bersihkan spasi di nama kolom
    # Pastikan semua kolom menjadi teks agar tidak error
    for col in df.columns:
        df[col] = df[col].astype(str)
    return df

try:
    df = load_data()

    # Identifikasi Kolom Otomatis
    col_kantah = [c for c in df.columns if 'Kantor Pertanahan' in c][0]
    col_ppat = [c for c in df.columns if 'Kantah' in c or 'Nama' in c][0]
    col_bulan = [c for c in df.columns if 'Bulan' in c][0]

    st.title("📊 Monitoring Pelaporan PPAT Per Wilayah")
    st.divider()

    # --- FITUR FILTER DI SIDEBAR ---
    st.sidebar.header("Pilihan Wilayah")
    list_kantah = sorted(df[col_kantah].unique().tolist())
    pilihan_kantah = st.sidebar.selectbox("Pilih Kantor Pertanahan:", ["Semua Wilayah"] + list_kantah)

    # Logika Filter
    if pilihan_kantah != "Semua Wilayah":
        df_filtered = df[df[col_kantah] == pilihan_kantah]
        st.subheader(f"📍 Daftar PPAT yang Melapor di {pilihan_kantah}")
    else:
        df_filtered = df
        st.subheader("📍 Daftar PPAT yang Melapor (Seluruh Wilayah)")

    # --- RINGKASAN ---
    col_stat1, col_stat2 = st.columns(2)
    col_stat1.metric("Total Laporan", len(df_filtered))
    col_stat2.metric("Jumlah PPAT Unik", df_filtered[col_ppat].nunique())

    # --- GRAFIK UTAMA: PPAT MANA SAJA YANG MELAPOR ---
    # Menghitung laporan per PPAT berdasarkan filter wilayah
    df_ppat_count = df_filtered[col_ppat].value_counts().reset_index()
    df_ppat_count.columns = [col_ppat, 'Jumlah Laporan']

    fig_ppat = px.bar(
        df_ppat_count, 
        x='Jumlah Laporan', 
        y=col_ppat, 
        orientation='h',
        color='Jumlah Laporan',
        color_continuous_scale='Viridis',
        title=f"Aktivitas PPAT di {pilihan_kantah}"
    )
    fig_ppat.update_layout(yaxis={'categoryorder':'total ascending'}) # Urutkan dari yang terbanyak
    st.plotly_chart(fig_ppat, use_container_width=True)

    # --- GRAFIK TAMBAHAN: TREN BULANAN DI WILAYAH TERSEBUT ---
    st.markdown("### 📅 Tren Waktu Pelaporan")
    df_bulan_count = df_filtered[col_
