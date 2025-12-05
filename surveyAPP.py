import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
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
        "success_message": "✅ Data berhasil dimuat! Dataset memiliki",
        "rows_text": "baris",
        "columns_text": "kolom",
        "descriptive_analysis": "📈 Analisis Deskriptif",
        "association_analysis": "🔗 Analisis Asosiasi",
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
        "instructions": "🚀 Cara Menggunakan Aplikasi Ini",
        "upload_step": "Upload file Excel (.xlsx) atau CSV (.csv)",
        "analysis_step": "Pilih analisis yang ingin dilakukan",
        "export_step": "Download hasil analisis dalam format CSV",
        "features_title": "📋 Fitur Utama",
        "descriptive_features": "📈 Analisis Deskriptif",
        "association_features": "🔗 Analisis Asosiasi",
        "supported_formats": "📊 Format File yang Didukung",
        "tip": "Pastikan data Anda memiliki header yang jelas dan format yang konsisten untuk hasil analisis yang optimal.",
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
        "numerical_columns": "Kolom Numerik",
        "categorical_columns": "Kolom Kategorikal",
        "category": "Kategori",
        "frequency": "Frekuensi",
        "percentage": "Persentase",
        "columns": "Kolom"
    },
    "en": {
        "title": "Survey Data Analysis",
        "upload_title": "📊 Upload Your Excel File to Start Analysis",
        "upload_description": "Drag and drop file here<br>Limit 200MB per file • XLSX, XLS, CSV formats",
        "upload_button": "📁 Browse Excel/CSV Files",
        "success_message": "✅ Data successfully loaded! Dataset has",
        "rows_text": "rows",
        "columns_text": "columns",
        "descriptive_analysis": "📈 Descriptive Analysis",
        "association_analysis": "🔗 Association Analysis",
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
        "instructions": "🚀 How to Use This Application",
        "upload_step": "Upload Excel (.xlsx) or CSV (.csv) file",
        "analysis_step": "Choose an analysis to perform",
        "export_step": "Download analysis results in CSV format",
        "features_title": "📋 Main Features",
        "descriptive_features": "📈 Descriptive Analysis",
        "association_features": "🔗 Association Analysis",
        "supported_formats": "📊 Supported File Formats",
        "tip": "Ensure your data has clear headers and consistent format for optimal analysis results.",
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
        "numerical_columns": "Numerical Columns",
        "categorical_columns": "Categorical Columns",
        "category": "Category",
        "frequency": "Frequency",
        "percentage": "Percentage",
        "columns": "Columns"
    }
}

def load_background_styles():
    """Load background image styles"""
    background_styles = []
    
    # Method 1: Try to load from current directory
    try:
        if os.path.exists('background.png'):
            with open('background.png', 'rb') as f:
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
        
        /* Remove top margin and padding */
        .main .block-container {{
            padding-top: 1rem;
            margin-top: 0;
        }}
        
        /* Main content area with glassmorphism */
        .main-content {{
            background: rgba(255, 255, 255, 0.92);
            backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 2rem;
            margin: 1rem auto;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            max-width: 1000px;
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
        }}
        
        /* Language selector */
        .language-selector {{
            display: flex;
            justify-content: center;
            gap: 0.5rem;
            margin-bottom: 1rem;
        }}
        
        /* Upload area styling - CENTERED */
        .upload-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 400px;
            margin: 1rem 0;
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
        
        /* Hide streamlit footer */
        footer {{
            visibility: hidden;
        }}
        
        /* Hide streamlit header */
        .stHeader {{
            visibility: hidden;
        }}
        
        /* Hide streamlit menu */
        .stMainMenu {{
            visibility: hidden;
        }}
        
        /* Reduce padding around main content */
        .stApp > div {{
            padding-top: 0 !important;
        }}
        
        /* Gradient animation */
        @keyframes gradientShift {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        
        /* Responsive design */
        @media (max-width: 768px) {{
            .main-content {{
                padding: 1rem;
                margin: 0.5rem;
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
                    <div class="metric-card">
                        <strong>💡 {LANGUAGES[st.session_state.language]["significant_association"]}</strong> {var1} dan {var2}.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="metric-card">
                        <strong>💡 {LANGUAGES[st.session_state.language]["no_significant_association"]}</strong> {var1} dan {var2}.
                    </div>
                    """, unsafe_allow_html=True)

def main():
    # Apply custom styles
    apply_custom_styles()
    
    # Language selector - ONLY 2 LANGUAGES
    col1, col2, col3, col4 = st.columns([1, 1, 6, 1])
    with col1:
        if st.button("🇮🇩 ID", key="lang_id", help="Bahasa Indonesia"):
            st.session_state.language = 'id'
    with col2:
        if st.button("🇬🇧 EN", key="lang_en", help="English"):
            st.session_state.language = 'en'
    
    # Main header - WRAPPED IN MAIN CONTENT
    st.markdown(f'<div class="main-content">', unsafe_allow_html=True)
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
            
            # File uploader
            uploaded_file = st.file_uploader(
                LANGUAGES[st.session_state.language]["upload_button"],
                type=['xlsx', 'xls', 'csv'],
                key="file_uploader"
            )
            
            # Handle file upload
            if uploaded_file is not None:
                with st.spinner("Loading data..."):
                    df = load_data(uploaded_file)
                    if df is not None:
                        st.session_state.data = df
                        st.session_state.uploaded_file = uploaded_file
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

<div style="background: #f8fafc; padding: 1rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #3b82f6;">
<h4 style="color: #1e40af; margin-bottom: 0.5rem;">{LANGUAGES[st.session_state.language]["descriptive_features"]}</h4>
<ul style="color: #374151; line-height: 1.5;">
    <li>Statistik dasar (mean, median, modus, standar deviasi)</li>
    <li>Visualisasi distribusi data</li>
    <li>Analisis missing values</li>
    <li>Matriks korelasi</li>
</ul>
</div>

<div style="background: #f8fafc; padding: 1rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #dc2626;">
<h4 style="color: #dc2626; margin-bottom: 0.5rem;">{LANGUAGES[st.session_state.language]["association_features"]}</h4>
<ul style="color: #374151; line-height: 1.5;">
    <li>Uji Chi-Square untuk variabel kategorikal</li>
    <li>Analisis korelasi untuk variabel numerik</li>
    <li>ANOVA untuk analisis kategorikal vs numerik</li>
    <li>Visualisasi hubungan antar variabel</li>
</ul>
</div>

<div style="background: linear-gradient(135deg, #f0fdf4, #dcfce7); padding: 1rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #22c55e;">
<h4 style="color: #ea580c; margin-bottom: 0.5rem;">{LANGUAGES[st.session_state.language]["supported_formats"]}</h4>
<ul style="color: #374151; line-height: 1.5;">
    <li>Excel (.xlsx, .xls)</li>
    <li>CSV (.csv)</li>
</ul>
</div>

<div style="background: linear-gradient(135deg, #eff6ff, #dbeafe); padding: 1rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #3b82f6;">
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
            <div class="metric-card">
                <strong>📁 {uploaded_file.name}</strong> ({uploaded_file.size / 1024 / 1024:.2f} MB)
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
    
    # Close main content div
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

