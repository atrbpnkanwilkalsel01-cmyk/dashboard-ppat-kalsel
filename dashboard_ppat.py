import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Halaman Dasar
st.set_page_config(page_title="Dashboard Lengkap PPAT Kalsel", layout="wide")

# 2. Link Google Sheets (Format CSV Export)
# Pastikan link ini bisa diakses publik (Anyone with the link can view)
URL_SHEET = "https://docs.google.com/spreadsheets/d/1OfPHzg74p-WKeC0WzwT931cLdVEW20mbggv-2W8X7Gw/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    # Membaca data dan memastikan dibaca sebagai string untuk menghindari error tipe data
    df = pd.read_csv(URL_SHEET, dtype=str)
    
    # Membersihkan nama kolom dari spasi yang tidak terlihat
    df.columns = [str(c).strip() for c in df.columns]
    
    # --- PRE-PROCESSING DATA UNTUK GRAFIK WAKTU ---
    # Mencari kolom Timestamp secara otomatis
    col_time = [c for c in df.columns if 'Timestamp' in c or 'Waktu' in c]
    if col_time:
        # Ubah menjadi format tanggal Python, abaikan error jika ada data kotor
        df[col_time[0]] = pd.to_datetime(df[col_time[0]], errors='coerce')
        # Buat kolom baru hanya berisi Tanggal (tanpa jam)
        df['Tanggal_Lapor'] = df[col_time[0]].dt.date

    return df

try:
    df = load_data()
    
    st.title("📊 Monitoring Pelaporan PPAT Kalsel (Data Lengkap)")
    st.markdown("---")

    # --- BAGIAN FILTER DINAMIS (Sidebar) ---
    st.sidebar.header("Filter Data")
    
    # Mencari kolom Kantor Pertanahan secara otomatis untuk filter
    col_kantah = [c for c in df.columns if 'Kantor' in c or 'Kantah' in c]
    
    if col_kantah:
        ck = col_kantah[0]
        # Ambil daftar Kantah unik, hapus data kosong (NaN)
        list_kantah = sorted(df[ck].dropna().unique().tolist())
        pilih_kantah = st.sidebar.selectbox("Pilih Wilayah (Kantah):", ["Semua Wilayah"] + list_kantah)
        
        # Logika Filter
        if pilih_kantah != "Semua Wilayah":
            df_display = df[df[ck] == pilih_kantah]
        else:
            df_display = df
    else:
        df_display = df
        st.sidebar.warning("Kolom wilayah tidak ditemukan, menampilkan semua data.")

    # --- RINGKASAN DATA ---
    st.subheader("📌 Ringkasan")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Laporan Masuk", len(df_display))
    
    # Cari kolom Nama PPAT untuk hitung jumlah orang
    col_ppat = [c for c in df.columns if 'Nama' in c and 'PPAT' in c]
    if col_ppat:
        cp = col_ppat[0]
        c2.metric("Jumlah PPAT Melapor", df_display[cp].nunique())
    
    c3.info("Data diperbarui otomatis setiap 60 detik")
    st.markdown("---")

    # --- BAGIAN GRAFIK ---
    st.subheader("📈 Grafik Aktivitas")
    
    # Tampilan grafik hanya jika data tidak kosong
    if not df_display.empty:
        
        # Kolom 1: Grafik Aktivitas per PPAT (Bar Horizontal)
        col_grafik_1, col_grafik_2 = st.columns([2, 1])
        
        with col_grafik_1:
            if col_ppat:
                st.subheader("Pelaporan per Nama PPAT")
                cp = col_ppat[0]
                counts_ppat = df_display[cp].value_counts().reset_index()
                counts_ppat.columns = ['Nama PPAT', 'Jumlah']
                
                # Gunakan warna Blues agar seragam
                fig_ppat = px.bar(counts_ppat.head(30), x='Jumlah', y='Nama PPAT', 
                                orientation='h', text='Jumlah',
                                color='Jumlah', color_continuous_scale='Blues')
                
                # Atur agar nama tidak terpotong dan tinggi dinamis
                fig_ppat.update_layout(
                    height=max(500, len(counts_ppat.head(30)) * 25), 
                    yaxis={'categoryorder':'total ascending'},
                    xaxis_title="", yaxis_title=""
                )
                st.plotly_chart(fig_ppat, use_container_width=True)
            else:
                st.warning("Kolom 'Nama PPAT' tidak ditemukan untuk grafik.")

        # Kolom 2: Grafik Distribusi per Kantah (Pie Chart)
        with col_grafik_2:
            if col_kantah and pilih_kantah == "Semua Wilayah":
                st.subheader("Distribusi per Kantah")
                ck = col_kantah[0]
                counts_kantah = df_display[ck].value_counts().reset_index()
                counts_kantah.columns = ['Kantor Pertanahan', 'Jumlah']
                
                fig_kantah = px.pie(counts_kantah, values='Jumlah', names='Kantor Pertanahan', 
                                    hole=0.4, # Membuatnya menjadi grafik donat
                                    color_discrete_sequence=px.colors.qualitative.Blues)
                fig_kantah.update_layout(height=450)
                # Tampilkan label di dalam pie chart
                fig_kantah.update_traces(textposition='inside', textinfo='percent+label')
                
                st.plotly_chart(fig_kantah, use_container_width=True)
            elif pilih_kantah != "Semua Wilayah":
                st.info(f"Distribusi per Kantah disembunyikan karena filter {pilih_kantah} aktif.")
            else:
                st.warning("Kolom 'Kantor Pertanahan' tidak ditemukan untuk grafik Pie.")

        # Baris Bawah: Grafik Tren Waktu (Line Chart)
        st.markdown("---")
        st.subheader("🕒 Tren Waktu Pelaporan")
        
        # Cek apakah kolom Tanggal berhasil dibuat di Pre-processing
        if 'Tanggal_Lapor' in df_display.columns:
            tren_waktu = df_display.groupby('Tanggal_Lapor').size().reset_index()
            tren_waktu.columns = ['Tanggal', 'Jumlah']
            
            fig_tren = px.line(tren_waktu, x='Tanggal', y='Jumlah',
                                markers=True, # Tambahkan titik di setiap tanggal
                                color_discrete_sequence=['#2c3e50']) # Warna gelap
            
            fig_tren.update_layout(
                height=350,
                xaxis_title="Tanggal", 
                yaxis_title="Total Laporan",
                xaxis=dict(tickformat="%d %b") # Format tanggal sumbu X
            )
            st.plotly_chart(fig_tren, use_container_width=True)
        else:
            st.warning("Kolom 'Timestamp' tidak ditemukan atau kotor, tren waktu tidak bisa ditampilkan.")

    else:
        st.warning(f"Tidak ada data ditemukan untuk wilayah {pilih_kantah}.")

    # --- TABEL DATA LENGKAP (Tampilkan SEMUA Kolom) ---
    st.markdown("---")
    st.subheader("📑 Tabel Data Lengkap (Semua Kolom & Sheet)")
    st.write("Gunakan fitur *search* di tabel bawah ini untuk mencari data spesifik.")
    
    # Hapus kolom tanggal tambahan agar tabel bersih
    kolom_tabel = df_display.columns.drop(['Tanggal_Lapor'], errors='ignore')
    
    # Menampilkan seluruh dataframe (semua kolom dari sheet)
    st.dataframe(df_display[kolom_tabel], use_container_width=True)

    # Fitur Download Data
    csv = df_display[kolom_tabel].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Data PPAT (.csv)",
        data=csv,
        file_name='data_monitoring_ppat.csv',
        mime='text/csv',
    )

except Exception as e:
    st.error(f"Terjadi Kendala Teknis: {e}")
    st.info("Pastikan link Google Sheets sudah benar dan dapat diakses publik (Anyone with the link).")import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Dashboard PPAT Kalsel", layout="wide")

# 2. Link Google Sheets (Format CSV)import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Judul
st.set_page_config(page_title="Dashboard PPAT", layout="wide")
st.title("📊 Monitoring Pelaporan PPAT")

# 2. Link Data
URL = "https://docs.google.com/spreadsheets/d/1OfPHzg74p-WKeC0WzwT931cLdVEW20mbggv-2W8X7Gw/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    # Mengambil data dan memastikan dibaca sebagai string untuk menghindari error tipe data
    df = pd.read_csv(URL, dtype=str)
    # Bersihkan spasi di nama kolom
    df.columns = [str(c).strip() for c in df.columns]
    return df

try:
    df = load_data()
    
    # --- PENCARIAN KOLOM SECARA DINAMIS (ANTI ERROR INDEX) ---
    # Mencari kolom yang mengandung kata 'Kantor'
    cols_kantah = [c for c in df.columns if 'Kantor' in c or 'Kantah' in c]
    # Mencari kolom yang mengandung kata 'Nama'
    cols_ppat = [c for c in df.columns if 'Nama' in c]
    # Mencari kolom waktu
    cols_time = [c for c in df.columns if 'Timestamp' in c or 'Waktu' in c]

    # Validasi: Jika kolom tidak ditemukan, pakai kolom pertama dan kedua yang tersedia
    ck = cols_kantah[0] if cols_kantah else df.columns[1]
    cp = cols_ppat[0] if cols_ppat else df.columns[2]

    # --- SIDEBAR FILTER ---
    list_kantah = sorted(df[ck].dropna().unique().tolist())
    pilih = st.sidebar.selectbox("Pilih Wilayah:", ["Semua"] + list_kantah)

    # Filter Data
    df_f = df[df[ck] == pilih] if pilih != "Semua" else df

    # --- TAMPILAN DASHBOARD ---
    st.metric("Total Laporan", len(df_f))

    # Grafik Batang Horizontal
    st.subheader(f"Aktivitas PPAT - {pilih}")
    counts = df_f[cp].value_counts().reset_index()
    counts.columns = ['PPAT', 'Jumlah']
    
    fig = px.bar(counts.head(30), x='Jumlah', y='PPAT', orientation='h', 
                 text='Jumlah', color='Jumlah', color_continuous_scale='Blues')
    
    fig.update_layout(height=max(500, len(counts.head(30)) * 25), yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig, use_container_width=True)

    # --- TABEL DATA LENGKAP ---
    st.markdown("---")
    with st.expander("Klik untuk melihat Tabel Data Lengkap"):
        st.dataframe(df_f, use_container_width=True)

except Exception as e:
    st.error(f"Terjadi kesalahan teknis: {e}")
    st.info("Saran: Pastikan link Google Sheets Anda sudah diatur 'Siapa saja yang memiliki link dapat melihat'.")
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
