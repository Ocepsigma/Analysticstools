import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr, chi2_contingency
from scipy.stats import shapiro

st.title("Aplikasi Analisis Survey")

uploaded_file = st.file_uploader("Upload file Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("Preview Data")
    st.dataframe(df)

    st.subheader("Analisis Deskriptif")
    st.write(df.describe(include="all"))

    st.subheader("Analisis Asosiasi Otomatis")

    # Pilih dua kolom
    col1 = st.selectbox("Pilih variabel 1", df.columns)
    col2 = st.selectbox("Pilih variabel 2", df.columns)

    if col1 and col2:
        x = df[col1].dropna()
        y = df[col2].dropna()

        # Tentukan tipe data
        x_is_num = pd.api.types.is_numeric_dtype(x)
        y_is_num = pd.api.types.is_numeric_dtype(y)

        st.write(f"**Tipe data {col1}:**", "Numeric" if x_is_num else "Kategori")
        st.write(f"**Tipe data {col2}:**", "Numeric" if y_is_num else "Kategori")

        # CASE 1: KEDUA NUMERIC → PEARSON ATAU SPEARMAN
        if x_is_num and y_is_num:
            st.write("### Kedua variabel adalah numeric")

            # Uji normalitas
            stat1, p1 = shapiro(x)
            stat2, p2 = shapiro(y)

            st.write(f"Normalitas {col1}: p = {p1:.4f}")
            st.write(f"Normalitas {col2}: p = {p2:.4f}")

            normal = (p1 > 0.05) and (p2 > 0.05)

            if normal:
                st.success("Data normal → menggunakan **Pearson Correlation**")

                r, p_value = pearsonr(x, y)

                st.write("### Hasil Pearson")
                st.write(f"Correlation (r): **{r:.4f}**")
                st.write(f"P-value: **{p_value:.4f}**")

            else:
                st.warning("Data tidak normal → menggunakan **Spearman Correlation**")

                r, p_value = spearmanr(x, y)

                st.write("### Hasil Spearman")
                st.write(f"Correlation (rho): **{r:.4f}**")
                st.write(f"P-value: **{p_value:.4f}**")

        # CASE 2: SALAH SATU KATEGORI → CHI-SQUARE
        else:
            st.info("Salah satu variabel kategori → menggunakan **Chi-Square Test**")

            contingency_table = pd.crosstab(df[col1], df[col2])
            st.write("### Tabel Kontingensi")
            st.dataframe(contingency_table)

            chi2, p, dof, expected = chi2_contingency(contingency_table)

            st.write("### Hasil Chi-Square")
            st.write(f"Chi-square: **{chi2:.4f}**")
            st.write(f"P-value: **{p:.4f}**")
            st.write(f"Degrees of freedom: **{dof}**")




