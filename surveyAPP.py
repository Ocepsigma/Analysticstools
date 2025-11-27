import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr, chi2_contingency, shapiro
import matplotlib.pyplot as plt

# ==============================
# PILIHAN BAHASA
# ==============================
lang = st.sidebar.selectbox("Select Language / Pilih Bahasa", ["Bahasa Indonesia", "English"])

def txt(id, en):
    return id if lang == "Bahasa Indonesia" else en

st.title(txt("Aplikasi Analisis Data Survey", "Survey Data Analysis App"))

uploaded_file = st.file_uploader(txt("Upload file Excel", "Upload Excel file"), type=["xlsx"])

# ==============================
# Function interpretasi
# ==============================
def interpret_strength(r):
    r = abs(r)
    if r < 0.2: return txt("Sangat lemah", "Very weak")
    elif r < 0.4: return txt("Lemah", "Weak")
    elif r < 0.6: return txt("Moderat", "Moderate")
    elif r < 0.8: return txt("Kuat", "Strong")
    else: return txt("Sangat kuat", "Very strong")

# ==============================
# Jika file diupload
# ==============================
if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # ---- PREVIEW ----
    st.subheader(txt("Preview Data", "Data Preview"))
    st.dataframe(df)

    # ---- ANALISIS DESKRIPTIF ----
    st.subheader(txt("Analisis Deskriptif", "Descriptive Analysis"))
    st.write(df.describe(include="all"))

    # ==============================
    # HISTOGRAM & BOXPLOT
    # ==============================
    st.subheader(txt("Distribusi Data & Outlier", "Data Distribution & Outliers"))

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    if len(numeric_cols) > 0:
        selected_col = st.selectbox(
            txt("Pilih variabel numeric", "Select numeric variable"),
            numeric_cols
        )

        st.write(f"### {txt('Histogram untuk', 'Histogram for')} {selected_col}")

        # Histogram
        fig, ax = plt.subplots()
        ax.hist(df[selected_col].dropna(), bins=20)
        ax.set_xlabel(selected_col)
        ax.set_ylabel(txt("Frekuensi", "Frequency"))
        ax.set_title(txt(f"Histogram {selected_col}", f"Histogram of {selected_col}"))
        st.pyplot(fig)

        # Boxplot
        st.write(f"### {txt('Boxplot untuk Outlier', 'Boxplot for Outliers')}")

        fig2, ax2 = plt.subplots()
        ax2.boxplot(df[selected_col].dropna(), vert=True)
        ax2.set_ylabel(selected_col)
        ax2.set_title(txt(f"Boxplot {selected_col}", f"Boxplot of {selected_col}"))
        st.pyplot(fig2)

    else:
        st.info(txt(
            "Tidak ada kolom numeric untuk ditampilkan.",
            "No numeric columns available for visualization."
        ))

    # ==============================
    # ANALISIS ASOSIASI OTOMATIS
    # ==============================
    st.subheader(txt("Analisis Asosiasi Otomatis", "Automatic Association Analysis"))

    col1 = st.selectbox(txt("Pilih variabel 1", "Select variable 1"), df.columns)
    col2 = st.selectbox(txt("Pilih variabel 2", "Select variable 2"), df.columns)

    if col1 and col2:
        x = df[col1].dropna()
        y = df[col2].dropna()

        x_is_num = pd.api.types.is_numeric_dtype(x)
        y_is_num = pd.api.types.is_numeric_dtype(y)

        st.write(f"**{txt('Tipe data', 'Data type')} {col1}:**", txt("Numeric", "Numeric") if x_is_num else txt("Kategori", "Category"))
        st.write(f"**{txt('Tipe data', 'Data type')} {col2}:**", txt("Numeric", "Numeric") if y_is_num else txt("Kategori", "Category"))

        # ==================================================
        # KEDUA-NYA NUMERIC
        # ==================================================
        if x_is_num and y_is_num:

            st.write("### " + txt("Kedua variabel numeric", "Both variables are numeric"))

            # Normalitas
            stat1, p1 = shapiro(x)
            stat2, p2 = shapiro(y)

            st.write(f"{txt('Normalitas', 'Normality')} {col1}: p = {p1:.4f}")
            st.write(f"{txt('Normalitas', 'Normality')} {col2}: p = {p2:.4f}")

            normal = (p1 > 0.05) and (p2 > 0.05)

            if normal:
                st.success(txt(
                    "Data normal → menggunakan Pearson Correlation",
                    "Data is normal → using Pearson Correlation"
                ))

                r, p_value = pearsonr(x, y)

                st.write("### Pearson")
                st.write(f"r = **{r:.4f}**")
                st.write(f"P-value = **{p_value:.4f}**")

                # Kesimpulan
                st.subheader(txt("Kesimpulan", "Conclusion"))
                direction = txt("positif", "positive") if r > 0 else txt("negatif", "negative")
                strength = interpret_strength(r)
                signif = txt("Signifikan", "Significant") if p_value < 0.05 else txt("Tidak signifikan", "Not significant")

                st.write(
                    txt(
                        f"Hasil menunjukkan korelasi {direction} dengan kekuatan **{strength}** (r = {r:.4f}). "
                        f"Nilai p = {p_value:.4f}, sehingga hubungan **{signif}**.",
                        f"The results indicate a {direction} correlation with **{strength}** strength (r = {r:.4f}). "
                        f"P-value = {p_value:.4f}, so the relationship is **{signif}**."
                    )
                )

            else:
                st.warning(txt(
                    "Data tidak normal → menggunakan Spearman Correlation",
                    "Data not normal → using Spearman Correlation"
                ))

                r, p_value = spearmanr(x, y)

                st.write("### Spearman")
                st.write(f"rho = **{r:.4f}**")
                st.write(f"P-value = **{p_value:.4f}**")

                # Kesimpulan
                st.subheader(txt("Kesimpulan", "Conclusion"))
                direction = txt("positif", "positive") if r > 0 else txt("negatif", "negative")
                strength = interpret_strength(r)
                signif = txt("Signifikan", "Significant") if p_value < 0.05 else txt("Tidak signifikan", "Not significant")

                st.write(
                    txt(
                        f"Hasil menunjukkan korelasi {direction} dengan kekuatan **{strength}** (rho = {r:.4f}). "
                        f"Nilai p = {p_value:.4f}, sehingga hubungan **{signif}**.",
                        f"The results indicate a {direction} correlation with **{strength}** strength (rho = {r:.4f}). "
                        f"P-value = {p_value:.4f}, so the relationship is **{signif}**."
                    )
                )

        # ==================================================
        # SALAH SATU ATAU KEDUANYA KATEGORIK
        # ==================================================
        else:
            st.info(txt(
                "Salah satu variabel kategori → menggunakan Chi-Square Test",
                "One variable is categorical → using Chi-Square Test"
            ))

            contingency_table = pd.crosstab(df[col1], df[col2])
            st.write("### " + txt("Tabel Kontingensi", "Contingency Table"))
            st.dataframe(contingency_table)

            chi2, p, dof, expected = chi2_contingency(contingency_table)

            st.write("### Chi-Square")
            st.write(f"Chi-square: **{chi2:.4f}**")
            st.write(f"P-value: **{p:.4f}**")
            st.write(f"Degrees of freedom: **{dof}**")

            st.subheader(txt("Kesimpulan", "Conclusion"))

            if p < 0.05:
                st.write(txt(
                    f"Nilai p = {p:.4f} < 0.05 → terdapat **asosiasi signifikan** antara {col1} dan {col2}.",
                    f"P-value = {p:.4f} < 0.05 → there is a **significant association** between {col1} and {col2}."
                ))
            else:
                st.write(txt(
                    f"Nilai p = {p:.4f} ≥ 0.05 → **tidak ada asosiasi signifikan** antara {col1} dan {col2}.",
                    f"P-value = {p:.4f} ≥ 0.05 → **no significant association** between {col1} and {col2}."
                ))

