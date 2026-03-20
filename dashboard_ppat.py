import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Dashboard PPAT Kalsel", layout="wide")

# 2. Link Google Sheets (Format CSV)
URL = "https://docs.google.com/spreadsheets/d/1OfPHzg74p-WKeC0WzwT931cLdVEW20mbggv-2W8X7Gw/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(URL)
    df.columns = [str(c).strip() for c in df.columns]
    # Konversi tanggal agar grafik tren muncul
    col_time = [c for c in df.columns if 'Timestamp' in c or 'Waktu' in c]
    if col_time:
        df['TGL_BERSIH'] = pd.to_datetime(df[col_time[0]], errors='coerce')
    return df

try:
    df = load_data()
    st.title("📊 Monitoring Pelaporan PPAT")
    st.markdown("---")

    # Deteksi Kolom
    c_kantah = [c for c in df.columns if 'Kantor' in c or 'Kantah' in c][0]
    c_ppat = [c for c in df.columns if 'Nama' in c and 'PPAT' in c][0]

    # Sidebar Filter
    list_kantah = sorted(df[c_kantah].dropna().unique().tolist())
    pilih = st.sidebar.selectbox("Pilih Wilayah:", ["Semua"] + list_kantah)
    df_f = df[df[c_kantah] == pilih] if pilih != "Semua" else df

    # Ringkasan Angka
    st.metric("Total Laporan", len(df_f))

    # --- BAGIAN GRAFIK ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Aktivitas per PPAT")
        counts = df_f[c_ppat].value_counts().reset_index()
        counts.columns = ['PPAT', 'Jumlah']
        fig1 = px.bar(counts.head(20), x='Jumlah', y='PPAT', orientation='h', text='Jumlah', color='Jumlah', color_continuous_scale='Blues')
        fig1.update_layout(height=500, yaxis={'categoryorder':'total ascending'}, yaxis_title="")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        if pilih == "Semua":
            st.subheader("Distribusi per Wilayah")
            dist = df[c_kantah].value_counts().reset_index()
            dist.columns = ['Kantah', 'Total']
            fig2 = px.pie(dist, values='Total', names='Kantah', hole=0.4)
            st.plotly_chart(fig2, use_container_width=True)
        else:
            # Jika filter aktif, tampilkan grafik tren di kolom kedua
            if 'TGL_BERSIH' in df_f.columns:
                st.subheader("Tren Pelaporan")
                tren = df_f.groupby(df_f['TGL_BERSIH'].dt.date).size().reset_index()
                tren.columns = ['Tanggal', 'Jumlah']
                fig3 = px.line(tren, x='Tanggal', y='Jumlah', markers=True)
                st.plotly_chart(fig3, use_container_width=True)

    # --- TABEL DATA LENGKAP ---
    st.markdown("---")
    st.subheader("📑 Tabel Data Lengkap (Semua Kolom)")
    st.dataframe(df_f, use_container_width=True)

except Exception as e:
    st.error(f"Terjadi kesalahan teknis: {e}")
