import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi
st.set_page_config(page_title="Dashboard PPAT Lengkap", layout="wide")

# 2. Link Data
URL = "https://docs.google.com/spreadsheets/d/1OfPHzg74p-WKeC0WzwT931cLdVEW20mbggv-2W8X7Gw/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(URL, dtype=str)
    df.columns = [str(c).strip() for c in df.columns]
    return df

try:
    df = load_data()
    st.title("📊 Monitoring Pelaporan PPAT (Semua Kolom)")

    # Cari kolom otomatis
    cols_kantah = [c for c in df.columns if 'Kantor' in c or 'Kantah' in c]
    cols_ppat = [c for c in df.columns if 'Nama' in c]
    
    ck = cols_kantah[0] if cols_kantah else df.columns[1]
    cp = cols_ppat[0] if cols_ppat else df.columns[2]

    # Sidebar
    list_kantah = sorted(df[ck].dropna().unique().tolist())
    pilih = st.sidebar.selectbox("Filter Wilayah:", ["Semua"] + list_kantah)
    df_f = df[df[ck] == pilih] if pilih != "Semua" else df

    # --- TAMPILAN GRAFIK ---
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("Grafik Per Nama PPAT")
        c_ppat = df_f[cp].value_counts().reset_index()
        c_ppat.columns = ['Nama', 'Total']
        fig1 = px.bar(c_ppat.head(20), x='Total', y='Nama', orientation='h', text='Total', color='Total')
        fig1.update_layout(yaxis={'categoryorder':'total ascending'}, height=500)
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        st.subheader("Grafik Per Wilayah")
        c_wil = df[ck].value_counts().reset_index()
        c_wil.columns = ['Wilayah', 'Total']
        fig2 = px.pie(c_wil, values='Total', names='Wilayah', hole=0.4)
        st.plotly_chart(fig2, use_container_width=True)

    # --- TAMPILAN SEMUA DATA ---
    st.markdown("---")
    st.subheader("📑 Tabel Data Lengkap (Semua Kolom)")
    st.dataframe(df_f, use_container_width=True)

except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
