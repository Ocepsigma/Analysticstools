import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import chi2_contingency, pearsonr, spearmanr, f_oneway
import io
import base64
import warnings
warnings.filterwarnings('ignore')

# Set page config
st.set_page_config(
    page_title="Analisis Data Survei",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Multi-language translations
TRANSLATIONS = {
    "id": {
        "title": "Analisis Data Survei",
        "upload_title": "📊 Unggah File Excel Anda untuk Memulai Analisis",
        "upload_description": "Drag and drop file di sini<br>Limit 200MB per file • Format XLSX, XLS, CSV",
        "upload_button": "📁 Pilih File Excel/CSV",
        "success_message": "✅ Data berhasil dimuat! Dataset memiliki",
        "rows_text": "baris",
        "columns_text": "kolom",
        "numerical_columns": "Kolom Numerik",
        "categorical_columns": "Kolom Kategorikal",
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
        "descriptive_features_list": "<li>Statistik dasar (mean, median, modus, standar deviasi)</li><li>Visualisasi distribusi data</li><li>Analisis missing values</li><li>Matriks korelasi</li>",
        "association_features_list": "<li>Uji Chi-Square untuk variabel kategorikal</li><li>Analisis korelasi (Pearson/Spearman) untuk variabel numerik</li><li>ANOVA untuk analisis kategorikal vs numerik</li><li>Visualisasi hubungan antar variabel</li>",
        "descriptive_features": "📈 Analisis Deskriptif",
        "association_features": "🔗 Analisis Asosiasi",
        "supported_formats_list": "<li>Excel (.xlsx, .xls)</li><li>CSV (.csv)</li>",
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
        "category": "Kategori",
        "frequency": "Frekuensi",
        "percentage": "Persentase",
        "columns": "Kolom",
        "file_name": "📁",
        "file_size": "Ukuran",
        "download_summary": "Download Summary Report",
        "see_raw_data": "👀 Lihat Data Mentah",
        "export_results": "💾 Export Hasil Analisis",
        "loading_data": "Memuat data...",
        "conclusion": "💡 Kesimpulan:",
        "significant_conclusion": "Terdapat asosiasi yang signifikan antara variabel",
        "not_significant_conclusion": "Tidak terdapat asosiasi yang signifikan antara variabel",
        "independent_variables": "Variabel-variabel ini tidak independen satu sama lain.",
        "independent_variables_alt": "Variabel-variabel ini cenderung independen.",
        "correlation_strength": "sangat kuat",
        "positive": "positif",
        "negative": "negatif",
        "correlation_conclusion": "Terdapat hubungan",
        "between_variables": "antara",
        "statistical_significance": "Hubungan ini signifikan secara statistik.",
        "no_statistical_significance": "Hubungan ini tidak signifikan secara statistik.",
        "mean_difference_conclusion": "Terdapat perbedaan yang signifikan dalam rata-rata",
        "between_categories": "antar kategori",
        "no_mean_difference_conclusion": "Tidak ada perbedaan signifikan dalam rata-rata",
        "between_categories_alt": "antar kategori",
        "distribution": "Distribusi",
        "frequency_chart": "Frekuensi",
        "chi_square_statistic": "Chi-Square Statistic",
        "degrees_of_freedom": "Degrees of Freedom",
        "significance": "Signifikansi",
        "correlation_coefficient": "Koefisien Korelasi",
        "statistics_by": "Statistik {0} berdasarkan {1}",
        "distribution_by": "Distribusi {0} berdasarkan {1}",
        "f_statistic": "F-statistic",
        "p_value": "P-value",
        "automatic_analysis": "🤖 Analisis Asosiasi Otomatis",
        "select_two_variables": "Pilih dua variabel untuk analisis:",
        "analyze_button": "Analisis",
        "analysis_type": "Tipe Analisis",
        "chi_square_desc": "Menganalisis asosiasi antara dua variabel kategorikal",
        "correlation_desc": "Mengukur hubungan linear antara dua variabel numerik",
        "anova_desc": "Membandingkan rata-rata antar kategori",
        "analysis_results": "Hasil Analisis",
        "determined_test": "Tes yang Ditentukan",
        "sample_size": "Ukuran Sampel",
        "correlation_strength_indicator": "Indikator Kekuatan Korelasi",
        "profile_title": "👤 Profil Pembuat",
        "main_developer": "Pengembang Utama",
        "name": "Nama",
        "student_id": "ID Mahasiswa",
        "group": "Grup",
        "role": "Peran",
        "project_overview": "🎯 Ikhtisar Proyek",
        "contributions": "💪 Kontribusi"
    },
    "en": {
        "title": "Survey Data Analysis",
        "upload_title": "📊 Upload Your Excel File to Start Analysis",
        "upload_description": "Drag and drop file here<br>Limit 200MB per file • XLSX, XLS, CSV formats",
        "upload_button": "📁 Browse Excel/CSV Files",
        "success_message": "✅ Data successfully loaded! Dataset has",
        "rows_text": "rows",
        "columns_text": "columns",
        "numerical_columns": "Numerical Columns",
        "categorical_columns": "Categorical Columns",
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
        "descriptive_features_list": "<li>Basic statistics (mean, median, mode, standard deviation)</li><li>Data distribution visualization</li><li>Missing values analysis</li><li>Correlation matrix</li>",
        "association_features_list": "<li>Chi-Square test for categorical variables</li><li>Correlation analysis (Pearson/Spearman) for numerical variables</li><li>ANOVA for categorical vs numerical analysis</li><li>Variable relationship visualization</li>",
        "descriptive_features": "📈 Descriptive Analysis",
        "association_features": "🔗 Association Analysis",
        "supported_formats_list": "<li>Excel (.xlsx, .xls)</li><li>CSV (.csv)</li>",
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
        "significant_difference": "There is a significant difference in mean",
        "mean_difference": "between categories",
        "no_significant_difference": "There is no significant difference in mean",
        "no_mean_difference": "between categories",
        "total_rows": "Total Rows",
        "total_columns": "Total Columns",
        "category": "Category",
        "frequency": "Frequency",
        "percentage": "Percentage",
        "columns": "Columns",
        "file_name": "📁",
        "file_size": "Size",
        "download_summary": "Download Summary Report",
        "see_raw_data": "👀 See Raw Data",
        "export_results": "💾 Export Analysis Results",
        "loading_data": "Loading data...",
        "conclusion": "💡 Conclusion:",
        "significant_conclusion": "There is a significant association between variables",
        "not_significant_conclusion": "There is no significant association between variables",
        "independent_variables": "These variables are not independent of each other.",
        "independent_variables_alt": "These variables tend to be independent.",
        "correlation_strength": "very strong",
        "positive": "positive",
        "negative": "negative",
        "correlation_conclusion": "There is a",
        "between_variables": "between",
        "statistical_significance": "This relationship is statistically significant.",
        "no_statistical_significance": "This relationship is not statistically significant.",
        "mean_difference_conclusion": "There is a significant difference in mean",
        "between_categories": "between categories",
        "no_mean_difference_conclusion": "There is no significant difference in mean",
        "between_categories_alt": "between categories",
        "distribution": "Distribution",
        "frequency_chart": "Frequency",
        "chi_square_statistic": "Chi-Square Statistic",
        "degrees_of_freedom": "Degrees of Freedom",
        "significance": "Significance",
        "correlation_coefficient": "Correlation Coefficient",
        "statistics_by": "Statistics of {0} by {1}",
        "distribution_by": "Distribution of {0} by {1}",
        "f_statistic": "F-statistic",
        "p_value": "P-value",
        "automatic_analysis": "🤖 Automatic Association Analysis",
        "select_two_variables": "Select two variables for analysis:",
        "analyze_button": "Analyze",
        "analysis_type": "Analysis Type",
        "chi_square_desc": "Analyzes association between two categorical variables",
        "correlation_desc": "Measures linear relationship between two numerical variables",
        "anova_desc": "Compares means across different categories",
        "analysis_results": "Analysis Results",
        "determined_test": "Determined Test",
        "sample_size": "Sample Size",
        "correlation_strength_indicator": "Correlation Strength Indicator",
        "profile_title": "👤 Developer Profile",
        "main_developer": "Main Developer",
        "name": "Name",
        "student_id": "Student ID",
        "group": "Group",
        "role": "Role",
        "project_overview": "🎯 Project Overview",
        "contributions": "💪 Contributions"
    }
}

# Initialize session state for language
if 'language' not in st.session_state:
    st.session_state.language = 'id'

def get_translation(key):
    """Get translation for current language"""
    return TRANSLATIONS[st.session_state.language].get(key, key)

# Custom CSS
st.markdown("""
<style>
    /* Main container with glassmorphism effect */
    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin-top: 1rem;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(135deg, rgba(30, 64, 175, 0.95), rgba(55, 48, 163, 0.95));
        backdrop-filter: blur(10px);
    }
    
    /* Main header */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #1e40af, #3b82f6, #60a5fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Profile header */
    .profile-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #1e40af, #3b82f6, #60a5fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.6rem;
        font-weight: 600;
        color: #1e40af;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-left: 4px solid #3b82f6;
        padding-left: 1rem;
        background: linear-gradient(90deg, rgba(59, 130, 246, 0.1), transparent);
        padding: 0.5rem 1rem;
        border-radius: 8px;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #f8fafc, #f1f5f9);
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        border-color: #3b82f6;
    }
    
    /* Insight boxes */
    .insight-box {
        background: linear-gradient(135deg, #eff6ff, #dbeafe);
        border-left: 4px solid #3b82f6;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 8px;
        border: 1px solid #bfdbfe;
    }
    
    /* Analysis type cards */
    .analysis-type-card {
        background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
        border: 1px solid #bae6fd;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1);
    }
    
    .analysis-type-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1e40af;
        margin-bottom: 0.5rem;
    }
    
    .analysis-type-desc {
        color: #64748b;
        font-size: 0.9rem;
        line-height: 1.4;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6, #1e40af);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1e40af, #1e3a8a);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }
    
    /* Upload area */
    .upload-area {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(248, 250, 252, 0.95));
        border: 2px dashed #cbd5e1;
        border-radius: 16px;
        padding: 3rem;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    
    .upload-area:hover {
        border-color: #3b82f6;
        background: linear-gradient(135deg, rgba(239, 246, 255, 0.95), rgba(219, 234, 254, 0.95));
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(59, 130, 246, 0.2);
    }
    
    /* File info */
    .file-info {
        background: linear-gradient(135deg, #f0fdf4, #dcfce7);
        border-left: 4px solid #22c55e;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #bbf7d0;
        box-shadow: 0 2px 10px rgba(34, 197, 94, 0.1);
        text-align: center;
    }
    
    /* Hide default elements */
    .stHeader {
        visibility: hidden;
    }
    
    footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
def load_data(file):
    """Load data from uploaded file"""
    try:
        if file.name.endswith('.xlsx'):
            df = pd.read_excel(file)
        elif file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            st.error(get_translation("error_no_file"))
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

def determine_variable_type(series):
    """Determine variable type for automatic analysis"""
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

def determine_analysis_type(var1_type, var2_type):
    """Determine appropriate analysis type based on variable types"""
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
        return "chi_square"

def get_correlation_strength(correlation):
    """Get correlation strength description"""
    abs_corr = abs(correlation)
    if abs_corr >= 0.8:
        return "sangat kuat"
    elif abs_corr >= 0.6:
        return "kuat"
    elif abs_corr >= 0.4:
        return "sedang"
    elif abs_corr >= 0.2:
        return "lemah"
    else:
        return "sangat lemah"

def automatic_association_analysis(df, var1, var2, alpha=0.05):
    """Perform automatic association analysis based on variable types"""
    try:
        # Determine variable types
        var1_type = determine_variable_type(df[var1])
        var2_type = determine_variable_type(df[var2])
        
        # Determine analysis type
        analysis_type = determine_analysis_type(var1_type, var2_type)
        
        analysis_type_names = {
            "chi_square": "Chi-Square Test",
            "pearson": "Pearson Correlation",
            "spearman": "Spearman Correlation",
            "anova": "ANOVA Test"
        }
        
        # Show analysis type
        st.markdown(f"""
        <div class="analysis-type-card">
            <div class="analysis-type-title">🎯 {analysis_type_names.get(analysis_type, 'Unknown')}</div>
            <div class="analysis-type-desc">Analisis yang direkomendasikan berdasarkan tipe data</div>
            <div style="margin-top: 1rem; padding: 0.5rem; background: rgba(255,255,255,0.7); border-radius: 6px;">
                <strong>Variable 1:</strong> {var1} ({var1_type})<br>
                <strong>Variable 2:</strong> {var2} ({var2_type})
            </div>
        </div>
        """, unsafe_allow_html=True)
        
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
        
        if analysis_type == "chi_square":
            # Chi-Square Test
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
                strength = get_correlation_strength(corr)
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
                strength = get_correlation_strength(corr)
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
        
        return results
        
    except Exception as e:
        st.error(f"Error in automatic association analysis: {str(e)}")
        return None

def descriptive_analysis(df, numerical_cols, categorical_cols):
    """Perform descriptive analysis"""
    try:
        st.markdown(f'<div class="section-header">{get_translation("descriptive_analysis")}</div>', unsafe_allow_html=True)
        
        # Basic Statistics
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f'<div style="font-size: 1.3rem; font-weight: 600; color: #1e40af; margin: 1rem 0;">{get_translation("dataset_overview")}</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="metric-card">
                <strong>{get_translation("total_rows")}:</strong> {df.shape[0]:,}<br>
                <strong>{get_translation("total_columns")}:</strong> {df.shape[1]}<br>
                <strong>{get_translation("numerical_columns")}:</strong> {len(numerical_cols)}<br>
                <strong>{get_translation("categorical_columns")}:</strong> {len(categorical_cols)}
            </div>
            """, unsafe_allow_html=True)
            
            # Missing values
            missing_data = df.isnull().sum()
            if missing_data.sum() > 0:
                st.markdown(f'<div style="font-size: 1.3rem; font-weight: 600; color: #f59e0b; margin: 1rem 0;">{get_translation("missing_values")}</div>', unsafe_allow_html=True)
                missing_df = pd.DataFrame({
                    get_translation("columns"): missing_data.index,
                    'Jumlah Missing': missing_data.values,
                    'Persentase': (missing_data.values / len(df) * 100).round(2)
                })
                missing_df = missing_df[missing_df['Jumlah Missing'] > 0]
                st.dataframe(missing_df, use_container_width=True)
        
        with col2:
            # Numerical columns statistics
            if numerical_cols:
                st.markdown(f'<div style="font-size: 1.3rem; font-weight: 600; color: #059669; margin: 1rem 0;">{get_translation("numerical_stats")}</div>', unsafe_allow_html=True)
                stats_df = df[numerical_cols].describe().round(2)
                st.dataframe(stats_df, use_container_width=True)
        
        # Visualizations
        if numerical_cols:
            st.markdown(f'<div style="font-size: 1.3rem; font-weight: 600; color: #1e40af; margin: 1rem 0;">{get_translation("data_visualization")}</div>', unsafe_allow_html=True)
            
            # Distribution plots
            selected_num_col = st.selectbox(get_translation("select_numerical_column"), numerical_cols)
            
            col1, col2 = st.columns(2)
            with col1:
                # Histogram
                fig_hist = px.histogram(df, x=selected_num_col, title=f'{get_translation("distribution")} {selected_num_col}',
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
                st.markdown(f'<div style="font-size: 1.3rem; font-weight: 600; color: #7c3aed; margin: 1rem 0;">{get_translation("correlation_matrix")}</div>', unsafe_allow_html=True)
                correlation_matrix = df[numerical_cols].corr()
                
                fig_corr = px.imshow(correlation_matrix, 
                                    text_auto=True, 
                                    aspect="auto",
                                    color_continuous_scale='RdBu_r',
                                    title=get_translation("correlation_matrix"))
                fig_corr.update_layout(height=500)
                st.plotly_chart(fig_corr, use_container_width=True)
        
        # Categorical analysis
        if categorical_cols:
            st.markdown(f'<div style="font-size: 1.3rem; font-weight: 600; color: #dc2626; margin: 1rem 0;">{get_translation("categorical_analysis")}</div>', unsafe_allow_html=True)
            
            selected_cat_col = st.selectbox(get_translation("select_categorical_column"), categorical_cols)
            
            # Value counts
            value_counts = df[selected_cat_col].value_counts()
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Pie chart
                fig_pie = px.pie(values=value_counts.values, 
                                names=value_counts.index, 
                                title=f'{get_translation("distribution")} {selected_cat_col}')
                fig_pie.update_layout(height=400)
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                # Bar chart
                fig_bar = px.bar(x=value_counts.index, 
                               y=value_counts.values,
                               title=f'{get_translation("frequency_chart")} {selected_cat_col}')
                fig_bar.update_layout(height=400, xaxis_title=selected_cat_col, yaxis_title=get_translation("frequency_chart"))
                st.plotly_chart(fig_bar, use_container_width=True)
            
            # Frequency table
            st.markdown(f'<div style="font-size: 1.3rem; font-weight: 600; color: #0891b2; margin: 1rem 0;">{get_translation("frequency_table")}</div>', unsafe_allow_html=True)
            freq_table = pd.DataFrame({
                get_translation("category"): value_counts.index,
                get_translation("frequency"): value_counts.values,
                get_translation("percentage"): (value_counts.values / len(df) * 100).round(2)
            })
            st.dataframe(freq_table, use_container_width=True)
                
    except Exception as e:
        st.error(f"Error in descriptive analysis: {str(e)}")

def association_analysis(df, numerical_cols, categorical_cols):
    """Perform automatic association analysis"""
    try:
        st.markdown(f'<div class="section-header">{get_translation("association_analysis")}</div>', unsafe_allow_html=True)
        
        # Automatic Analysis Section
        st.markdown(f'<div style="font-size: 1.4rem; font-weight: 600; color: #1e40af; margin: 1rem 0;">{get_translation("automatic_analysis")}</div>', unsafe_allow_html=True)
        
        all_columns = numerical_cols + categorical_cols
        
        if len(all_columns) < 2:
            st.warning("You need at least 2 columns to perform association analysis.")
            return
        
        col1, col2 = st.columns(2)
        with col1:
            var1 = st.selectbox(get_translation("select_variable_1"), all_columns, key='auto_var1')
        with col2:
            available_vars = [col for col in all_columns if col != var1]
            var2 = st.selectbox(get_translation("select_variable_2"), available_vars, key='auto_var2')
        
        if st.button(get_translation("analyze_button"), key="auto_analyze"):
            try:
                results = automatic_association_analysis(df, var1, var2)
                
                if results:
                    # Display results
                    st.markdown("### 📈 Hasil Analisis")
                    
                    # Metrics
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown(f"""
                        <div class="metric-card">
                            <h4>{results['var1']}</h4>
                            <p>{results['var1_type']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"""
                        <div class="metric-card">
                            <h4>{results['var2']}</h4>
                            <p>{results['var2_type']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        analysis_type_names = {
                            "chi_square": "Chi-Square Test",
                            "pearson": "Pearson Correlation",
                            "spearman": "Spearman Correlation",
                            "anova": "ANOVA Test"
                        }
                        st.markdown(f"""
                        <div class="metric-card">
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
                        strength = get_correlation_strength(results['correlation'])
                        st.markdown(f"**Kekuatan Korelasi**: {strength}")
                    
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
                    <div class="insight-box">
                        <p>{results['interpretation']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Recommendation
                    st.markdown("### 💡 Rekomendasi")
                    st.markdown(f"""
                    <div class="insight-box">
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
                st.error(f"Error in automatic analysis: {str(e)}")
                        
    except Exception as e:
        st.error(f"Error in association analysis section: {str(e)}")

def profile_page():
    """Display developer profile page"""
    st.markdown(f'<h1 class="profile-header">{get_translation("profile_title")}</h1>', unsafe_allow_html=True)
    
    # Main Developer Card
    with st.container():
        # Profile Header with Image and Basic Info
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Profile Image Placeholder
            st.markdown("""
            <div style="text-align: center; margin-bottom: 20px;">
                <div style="width: 150px; height: 150px; background-color: #e0e7ff; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto; border: 4px solid #3b82f6;">
                    <span style="font-size: 60px; color: #3b82f6;">👤</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Name and Location
            st.markdown("""
            <div style="text-align: center; background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <h2 style="color: #1e40af; margin: 0 0 10px 0; font-size: 24px;">Yoseph Sihite</h2>
                <p style="color: #64748b; margin: 0; font-size: 16px;">📍 Cikarang, Indonesia</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Main Developer Information
            st.markdown("""
            <div style="background: linear-gradient(135deg, #3b82f6, #1e40af); color: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 20px rgba(59, 130, 246, 0.3);">
                <h3 style="margin: 0 0 15px 0; font-size: 20px; display: flex; align-items: center;">
                    <span style="margin-right: 10px;">👨‍💻</span> Main Developer
                </h3>
                <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin-top: 15px;">
                    <p style="margin: 5px 0;"><strong>Nama:</strong> Yoseph Sihite</p>
                    <p style="margin: 5px 0;"><strong>Student ID:</strong> 004202400113</p>
                    <p style="margin: 5px 0;"><strong>Group:</strong> Group 2 Linear Algebra</p>
                    <p style="margin: 5px 0;"><strong>Role:</strong> Lead Group</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Contributions Section
    st.markdown("---")
    st.markdown("### 💪 Kontribusi")
    
    st.markdown("""
    <div style="background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        <h3 style="color: #1e40af; margin: 0 0 15px 0; font-size: 20px;">Kontribusi Pengembangan</h3>
        
        <p style="color: #374151; line-height: 1.6; margin: 0 0 15px 0;">
            Ada pelaksanaan final project Statistik 1, saya berkontribusi secara penuh dengan mengerjakan seluruh tahapan proyek secara mandiri. 
            Mulai dari perencanaan konsep, pengolahan dan analisis data, hingga perancangan dan pengembangan web app, 
            seluruh proses dikerjakan sendiri tanpa pembagian tugas dengan anggota lain.
        </p>
        
        <p style="color: #374151; line-height: 1.6; margin: 0 0 15px 0;">
            Hal ini dikarenakan pada Kelompok 2 saya merupakan satu-satunya anggota yang aktif, sehingga tanggung jawab 
            penyelesaian proyek dari awal hingga akhir sepenuhnya berada pada saya.
        </p>
        
        <p style="color: #374151; line-height: 1.6; margin: 0 0 20px 0;">
            Kontribusi ini mencerminkan kemandirian, pemahaman materi Statistik 1, serta kemampuan saya dalam 
            mengimplementasikan analisis statistik ke dalam bentuk aplikasi berbasis web secara utuh.
        </p>
        
        <div style="background: #f0f9ff; padding: 15px; border-radius: 10px; margin-top: 20px; border-left: 4px solid #3b82f6;">
            <p style="color: #1e40af; margin: 0; font-weight: 600;">
                <strong>Tahapan yang Dikerjakan:</strong>
            </p>
            <ul style="color: #1e40af; margin: 10px 0 0 20px; padding: 0;">
                <li>Perencanaan konsep proyek</li>
                <li>Pengolahan dan analisis data statistik</li>
                <li>Perancangan arsitektur aplikasi</li>
                <li>Pengembangan web application dengan Streamlit</li>
                <li>Implementasi visualisasi data interaktif</li>
                <li>Testing dan debugging fungsionalitas</li>
                <li>Dokumentasi dan presentasi hasil</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown(
        f"<div style='text-align: center; color: #64748b; margin-top: 2rem; padding: 20px; background: rgba(255,255,255,0.8); border-radius: 15px;'>"
        f"<em>Proyek ini dikembangkan sebagai bagian dari Mata Kuliah Statistik 1 • "
        f"Tahun Akademik 2024</em>"
        f"</div>", 
        unsafe_allow_html=True
    )

def main():
    try:
        # Create navigation
        page = st.sidebar.selectbox(
            "Navigation",
            ["📊 Analisis Data", "👤 Profil Pembuat"]
        )
        
        # Language buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🇮🇩 ID", key="lang_id"):
                st.session_state.language = 'id'
                st.rerun()
        with col2:
            if st.button("🇬🇧 EN", key="lang_en"):
                st.session_state.language = 'en'
                st.rerun()
        with col3:
            if st.button("🇨🇳 中文", key="lang_zh"):
                st.session_state.language = 'zh'
                st.rerun()
        
        if page == "👤 Profil Pembuat":
            profile_page()
        else:
            # Main header
            st.markdown(f'<h1 class="main-header">{get_translation("title")}</h1>', unsafe_allow_html=True)
            
            # Upload area
            st.markdown("### 📁 Upload Data")
            uploaded_file = st.file_uploader("Upload file CSV atau Excel", type=["csv", "xlsx", "xls"])
            
            if uploaded_file is not None:
                # Show file info
                st.markdown(f"""
                <div class="file-info">
                    <div class="file-name">{get_translation("file_name")} {uploaded_file.name}</div>
                    <div class="file-size">{get_translation("file_size")}: {uploaded_file.size / 1024 / 1024:.2f} MB</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Load data
                with st.spinner(get_translation("loading_data")):
                    df = load_data(uploaded_file)
                
                if df is not None:
                    # Success message
                    st.success(f"{get_translation('success_message')} {df.shape[0]} {get_translation('rows_text')} dan {df.shape[1]} {get_translation('columns_text')}.")
                    
                    # Show raw data
                    with st.expander(get_translation("see_raw_data")):
                        st.dataframe(df.head(), use_container_width=True)
                    
                    # Get column types
                    numerical_cols, categorical_cols = get_column_types(df)
                    
                    # Show column information
                    col1, col2 = st.columns(2)
                    with col1:
                        if numerical_cols:
                            st.markdown(f'<div style="font-size: 1.1rem; font-weight: 600; color: #1e40af; margin: 0.5rem 0;">{get_translation("numerical_columns")}:</div>', unsafe_allow_html=True)
                            for col in numerical_cols:
                                st.markdown(f"• {col}")
                    
                    with col2:
                        if categorical_cols:
                            st.markdown(f'<div style="font-size: 1.1rem; font-weight: 600; color: #dc2626; margin: 0.5rem 0;">{get_translation("categorical_columns")}:</div>', unsafe_allow_html=True)
                            for col in categorical_cols:
                                st.markdown(f"• {col}")
                    
                    # Analysis tabs
                    tab1, tab2 = st.tabs([get_translation("descriptive_analysis"), get_translation("association_analysis")])
                    
                    with tab1:
                        descriptive_analysis(df, numerical_cols, categorical_cols)
                    
                    with tab2:
                        association_analysis(df, numerical_cols, categorical_cols)
                    
                    # Export functionality
                    st.markdown("---")
                    st.markdown(f'<div style="font-size: 1.3rem; font-weight: 600; color: #059669; margin: 1rem 0;">{get_translation("export_results")}</div>', unsafe_allow_html=True)
                    
                    if st.button(get_translation("download_summary")):
                        try:
                            # Create a summary report
                            summary_data = {
                                'Metric': [get_translation("total_rows"), get_translation("total_columns"), get_translation("numerical_columns"), get_translation("categorical_columns"), 'Missing Values'],
                                'Value': [df.shape[0], df.shape[1], len(numerical_cols), len(categorical_cols), df.isnull().sum().sum()]
                            }
                            summary_df = pd.DataFrame(summary_data)
                            
                            # Convert to CSV
                            csv = summary_df.to_csv(index=False)
                            b64 = base64.b64encode(csv.encode()).decode()
                            href = f'<a href="data:file/csv;base64,{b64}" download="survey_analysis_summary.csv" style="background: #3b82f6; color: white; padding: 0.75rem 1.5rem; border-radius: 8px; text-decoration: none; font-weight: 600;">Download CSV Summary</a>'
                            st.markdown(href, unsafe_allow_html=True)
                        except Exception as e:
                            st.error(f"Error creating download: {str(e)}")
            
            else:
                # Instructions
                st.markdown(f"""
        <div style="background: rgba(255, 255, 255, 0.9); padding: 2rem; border-radius: 15px; border: 1px solid #e5e7eb; margin: 2rem 0;">
        <h2 style="color: #1e40af; margin-bottom: 1rem;">{get_translation("instructions")}</h2>
        <ol style="color: #374151; line-height: 1.6;">
            <li><strong style="color: #3b82f6;">{get_translation("upload_step")}</strong></li>
            <li><strong style="color: #7c3aed;">{get_translation("analysis_step")}</strong></li>
            <li><strong style="color: #dc2626;">{get_translation("export_step")}</strong></li>
        </ol>

        <h3 style="color: #1e40af; margin: 1.5rem 0 1rem 0;">{get_translation("features_title")}</h3>

        <div style="background: #f8fafc; padding: 1rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #3b82f6;">
        <h4 style="color: #1e40af; margin-bottom: 0.5rem;">{get_translation("descriptive_features")}:</h4>
        <ul style="color: #374151; line-height: 1.5;">
            {get_translation("descriptive_features_list")}
        </ul>
        </div>

        <div style="background: #f8fafc; padding: 1rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #dc2626;">
        <h4 style="color: #dc2626; margin-bottom: 0.5rem;">{get_translation("association_features")}:</h4>
        <ul style="color: #374151; line-height: 1.5;">
            {get_translation("association_features_list")}
        </ul>
        </div>

        <h3 style="color: #ea580c; margin: 1.5rem 0 1rem 0;">{get_translation("supported_formats")}</h3>
        <ul style="color: #374151; line-height: 1.5;">
          {get_translation("supported_formats_list")}
        </ul>

        <div style="background: linear-gradient(135deg, #eff6ff, #dbeafe); padding: 1rem; border-radius: 10px; border-left: 4px solid #3b82f6; margin: 1rem 0;">
        <p style="color: #1e40af; margin: 0; font-weight: 600;">💡 <strong>Tip</strong>: {get_translation("tip")}</p>
        </div>
        </div>
                """, unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Unexpected error in main application: {str(e)}")
        st.error("Please refresh page and try again.")
        if st.button("Clear Session and Restart"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    main()
