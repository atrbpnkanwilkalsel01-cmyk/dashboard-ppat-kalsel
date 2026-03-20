import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard PPAT Kalsel", layout="wide")

# Link Google Sheets
SHEET_URL = "https://docs.google.com/spreadsheets/d/1QPeMTsbhho_YNS8nEq4gtz3WHk925Zb_gtYXpUvXkH0/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    # Membaca data dan membersihkan spasi di nama kolom
    df = pd.read_csv(SHEET_URL)
    df.columns = df.columns.str.strip() 
    return df

try:
    df = load_data()

    st.title("📊 Dashboard Pelaporan PPAT Kalsel")
    
    # Mencari nama kolom secara fleksibel agar tidak error lagi
    col_kantah = [c for c in df.columns if 'Kantor Pertanahan' in c][0]
    col_bulan = [c for c in df.columns if 'Bulan' in c][0]
    # Mencari kolom PPAT (biasanya yang ada kata 'Nama' atau 'Kotabaru')
    col_ppat_list = [c for c in df.columns if 'Kantah' in c or 'Nama' in c]
    col_ppat = col_ppat_list[0] if col_ppat_list else df.columns[2]

    # Ringkasan Singkat
    st.success(f"Berhasil memuat {len(df)} data pelaporan.")

    # --- GRAFIK 1: PER WILAYAH ---
    st.subheader("🏢 Laporan per Kantor Pertanahan")
    data_kantah = df[col_kantah].value_counts().reset_index()
    fig1 = px.bar(data_kantah, x=col_kantah, y='count', color='count',
                  labels={'count':'Jumlah', col_kantah:'Wilayah'})
    st.plotly_chart(fig1, use_container_width=True)

    col_left, col_right = st.columns(2)

    with col_left:
        # --- GRAFIK 2: PER BULAN ---
        st.subheader("📅 Distribusi per Bulan")
        data_bulan = df[col_bulan].value_counts().reset_index()
        fig2 = px.pie(data_bulan, names=col_bulan, values='count', hole=0.3)
        st.plotly_chart(fig2, use_container_width=True)

    with col_right:
        # --- GRAFIK 3: TOP PPAT ---
        st.subheader("👤 Top 10 PPAT (Pelaporan Terbanyak)")
        data_ppat = df[col_ppat].value_counts().head(10).reset_index()
        fig3 = px.bar(data_ppat, x='count', y=col_ppat, orientation='h', 
                      color_discrete_sequence=['#00CC96'])
        st.plotly_chart(fig3, use_container_width=True)

    # Menampilkan Tabel
    with st.expander("Lihat Tabel Data Lengkap"):
        st.dataframe(df)

except Exception as e:
    st.error("Terjadi kendala pembacaan kolom.")
    st.info("Pastikan nama kolom di Google Sheets tidak diubah-ubah.")
    # Menampilkan nama kolom yang terdeteksi untuk memudahkan pengecekan
    if 'df' in locals():
        st.write("Kolom yang ditemukan di Sheets Anda:", list(df.columns))
