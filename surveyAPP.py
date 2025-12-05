import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
from scipy.stats import chi2_contingency
import base64
import os

# Page configuration
st.set_page_config(
    page_title="Analisis Data Survei",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Multi-language support - ONLY INDONESIA AND ENGLISH
LANGUAGES = {
    "id": {
        "title": "Analisis Data Survei",
        "upload_title": "📊 Unggah File Excel Anda untuk Memulai Analisis",
        "upload_description": "Seret dan lepas file di sini<br>Batas 200MB per file • Format XLSX, XLS, CSV",
        "upload_button": "📁 Pilih File Excel/CSV",
        "file_info_name": "📁",
        "file_size": "Ukuran",
        "success_message": "✅ Data berhasil dimuat! Dataset memiliki",
        "rows_text": "baris",
        "columns_text": "kolom",
        "numerical_columns": "Kolom Numerik",
        "categorical_columns": "Kolom Kategorikal",
        "descriptive_analysis": "📈 Analisis Deskriptif",
        "association_analysis": "🔗 Analisis Asosiasi",
        "export_results": "💾 Export Hasil Analisis",
        "dataset_overview": "📊 Dataset Overview",
        "missing_values": "🔍 Missing Values",
        "numerical_stats": "🔢 Statistik Numerik",
        "data_visualization": "📊 Visualisasi Data",
        "correlation_matrix": "🔗 Matriks Korelasi",
        "categorical_analysis": "📋 Analisis Kategorikal",
        "frequency_table": "📊 Tabel Frekuensi",
        "chi_square_test": "🎯 Uji Chi-Square",
        "correlation_analysis": "📊 Analisis Korelasi",
        "anova_test": "🔄 Uji ANOVA",
        "insights_header": "💡 AI Insights",
        "ask_ai": "Tanyakan AI tentang data Anda",
        "ask_ai_placeholder": "Contoh: Apa perilaku pelanggan yang paling umum?",
        "getting_insights": "Mendapatkan wawasan...",
        "download_summary": "Download Ringkasan Laporan",
        "instructions": "🚀 Cara Menggunakan Aplikasi Ini",
        "upload_step": "Upload file Excel (.xlsx) atau CSV (.csv)",
        "analysis_step": "Pilih analisis yang ingin dilakukan",
        "export_step": "Download hasil analisis dalam format CSV",
        "features_title": "📋 Fitur Utama",
        "descriptive_features": "📈 Analisis Deskriptif",
        "descriptive_list": "Statistik dasar (mean, median, modus, standar deviasi), Visualisasi distribusi data, Analisis missing values, Matriks korelasi",
        "association_features": "🔗 Analisis Asosiasi",
        "association_list": "Uji Chi-Square untuk variabel kategorikal, Analisis korelasi (Pearson/Spearman) untuk variabel numerik, ANOVA untuk analisis kategorikal vs numerik, Visualisasi hubungan variabel",
        "supported_formats": "📊 Format File yang Didukung",
        "format_list": "Excel (.xlsx, .xls), CSV (.csv)",
        "tip": "Pastikan data Anda memiliki header yang jelas dan format yang konsisten untuk hasil analisis yang optimal.",
        "language_selector": "Pilih Bahasa:",
        "indonesian": "🇮🇩 Indonesia",
        "english": "🇬🇧 English",
        "error_no_file": "Silakan upload file terlebih dahulu!",
        "select_numerical_column": "Pilih kolom numerik:",
        "select_categorical_column": "Pilih kolom kategorikal:",
        "select_variable_1": "Pilih variabel 1:",
        "select_variable_2": "Pilih variabel 2:",
        "analyze_chi_square": "Analisis Chi-Square",
        "contingency_table": "Tabel Kontingensi",
        "chi_square_results": "Hasil Chi-Square",
        "significant": "Signifikan",
        "not_significant": "Tidak Signifikan",
        "significant_association": "Ada hubungan signifikan antara",
        "no_significant_association": "Tidak ada hubungan signifikan antara",
        "correlation_method": "Metode Korelasi",
        "pearson": "Pearson",
        "spearman": "Spearman",
        "analyze_correlation": "Analisis Korelasi",
        "correlation_results": "Hasil Korelasi",
        "correlation_insight": "Ada hubungan",
        "correlation_strength": "sangat kuat" if abs(0.8) >= 0.8 else "kuat" if abs(0.8) >= 0.6 else "sedang" if abs(0.8) >= 0.4 else "lemah" if abs(0.8) >= 0.2 else "sangat lemah",
        "positive": "positif",
        "negative": "negatif",
        "categorical_numerical_analysis": "Analisis Kategorikal vs Numerik",
        "select_categorical_variable": "Pilih variabel kategorikal:",
        "select_numerical_variable": "Pilih variabel numerik:",
        "analyze_categorical_numerical": "Analisis Kategorikal-Numerik",
        "anova_results": "Hasil ANOVA",
        "significant_difference": "Ada perbedaan signifikan dalam rata-rata",
        "mean_difference": "antara kategori",
        "no_significant_difference": "Tidak ada perbedaan signifikan dalam rata-rata",
        "no_mean_difference": "antara kategori",
        "total_rows": "Total Baris",
        "total_columns": "Total Kolom",
        "category": "Kategori",
        "frequency": "Frekuensi",
        "percentage": "Persentase"
    },
    "en": {
        "title": "Survey Data Analysis",
        "upload_title": "📊 Upload Your Excel File to Start Analysis",
        "upload_description": "Drag and drop file here<br>Limit 200MB per file • XLSX, XLS, CSV formats",
        "upload_button": "📁 Browse Excel/CSV Files",
        "file_info_name": "📁",
        "file_size": "Size",
        "success_message": "✅ Data successfully loaded! Dataset has",
        "rows_text": "rows",
        "columns_text": "columns",
        "numerical_columns": "Numerical Columns",
        "categorical_columns": "Categorical Columns",
        "descriptive_analysis": "📈 Descriptive Analysis",
        "association_analysis": "🔗 Association Analysis",
        "export_results": "💾 Export Analysis Results",
        "dataset_overview": "📊 Dataset Overview",
        "missing_values": "🔍 Missing Values",
        "numerical_stats": "🔢 Numerical Statistics",
        "data_visualization": "📊 Data Visualization",
        "correlation_matrix": "🔗 Correlation Matrix",
        "categorical_analysis": "📋 Categorical Analysis",
        "frequency_table": "📊 Frequency Table",
        "chi_square_test": "🎯 Chi-Square Test",
        "correlation_analysis": "📊 Correlation Analysis",
        "anova_test": "🔄 ANOVA Test",
        "insights_header": "💡 AI Insights",
        "ask_ai": "Ask AI about your data",
        "ask_ai_placeholder": "Example: What are the most common customer behaviors?",
        "getting_insights": "Getting insights...",
        "download_summary": "Download Summary Report",
        "instructions": "🚀 How to Use This Application",
        "upload_step": "Upload Excel (.xlsx) or CSV (.csv) file",
        "analysis_step": "Choose an analysis to perform",
        "export_step": "Download analysis results in CSV format",
        "features_title": "📋 Main Features",
        "descriptive_features": "📈 Descriptive Analysis",
        "descriptive_list": "Basic statistics (mean, median, mode, standard deviation), Data distribution visualization, Missing values analysis, Correlation matrix",
        "association_features": "🔗 Association Analysis",
        "association_list": "Chi-Square test for categorical variables, Correlation analysis (Pearson/Spearman) for numerical variables, ANOVA for categorical vs numerical analysis, Variable relationship visualization",
        "supported_formats": "📊 Supported File Formats",
        "format_list": "Excel (.xlsx, .xls), CSV (.csv)",
        "tip": "Ensure your data has clear headers and consistent format for optimal analysis results.",
        "language_selector": "Select Language:",
        "indonesian": "🇮🇩 Indonesia",
        "english": "🇬🇧 English",
        "error_no_file": "Please upload a file first!",
        "select_numerical_column": "Select numerical column:",
        "select_categorical_column": "Select categorical column:",
        "select_variable_1": "Select variable 1:",
        "select_variable_2": "Select variable 2:",
        "analyze_chi_square": "Analyze Chi-Square",
        "contingency_table": "Contingency Table",
        "chi_square_results": "Chi-Square Results",
        "significant": "Significant",
        "not_significant": "Not Significant",
        "significant_association": "There is a significant association between",
        "no_significant_association": "There is no significant association between",
        "correlation_method": "Correlation Method",
        "pearson": "Pearson",
        "spearman": "Spearman",
        "analyze_correlation": "Analyze Correlation",
        "correlation_results": "Correlation Results",
        "correlation_insight": "There is a",
        "correlation_strength": "very strong" if abs(0.8) >= 0.8 else "strong" if abs(0.8) >= 0.6 else "moderate" if abs(0.8) >= 0.4 else "weak" if abs(0.8) >= 0.2 else "very weak",
        "positive": "positive",
        "negative": "negative",
        "categorical_numerical_analysis": "Categorical vs Numerical Analysis",
        "select_categorical_variable": "Select categorical variable:",
        "select_numerical_variable": "Select numerical variable:",
        "analyze_categorical_numerical": "Analyze Categorical-Numerical",
        "anova_results": "ANOVA Results",
        "significant_difference": "There is a significant difference in the mean",
        "mean_difference": "between categories",
        "no_significant_difference": "There is no significant difference in the mean",
        "no_mean_difference": "between categories",
        "total_rows": "Total Rows",
        "total_columns": "Total Columns",
        "category": "Category",
        "frequency": "Frequency",
        "percentage": "Percentage"
    }
}

def load_background_styles():
    """Load background image styles"""
    background_styles = []
    
    # Method 1: Try to load from current directory
    try:
        if os.path.exists('background_digital.png'):
            with open('background_digital.png', 'rb') as f:
                image_data = f.read()
            encoded = base64.b64encode(image_data).decode()
            background_styles.append(f"""
                .stApp {{
                    background-image: url("data:image/png;base64,{encoded}");
                    background-size: cover;
                    background-position: center;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                }}
            """)
    except Exception as e:
        print(f"Error loading background: {e}")
    
    # Method 2: Try to load from assets folder
    try:
        if os.path.exists('assets/background.jpg'):
            with open('assets/background.jpg', 'rb') as f:
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
        elif os.path.exists('assets/background.png'):
            with open('assets/background.png', 'rb') as f:
                image_data = f.read()
            encoded = base64.b64encode(image_data).decode()
            background_styles.append(f"""
                .stApp {{
                    background-image: url("data:image/png;base64,{encoded}");
                    background-size: cover;
                    background-position: center;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                }}
            """)
    except Exception as e:
        print(f"Error loading background from assets: {e}")
    
    # If no background found, use gradient fallback
    if not background_styles:
        background_styles.append("""
            .stApp {
                background: linear-gradient(135deg, #0f172a 0%, #1e293b 25%, #334155 50%, #1e293b 75%, #0f172a 100%);
                background-size: 400% 400%;
                animation: gradientShift 15s ease infinite;
            }
            """)
    
    return background_styles

def apply_custom_styles():
    """Apply custom CSS styles"""
    background_styles = load_background_styles()
    
    st.markdown(f"""
    <style>
        {"".join(background_styles)}
        
        /* Global styles */
        .stApp {{
            background-attachment: fixed;
        }}
        
        /* Main content area with glassmorphism */
        .main .block-container {{
            background: rgba(255, 255, 255, 0.92);
            backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 2rem;
            margin-top: 2rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            max-width: 1000px;
            margin-left: auto;
            margin-right: auto;
        }}
        
        /* Sidebar with professional gradient */
        .css-1d391kg {{
            background: linear-gradient(135deg, rgba(30, 64, 175, 0.95), rgba(55, 48, 163, 0.95));
            backdrop-filter: blur(10px);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .css-1d391kg .stSelectbox > div > div {{
            background-color: rgba(255, 255, 255, 0.95);
            color: #1e293b;
            border-radius: 8px;
        }}
        
        .css-1d391kg .stFileUploader {{
            background-color: rgba(255, 255, 255, 0.1);
            border: 2px dashed rgba(255, 255, 255, 0.4);
            border-radius: 10px;
            padding: 1rem;
        }}
        
        .css-1d391kg .stFileUploader label {{
            color: white;
            font-weight: 500;
        }}
        
        /* Main header with professional blue gradient */
        .main-header {{
            font-size: 2.8rem;
            font-weight: 700;
            background: linear-gradient(135deg, #1e40af, #3b82f6, #60a5fa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-align: center;
            margin-bottom: 1rem;
            text-shadow: 0px 2px 4px rgba(0,0,0,0.1);
            animation: textGlow 3s ease-in-out infinite alternate;
        }}
        
        /* Text glow animation */
        @keyframes textGlow {{
            from {{ filter: drop-shadow(0 0 10px rgba(59, 130, 246, 0.5)); }}
            to {{ filter: drop-shadow(0 0 20px rgba(59, 130, 246, 0.8)); }}
        }}
        
        /* Language selector */
        .language-selector {{
            display: flex;
            justify-content: center;
            gap: 0.5rem;
            margin-bottom: 2rem;
        }}
        
        /* Upload area styling - CENTERED */
        .upload-container {{
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
        
        /* Section headers */
        .section-header {{
            font-size: 1.8rem;
            font-weight: 700;
            color: #1e40af;
            margin: 2rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 3px solid #3b82f6;
            position: relative;
            background: linear-gradient(135deg, #1e40af, #3b82f6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        /* Metric cards */
        .metric-card {{
            background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
            border: 1px solid #bae6fd;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.1);
            transition: all 0.3s ease;
        }}
        
        .metric-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.2);
        }}
        
        /* Success message */
        .success-message {{
            background: linear-gradient(135deg, #f0fdf4, #dcfce7);
            border: 1px solid #bbf7d0;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 15px rgba(34, 197, 94, 0.1);
        }}
        
        /* AI insights box */
        .insights-box {{
            background: linear-gradient(135deg, #fef3c7, #fde68a);
            border: 1px solid #fbbf24;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 15px rgba(251, 191, 36, 0.1);
        }}
        
        /* Buttons */
        .stButton > button {{
            background: linear-gradient(135deg, #3b82f6, #1e40af);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}
        
        .stButton > button::before {{
            content: "";
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.5s ease;
        }}
        
        .stButton > button:hover::before {{
            left: 100%;
        }}
        
        .stButton > button:hover {{
            background: linear-gradient(135deg, #1e40af, #1e3a8a);
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
        }}
        
        /* Select boxes */
        .stSelectbox > div > div {{
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 8px;
            border: 1px solid #d1d5db;
        }}
        
        /* Radio buttons */
        .stRadio > div {{
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 8px;
            padding: 1rem;
            border: 1px solid #e5e7eb;
        }}
        
        /* Tabs */
        .stTabs {{
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 12px;
            padding: 0.5rem;
            border: 1px solid #e5e7eb;
        }}
        
        /* Dataframes */
        .dataframe {{
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }}
        
        /* Expander */
        .streamlit-expanderHeader {{
            background-color: #f8fafc;
            border-radius: 8px;
            font-weight: 600;
            color: #1e40af;
            border: 1px solid #e2e8f0;
        }}
        
        /* Sidebar text */
        .css-1d391kg h3 {{
            color: white;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        }}
        
        .css-1d391kg p {{
            color: rgba(255, 255, 255, 0.9);
            line-height: 1.5;
        }}
        
        /* Spinner */
        .stSpinner {{
            color: #3b82f6;
        }}
        
        /* Language buttons styling */
        .lang-button {{
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid #d1d5db;
            border-radius: 6px;
            padding: 0.5rem 1rem;
            margin: 0 0.25rem;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
            position: relative;
            overflow: hidden;
        }}
        
        .lang-button:hover {{
            background: #3b82f6;
            color: white;
            border-color: #3b82f6;
            transform: translateY(-1px);
        }}
        
        .lang-button.active {{
            background: #3b82f6;
            color: white;
            border-color: #3b82f6;
        }}
        
        /* Language indicator */
        .language-indicator {{
            text-align: center;
            font-size: 0.9rem;
            color: rgba(255, 255, 255, 0.8);
            margin-top: 0.5rem;
            font-weight: 500;
        }}
        
        /* Floating elements for tech feel */
        .floating-element {{
            position: fixed;
            width: 4px;
            height: 4px;
            background: rgba(59, 130, 246, 0.6);
            border-radius: 50%;
            pointer-events: none;
            animation: float 20s infinite linear;
            z-index: 0;
        }}
        
        @keyframes float {{
            0% {{
                transform: translateY(100vh) translateX(0) rotate(0deg);
                opacity: 0;
            }}
            10% {{
                opacity: 1;
            }}
            90% {{
                opacity: 1;
            }}
            100% {{
                transform: translateY(-100vh) translateX(100px) rotate(360deg);
                opacity: 0;
            }}
        }}
        
        /* Add multiple floating elements */
        .floating-element:nth-child(2) {{ animation-delay: 5s; left: 20%; }}
        .floating-element:nth-child(3) {{ animation-delay: 10s; left: 40%; }}
        .floating-element:nth-child(4) {{ animation-delay: 15s; left: 60%; }}
        .floating-element:nth-child(5) {{ animation-delay: 2s; left: 80%; }}
        
        /* Custom file uploader styling */
        .custom-file-upload {{
            position: relative;
            display: inline-block;
            cursor: pointer;
            width: 100%;
        }}
        
        .custom-file-upload input[type=file] {{
            position: absolute;
            left: -9999px;
        }}
        
        .custom-file-upload label {{
            display: block;
            padding: 2rem;
            background: linear-gradient(135deg, #f8fafc, #f1f5f9);
            border: 2px dashed #cbd5e1;
            border-radius: 12px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            color: #475569;
            font-weight: 500;
        }}
        
        .custom-file-upload label:hover {{
            border-color: #3b82f6;
            background: linear-gradient(135deg, #eff6ff, #dbeafe);
            color: #1e40af;
        }}
        
        .custom-file-upload label svg {{
            width: 48px;
            height: 48px;
            margin-bottom: 1rem;
            color: #3b82f6;
        }}
        
        /* File info display */
        .file-info {{
            background: linear-gradient(135deg, #f0fdf4, #dcfce7);
            border: 1px solid #bbf7d0;
            border-radius: 12px;
            padding: 1rem;
            margin: 1rem 0;
            color: #166534;
        }}
        
        /* Gradient animation */
        @keyframes gradientShift {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        
        /* Hide streamlit footer */
        footer {{
            visibility: hidden;
        }}
        
        /* Hide streamlit header */
        .stHeader {{
            visibility: hidden;
        }}
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {{
            width: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: rgba(59, 130, 246, 0.5);
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: rgba(59, 130, 246, 0.7);
        }}
        
        /* Responsive design */
        @media (max-width: 768px) {{
            .main .block-container {{
                padding: 1rem;
                margin: 1rem;
            }}
            
            .upload-area {{
                min-width: auto;
                padding: 2rem 1rem;
            }}
            
            .main-header {{
                font-size: 2rem;
            }}
        }}
    </style>
    
    <div class="floating-element"></div>
    <div class="floating-element"></div>
    <div class="floating-element"></div>
    <div class="floating-element"></div>
    <div class="floating-element"></div>
    """, unsafe_allow_html=True)

# Global state for language
if 'language' not in st.session_state:
    st.session_state.language = "id"

# Helper functions
def load_data(file):
    """Load data from uploaded file"""
    try:
        if file.name.endswith('.xlsx'):
            df = pd.read_excel(file)
        elif file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            st.error(LANGUAGES[st.session_state.language]["error_no_file"])
            return None
        return df
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None

def get_column_types(df):
    """Identify numerical and categorical columns"""
    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    return numerical_cols, categorical_cols

def get_data_summary(df, language="id"):
    """Generate data summary for AI analysis"""
    try:
        if language == "en":
            summary = f"""
            Dataset Shape: {df.shape}
            Columns: {list(df.columns)}
            Data Types: {df.dtypes.value_counts().to_dict()}
            Missing Values: {df.isnull().sum().to_dict()}
            Sample Data (first 5 rows):
        {df.head().to_string()}
            """
        else:  # Indonesian
            summary = f"""
            Dataset Shape: {df.shape}
            Kolom: {list(df.columns)}
            Tipe Data: {df.dtypes.value_counts().to_dict()}
            Missing Values: {df.isnull().sum().to_dict()}
            Sample Data (5 baris teratas):
            {df.head().to_string()}
            """
        
        return summary
    except Exception as e:
        return f"Error generating summary: {str(e)}"

def descriptive_analysis(df, numerical_cols, categorical_cols):
    """Perform descriptive analysis"""
    st.markdown(f'<div class="section-header">{LANGUAGES[st.session_state.language]["descriptive_analysis"]}</div>', unsafe_allow_html=True)
    
    # Basic Statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f'<div style="font-size: 1.3rem; font-weight: 600; color: #1e40af; margin: 1rem 0;">{LANGUAGES[st.session_state.language]["dataset_overview"]}</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="metric-card">
            <strong>{LANGUAGES[st.session_state.language]["rows_text"]}</strong> {df.shape[0]:,}<br>
            <strong>{LANGUAGES[st.session_state.language]["columns_text"]}</strong> {df.shape[1]}<br>
            <strong>{LANGUAGES[st.session_state.language]["numerical_columns"]}</strong> {len(numerical_cols)}<br>
            <strong>{LANGUAGES[st.session_state.language]["categorical_columns"]}</strong> {len(categorical_cols)}
        </div>
        """, unsafe_allow_html=True)
        
        # Missing values
        missing_data = df.isnull().sum()
        if missing_data.sum() > 0:
            st.markdown(f'<div style="font-size: 1.3rem; font-weight: 600; color: #f59e0b; margin: 1rem 0;">{LANGUAGES[st.session_state.language]["missing_values"]}</div>', unsafe_allow_html=True)
            missing_df = pd.DataFrame({
                LANGUAGES[st.session_state.language]["columns"]: missing_data.index,
                'Jumlah Missing': missing_data.values,
                'Persentase': (missing_data.values / len(df) * 100).round(2)
            })
            missing_df = missing_df[missing_df['Jumlah Missing'] > 0]
            st.dataframe(missing_df, use_container_width=True)
    
    with col2:
        # Numerical columns statistics
        if numerical_cols:
            st.markdown(f'<div style="font-size: 1.3rem; font-weight: 600; color: #059669; margin: 1rem 0;">{LANGUAGES[st.session_state.language]["numerical_stats"]}</div>', unsafe_allow_html=True)
            stats_df = df[numerical_cols].describe().round(2)
            st.dataframe(stats_df, use_container_width=True)
    
    # Visualizations
    if numerical_cols:
        st.markdown(f'<div style="font-size: 1.3rem; font-weight: 600; color: #1e40af; margin: 1rem 0;">{LANGUAGES[st.session_state.language]["data_visualization"]}</div>', unsafe_allow_html=True)
        
        # Distribution plots
        selected_num_col = st.selectbox(LANGUAGES[st.session_state.language]["select_numerical_column"], options=numerical_cols)
        
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
        
        # Correlation matrix for numerical variables
        if len(numerical_cols) > 1:
            st.markdown(f'<div style="font-size: 1.3rem; font-weight: 600; color: #7c3aed; margin: 1rem 0;">{LANGUAGES[st.session_state.language]["correlation_matrix"]}</div>', unsafe_allow_html=True)
            correlation_matrix = df[numerical_cols].corr()
            
            fig_corr = px.imshow(correlation_matrix, 
                                text_auto=True, 
                                aspect="auto",
                                color_continuous_scale='RdBu_r',
                                title=LANGUAGES[st.session_state.language]["correlation_matrix"])
            fig_corr.update_layout(height=500)
            st.plotly_chart(fig_corr, use_container_width=True)
    
    # Categorical analysis
    if categorical_cols:
        st.markdown(f'<div style="font-size: 1.3rem; font-weight: 600; color: #dc2626; margin: 1rem 0;">{LANGUAGES[st.session_state.language]["categorical_analysis"]}</div>', unsafe_allow_html=True)
        
        selected_cat_col = st.selectbox(LANGUAGES[st.session_state.language]["select_categorical_column"], options=categorical_cols)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Value counts
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
        st.markdown(f'<div style="font-size: 1.3rem; font-weight: 600; color: #0891b2; margin: 1rem 0;">{LANGUAGES[st.session_state.language]["frequency_table"]}</div>', unsafe_allow_html=True)
        freq_table = pd.DataFrame({
            LANGUAGES[st.session_state.language]["category"]: value_counts.index,
            LANGUAGES[st.session_state.language]["frequency"]: value_counts.values,
            LANGUAGES[st.session_state.language]["percentage"]: (value_counts.values / len(df) * 100).round(2)
        })
        st.dataframe(freq_table, use_container_width=True)

def association_analysis(df, numerical_cols, categorical_cols):
    """Perform association analysis"""
    st.markdown(f'<div class="section-header">{LANGUAGES[st.session_state.language]["association_analysis"]}</div>', unsafe_allow_html=True)
    
    # Chi-square test for categorical variables
    if len(categorical_cols) >= 2:
        st.markdown(f'<div style="font-size: 1.3rem; font-weight: 600; color: #ea580c; margin: 1rem 0;">{LANGUAGES[st.session_state.language]["chi_square_test"]}</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            var1 = st.selectbox(LANGUAGES[st.session_state.language]["select_variable_1"], options=categorical_cols, key='cat1')
        with col2:
            var2 = st.selectbox(LANGUAGES[st.session_state.language]["select_variable_2"], [col for col in categorical_cols if col != var1], key='cat2')
        
        if st.button(LANGUAGES[st.session_state.language]["analyze_chi_square"]):
            # Create contingency table
            contingency_table = pd.crosstab(df[var1], df[var2])
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f'<div style="font-size: 1.1rem; font-weight: 600; color: #dc2626; margin: 0.5rem 0;">{LANGUAGES[st.session_state.language]["contingency_table"]}</div>', unsafe_allow_html=True)
                st.dataframe(contingency_table, use_container_width=True)
            
            with col2:
                # Perform chi-square test
                chi2, p_value, dof, expected = chi2_contingency(contingency_table)
                
                st.markdown(f'<div style="font-size: 1.1rem; font-weight: 600; color: #059669; margin: 0.5rem 0;">{LANGUAGES[st.session_state.language]["chi_square_results"]}</div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="metric-card">
                    <strong>Chi-Square Statistic:</strong> {chi2:.4f}<br>
                    <strong>P-value:</strong> {p_value:.4f}<br>
                    <strong>Signifikansi:</strong> {'✅ Signifikan' if p_value < 0.05 else '❌ Tidak Signifikan'}
                </div>
                """, unsafe_allow_html=True)
                
                if p_value < 0.05:
                    st.markdown(f"""
                    <div class="insights-box">
                        <strong>💡 {LANGUAGES[st.session_state.language]["significant_association"]}</strong> {var1} dan {var2}.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="insights-box">
                        <strong>💡 {LANGUAGES[st.session_state.language]["no_significant_association"]}</strong> {var1} dan {var2}.
                    </div>
                    """, unsafe_allow_html=True)
    
    # Correlation analysis for numerical variables
    if len(numerical_cols) >= 2:
        st.markdown(f'<div style="font-size: 1.3rem; font-weight: 600; color: #0891b2; margin: 1rem 0;">{LANGUAGES[st.session_state.language]["correlation_analysis"]}</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            var3 = st.selectbox(LANGUAGES[st.session_state.language]["select_variable_1"], options=numerical_cols, key='num1')
        with col2:
            var4 = st.selectbox(LANGUAGES[st.session_state.language]["select_variable_2"], [col for col in numerical_cols if col != var3], key='num2')
        with col3:
            correlation_method = st.selectbox(LANGUAGES[st.session_state.language]["correlation_method"], 
                                           [LANGUAGES[st.session_state.language]["pearson"], LANGUAGES[st.session_state.language]["spearman"]])
        
        if st.button(LANGUAGES[st.session_state.language]["analyze_correlation"]):
            # Clean data for correlation analysis
            clean_df = df[[var3, var4]].dropna()
            
            if len(clean_df) < 3:
                st.error("Not enough data points for correlation analysis")
                return
            
            # Calculate correlation
            if correlation_method == LANGUAGES[st.session_state.language]["pearson"]:
                corr_coef, p_value = stats.pearsonr(clean_df[var3], clean_df[var4])
            else:
                corr_coef, p_value = stats.spearmanr(clean_df[var3], clean_df[var4])
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f'<div style="font-size: 1.1rem; font-weight: 600; color: #0d9488; margin: 0.5rem 0;">{LANGUAGES[st.session_state.language]["correlation_results"]}</div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="metric-card">
                    <strong>Koefisien Korelasi ({correlation_method}):</strong> {corr_coef:.4f}<br>
                    <strong>P-value:</strong> {p_value:.4f}<br>
                    <strong>Signifikansi:</strong> {'✅ Signifikan' if p_value < 0.05 else '❌ Tidak Signifikan'}
                </div>
                """, unsafe_allow_html=True)
                
                # Interpretation
                strength = "sangat kuat" if abs(corr_coef) >= 0.8 else "kuat" if abs(corr_coef) >= 0.6 else "sedang" if abs(corr_coef) >= 0.4 else "lemah" if abs(corr_coef) >= 0.2 else "sangat lemah"
                direction = LANGUAGES[st.session_state.language]["positive"] if corr_coef > 0 else LANGUAGES[st.session_state.language]["negative"]
                
                st.markdown(f"""
                <div class="insights-box">
                    <strong>💡 {LANGUAGES[st.session_state.language]["correlation_insight"]}</strong> {strength} {direction} antara {var3} dan {var4}.
                    {"Hubungan ini signifikan secara statistik." if p_value < 0.05 else "Hubungan ini tidak signifikan secara statistik."}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Scatter plot
                fig_scatter = px.scatter(clean_df, x=var3, y=var4, 
                                       title=f'Scatter Plot: {var3} vs {var4}',
                                       trendline='ols')
                fig_scatter.update_layout(height=400)
                st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Categorical vs Numerical analysis
    if numerical_cols and categorical_cols:
        st.markdown(f'<div style="font-size: 1.3rem; font-weight: 600; color: #0891b2; margin: 1rem 0;">{LANGUAGES[st.session_state.language]["categorical_numerical_analysis"]}</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            cat_var = st.selectbox(LANGUAGES[st.session_state.language]["select_categorical_variable"], options=categorical_cols, key='cat_num')
        with col2:
            num_var = st.selectbox(LANGUAGES[st.session_state.language]["select_numerical_variable"], options=numerical_cols, key='num_cat')
        
        if st.button(LANGUAGES[st.session_state.language]["analyze_categorical_numerical"]):
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
                
                st.markdown(f'<div style="font-size: 1.1rem; font-weight: 600; color: #dc2626; margin: 0.5rem 0;">{LANGUAGES[st.session_state.language]["anova_results"]}</div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="metric-card">
                    <strong>F-statistic:</strong> {f_stat:.4f}<br>
                    <strong>P-value:</strong> {p_value:.4f}<br>
                    <strong>Signifikansi:</strong> {'✅ Signifikan' if p_value < 0.05 else '❌ Tidak Signifikan'}
                </div>
                """, unsafe_allow_html=True)
                
                if p_value < 0.05:
                    st.markdown(f"""
                    <div class="insights-box">
                        <strong>💡 {LANGUAGES[st.session_state.language]["significant_difference"]}</strong> {num_var} {LANGUAGES[st.session_state.language]["mean_difference"]} {cat_var}.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="insights-box">
                        <strong>💡 {LANGUAGES[st.session_state.language]["no_significant_difference"]}</strong> {num_var} {LANGUAGES[st.session_state.language]["no_mean_difference"]}.
                    </div>
                    """, unsafe_allow_html=True)
    
    # Export functionality
    st.markdown("---")
    st.markdown(f'<div style="font-size: 1.3rem; font-weight: 600; color: #059669; margin: 1rem 0;">{LANGUAGES[st.session_state.language]["export_results"]}</div>', unsafe_allow_html=True)
            
    if st.button(LANGUAGES[st.session_state.language]["download_summary"]):
        # Create a summary report
        summary_data = {
            'Metric': [LANGUAGES[st.session_state.language]["total_rows"], LANGUAGES[st.session_state.language]["total_columns"], 
                     LANGUAGES[st.session_state.language]["numerical_columns"], LANGUAGES[st.session_state.language]["categorical_columns"], 
                     LANGUAGES[st.session_state.language]["missing_values"]],
            'Value': [df.shape[0], df.shape[1], len(numerical_cols), len(categorical_cols), df.isnull().sum().sum()]
        }
        summary_df = pd.DataFrame(summary_data)
        
        # Convert to CSV
        csv = summary_df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="survey_analysis_summary.csv" style="background: #3b82f6; color: white; padding: 0.75rem 1.5rem; border-radius: 8px; text-decoration: none; font-weight: 600;">Download CSV Summary</a>'
        st.markdown(href, unsafe_allow_html=True)

def main():
    # Apply custom styles
    apply_custom_styles()
    
    # Inisialisasi state bahasa jika belum ada
    if 'language' not in st.session_state:
        st.session_state.language = 'id'  # Default: Indonesia
    
    # Fungsi untuk mengganti bahasa
    def change_language(lang):
        st.session_state.language = lang
    
    # Selector bahasa dengan ikon bendera - ONLY 2 LANGUAGES
    col1, col2, col3, col4 = st.columns([1, 1, 6, 1])
    with col1:
        if st.button("🇮🇩 ID", key="lang_id", help="Bahasa Indonesia"):
            change_language('id')
    with col2:
        if st.button("🇬🇧 EN", key="lang_en", help="English"):
            change_language('en')
    
    # Tampilkan bahasa aktif
    active_lang = "🇮🇩 Indonesia" if st.session_state.language == 'id' else "🇬🇧 English"
    st.markdown(f"<p class='language-indicator'>{active_lang}</p>", unsafe_allow_html=True)
    
    # Main header
    st.markdown(f'<h1 class="main-header">{LANGUAGES[st.session_state.language]["title"]}</h1>', unsafe_allow_html=True)
    
    # File upload section - CENTERED
    if 'data' not in st.session_state:
        st.session_state.data = None
    
    if st.session_state.data is None:
        # Centered upload area
        st.markdown('<div class="upload-container">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f'<div class="upload-area">', unsafe_allow_html=True)
            
            # Upload title
            st.markdown(f'<h2 style="color: #1e40af; margin-bottom: 1rem;">{LANGUAGES[st.session_state.language]["upload_title"]}</h2>', unsafe_allow_html=True)
            st.markdown(f'<p style="color: #64748b; margin-bottom: 2rem;">{LANGUAGES[st.session_state.language]["upload_description"]}</p>', unsafe_allow_html=True)
            
            # Hidden file uploader for functionality
            hidden_file_uploader = st.file_uploader(
                LANGUAGES[st.session_state.language]["upload_button"],
                type=['xlsx', 'xls', 'csv'],
                key="hidden_file_uploader",
                label_visibility="collapsed"
            )
            
            # Visible custom file upload button
            if st.button(LANGUAGES[st.session_state.language]["upload_button"], key="visible_upload_button", use_container_width=True):
                # Trigger the hidden file uploader
                st.rerun()
            
            # Handle file upload
            if hidden_file_uploader is not None:
                with st.spinner(f"{LANGUAGES[st.session_state.language]['getting_insights']}..."):
                    df = load_data(hidden_file_uploader)
                    if df is not None:
                        st.session_state.data = df
                        st.session_state.uploaded_file = hidden_file_uploader
                        st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Instructions section
        st.markdown(f"""
<div style="background: rgba(255, 255, 255, 0.9); padding: 2rem; border-radius: 15px; border: 1px solid #e5e7eb; margin: 1rem 0;">
<h2 style="color: #1e40af; margin-bottom: 1rem;">{LANGUAGES[st.session_state.language]["instructions"]}</h2>
<ol style="color: #374151; line-height: 1.6;">
    <li><strong style="color: #3b82f6;">{LANGUAGES[st.session_state.language]["upload_step"]}</strong></li>
    <li><strong style="color: #7c3aed;">{LANGUAGES[st.session_state.language]["analysis_step"]}</strong></li>
    <li><strong style="color: #dc2626;">{LANGUAGES[st.session_state.language]["export_step"]}</strong></li>
</ol>

<h3 style="color: #1e40af; margin: 1.5rem 0;">{LANGUAGES[st.session_state.language]["features_title"]}</h3>

<div style="background: #f8fafc; padding: 1rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #3b82f6; margin: 1rem 0;">
<h4 style="color: #1e40af; margin: 1.5rem 0;">{LANGUAGES[st.session_state.language]["descriptive_features"]}</h4>
<ul style="color: #374151; line-height: 1.5;">
    {"".join([f"<li>{feature}</li>" for feature in LANGUAGES[st.session_state.language]["descriptive_list"].split(", ")])}
</ul>
</div>

<div style="background: #f8fafc; padding: 1rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #dc2626; margin: 1rem 0;">
<h4 style="color: #dc2626; margin: 1.5rem 0;">{LANGUAGES[st.session_state.language]["association_features"]}</h4>
<ul style="color: #374151; line-height: 1.5;">
    {"".join([f"<li>{feature}</li>" for feature in LANGUAGES[st.session_state.language]["association_list"].split(", ")])}
</ul>
</div>

<div style="background: linear-gradient(135deg, #f0fdf4, #dcfce7); padding: 1rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #22c55e; margin: 1rem 0;">
<h4 style="color: #ea580c; margin: 1.5rem 0;">{LANGUAGES[st.session_state.language]["supported_formats"]}</h4>
<ul style="color: #374151; line-height: 1.5;">
    {"".join([f"<li>{fmt}</li>" for fmt in LANGUAGES[st.session_state.language]["format_list"].split(", ")])}
</ul>
</div>

<div style="background: linear-gradient(135deg, #eff6ff, #dbeafe); padding: 1rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #3b82f6; margin: 1rem 0;">
<p style="color: #1e40af; margin: 0; font-weight: 600;">💡 <strong>Tip</strong>: {LANGUAGES[st.session_state.language]["tip"]}</p>
</div>
</div>
        """, unsafe_allow_html=True)
    
    else:
        # Data loaded successfully
        df = st.session_state.data
        uploaded_file = st.session_state.uploaded_file
        
        # Success message
        st.markdown(f"""
        <div class="success-message">
            <h3 style="color: #166534; margin-bottom: 1rem;">{LANGUAGES[st.session_state.language]["success_message"]} {df.shape[0]:,} {LANGUAGES[st.session_state.language]["rows_text"]} dan {df.shape[1]} {LANGUAGES[st.session_state.language]["columns_text"]}</h3>
            <div class="file-info">
                <strong>{LANGUAGES[st.session_state.language]["file_info_name"]} {uploaded_file.name}</strong> ({uploaded_file.size / 1024 / 1024:.2f} MB)
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Get column types
        numerical_cols, categorical_cols = get_column_types(df)
        
        # Create tabs for different analyses
        tab1, tab2 = st.tabs([LANGUAGES[st.session_state.language]["descriptive_analysis"], LANGUAGES[st.session_state.language]["association_analysis"]])
        
        with tab1:
            descriptive_analysis(df, numerical_cols, categorical_cols)
        
        with tab2:
            association_analysis(df, numerical_cols, categorical_cols)
        
        # Option to upload new file
        if st.button("📁 Upload File Baru", key="upload_new"):
            st.session_state.data = None
            st.session_state.uploaded_file = None
            st.rerun()

if __name__ == "__main__":
    main()
