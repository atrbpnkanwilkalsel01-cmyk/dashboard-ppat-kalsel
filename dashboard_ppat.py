import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard PPAT", layout="wide")

# Ambil Data
URL = "https://docs.google.com/spreadsheets/d/1OfPHzg74p-WKeC0WzwT931cLdVEW20mbggv-2W8X7Gw/export?format=csv"

def load_data():
    df = pd.read_csv(URL)
    return df

st.title("📊 Monitoring Pelaporan PPAT")

try:
    df = load_data()
    
    # Kita pakai urutan kolom:
    # Kolom 1 = Kantor Pertanahan, Kolom 2 = Nama PPAT
    c_kantah = df.columns[1]
    c_ppat = df.columns[2]

    # Sidebar Filter
    list_kantah = sorted(df[c_kantah].dropna().unique().tolist())
    pilih = st.sidebar.selectbox("Pilih Kantah:", ["Semua"] + list_kantah)

    # Logika Filter
    if pilih == "Semua":
        df_f = df
    else:
        df_f = df[df[c_kantah] == pilih]

    # Angka Total
    st.metric("Total Laporan", len(df_f))

    # Grafik
    counts = df_f[c_ppat].value_counts().reset_index()
    counts.columns = ['PPAT', 'Jumlah']
    
    fig = px.bar(counts, x='Jumlah', y='PPAT', orientation='h', text='Jumlah')
    fig.update_layout(height=max(400, len(counts)*30), yaxis={'categoryorder':'total ascending'})
    
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Error: {e}")
