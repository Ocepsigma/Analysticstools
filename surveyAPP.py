import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scipy import stats
from scipy.stats import chi2_contingency
import base64
import os

# Konfigurasi Halaman
st.set_page_config(
    page_title="Analisis Data Survei",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Multi-language Support - Hanya 2 Bahasa
TRANSLATIONS = {
    "id": {
        # Header dan Navigasi
        "title": "Analisis Data Survei",
        "language_indicator": "🇮🇩 Indonesia",
        
        # Upload Section
        "upload_title": "📊 Unggah File Excel Anda untuk Memulai Analisis",
        "upload_description": "Seret dan lepas file di sini<br>Batas 200MB per file • Format XLSX, XLS, CSV",
        "upload_button": "📁 Pilih File Excel/CSV",
        "success_message": "✅ Data berhasil dimuat! Dataset memiliki",
        
        # Dataset Info
        "rows_text": "baris",
        "columns_text": "kolom",
        "numerical_columns": "Kolom Numerik",
        "categorical_columns": "Kolom Kategorikal",
        
        # Analisis
        "descriptive_analysis": "📈 Analisis Deskriptif",
        "association_analysis": "🔗 Analisis Asosiasi",
        "dataset_overview": "📊 Dataset Overview",
        "missing_values": "🔍 Missing Values",
        "numerical_stats": "🔢 Statistik Numerik",
        "data_visualization": "📊 Visualisasi Data",
        "correlation_matrix": "🔗 Matriks Korelasi",
        "categorical_analysis": "📋 Analisis Kategorikal",
        "frequency_table": "📊 Tabel Frekuensi",
        
        # Uji Statistik
        "chi_square_test": "🎯 Uji Chi-Square",
        "correlation_analysis": "📊 Analisis Korelasi",
        "anova_test": "🔄 Uji ANOVA",
        "categorical_numerical_analysis": "Analisis Kategorikal vs Numerik",
        
        # Form Controls
        "select_numerical_column": "Pilih kolom numerik:",
        "select_categorical_column": "Pilih kolom kategorikal:",
        "select_variable_1": "Pilih variabel 1:",
        "select_variable_2": "Pilih variabel 2:",
        "select_categorical_variable": "Pilih variabel kategorikal:",
        "select_numerical_variable": "Pilih variabel numerik:",
        
        # Buttons
        "analyze_chi_square": "Analisis Chi-Square",
        "analyze_correlation": "Analisis Korelasi",
        "analyze_categorical_numerical": "Analisis Kategorikal-Numerik",
        "upload_new_file": "📁 Upload File Baru",
        
        # Results
        "contingency_table": "Tabel Kontingensi",
        "chi_square_results": "Hasil Chi-Square",
        "correlation_results": "Hasil Korelasi",
        "anova_results": "Hasil ANOVA",
        
        # Interpretasi
        "significant": "Signifikan",
        "not_significant": "Tidak Signifikan",
        "significant_association": "Ada hubungan signifikan antara",
        "no_significant_association": "Tidak ada hubungan signifikan antara",
        "significant_difference": "Ada perbedaan signifikan dalam rata-rata",
        "mean_difference": "antara kategori",
        "no_significant_difference": "Tidak ada perbedaan signifikan dalam rata-rata",
        "no_mean_difference": "antara kategori",
        
        # Metode
        "correlation_method": "Metode Korelasi",
        "pearson": "Pearson",
        "spearman": "Spearman",
        
        # Labels
        "total_rows": "Total Baris",
        "total_columns": "Total Kolom",
        "category": "Kategori",
        "frequency": "Frekuensi",
        "percentage": "Persentase",
        "columns": "Kolom",
        
        # Instructions
        "instructions": "🚀 Cara Menggunakan Aplikasi Ini",
        "upload_step": "Upload file Excel (.xlsx) atau CSV (.csv)",
        "analysis_step": "Pilih analisis yang ingin dilakukan",
        "export_step": "Download hasil analisis dalam format CSV",
        
        # Features
        "features_title": "📋 Fitur Utama",
        "descriptive_features": "📈 Analisis Deskriptif",
        "association_features": "🔗 Analisis Asosiasi",
        "supported_formats": "📊 Format File yang Didukung",
        
        # Tips
        "tip": "Pastikan data Anda memiliki header yang jelas dan format yang konsisten untuk hasil analisis yang optimal.",
        
        # Errors
        "error_no_file": "Silakan upload file terlebih dahulu!",
        "error_loading_file": "Error loading file:"
    },
    "en": {
        # Header dan Navigasi
        "title": "Survey Data Analysis",
        "language_indicator": "🇬🇧 English",
        
        # Upload Section
        "upload_title": "📊 Upload Your Excel File to Start Analysis",
        "upload_description": "Drag and drop file here<br>Limit 200MB per file • XLSX, XLS, CSV formats",
        "upload_button": "📁 Browse Excel/CSV Files",
        "success_message": "✅ Data successfully loaded! Dataset has",
        
        # Dataset Info
        "rows_text": "rows",
        "columns_text": "columns",
        "numerical_columns": "Numerical Columns",
        "categorical_columns": "Categorical Columns",
        
        # Analisis
        "descriptive_analysis": "📈 Descriptive Analysis",
        "association_analysis": "🔗 Association Analysis",
        "dataset_overview": "📊 Dataset Overview",
        "missing_values": "🔍 Missing Values",
        "numerical_stats": "🔢 Numerical Statistics",
        "data_visualization": "📊 Data Visualization",
        "correlation_matrix": "🔗 Correlation Matrix",
        "categorical_analysis": "📋 Categorical Analysis",
        "frequency_table": "📊 Frequency Table",
        
        # Uji Statistik
        "chi_square_test": "🎯 Chi-Square Test",
        "correlation_analysis": "📊 Correlation Analysis",
        "anova_test": "🔄 ANOVA Test",
        "categorical_numerical_analysis": "Categorical vs Numerical Analysis",
        
        # Form Controls
        "select_numerical_column": "Select numerical column:",
        "select_categorical_column": "Select categorical column:",
        "select_variable_1": "Select variable 1:",
        "select_variable_2": "Select variable 2:",
        "select_categorical_variable": "Select categorical variable:",
        "select_numerical_variable": "Select numerical variable:",
        
        # Buttons
        "analyze_chi_square": "Analyze Chi-Square",
        "analyze_correlation": "Analyze Correlation",
        "analyze_categorical_numerical": "Analyze Categorical-Numerical",
        "upload_new_file": "📁 Upload New File",
        
        # Results
        "contingency_table": "Contingency Table",
        "chi_square_results": "Chi-Square Results",
        "correlation_results": "Correlation Results",
        "anova_results": "ANOVA Results",
        
        # Interpretasi
        "significant": "Significant",
        "not_significant": "Not Significant",
        "significant_association": "There is a significant association between",
        "no_significant_association": "There is no significant association between",
        "significant_difference": "There is a significant difference in mean",
        "mean_difference": "between categories",
        "no_significant_difference": "There is no significant difference in mean",
        "no_mean_difference": "between categories",
        
        # Metode
        "correlation_method": "Correlation Method",
        "pearson": "Pearson",
        "spearman": "Spearman",
        
        # Labels
        "total_rows": "Total Rows",
        "total_columns": "Total Columns",
        "category": "Category",
        "frequency": "Frequency",
        "percentage": "Percentage",
        "columns": "Columns",
        
        # Instructions
        "instructions": "🚀 How to Use This Application",
        "upload_step": "Upload Excel (.xlsx) or CSV (.csv) file",
        "analysis_step": "Choose an analysis to perform",
        "export_step": "Download analysis results in CSV format",
        
        # Features
        "features_title": "📋 Main Features",
        "descriptive_features": "📈 Descriptive Analysis",
        "association_features": "🔗 Association Analysis",
        "supported_formats": "📊 Supported File Formats",
        
        # Tips
        "tip": "Ensure your data has clear headers and consistent format for optimal analysis results.",
        
        # Errors
        "error_no_file": "Please upload a file first!",
        "error_loading_file": "Error loading file:"
    }
}

class SurveyAnalysisApp:
    """Main Application Class for Survey Data Analysis"""
    
    def __init__(self):
        self.setup_session_state()
        self.apply_custom_styles()
    
    def setup_session_state(self):
        """Initialize session state variables"""
        if 'language' not in st.session_state:
            st.session_state.language = 'id'
        if 'data' not in st.session_state:
            st.session_state.data = None
        if 'uploaded_file' not in st.session_state:
            st.session_state.uploaded_file = None
    
    def apply_custom_styles(self):
        """Apply custom CSS styles"""
        background_styles = self.get_background_styles()
        
        st.markdown(f"""
        <style>
            {"".join(background_styles)}
            
            /* Global Styles */
            .stApp {{
                background-attachment: fixed;
            }}
            
            /* Remove default padding */
            .main .block-container {{
                padding-top: 0.5rem;
                margin-top: 0;
            }}
            
            /* Hide default Streamlit elements */
            .stHeader, .stMainMenu, footer {{
                visibility: hidden;
            }}
            
            .stApp > div {{
                padding-top: 0 !important;
            }}
            
            /* Main Content Container */
            .main-container {{
                background: rgba(255, 255, 255, 0.92);
                backdrop-filter: blur(15px);
                border-radius: 20px;
                padding: 2rem;
                margin: 0.5rem auto;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                max-width: 1200px;
            }}
            
            /* Header Styles */
            .app-header {{
                text-align: center;
                margin-bottom: 2rem;
            }}
            
            .main-title {{
                font-size: 3rem;
                font-weight: 700;
                background: linear-gradient(135deg, #1e40af, #3b82f6, #60a5fa);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-bottom: 0.5rem;
                text-shadow: 0px 2px 4px rgba(0,0,0,0.1);
            }}
            
            /* Language Selector */
            .language-selector {{
                display: flex;
                justify-content: center;
                gap: 0.5rem;
                margin-bottom: 1rem;
            }}
            
            .lang-btn {{
                background: rgba(255, 255, 255, 0.9);
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 0.5rem 1rem;
                font-weight: 600;
                transition: all 0.3s ease;
                cursor: pointer;
            }}
            
            .lang-btn:hover {{
                background: #3b82f6;
                color: white;
                border-color: #3b82f6;
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
            }}
            
            .lang-btn.active {{
                background: #3b82f6;
                color: white;
                border-color: #3b82f6;
            }}
            
            /* Upload Section */
            .upload-section {{
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 400px;
                margin: 2rem 0;
            }}
            
            .upload-area {{
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(248, 250, 252, 0.95));
                border: 2px dashed #cbd5e1;
                border-radius: 16px;
                padding: 3rem;
                text-align: center;
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
                min-width: 500px;
            }}
            
            .upload-area::before {{
                content: "";
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: linear-gradient(45deg, transparent, rgba(59, 130, 246, 0.05), transparent);
                animation: shimmer 3s infinite;
            }}
            
            @keyframes shimmer {{
                0% {{ transform: translateX(-100%) translateY(-100%) rotate(45deg); }}
                100% {{ transform: translateX(100%) translateY(100%) rotate(45deg); }}
            }}
            
            .upload-area:hover {{
                border-color: #3b82f6;
                background: linear-gradient(135deg, rgba(239, 246, 255, 0.95), rgba(219, 234, 254, 0.95));
                transform: translateY(-2px);
                box-shadow: 0 8px 30px rgba(59, 130, 246, 0.2);
            }}
            
            /* Section Headers */
            .section-header {{
                font-size: 1.8rem;
                font-weight: 700;
                color: #1e40af;
                margin: 2rem 0 1rem 0;
                padding-bottom: 0.5rem;
                border-bottom: 3px solid #3b82f6;
                position: relative;
            }}
            
            /* Cards */
            .info-card {{
                background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
                border: 1px solid #bae6fd;
                border-radius: 12px;
                padding: 1.5rem;
                margin: 1rem 0;
                box-shadow: 0 4px 15px rgba(59, 130, 246, 0.1);
                transition: all 0.3s ease;
            }}
            
            .info-card:hover {{
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(59, 130, 246, 0.2);
            }}
            
            .success-card {{
                background: linear-gradient(135deg, #f0fdf4, #dcfce7);
                border: 1px solid #bbf7d0;
                border-radius: 12px;
                padding: 1.5rem;
                margin: 1rem 0;
                box-shadow: 0 4px 15px rgba(34, 197, 94, 0.1);
            }}
            
            .warning-card {{
                background: linear-gradient(135deg, #fffbeb, #fef3c7);
                border: 1px solid #fde047;
                border-radius: 12px;
                padding: 1.5rem;
                margin: 1rem 0;
                box-shadow: 0 4px 15px rgba(251, 191, 36, 0.1);
            }}
            
            /* Instructions */
            .instructions-container {{
                background: rgba(255, 255, 255, 0.9);
                padding: 2rem;
                border-radius: 15px;
                border: 1px solid #e5e7eb;
                margin: 1rem 0;
            }}
            
            .feature-box {{
                background: #f8fafc;
                padding: 1rem;
                border-radius: 10px;
                margin: 1rem 0;
                border-left: 4px solid #3b82f6;
            }}
            
            .feature-box.association {{
                border-left-color: #dc2626;
            }}
            
            .feature-box.formats {{
                background: linear-gradient(135deg, #f0fdf4, #dcfce7);
                border-left-color: #22c55e;
            }}
            
            .feature-box.tip {{
                background: linear-gradient(135deg, #eff6ff, #dbeafe);
                border-left-color: #3b82f6;
            }}
            
            /* Responsive Design */
            @media (max-width: 768px) {{
                .main-container {{
                    padding: 1rem;
                    margin: 0.5rem;
                }}
                
                .upload-area {{
                    min-width: auto;
                    padding: 2rem 1rem;
                }}
                
                .main-title {{
                    font-size: 2rem;
                }}
            }}
            
            /* Gradient Animation */
            @keyframes gradientShift {{
                0% {{ background-position: 0% 50%; }}
                50% {{ background-position: 100% 50%; }}
                100% {{ background-position: 0% 50%; }}
            }}
        </style>
        """, unsafe_allow_html=True)
    
    def get_background_styles(self):
        """Load background image or use gradient fallback"""
        background_styles = []
        
        # Try to load background.jpg from current directory
        try:
            if os.path.exists('background.jpg'):
                with open('background.jpg', 'rb') as f:
                    image_data = f.read()
                encoded = base64.b64encode(image_data).decode()
                background_styles.append(f"""
                    .stApp {{
                        background-image: url("data:image/jpeg;base64,{encoded}");
                        background-size: cover;
                        background-position: center;
                        background-repeat: no-repeat;
                        background-attachment: fixed;
                    }}
                """)
                return background_styles
        except Exception as e:
            print(f"Error loading background.jpg: {e}")
        
        # Fallback to gradient
        background_styles.append("""
            .stApp {
                background: linear-gradient(135deg, #0f172a 0%, #1e293b 25%, #334155 50%, #1e293b 75%, #0f172a 100%);
                background-size: 400% 400%;
                animation: gradientShift 15s ease infinite;
            }
        """)
        
        return background_styles
    
    def get_translation(self, key):
        """Get translation for current language"""
        return TRANSLATIONS[st.session_state.language].get(key, key)
    
    def change_language(self, lang):
        """Change application language"""
        st.session_state.language = lang
        st.rerun()
    
    def load_data(self, file):
        """Load and validate data from uploaded file"""
        try:
            if file.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file)
            elif file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                st.error(self.get_translation("error_no_file"))
                return None
            return df
        except Exception as e:
            st.error(f"{self.get_translation('error_loading_file')} {str(e)}")
            return None
    
    def get_column_types(self, df):
        """Identify numerical and categorical columns"""
        numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        return numerical_cols, categorical_cols
    
    def render_language_selector(self):
        """Render language selection buttons"""
        col1, col2, col3, col4 = st.columns([1, 1, 6, 1])
        
        with col1:
            is_active_id = st.session_state.language == 'id'
            btn_class = "active" if is_active_id else ""
            st.markdown(f"""
            <button class="lang-btn {btn_class}" onclick="window.location.reload(); location.href='?lang=id'">
                🇮🇩 ID
            </button>
            """, unsafe_allow_html=True)
            
            if st.button("🇮🇩 ID", key="lang_id"):
                self.change_language('id')
        
        with col2:
            is_active_en = st.session_state.language == 'en'
            btn_class = "active" if is_active_en else ""
            st.markdown(f"""
            <button class="lang-btn {btn_class}" onclick="window.location.reload(); location.href='?lang=en'">
                🇬🇧 EN
            </button>
            """, unsafe_allow_html=True)
            
            if st.button("🇬🇧 EN", key="lang_en"):
                self.change_language('en')
    
    def render_header(self):
        """Render application header"""
        st.markdown(f"""
        <div class="app-header">
            <h1 class="main-title">{self.get_translation("title")}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    def render_upload_section(self):
        """Render file upload section"""
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="upload-area">', unsafe_allow_html=True)
            
            # Upload title and description
            st.markdown(f'<h2 style="color: #1e40af; margin-bottom: 1rem;">{self.get_translation("upload_title")}</h2>', unsafe_allow_html=True)
            st.markdown(f'<p style="color: #64748b; margin-bottom: 2rem;">{self.get_translation("upload_description")}</p>', unsafe_allow_html=True)
            
            # File uploader
            uploaded_file = st.file_uploader(
                self.get_translation("upload_button"),
                type=['xlsx', 'xls', 'csv'],
                key="main_file_uploader"
            )
            
            # Handle file upload
            if uploaded_file is not None:
                with st.spinner("Loading data..."):
                    df = self.load_data(uploaded_file)
                    if df is not None:
                        st.session_state.data = df
                        st.session_state.uploaded_file = uploaded_file
                        st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def render_instructions(self):
        """Render usage instructions"""
        st.markdown(f"""
        <div class="instructions-container">
            <h2 style="color: #1e40af; margin-bottom: 1rem;">{self.get_translation("instructions")}</h2>
            <ol style="color: #374151; line-height: 1.6;">
                <li><strong style="color: #3b82f6;">{self.get_translation("upload_step")}</strong></li>
                <li><strong style="color: #7c3aed;">{self.get_translation("analysis_step")}</strong></li>
                <li><strong style="color: #dc2626;">{self.get_translation("export_step")}</strong></li>
            </ol>
            
            <h3 style="color: #1e40af; margin: 1.5rem 0;">{self.get_translation("features_title")}</h3>
            
            <div class="feature-box">
                <h4 style="color: #1e40af; margin-bottom: 0.5rem;">{self.get_translation("descriptive_features")}</h4>
                <ul style="color: #374151; line-height: 1.5;">
                    <li>Statistik dasar (mean, median, modus, standar deviasi)</li>
                    <li>Visualisasi distribusi data</li>
                    <li>Analisis missing values</li>
                    <li>Matriks korelasi</li>
                </ul>
            </div>
            
            <div class="feature-box association">
                <h4 style="color: #dc2626; margin-bottom: 0.5rem;">{self.get_translation("association_features")}</h4>
                <ul style="color: #374151; line-height: 1.5;">
                    <li>Uji Chi-Square untuk variabel kategorikal</li>
                    <li>Analisis korelasi untuk variabel numerik</li>
                    <li>ANOVA untuk analisis kategorikal vs numerik</li>
                    <li>Visualisasi hubungan antar variabel</li>
                </ul>
            </div>
            
            <div class="feature-box formats">
                <h4 style="color: #ea580c; margin-bottom: 0.5rem;">{self.get_translation("supported_formats")}</h4>
                <ul style="color: #374151; line-height: 1.5;">
                    <li>Excel (.xlsx, .xls)</li>
                    <li>CSV (.csv)</li>
                </ul>
            </div>
            
            <div class="feature-box tip">
                <p style="color: #1e40af; margin: 0; font-weight: 600;">💡 <strong>Tip</strong>: {self.get_translation("tip")}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def render_success_message(self, df, uploaded_file):
        """Render success message after data upload"""
        st.markdown(f"""
        <div class="success-card">
            <h3 style="color: #166534; margin-bottom: 1rem;">
                {self.get_translation("success_message")} {df.shape[0]:,} {self.get_translation("rows_text")} dan {df.shape[1]} {self.get_translation("columns_text")}
            </h3>
            <div class="info-card">
                <strong>📁 {uploaded_file.name}</strong> ({uploaded_file.size / 1024 / 1024:.2f} MB)
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def perform_descriptive_analysis(self, df, numerical_cols, categorical_cols):
        """Perform and display descriptive analysis"""
        st.markdown(f'<div class="section-header">{self.get_translation("descriptive_analysis")}</div>', unsafe_allow_html=True)
        
        # Dataset Overview
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f'<div style="font-size: 1.3rem; font-weight: 600; color: #1e40af; margin: 1rem 0;">{self.get_translation("dataset_overview")}</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="info-card">
                <strong>{self.get_translation("rows_text")}</strong> {df.shape[0]:,}<br>
                <strong>{self.get_translation("columns_text")}</strong> {df.shape[1]}<br>
                <strong>{self.get_translation("numerical_columns")}</strong> {len(numerical_cols)}<br>
                <strong>{self.get_translation("categorical_columns")}</strong> {len(categorical_cols)}
            </div>
            """, unsafe_allow_html=True)
            
            # Missing values analysis
            missing_data = df.isnull().sum()
            if missing_data.sum() > 0:
                st.markdown(f'<div style="font-size: 1.3rem; font-weight: 600; color: #f59e0b; margin: 1rem 0;">{self.get_translation("missing_values")}</div>', unsafe_allow_html=True)
                missing_df = pd.DataFrame({
                    self.get_translation("columns"): missing_data.index,
                    'Jumlah Missing': missing_data.values,
                    'Persentase': (missing_data.values / len(df) * 100).round(2)
                })
                missing_df = missing_df[missing_df['Jumlah Missing'] > 0]
                st.dataframe(missing_df, use_container_width=True)
        
        with col2:
            # Numerical statistics
            if numerical_cols:
                st.markdown(f'<div style="font-size: 1.3rem; font-weight: 600; color: #059669; margin: 1rem 0;">{self.get_translation("numerical_stats")}</div>', unsafe_allow_html=True)
                stats_df = df[numerical_cols].describe().round(2)
                st.dataframe(stats_df, use_container_width=True)
        
        # Data Visualization
        if numerical_cols:
            st.markdown(f'<div style="font-size: 1.3rem; font-weight: 600; color: #1e40af; margin: 1rem 0;">{self.get_translation("data_visualization")}</div>', unsafe_allow_html=True)
            
            selected_num_col = st.selectbox(self.get_translation("select_numerical_column"), options=numerical_cols)
            
            col1, col2 = st.columns(2)
            with col1:
                # Histogram
                fig_hist = px.histogram(df, x=selected_num_col, title=f'Distribusi {selected_num_col}',
                                       nbins=30, marginal='box')
                fig_hist.update_layout(height=400)
                st.plotly_chart(fig_hist, use_container_width=True)
            
            with col2:
                # Box plot
                fig_box = px.box(df, y=selected_num_col, title=f'Box Plot {selected_num_col}')
                fig_box.update_layout(height=400)
                st.plotly_chart(fig_box, use_container_width=True)
            
            # Correlation matrix
            if len(numerical_cols) > 1:
                st.markdown(f'<div style="font-size: 1.3rem; font-weight: 600; color: #7c3aed; margin: 1rem 0;">{self.get_translation("correlation_matrix")}</div>', unsafe_allow_html=True)
                correlation_matrix = df[numerical_cols].corr()
                
                fig_corr = px.imshow(correlation_matrix, 
                                    text_auto=True, 
                                    aspect="auto",
                                    color_continuous_scale='RdBu_r',
                                    title=self.get_translation("correlation_matrix"))
                fig_corr.update_layout(height=500)
                st.plotly_chart(fig_corr, use_container_width=True)
        
        # Categorical analysis
        if categorical_cols:
            st.markdown(f'<div style="font-size: 1.3rem; font-weight: 600; color: #dc2626; margin: 1rem 0;">{self.get_translation("categorical_analysis")}</div>', unsafe_allow_html=True)
            
            selected_cat_col = st.selectbox(self.get_translation("select_categorical_column"), options=categorical_cols)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Pie chart
                value_counts = df[selected_cat_col].value_counts()
                fig_pie = px.pie(values=value_counts.values, 
                                names=value_counts.index, 
                                title=f'Distribusi {selected_cat_col}')
                fig_pie.update_layout(height=400)
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                # Bar chart
                fig_bar = px.bar(x=value_counts.index, 
                               y=value_counts.values,
                               title=f'Frekuensi {selected_cat_col}')
                fig_bar.update_layout(height=400, xaxis_title=selected_cat_col, yaxis_title='Frekuensi')
                st.plotly_chart(fig_bar, use_container_width=True)
            
            # Frequency table
            st.markdown(f'<div style="font-size: 1.3rem; font-weight: 600; color: #0891b2; margin: 1rem 0;">{self.get_translation("frequency_table")}</div>', unsafe_allow_html=True)
            freq_table = pd.DataFrame({
                self.get_translation("category"): value_counts.index,
                self.get_translation("frequency"): value_counts.values,
                self.get_translation("percentage"): (value_counts.values / len(df) * 100).round(2)
            })
            st.dataframe(freq_table, use_container_width=True)
    
    def perform_association_analysis(self, df, numerical_cols, categorical_cols):
        """Perform and display association analysis"""
        st.markdown(f'<div class="section-header">{self.get_translation("association_analysis")}</div>', unsafe_allow_html=True)
        
        # Chi-Square Test
        if len(categorical_cols) >= 2:
            st.markdown(f'<div style="font-size: 1.3rem; font-weight: 600; color: #ea580c; margin: 1rem 0;">{self.get_translation("chi_square_test")}</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                var1 = st.selectbox(self.get_translation("select_variable_1"), options=categorical_cols, key='cat1')
            with col2:
                var2 = st.selectbox(self.get_translation("select_variable_2"), [col for col in categorical_cols if col != var1], key='cat2')
            
            if st.button(self.get_translation("analyze_chi_square")):
                # Create contingency table
                contingency_table = pd.crosstab(df[var1], df[var2])
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f'<div style="font-size: 1.1rem; font-weight: 600; color: #dc2626; margin: 0.5rem 0;">{self.get_translation("contingency_table")}</div>', unsafe_allow_html=True)
                    st.dataframe(contingency_table, use_container_width=True)
                
                with col2:
                    # Perform chi-square test
                    chi2, p_value, dof, expected = chi2_contingency(contingency_table)
                    
                    st.markdown(f'<div style="font-size: 1.1rem; font-weight: 600; color: #059669; margin: 0.5rem 0;">{self.get_translation("chi_square_results")}</div>', unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="info-card">
                        <strong>Chi-Square Statistic:</strong> {chi2:.4f}<br>
                        <strong>P-value:</strong> {p_value:.4f}<br>
                        <strong>Signifikansi:</strong> {'✅ ' + self.get_translation("significant") if p_value < 0.05 else '❌ ' + self.get_translation("not_significant")}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Interpretation
                    if p_value < 0.05:
                        st.markdown(f"""
                        <div class="warning-card">
                            <strong>💡 {self.get_translation("significant_association")}</strong> {var1} dan {var2}.
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="warning-card">
                            <strong>💡 {self.get_translation("no_significant_association")}</strong> {var1} dan {var2}.
                        </div>
                        """, unsafe_allow_html=True)
        
        # Correlation Analysis
        if len(numerical_cols) >= 2:
            st.markdown(f'<div style="font-size: 1.3rem; font-weight: 600; color: #0891b2; margin: 1rem 0;">{self.get_translation("correlation_analysis")}</div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                var3 = st.selectbox(self.get_translation("select_variable_1"), options=numerical_cols, key='num1')
            with col2:
                var4 = st.selectbox(self.get_translation("select_variable_2"), [col for col in numerical_cols if col != var3], key='num2')
            with col3:
                correlation_method = st.selectbox(self.get_translation("correlation_method"), 
                                               [self.get_translation("pearson"), self.get_translation("spearman")])
            
            if st.button(self.get_translation("analyze_correlation")):
                # Clean data for correlation analysis
                clean_df = df[[var3, var4]].dropna()
                
                if len(clean_df) < 3:
                    st.error("Not enough data points for correlation analysis")
                    return
                
                # Calculate correlation
                if correlation_method == self.get_translation("pearson"):
                    corr_coef, p_value = stats.pearsonr(clean_df[var3], clean_df[var4])
                else:
                    corr_coef, p_value = stats.spearmanr(clean_df[var3], clean_df[var4])
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f'<div style="font-size: 1.1rem; font-weight: 600; color: #0d9488; margin: 0.5rem 0;">{self.get_translation("correlation_results")}</div>', unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="info-card">
                        <strong>Koefisien Korelasi ({correlation_method}):</strong> {corr_coef:.4f}<br>
                        <strong>P-value:</strong> {p_value:.4f}<br>
                        <strong>Signifikansi:</strong> {'✅ ' + self.get_translation("significant") if p_value < 0.05 else '❌ ' + self.get_translation("not_significant")}
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Scatter plot
                    fig_scatter = px.scatter(clean_df, x=var3, y=var4, 
                                           title=f'Scatter Plot: {var3} vs {var4}',
                                           trendline='ols')
                    fig_scatter.update_layout(height=400)
                    st.plotly_chart(fig_scatter, use_container_width=True)
        
        # ANOVA Test (Categorical vs Numerical)
        if numerical_cols and categorical_cols:
            st.markdown(f'<div style="font-size: 1.3rem; font-weight: 600; color: #0891b2; margin: 1rem 0;">{self.get_translation("categorical_numerical_analysis")}</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                cat_var = st.selectbox(self.get_translation("select_categorical_variable"), options=categorical_cols, key='cat_num')
            with col2:
                num_var = st.selectbox(self.get_translation("select_numerical_variable"), options=numerical_cols, key='num_cat')
            
            if st.button(self.get_translation("analyze_categorical_numerical")):
                # Group by categorical variable
                grouped_data = df.groupby(cat_var)[num_var].describe()
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f'<div style="font-size: 1.1rem; font-weight: 600; color: #0d9488; margin: 0.5rem 0;">Statistik {num_var} berdasarkan {cat_var}</div>', unsafe_allow_html=True)
                    st.dataframe(grouped_data.round(2), use_container_width=True)
                
                with col2:
                    # Box plot by category
                    fig_box_cat = px.box(df, x=cat_var, y=num_var, 
                                       title=f'Distribusi {num_var} berdasarkan {cat_var}')
                    fig_box_cat.update_layout(height=400)
                    st.plotly_chart(fig_box_cat, use_container_width=True)
                
                # ANOVA test
                categories = df[cat_var].unique()
                category_groups = [df[df[cat_var] == cat][num_var].dropna() for cat in categories]
                
                # Remove empty groups
                category_groups = [group for group in category_groups if len(group) > 0]
                
                if len(category_groups) >= 2:
                    f_stat, p_value = stats.f_oneway(*category_groups)
                    
                    st.markdown(f'<div style="font-size: 1.1rem; font-weight: 600; color: #dc2626; margin: 0.5rem 0;">{self.get_translation("anova_results")}</div>', unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="info-card">
                        <strong>F-statistic:</strong> {f_stat:.4f}<br>
                        <strong>P-value:</strong> {p_value:.4f}<br>
                        <strong>Signifikansi:</strong> {'✅ ' + self.get_translation("significant") if p_value < 0.05 else '❌ ' + self.get_translation("not_significant")}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if p_value < 0.05:
                        st.markdown(f"""
                        <div class="warning-card">
                            <strong>💡 {self.get_translation("significant_difference")}</strong> {num_var} {self.get_translation("mean_difference")} {cat_var}.
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="warning-card">
                            <strong>💡 {self.get_translation("no_significant_difference")}</strong> {num_var} {self.get_translation("no_mean_difference")}.
                        </div>
                        """, unsafe_allow_html=True)
    
    def run(self):
        """Main application runner"""
        # Render language selector
        self.render_language_selector()
        
        # Render header
        self.render_header()
        
        # Main container
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        
        if st.session_state.data is None:
            # Show upload section
            self.render_upload_section()
            self.render_instructions()
        else:
            # Show analysis section
            df = st.session_state.data
            uploaded_file = st.session_state.uploaded_file
            
            # Success message
            self.render_success_message(df, uploaded_file)
            
            # Get column types
            numerical_cols, categorical_cols = self.get_column_types(df)
            
            # Create tabs
            tab1, tab2 = st.tabs([
                self.get_translation("descriptive_analysis"), 
                self.get_translation("association_analysis")
            ])
            
            with tab1:
                self.perform_descriptive_analysis(df, numerical_cols, categorical_cols)
            
            with tab2:
                self.perform_association_analysis(df, numerical_cols, categorical_cols)
            
            # Upload new file button
            if st.button(self.get_translation("upload_new_file"), key="upload_new"):
                st.session_state.data = None
                st.session_state.uploaded_file = None
                st.rerun()
        
        # Close main container
        st.markdown('</div>', unsafe_allow_html=True)

# Main execution
if __name__ == "__main__":
    app = SurveyAnalysisApp()
    app.run()
