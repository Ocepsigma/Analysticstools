import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import scipy.stats as stats
from scipy.stats import chi2_contingency, pearsonr, spearmanr, f_oneway
import io
import base64
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

# Set page config
st.set_page_config(
    page_title="Survey Analysis Tools",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to determine variable type
def determine_variable_type(series):
    if pd.api.types.is_numeric_dtype(series):
        if series.nunique() <= 10:
            return "ordinal"
        else:
            return "continuous"
    else:
        if series.nunique() <= 5:
            return "nominal"
        else:
            return "ordinal"

# Function to get appropriate analysis based on variable types
def determine_analysis_type(var1_type, var2_type):
    if var1_type == "nominal" and var2_type == "nominal":
        return "chi_square"
    elif var1_type == "nominal" and var2_type in ["ordinal", "continuous"]:
        return "anova"
    elif var1_type in ["ordinal", "continuous"] and var2_type == "nominal":
        return "anova"
    elif var1_type == "ordinal" and var2_type == "ordinal":
        return "spearman"
    elif var1_type in ["ordinal", "continuous"] and var2_type in ["ordinal", "continuous"]:
        return "pearson"
    else:
        return "chi_square"  # default

# Function to perform automatic association analysis
def automatic_association_analysis(df, var1, var2, alpha=0.05):
    """
    Automatically performs appropriate association analysis based on variable types
    """
    # Determine variable types
    var1_type = determine_variable_type(df[var1])
    var2_type = determine_variable_type(df[var2])
    
    # Determine analysis type
    analysis_type = determine_analysis_type(var1_type, var2_type)
    
    results = {
        'var1': var1,
        'var2': var2,
        'var1_type': var1_type,
        'var2_type': var2_type,
        'analysis_type': analysis_type,
        'alpha': alpha,
        'interpretation': '',
        'recommendation': '',
        'visualization': None
    }
    
    try:
        if analysis_type == "chi_square":
            # Chi-Square Test for Independence
            contingency_table = pd.crosstab(df[var1], df[var2])
            chi2, p_value, dof, expected = chi2_contingency(contingency_table)
            
            results.update({
                'test_statistic': chi2,
                'p_value': p_value,
                'degrees_of_freedom': dof,
                'contingency_table': contingency_table,
                'expected_values': expected
            })
            
            # Interpretation
            if p_value < alpha:
                results['interpretation'] = f'Terdapat asosiasi yang signifikan antara {var1} dan {var2} (χ²={chi2:.3f}, p={p_value:.4f})'
                results['recommendation'] = 'Variabel-variabel ini tidak independen dan memiliki hubungan statistik'
            else:
                results['interpretation'] = f'Tidak ada asosiasi signifikan antara {var1} dan {var2} (χ²={chi2:.3f}, p={p_value:.4f})'
                results['recommendation'] = 'Variabel-variabel ini independen secara statistik'
                
            # Visualization
            fig = px.imshow(
                contingency_table,
                title=f'Hubungan antara {var1} dan {var2}',
                labels=dict(x=var2, y=var1, color="Frekuensi"),
                color_continuous_scale="Blues"
            )
            results['visualization'] = fig
            
        elif analysis_type == "anova":
            # ANOVA Test
            if var1_type == "nominal":
                groups = [df[df[var1] == group][var2].dropna() for group in df[var1].unique()]
                group_labels = df[var1].unique()
            else:
                groups = [df[df[var2] == group][var1].dropna() for group in df[var2].unique()]
                group_labels = df[var2].unique()
            
            # Filter out empty groups
            groups = [group for group in groups if len(group) > 0]
            
            if len(groups) < 2:
                results['interpretation'] = 'Tidak cukup kelompok data untuk melakukan ANOVA'
                results['recommendation'] = 'Periksa kategori variabel dan pastikan ada cukup data di setiap kelompok'
                return results
            
            f_stat, p_value = f_oneway(*groups)
            
            results.update({
                'test_statistic': f_stat,
                'p_value': p_value,
                'group_means': [np.mean(group) for group in groups],
                'group_stds': [np.std(group) for group in groups],
                'group_labels': group_labels
            })
            
            # Interpretation
            if p_value < alpha:
                results['interpretation'] = f'Terdapat perbedaan signifikan antara kelompok-kelompok (F={f_stat:.3f}, p={p_value:.4f})'
                results['recommendation'] = 'Setidaknya satu kelompok berbeda secara signifikan dari yang lain'
            else:
                results['interpretation'] = f'Tidak ada perbedaan signifikan antara kelompok-kelompok (F={f_stat:.3f}, p={p_value:.4f})'
                results['recommendation'] = 'Semua kelompok memiliki rata-rata yang tidak berbeda secara signifikan'
            
            # Visualization
            fig = go.Figure()
            
            if var1_type == "nominal":
                for i, group in enumerate(groups):
                    fig.add_trace(go.Box(
                        y=group,
                        name=str(group_labels[i]),
                        boxpoints='outliers'
                    ))
                fig.update_layout(
                    title=f'Distribusi {var2} berdasarkan {var1}',
                    xaxis_title=var1,
                    yaxis_title=var2
                )
            else:
                for i, group in enumerate(groups):
                    fig.add_trace(go.Box(
                        y=group,
                        name=str(group_labels[i]),
                        boxpoints='outliers'
                    ))
                fig.update_layout(
                    title=f'Distribusi {var1} berdasarkan {var2}',
                    xaxis_title=var2,
                    yaxis_title=var1
                )
            
            results['visualization'] = fig
            
        elif analysis_type == "pearson":
            # Pearson Correlation
            x = df[var1].dropna()
            y = df[var2].dropna()
            
            # Align the data
            common_idx = x.index.intersection(y.index)
            x = x.loc[common_idx]
            y = y.loc[common_idx]
            
            if len(x) < 3:
                results['interpretation'] = 'Tidak cukup data untuk melakukan korelasi Pearson'
                results['recommendation'] = 'Diperlukan setidaknya 3 pasang data yang valid'
                return results
            
            corr, p_value = pearsonr(x, y)
            
            results.update({
                'correlation': corr,
                'p_value': p_value,
                'sample_size': len(x)
            })
            
            # Interpretation
            if p_value < alpha:
                if abs(corr) < 0.3:
                    strength = 'lemah'
                elif abs(corr) < 0.7:
                    strength = 'sedang'
                else:
                    strength = 'kuat'
                
                direction = 'positif' if corr > 0 else 'negatif'
                results['interpretation'] = f'Terdapat korelasi {direction} yang signifikan dengan kekuatan {strength} (r={corr:.3f}, p={p_value:.4f})'
                results['recommendation'] = f'Variabel {var1} dan {var2} memiliki hubungan linear {direction} yang {strength}'
            else:
                results['interpretation'] = f'Tidak ada korelasi signifikan antara variabel (r={corr:.3f}, p={p_value:.4f})'
                results['recommendation'] = 'Tidak ada bukti hubungan linear antara variabel-variabel ini'
            
            # Visualization
            fig = px.scatter(
                x=x, y=y,
                title=f'Hubungan antara {var1} dan {var2}',
                labels={'x': var1, 'y': var2}
            )
            
            # Add trendline
            coeffs = np.polyfit(x, y, 1)
            trendline = np.poly1d(coeffs)
            x_trend = np.linspace(x.min(), x.max(), 100)
            y_trend = trendline(x_trend)
            
            fig.add_trace(go.Scatter(
                x=x_trend, y=y_trend,
                mode='lines',
                name=f'Trendline (r={corr:.3f})',
                line=dict(color='red', dash='dash')
            ))
            
            results['visualization'] = fig
            
        elif analysis_type == "spearman":
            # Spearman Correlation
            x = df[var1].dropna()
            y = df[var2].dropna()
            
            # Align the data
            common_idx = x.index.intersection(y.index)
            x = x.loc[common_idx]
            y = y.loc[common_idx]
            
            if len(x) < 3:
                results['interpretation'] = 'Tidak cukup data untuk melakukan korelasi Spearman'
                results['recommendation'] = 'Diperlukan setidaknya 3 pasang data yang valid'
                return results
            
            corr, p_value = spearmanr(x, y)
            
            results.update({
                'correlation': corr,
                'p_value': p_value,
                'sample_size': len(x)
            })
            
            # Interpretation
            if p_value < alpha:
                if abs(corr) < 0.3:
                    strength = 'lemah'
                elif abs(corr) < 0.7:
                    strength = 'sedang'
                else:
                    strength = 'kuat'
                
                direction = 'positif' if corr > 0 else 'negatif'
                results['interpretation'] = f'Terdapat korelasi {direction} yang signifikan dengan kekuatan {strength} (ρ={corr:.3f}, p={p_value:.4f})'
                results['recommendation'] = f'Variabel {var1} dan {var2} memiliki hubungan monoton {direction} yang {strength}'
            else:
                results['interpretation'] = f'Tidak ada korelasi signifikan antara variabel (ρ={corr:.3f}, p={p_value:.4f})'
                results['recommendation'] = 'Tidak ada bukti hubungan monoton antara variabel-variabel ini'
            
            # Visualization
            fig = px.scatter(
                x=x, y=y,
                title=f'Hubungan antara {var1} dan {var2}',
                labels={'x': var1, 'y': var2}
            )
            
            results['visualization'] = fig
            
    except Exception as e:
        results['interpretation'] = f'Terjadi kesalahan dalam analisis: {str(e)}'
        results['recommendation'] = 'Periksa kembali data dan variabel yang dipilih'
    
    return results

# Function to get correlation strength description
def get_correlation_strength(corr):
    abs_corr = abs(corr)
    if abs_corr < 0.1:
        return "sangat lemah", "Negligible"
    elif abs_corr < 0.3:
        return "lemah", "Weak"
    elif abs_corr < 0.5:
        return "sedang", "Moderate"
    elif abs_corr < 0.7:
        return "kuat", "Strong"
    else:
        return "sangat kuat", "Very Strong"

# Function to create profile page
def profile_page():
    st.markdown("""
    <style>
        .profile-container {
            background-color: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            margin-bottom: 30px;
        }
        .profile-header {
            text-align: center;
            margin-bottom: 30px;
        }
        .profile-content {
            display: flex;
            flex-wrap: wrap;
            gap: 30px;
        }
        .profile-left {
            flex: 1;
            min-width: 300px;
        }
        .profile-right {
            flex: 2;
            min-width: 300px;
        }
        .profile-section {
            margin-bottom: 25px;
        }
        .profile-section h3 {
            color: #1e88e5;
            margin-bottom: 15px;
            border-bottom: 2px solid #1e88e5;
            padding-bottom: 5px;
        }
        .skill-tag {
            display: inline-block;
            background-color: #e3f2fd;
            color: #1e88e5;
            padding: 5px 12px;
            margin: 3px;
            border-radius: 15px;
            font-size: 14px;
        }
        .contact-item {
            margin-bottom: 10px;
            display: flex;
            align-items: center;
        }
        .contact-item span {
            margin-right: 10px;
        }
        .project-card {
            background-color: #f5f5f5;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
        }
        .project-card h4 {
            color: #1e88e5;
            margin-bottom: 8px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("""
            <div class="profile-left">
                <div class="profile-section">
                    <h3>👤 Tentang Saya</h3>
                    <p>Saya adalah seorang Data Analyst dan Web Developer dengan pengalaman dalam mengembangkan aplikasi analisis data yang interaktif dan user-friendly. Saya memiliki keahlian dalam statistik, visualisasi data, dan pengembangan web modern.</p>
                </div>
                
                <div class="profile-section">
                    <h3>📊 Keahlian</h3>
                    <div>
                        <span class="skill-tag">Python</span>
                        <span class="skill-tag">Streamlit</span>
                        <span class="skill-tag">Data Analysis</span>
                        <span class="skill-tag">Statistik</span>
                        <span class="skill-tag">Plotly</span>
                        <span class="skill-tag">Pandas</span>
                        <span class="skill-tag">Machine Learning</span>
                        <span class="skill-tag">Web Development</span>
                    </div>
                </div>
                
                <div class="profile-section">
                    <h3>🎓 Pendidikan</h3>
                    <p><strong>S1 Teknik Informatika</strong><br>
                    Universitas Indonesia<br>
                    2015 - 2019</p>
                </div>
                
                <div class="profile-section">
                    <h3>📞 Kontak</h3>
                    <div class="contact-item">
                        <span>📧</span>
                        <span>data.analyst@example.com</span>
                    </div>
                    <div class="contact-item">
                        <span>📱</span>
                        <span>+62 812-3456-7890</span>
                    </div>
                    <div class="contact-item">
                        <span>🔗</span>
                        <span>linkedin.com/in/dataanalyst</span>
                    </div>
                    <div class="contact-item">
                        <span>🐙</span>
                        <span>github.com/dataanalyst</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="profile-right">
                <div class="profile-section">
                    <h3>💼 Pengalaman Kerja</h3>
                    <div class="project-card">
                        <h4>Senior Data Analyst</h4>
                        <p><strong>PT Tech Solutions Indonesia</strong> | 2021 - Sekarang</p>
                        <p>Mengembangkan dashboard analitik interaktif dan sistem prediksi menggunakan machine learning untuk meningkatkan efisiensi bisnis sebesar 25%.</p>
                    </div>
                    <div class="project-card">
                        <h4>Data Analyst</h4>
                        <p><strong>PT Data Analytics Indonesia</strong> | 2019 - 2021</p>
                        <p>Menganalisis data pelanggan dan menghasilkan insight yang membantu meningkatkan retensi pelanggan sebesar 30%.</p>
                    </div>
                </div>
                
                <div class="profile-section">
                    <h3>🚀 Proyek Unggulan</h3>
                    <div class="project-card">
                        <h4>Survey Analysis Tools</h4>
                        <p>Aplikasi web berbasis Streamlit untuk analisis data survei dengan kemampuan deteksi otomatis jenis uji statistik yang tepat berdasarkan tipe data.</p>
                    </div>
                    <div class="project-card">
                        <h4>Sales Prediction Dashboard</h4>
                        <p>Dashboard interaktif untuk memprediksi penjualan menggunakan time series forecasting dan machine learning.</p>
                    </div>
                    <div class="project-card">
                        <h4>Customer Segmentation System</h4>
                        <p>Sistem segmentasi pelanggan menggunakan clustering algorithms untuk strategi pemasaran yang lebih tepat sasaran.</p>
                    </div>
                </div>
                
                <div class="profile-section">
                    <h3>🏆 Sertifikasi</h3>
                    <div class="project-card">
                        <h4>Google Data Analytics Professional Certificate</h4>
                        <p>Google | 2022</p>
                    </div>
                    <div class="project-card">
                        <h4>Microsoft Certified: Azure Data Scientist Associate</h4>
                        <p>Microsoft | 2021</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Main function
def main():
    # Custom CSS
    st.markdown("""
    <style>
        .main-header {
            background: linear-gradient(90deg, #1e88e5, #42a5f5);
            padding: 2rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
        }
        .analysis-card {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 1.5rem;
        }
        .metric-card {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            text-align: center;
            border-left: 4px solid #1e88e5;
        }
        .insight-box {
            background: #e3f2fd;
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid #1e88e5;
            margin-bottom: 1rem;
        }
        .stTabs [data-baseweb="tab-list"] {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 0.5rem;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 5px;
            padding: 0.5rem 1rem;
            font-weight: 500;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(90deg, #1e88e5, #42a5f5); border-radius: 10px; margin-bottom: 20px; color: white;'>
        <h2>📊 Survey Analysis Tools</h2>
        <p>Automatic Statistical Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    page = st.sidebar.selectbox("Navigasi", ["Analisis Data", "Profil Developer"])
    
    if page == "Profil Developer":
        profile_page()
        return
    
    # Main content
    st.markdown("""
    <div class='main-header'>
        <h1>📊 Survey Analysis Tools</h1>
        <p>Automatic Statistical Analysis Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload
    st.markdown("### 📁 Upload Data")
    uploaded_file = st.file_uploader("Upload file CSV atau Excel", type=["csv", "xlsx", "xls"])
    
    if uploaded_file is not None:
        try:
            # Read data
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # Display data info
            st.markdown("### 📋 Informasi Data")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Jumlah Baris", df.shape[0])
            
            with col2:
                st.metric("Jumlah Kolom", df.shape[1])
            
            with col3:
                st.metric("Kolom Numerik", df.select_dtypes(include=np.number).shape[1])
            
            with col4:
                st.metric("Kolom Kategorikal", df.select_dtypes(exclude=np.number).shape[1])
            
            # Display data preview
            st.markdown("### 🔍 Preview Data")
            st.dataframe(df.head())
            
            # Variable selection
            st.markdown("### 🎯 Pilih Variabel untuk Analisis")
            
            all_columns = df.columns.tolist()
            var1 = st.selectbox("Pilih Variabel 1", all_columns)
            var2 = st.selectbox("Pilih Variabel 2", all_columns)
            
            if var1 and var2:
                # Show variable types
                var1_type = determine_variable_type(df[var1])
                var2_type = determine_variable_type(df[var2])
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Tipe {var1}**: {var1_type}")
                with col2:
                    st.markdown(f"**Tipe {var2}**: {var2_type}")
                
                # Determine analysis type
                analysis_type = determine_analysis_type(var1_type, var2_type)
                
                analysis_type_names = {
                    "chi_square": "Chi-Square Test",
                    "pearson": "Pearson Correlation",
                    "spearman": "Spearman Correlation",
                    "anova": "ANOVA Test"
                }
                
                st.markdown(f"**Analisis yang Direkomendasikan**: {analysis_type_names.get(analysis_type, 'Unknown')}")
                
                # Perform analysis button
                if st.button("🔬 Lakukan Analisis", type="primary"):
                    with st.spinner("Sedang melakukan analisis..."):
                        results = automatic_association_analysis(df, var1, var2)
                    
                    # Display results
                    st.markdown("### 📈 Hasil Analisis")
                    
                    # Metrics
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown(f"""
                        <div class='metric-card'>
                            <h4>{results['var1']}</h4>
                            <p>{results['var1_type']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"""
                        <div class='metric-card'>
                            <h4>{results['var2']}</h4>
                            <p>{results['var2_type']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown(f"""
                        <div class='metric-card'>
                            <h4>{analysis_type_names.get(results['analysis_type'], 'Unknown')}</h4>
                            <p>α = {results['alpha']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Test statistic
                    if 'test_statistic' in results:
                        st.markdown(f"**Statistik Uji**: {results['test_statistic']:.4f}")
                    
                    if 'correlation' in results:
                        st.markdown(f"**Korelasi**: {results['correlation']:.4f}")
                        
                        # Show correlation strength
                        strength_id, strength_en = get_correlation_strength(results['correlation'])
                        st.markdown(f"**Kekuatan Korelasi**: {strength_id} ({strength_en})")
                    
                    # P-value
                    if 'p_value' in results:
                        st.markdown(f"**P-value**: {results['p_value']:.4f}")
                        
                        # Significance indicator
                        if results['p_value'] < results['alpha']:
                            st.markdown("🔴 **Signifikan** (Tolak H₀)")
                        else:
                            st.markdown("🟢 **Tidak Signifikan** (Gagal Tolak H₀)")
                    
                    # Interpretation
                    st.markdown("### 📝 Interpretasi")
                    st.markdown(f"""
                    <div class='insight-box'>
                        <p>{results['interpretation']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Recommendation
                    st.markdown("### 💡 Rekomendasi")
                    st.markdown(f"""
                    <div class='insight-box'>
                        <p>{results['recommendation']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Visualization
                    if results['visualization'] is not None:
                        st.markdown("### 📊 Visualisasi")
                        st.plotly_chart(results['visualization'], use_container_width=True)
                    
                    # Additional details based on analysis type
                    if results['analysis_type'] == "chi_square" and 'contingency_table' in results:
                        st.markdown("### 📋 Tabel Kontingensi")
                        st.dataframe(results['contingency_table'])
                    
                    elif results['analysis_type'] == "anova" and 'group_means' in results:
                        st.markdown("### 📊 Statistik Kelompok")
                        
                        group_stats = pd.DataFrame({
                            'Kelompok': results['group_labels'],
                            'Mean': results['group_means'],
                            'Std Dev': results['group_stds']
                        })
                        
                        st.dataframe(group_stats)
                    
                    elif results['analysis_type'] in ["pearson", "spearman"] and 'sample_size' in results:
                        st.markdown(f"**Ukuran Sampel**: {results['sample_size']}")
                        
                        if results['analysis_type'] == "pearson":
                            st.markdown("""
                            **Catatan**: Korelasi Pearson mengukur hubungan linear antara dua variabel kontinyu.
                            """)
                        else:
                            st.markdown("""
                            **Catatan**: Korelasi Spearman mengukur hubungan monoton antara dua variabel ordinal.
                            """)
            
        except Exception as e:
            st.error(f"Terjadi kesalahan: {str(e)}")
    
    else:
        # Instructions
        st.markdown("""
        ### 📖 Cara Penggunaan
        
        1. **Upload Data**: Upload file CSV atau Excel yang berisi data survei Anda
        2. **Pilih Variabel**: Pilih dua variabel yang ingin dianalisis hubungannya
        3. **Analisis Otomatis**: Sistem akan secara otomatis menentukan jenis uji statistik yang tepat:
           - **Chi-Square**: Untuk dua variabel kategorikal
           - **ANOVA**: Untuk variabel kategorikal dan numerik
           - **Pearson**: Untuk dua variabel numerik dengan hubungan linear
           - **Spearman**: Untuk dua variabel ordinal dengan hubungan monoton
        4. **Hasil Analisis**: Lihat hasil lengkap dengan interpretasi dan visualisasi
        
        ### 🎯 Fitur Utama
        
        - ✅ Deteksi otomatis tipe data
        - ✅ Pemilihan uji statistik yang tepat
        - ✅ Interpretasi hasil yang mudah dipahami
        - ✅ Visualisasi data interaktif
        - ✅ Rekomendasi berdasarkan hasil analisis
        """)

if __name__ == "__main__":
    main()
