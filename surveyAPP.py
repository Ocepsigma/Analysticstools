import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr, chi2_contingency, shapiro


# ===================================================================
# ======================= CUSTOM PAGE CONFIG ========================
# ===================================================================
st.set_page_config(
    page_title="Aplikasi Analisis Survey",
    layout="wide"
)

# ===================================================================
# ======================= CUSTOM BACKGROUND CSS ======================
# ===================================================================
background_css = """
<style>

body {
    background: linear-gradient(135deg, #eef2f3 0%, #d9e4ec 100%);
    font-family: 'Helvetica';
}

/* Box container styling */
.block-container {
    padding-top: 2rem;
}

/* Card style */
.custom-card {
    background: white;
    padding: 22px 30px;
    border-radius: 14px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.15);
    margin-bottom: 25px;
}

/* Title */
h1, h2, h3 {
    font-weight: 650;
}

</style>
"""
st.markdown(background_css, unsafe_allow_html=True)

# ===================================================================
# =========================== BAHASA ================================
# ===================================================================
lang = st.sidebar.selectbox("Pilih Bahasa / Select Language", ["Indonesia", "English"])

def T(id, en):
    return id if lang == "Indonesia" else en

# ===================================================================
# ============================ MENU =================================
# ===================================================================
page = st.sidebar.radio("Menu", [T("Analisis Data", "Data Analysis"), 
                                 T("Profil Pembuat", "Creator Profile")])


# ===================================================================
# ====================== 1. HALAMAN ANALISIS DATA ===================
# ===================================================================
if page == T("Analisis Data", "Data Analysis"):

    st.markdown(f"""
    <h1 style='text-align:center; margin-top: 20px;'>
        {T("Analisis Data Survey", "Survey Data Analysis")}
    </h1>
""", unsafe_allow_html=True)

    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        T("Upload File Excel (.xlsx)", "Upload Excel File (.xlsx)"), type="xlsx"
    )

    if uploaded_file:
        df = pd.read_excel(uploaded_file)

        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.subheader(T("Data yang Diupload", "Uploaded Data"))
        st.dataframe(df)
        st.markdown("</div>", unsafe_allow_html=True)

        numeric_cols = df.select_dtypes(include="number").columns.tolist()

        # =====================================================
        # VISUALISASI
        # =====================================================
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
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

        st.markdown("</div>", unsafe_allow_html=True)

        # =====================================================
        # ANALISIS HUBUNGAN
        # =====================================================
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.subheader(T("Analisis Hubungan Variabel", "Variable Relationship Analysis"))

        col1 = st.selectbox(T("Pilih Variabel 1", "Select Variable 1"), df.columns)
        col2 = st.selectbox(T("Pilih Variabel 2", "Select Variable 2"), df.columns)

        if col1 and col2:
            x = df[col1].dropna()
            y = df[col2].dropna()

            x_num = pd.api.types.is_numeric_dtype(x)
            y_num = pd.api.types.is_numeric_dtype(y)

            st.write(f"{col1} → {'Numeric' if x_num else 'Category'}")
            st.write(f"{col2} → {'Numeric' if y_num else 'Category'}")

            # =====================================================
            # PEARSON / SPEARMAN
            # =====================================================
            if x_num and y_num:

                st.info(T("Kedua variabel numeric → cek normalitas",
                          "Both variables numeric → checking normality"))

                p_norm_x = shapiro(x)[1]
                p_norm_y = shapiro(y)[1]

                st.write(f"Normalitas {col1}: p = {p_norm_x:.4f}")
                st.write(f"Normalitas {col2}: p = {p_norm_y:.4f}")

                normal = (p_norm_x > 0.05) and (p_norm_y > 0.05)

                if normal:
                    st.success(T("Data normal → menggunakan Pearson",
                                 "Normal data → using Pearson"))
                    r, p_value = pearsonr(x, y)
                    metode = "Pearson"
                else:
                    st.warning(T("Data tidak normal → menggunakan Spearman",
                                 "Non-normal data → using Spearman"))
                    r, p_value = spearmanr(x, y)
                    metode = "Spearman"

                st.write(f"### {metode}")
                st.write(f"r = {r:.4f}")
                st.write(f"P-value = {p_value:.4f}")

                arah = T("positif", "positive") if r > 0 else T("negatif", "negative")
                signif = T("Signifikan", "Significant") if p_value < 0.05 else T("Tidak signifikan", "Not significant")

                st.subheader(T("Kesimpulan", "Conclusion"))
                st.write(
                    T(
                        f"Hubungan {arah} dengan koefisien {metode} = {r:.4f}. "
                        f"Nilai p = {p_value:.4f} → hubungan {signif}.",
                        f"{arah.capitalize()} correlation with {metode} coefficient {r:.4f}. "
                        f"P-value = {p_value:.4f} → relationship is {signif}."
                    )
                )

            # =====================================================
            # CHI-SQUARE
            # =====================================================
            else:
                st.info(T("Variabel kategorik → menggunakan Chi-Square",
                          "Categorical variable → using Chi-Square Test"))

                table = pd.crosstab(df[col1], df[col2])
                st.write("### Tabel Kontingensi")
                st.dataframe(table)

                chi2, p, dof, expected = chi2_contingency(table)

                st.write(f"Chi2 = {chi2:.4f}")
                st.write(f"P-value = {p:.4f}")
                st.write(f"Degrees of freedom = {dof}")

                signif = p < 0.05

                st.subheader(T("Kesimpulan", "Conclusion"))

                if signif:
                    st.success(T(
                        f"Terdapat hubungan signifikan antara {col1} dan {col2}.",
                        f"There is a significant association between {col1} and {col2}."
                    ))
                else:
                    st.warning(T(
                        f"Tidak terdapat hubungan signifikan antara {col1} dan {col2}.",
                        f"No significant association between {col1} and {col2}."
                    ))

        st.markdown("</div>", unsafe_allow_html=True)

# ================================
#  HALAMAN PROFIL PEMBUAT
# ================================
else:
    # Judul
    st.markdown(
        f"<h1 style='text-align:center; margin-bottom:20px;'>{T('Profil Pembuat Aplikasi', 'App Creator Profile')}</h1>",
        unsafe_allow_html=True
    )

   # ======================
#   FOTO PROFIL (AMAN)
# ======================
try:
    # Versi HTML
    st.markdown(
        """
        <div style='text-align:center; margin-top:10px; margin-bottom:10px;'>
            <img src='foto_yoseph.jpg' style='width:280px; border-radius:20px;'/>
        </div>
        """,
        unsafe_allow_html=True
    )
except:
    # Versi backup Streamlit (jika HTML gagal / file tidak ditemukan)
    st.image("foto_yoseph.jpg", width=280)


    # ======================
    #   PERKENALAN (Bilingual)
    # ======================
    intro_id = """
    <div style='text-align:center; font-size:18px; line-height:1.6; margin-top:15px;'>
    Nama saya <b>Yoseph Sihite</b>. Web App ini dibuat sebagai bagian dari Final Project mata kuliah Statistik 1.  
    Saya kuliah di jurusan Teknik Industri, kelas 3, dengan SID 004202400113.  
    Saya berasal dari Group 2 dalam mata kuliah ini.  
    Web App ini selesai dibuat pada tanggal 1 Desember 2025.
    </div>
    """

    intro_en = """
    <div style='text-align:center; font-size:18px; line-height:1.6; margin-top:15px;'>
    My name is <b>Yoseph Sihite</b>. This Web App was created as part of the Final Project for the Statistics 1 course.  
    I am studying Industrial Engineering, class 3, with SID 004202400113.  
    I am from Group 2 in this course.  
    This Web App was completed on December 1st, 2025.
    </div>
    """

    st.markdown(T(intro_id, intro_en), unsafe_allow_html=True)

    # ======================
    #   KONTRIBUSI SAYA
    # ======================
    st.markdown(
        f"<h2 style='text-align:center; margin-top:40px;'>{T('Kontribusi Saya', 'My Contributions')}</h2>",
        unsafe_allow_html=True
    )

    contrib_id = """
    <div style='text-align:center; font-size:18px; line-height:1.6; margin-top:10px;'>
    Saya membuat seluruh pertanyaan untuk kuesioner, membangun Web App ini sendiri,  
    dan saya menyelesaikan seluruh proses pengerjaan dari awal sampai selesai secara mandiri.
    </div>
    """

    contrib_en = """
    <div style='text-align:center; font-size:18px; line-height:1.6; margin-top:10px;'>
    I created all the questionnaire questions, built this Web App myself,  
    and completed the entire development process independently from start to finish.
    </div>
    """

    st.markdown(T(contrib_id, contrib_en), unsafe_allow_html=True)
