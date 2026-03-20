import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard PPAT Kalsel", layout="wide")

# Link Google Sheets Baru (Format CSV Export)import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard PPAT Kalsel", layout="wide")

# Link Google Sheets Baru (Format CSV Export)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1OfPHzg74p-WKeC0WzwT931cLdVEW20mbggv-2W8X7Gw/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(SHEET_URL)
    df.columns = df.columns.str.strip() # Menghapus spasi gaib di nama kolom
    # Memastikan semua data dibaca sebagai teks agar tidak error tipe data
    for col in df.columns:
        df[col] = df[col].astype(str)
    return df

try:
    df = load_data()

    # --- IDENTIFIKASI KOLOM OTOMATIS BERDASARKAN SHEET BARU ---
    # Mencari kolom Kantor Pertanahan
    col_kantah = [c for c in df.columns if 'Kantor Pertanahan' in c][0]
    # Mencari kolom Nama PPAT
    col_ppat = [c for c in df.columns if 'Nama' in c and 'PPAT' in c][0]

    st.title("📊 Monitoring Aktivitas PPAT Kalsel")
    st.markdown(f"**Sumber Data:** Pelaporan Bulanan PPAT")
    st.divider()

    # --- FITUR FILTER DI SIDEBAR ---
    st.sidebar.header("Filter Wilayah")
    list_kantah = sorted(df[col_kantah].unique().tolist())
    pilihan_kantah = st.sidebar.selectbox("Pilih Kantor Pertanahan:", ["Semua Wilayah"] + list_kantah)

    # Logika Penyaringan Data
    if pilihan_kantah != "Semua Wilayah":
        df_filtered = df[df[col_kantah] == pilihan_kantah]
        st.subheader(f"📍 Daftar Aktivitas PPAT di {pilihan_kantah}")
    else:
        df_filtered = df
        st.subheader("📍 Daftar Aktivitas PPAT (Seluruh Wilayah)")

    # --- RINGKASAN DATA ---
    col_1, col_2 = st.columns(2)
    with col_1:
        st.metric("Total Laporan Masuk", len(df_filtered))
    with col_2:
        st.metric("Jumlah PPAT Terdaftar", df_filtered[col_ppat].nunique())

    # --- GRAFIK UTAMA: NAMA PPAT (FOKUS UTAMA) ---
    # Menghitung jumlah laporan per Nama PPAT
    df_ppat_count = df_filtered[col_ppat].value_counts().reset_index()
    df_ppat_count.columns = [col_ppat, 'Jumlah Laporan']

    # Membuat Grafik Batang Horizontal
    fig_ppat = px.bar(
        df_ppat_count, 
        x='Jumlah Laporan', 
        y=col_ppat, 
        orientation='h',
        color='Jumlah Laporan',
        color_continuous_scale='Reds', # Ubah warna agar lebih jelas
        text='Jumlah Laporan',
        title=f"Statistik Pelaporan per Nama PPAT ({pilihan_kantah})"
    )

    # Pengaturan tampilan agar nama tidak terpotong
    fig_ppat.update_traces(textposition='outside')
    
    # Menghitung tinggi grafik dinamis berdasarkan jumlah nama PPAT
    tinggi_grafik = max(400, len(df_ppat_count) * 35)
    
    # --- BAGIAN INI SUDAH DIPERBAIKI (KURUNG SUDAH DITUTUP) ---
    fig_ppat.update_layout(
        yaxis={'categoryorder':'total ascending'},
        height=tinggi_grafik, # Diperbaiki: Tidak ada lagi SyntaxError di sini
        margin=dict(l=200) # Memberi ruang lebih untuk nama PPAT yang panjang
    )
    # --------------------------------------------------------

    st.plotly_chart(fig_ppat, use_container_width=True)

    # --- TABEL DETAIL ---
    st.markdown("---")
    with st.expander("Klik untuk lihat detail tabel data lengkap"):
        # Menampilkan kolom Nama PPAT, Kantah, dan Waktu saja agar rapi
        st.dataframe(df_filtered[[col_ppat, col_kantah, 'Timestamp']], use_container_width=True)

except Exception as e:
    st.error("Terjadi kendala pembacaan data.")
    st.info("Pastikan kolom 'Kantor Pertanahan' dan 'Nama PPAT' ada di Google Sheets Anda.")
    if 'df' in locals():
        st.write("Nama kolom yang ditemukan:", list(df.columns))
SHEET_URL = "https://docs.google.com/spreadsheets/d/1OfPHzg74p-WKeC0WzwT931cLdVEW20mbggv-2W8X7Gw/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    # Membaca data
    df = pd.read_csv(SHEET_URL)
    # Membersihkan nama kolom dari spasi tambahan
    df.columns = df.columns.str.strip()
    # Memastikan semua data terbaca sebagai teks (mencegah error tipe data)
    for col in df.columns:
        df[col] = df[col].astype(str)
    return df

try:
    df = load_data()

    # --- IDENTIFIKASI KOLOM BERDASARKAN SHEET BARU ---
    # Mencari kolom Kantor Pertanahan
    col_kantah = [c for c in df.columns if 'Kantor Pertanahan' in c][0]
    # Mencari kolom Nama PPAT (berdasarkan sheet baru biasanya kolom 'Nama PPAT')
    col_ppat = [c for c in df.columns if 'Nama' in c and 'PPAT' in c][0]

    st.title("📊 Monitoring Pelaporan PPAT")
    st.markdown(f"**Sumber Data:** Pelaporan Bulanan PPAT")
    st.divider()

    # --- SIDEBAR FILTER ---
    st.sidebar.header("Filter Wilayah")
    list_kantah = sorted(df[col_kantah].unique().tolist())
    pilihan_kantah = st.sidebar.selectbox("Pilih Kantor Pertanahan:", ["Semua Wilayah"] + list_kantah)

    # Logika Penyaringan Data
    if pilihan_kantah != "Semua Wilayah":
        df_filtered = df[df[col_kantah] == pilihan_kantah]
        st.subheader(f"📍 Daftar Aktivitas PPAT di {pilihan_kantah}")
    else:
        df_filtered = df
        st.subheader("📍 Daftar Aktivitas PPAT (Seluruh Wilayah)")

    # --- RINGKASAN DATA ---
    col_1, col_2 = st.columns(2)
    with col_1:
        st.metric("Total Laporan Masuk", len(df_filtered))
    with col_2:
        st.metric("Jumlah PPAT Terdaftar", df_filtered[col_ppat].nunique())

    # --- GRAFIK UTAMA: NAMA PPAT ---
    # Menghitung jumlah laporan per Nama PPAT
    df_ppat_count = df_filtered[col_ppat].value_counts().reset_index()
    df_ppat_count.columns = [col_ppat, 'Jumlah Laporan']

    # Membuat Grafik Batang Horizontal
    fig_ppat = px.bar(
        df_ppat_count, 
        x='Jumlah Laporan', 
        y=col_ppat, 
        orientation='h',
        color='Jumlah Laporan',
        color_continuous_scale='Blues',
        text='Jumlah Laporan',
        title=f"Statistik Pelaporan per Nama PPAT ({pilihan_kantah})"
    )

    # Pengaturan tampilan agar nama tidak terpotong
    fig_ppat.update_traces(textposition='outside')
    
    # Menghitung tinggi grafik secara dinamis berdasarkan jumlah nama PPAT
    tinggi_grafik = max(400, len(df_ppat_count) * 35)
