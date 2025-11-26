import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Aplikasi Analisis Survey", layout="wide")

st.title("📊 Aplikasi Analisis Data Survey")
st.write("Upload file Excel untuk melakukan analisis deskriptif dan asosiasi.")

# ================================
# Fungsi Utilitas
# ================================
def prepare_categorical(col_series, make_bins=None, min_freq=3):
    """Konversi kolom menjadi kategori + gabung kategori jarang."""
    s = col_series.dropna()

    # Jika numerik dan user menentukan jumlah bins
    if make_bins:
        try:
            s = pd.qcut(s, q=make_bins, duplicates='drop')
        except:
            s = pd.cut(s, bins=make_bins)
        s = s.astype(str)

    # Gabung kategori jarang
    freqs = s.value_counts()
    rare = freqs[freqs < min_freq].index
    s = s.replace(list(rare), "Lainnya")

    return s


def chi_square_manual(table):
    """Hitung chi-square tanpa scipy."""
    total = table.values.sum()
    expected = np.outer(table.sum(axis=1), table.sum(axis=0)) / total
    chi2 = ((table - expected) ** 2 / expected).sum().sum()
    dof = (table.shape[0] - 1) * (table.shape[1] - 1)
    return chi2, dof, expected


# ================================
# Upload File
# ================================
uploaded = st.file_uploader("Upload file Excel (.xlsx)", type=["xlsx"])

if uploaded:
    df = pd.read_excel(uploaded)
    st.subheader("📁 Data Preview")
    st.dataframe(df.head())

    # ================================
    # ANALISIS DESKRIPTIF
    # ================================
    st.header("📈 Analisis Deskriptif")

    deskripsi_kolom = st.selectbox("Pilih kolom untuk analisis deskriptif:", df.columns)

    if deskripsi_kolom:
        col = df[deskripsi_kolom]

        # Jika numerik
        if pd.api.types.is_numeric_dtype(col):
            st.subheader("📊 Statistik Numerik")
            st.write(col.describe())

            st.subheader("📉 Histogram")
            st.bar_chart(col)

        # Jika kategori / string
        else:
            st.subheader("📊 Frekuensi Kategori")
            count_data = col.value_counts()
            st.write(count_data)
            st.bar_chart(count_data)

    # ================================
    # ANALISIS ASOSIASI
    # ================================
    st.header("🔗 Analisis Asosiasi (Chi-square)")

    kolom_asosiasi = st.multiselect("Pilih 2 kolom kategorikal atau numerik:", df.columns)

    if len(kolom_asosiasi) == 2:
        c1, c2 = kolom_asosiasi

        st.write(f"Variabel dipilih: **{c1}** dan **{c2}**")

        # Opsi binning
        bins1 = st.number_input(f"Jumlah bins untuk {c1} (0 = tidak perlu)", min_value=0, max_value=20, value=0)
        bins2 = st.number_input(f"Jumlah bins untuk {c2} (0 = tidak perlu)", min_value=0, max_value=20, value=0)

        # Proses kategorisasi
        s1 = prepare_categorical(df[c1], make_bins=(bins1 if bins1 > 1 else None))
        s2 = prepare_categorical(df[c2], make_bins=(bins2 if bins2 > 1 else None))

        # Buat tabel kontingensi
        st.subheader("📋 Tabel Kontingensi")
        table = pd.crosstab(s1, s2)
        st.dataframe(table)

        # Cek minimal 2 kategori
        if table.shape[0] < 2 or table.shape[1] < 2:
            st.error("❌ Tidak bisa menghitung asosiasi. Minimal harus ada 2 kategori di masing-masing variabel.")
        else:
            # Hitung chi-square manual
            chi2, dof, expected = chi_square_manual(table)

            st.subheader("📐 Hasil Chi-square")
            st.write(f"**Chi-square:** {chi2:.4f}")
            st.write(f"**Derajat kebebasan (df):** {dof}")

            st.write("📊 **Expected Frequencies**")
            st.dataframe(pd.DataFrame(expected, index=table.index, columns=table.columns))

            st.info("Catatan: P-value tidak ditampilkan karena scipy tidak tersedia di Streamlit Community.")
    else:
        st.warning("Pilih **tepat 2 kolom** untuk analisis asosiasi.")



