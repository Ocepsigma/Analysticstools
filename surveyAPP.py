import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr, chi2_contingency, shapiro

st.set_page_config(page_title="Aplikasi Analisis Survey", layout="wide")

# Bahasa
lang = st.sidebar.selectbox("Pilih Bahasa / Select Language", ["Indonesia", "English"])

def T(id, en):
    return id if lang == "Indonesia" else en

# Menu
page = st.sidebar.radio("Menu", [T("Analisis Data", "Data Analysis"), T("Profil Pembuat", "Creator Profile")])


# =========================================================
# =============== 1. HALAMAN ANALISIS DATA =================
# =========================================================
if page == T("Analisis Data", "Data Analysis"):
    
    st.title(T("Analisis Data Survey", "Survey Data Analysis"))

    uploaded_file = st.file_uploader(T("Upload File Excel (.xlsx)", "Upload Excel File (.xlsx)"), type="xlsx")

    if uploaded_file:
        df = pd.read_excel(uploaded_file)

        st.subheader(T("Data yang Diupload", "Uploaded Data"))
        st.dataframe(df)

        numeric_cols = df.select_dtypes(include="number").columns.tolist()

        # =====================================================
        # VISUALISASI HISTOGRAM DAN BOXPLOT
        # =====================================================
        st.subheader(T("Distribusi Data", "Data Distribution"))

        if numeric_cols:
            selected = st.selectbox(T("Pilih Variabel", "Select Variable"), numeric_cols)

            # Histogram
            fig, ax = plt.subplots()
            ax.hist(df[selected], bins=20)
            ax.set_title(f"Histogram - {selected}")
            st.pyplot(fig)

            # Boxplot
            fig2, ax2 = plt.subplots()
            ax2.boxplot(df[selected])
            ax2.set_title(f"Boxplot - {selected}")
            st.pyplot(fig2)

        # =====================================================
        # ANALISIS ASOSIASI OTOMATIS
        # =====================================================
        st.subheader(T("Analisis Hubungan Variabel", "Variable Relationship Analysis"))

        col1 = st.selectbox(T("Pilih Variabel 1", "Select Variable 1"), df.columns)
        col2 = st.selectbox(T("Pilih Variabel 2", "Select Variable 2"), df.columns)

        if col1 and col2:
            x = df[col1].dropna()
            y = df[col2].dropna()

            x_num = pd.api.types.is_numeric_dtype(x)
            y_num = pd.api.types.is_numeric_dtype(y)

            st.write(f"**{col1}** → {'Numeric' if x_num else 'Category'}")
            st.write(f"**{col2}** → {'Numeric' if y_num else 'Category'}")

            # =====================================================
            # CASE 1: BOTH NUMERIC → PEARSON / SPEARMAN
            # =====================================================
            if x_num and y_num:

                st.info(T("Kedua variabel numeric → cek normalitas", 
                          "Both variables numeric → checking normality"))

                # Uji normalitas
                p_norm_x = shapiro(x)[1]
                p_norm_y = shapiro(y)[1]

                st.write(f"Normalitas {col1}: p = {p_norm_x:.4f}")
                st.write(f"Normalitas {col2}: p = {p_norm_y:.4f}")

                normal = (p_norm_x > 0.05) and (p_norm_y > 0.05)

                # ---- Pearson ----
                if normal:
                    st.success(T("Data normal → menggunakan Pearson Correlation", 
                                 "Normal data → using Pearson Correlation"))
                    r, p_value = pearsonr(x, y)
                    metode = "Pearson"

                # ---- Spearman ----
                else:
                    st.warning(T("Data tidak normal → menggunakan Spearman Correlation", 
                                 "Non-normal data → using Spearman Correlation"))
                    r, p_value = spearmanr(x, y)
                    metode = "Spearman"

                # --- Output ---
                st.write(f"### {metode}")
                st.write(f"r = **{r:.4f}**")
                st.write(f"P-value = **{p_value:.4f}**")

                # --- Kesimpulan otomatis ---
                arah = T("positif", "positive") if r > 0 else T("negatif", "negative")
                signif = T("Signifikan", "Significant") if p_value < 0.05 else T("Tidak signifikan", "Not significant")

                st.subheader(T("Kesimpulan", "Conclusion"))
                st.write(
                    T(
                        f"Hubungan {arah} dengan koefisien {metode} = {r:.4f}. "
                        f"Nilai p = {p_value:.4f} → hubungan **{signif}**.",
                        f"{arah.capitalize()} correlation with {metode} coefficient {r:.4f}. "
                        f"P-value = {p_value:.4f} → relationship is **{signif}**."
                    )
                )


            # =====================================================
            # CASE 2: SALAH SATU / DUA-DUANYA KATEGORI → CHI SQUARE
            # =====================================================
            else:
                st.info(T("Variabel bersifat kategorik → menggunakan Chi-Square", 
                          "Categorical variable detected → using Chi-Square Test"))

                table = pd.crosstab(df[col1], df[col2])
                st.write("### Tabel Kontingensi")
                st.dataframe(table)

                chi2, p, dof, expected = chi2_contingency(table)

                st.write("### Chi-Square Test")
                st.write(f"Chi2 = **{chi2:.4f}**")
                st.write(f"P-value = **{p:.4f}**")
                st.write(f"Degrees of freedom = **{dof}**")

                # Kesimpulan
                signif = p < 0.05

                st.subheader(T("Kesimpulan", "Conclusion"))

                if signif:
                    st.success(
                        T(
                            f"Terdapat hubungan signifikan antara {col1} dan {col2}.",
                            f"There is a significant association between {col1} and {col2}."
                        )
                    )
                else:
                    st.warning(
                        T(
                            f"Tidak terdapat hubungan signifikan antara {col1} dan {col2}.",
                            f"No significant association between {col1} and {col2}."
                        )
                    )


# =========================================================
# =============== 2. HALAMAN PROFIL PEMBUAT ===============
# =========================================================
else:
    st.title(T("Profil Pembuat Aplikasi", "App Creator Profile"))

    # Foto profil
    st.image("foto.jpg", width=300)

    # Perkenalan
    intro_id = """
    Nama saya Yoseph Sihite. Web App ini dibuat sebagai bagian dari Final Project mata kuliah Statistik 1.
    Saya kuliah di President University pada jurusan Teknik Industri, kelas 3, dengan SID 004202400113.
    Saya berasal dari Group 2 dalam pengerjaan tugas ini. Web App ini selesai dibuat pada tanggal 1 Desember 2025.
    """

    intro_en = """
    My name is Yoseph Sihite. This Web App was created as part of the Final Project for the Statistics 1 course.
    I am currently studying at President University majoring in Industrial Engineering, class 3, with SID 004202400113.
    I am part of Group 2 for this project. This Web App was completed on December 1st, 2025.
    """

    st.write(T(intro_id, intro_en))

    # Kontribusi
    st.subheader(T("Kontribusi Saya", "My Contributions"))

    contrib_id = """
    Saya membuat seluruh pertanyaan untuk kuesioner, saya membuat dan membangun Web App ini sendiri,
    serta saya melakukan seluruh proses pengerjaan dari awal hingga selesai.
    """

    contrib_en = """
    I created all of the questionnaire questions, I designed and built this entire Web App myself,
    and I completed the whole development process from start to finish independently.
    """

    st.write(T(contrib_id, contrib_en))
