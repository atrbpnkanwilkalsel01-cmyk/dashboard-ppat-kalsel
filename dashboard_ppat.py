import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard PPAT Kalsel", layout="wide")

# Link Google Sheets
SHEET_URL = "https://docs.google.com/spreadsheets/d/1QPeMTsbhho_YNS8nEq4gtz3WHk925Zb_gtYXpUvXkH0/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(SHEET_URL)
    df.columns = df.columns.str.strip() # Menghapus spasi gaib di nama kolom
    # Memastikan semua kolom utama adalah string agar tidak error
    for col in df.columns:
        df[col] = df[col].astype(str)
    return df

try:
    df = load_data()

    # Identifikasi Kolom secara otomatis
    col_kantah = [c for c in df.columns if 'Kantor Pertanahan' in c][0]
    col_bulan = [c for c in df.columns if 'Bulan' in c][0]
    col_ppat_list = [c for c in df.columns if 'Kantah' in c or 'Nama' in c]
    col_ppat = col_ppat_list[0] if col_ppat_list else df.columns[2]

    st.title("📊 Dashboard Pelaporan PPAT Kalsel")
    
    # --- FITUR FILTER KANTAH ---
    st.sidebar.header("Pilih Wilayah")
    opsi_kantah = ["Semua Kantah"] + sorted(df[col_kantah].unique().tolist())
    pilihan_kantah = st.sidebar.selectbox("Lihat Laporan PPAT per Kantah:", opsi_kantah)

    # Filter Data berdasarkan pilihan
    if pilihan_kantah != "Semua Kantah":
        df_display = df[df[col_kantah] == pilihan_kantah]
        st.subheader(f"📍 Menampilkan Laporan PPAT di: {pilihan_kantah}")
    else:
        df_display = df
        st.subheader("📍 Menampilkan Laporan Seluruh Wilayah")

    # Ringkasan Angka
    st.info(f"Ditemukan {len(df_display)} laporan pelaporan.")

    # --- GRAFIK 1: DAFTAR PPAT DI KANTAH TERSEBUT ---
    st.markdown(f"### 👤 Daftar PPAT yang Melapor")
    # Menghitung berapa kali tiap PPAT melapor di wilayah/filter tersebut
    data_ppat = df_display[col_ppat].value_counts().reset_index()
    
    fig_ppat = px.bar(data_ppat, x='count', y=col_ppat, orientation='h', 
                      color='count', color_continuous_scale='Reds',
                      labels={'count':'Jumlah Laporan', col_ppat:'Nama PPAT'},
                      title=f"Aktivitas PPAT di {pilihan_kantah}")
    st.plotly_chart(fig_ppat, use_container_width=True)

    col_left, col_right = st.columns(2)

    with col_left:
        # --- GRAFIK 2: PER BULAN ---
        st.subheader("📅 Distribusi per Bulan")
        data_bulan = df_display[col_bulan].value_counts().reset_index()
        fig_bulan = px.pie(data_bulan, names=col_bulan, values='count', hole=0.3)
        st.plotly_chart(fig_bulan, use_container_width=True)

    with col_right:
        # --- GRAFIK 3: PERBANDINGAN WILAYAH ---
        st.subheader("🏢 Sebaran Wilayah")
        data_wilayah = df_display[col_kantah].value_counts().reset_index()
        fig_wilayah = px.bar(data_wilayah, x=col_kantah, y='count', color_discrete_sequence=['#3498db'])
        st.plotly_chart(fig_wilayah, use_container_width=True)

    # Menampilkan Tabel Detail
    with st.expander("Klik untuk lihat detail Nama PPAT dan Tanggal Laporan"):
        # Menampilkan kolom yang paling penting saja agar rapi
        st.dataframe(df_display[[col_kantah, col_ppat, col_bulan, 'Timestamp']], use_container_width
