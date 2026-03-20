import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard PPAT", layout="wide")

# Link Google Sheets Anda
URL = "https://docs.google.com/spreadsheets/d/1OfPHzg74p-WKeC0WzwT931cLdVEW20mbggv-2W8X7Gw/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(URL)
    # Bersihkan nama kolom dari spasi di depan/belakang
    df.columns = [str(c).strip() for c in df.columns]
    return df

st.title("📊 Monitoring Pelaporan PPAT")

try:
    df = load_data()
    
    # --- CARA AMAN CARI KOLOM ---
    # Cari kolom yang ada kata 'Kantor' atau 'Kantah'
    col_kantah = [c for c in df.columns if 'Kantor' in c or 'Kantah' in c]
    # Cari kolom yang ada kata 'Nama' dan 'PPAT'
    col_ppat = [c for c in df.columns if 'Nama' in c and 'PPAT' in c]

    else:
        ck = col_kantah[0]
        cp = col_ppat[0]

        # Filter Sidebar
        list_kantah = sorted(df[ck].unique().tolist())
        pilih = st.sidebar.selectbox("Pilih Wilayah:", ["Semua"] + list_kantah)

        # Filter Data
        df_f = df[df[ck] == pilih] if pilih != "Semua" else df

        # Statistik
        st.metric("Total Laporan", len(df_f))

        # Grafik
        counts = df_f[cp].value_counts().reset_index()
        counts.columns = ['PPAT', 'Jumlah']
        
        fig = px.bar(counts, x='Jumlah', y='PPAT', orientation='h', text='Jumlah',
                     color_discrete_sequence=['#3498db'])
        
        fig.update_layout(
            height=max(400, len(counts)*30),
            yaxis={'categoryorder':'total ascending'},
            xaxis_title="Jumlah Laporan",
            yaxis_title=""
        )
        st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
