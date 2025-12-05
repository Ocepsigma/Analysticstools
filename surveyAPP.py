import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
import base64
import os
from scipy import stats
from scipy.stats import chi2_contingency, pearsonr, spearmanr
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
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
        "insight": "💡 Insight:",
        "significant_insight": "Terdapat asosiasi yang signifikan antara variabel",
        "not_significant_insight": "Tidak terdapat asosiasi yang signifikan antara variabel",
        "independent_variables": "Variabel-variabel ini tidak independen satu sama lain.",
        "independent_variables_alt": "Variabel-variabel ini cenderung independen.",
        "correlation_strength": "sangat kuat" if abs(0.8) >= 0.8 else "kuat" if abs(0.8) >= 0.6 else "sedang" if abs(0.8) >= 0.4 else "lemah" if abs(0.8) >= 0.2 else "sangat lemah",
        "positive": "positif",
        "negative": "negatif",
        "correlation_insight": "Terdapat hubungan",
        "between_variables": "antara",
        "statistical_significance": "Hubungan ini signifikan secara statistik.",
        "no_statistical_significance": "Hubungan ini tidak signifikan secara statistik.",
        "mean_difference_insight": "Terdapat perbedaan yang signifikan dalam rata-rata",
        "between_categories": "antar kategori",
        "no_mean_difference_insight": "Tidak ada perbedaan signifikan dalam rata-rata",
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
        "p_value": "P-value"
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
        "insight": "💡 Insight:",
        "significant_insight": "There is a significant association between variables",
        "not_significant_insight": "There is no significant association between variables",
        "independent_variables": "These variables are not independent of each other.",
        "independent_variables_alt": "These variables tend to be independent.",
        "correlation_strength": "very strong" if abs(0.8) >= 0.8 else "strong" if abs(0.8) >= 0.6 else "moderate" if abs(0.8) >= 0.4 else "weak" if abs(0.8) >= 0.2 else "very weak",
        "positive": "positive",
        "negative": "negative",
        "correlation_insight": "There is a",
        "between_variables": "between",
        "statistical_significance": "This relationship is statistically significant.",
        "no_statistical_significance": "This relationship is not statistically significant.",
        "mean_difference_insight": "There is a significant difference in mean",
        "between_categories": "between categories",
        "no_mean_difference_insight": "There is no significant difference in mean",
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
        "p_value": "P-value"
    },
    "zh": {
        "title": "调查数据分析",
        "upload_title": "📊 上传您的Excel文件以开始分析",
        "upload_description": "拖放文件到这里<br>每个文件限制200MB • XLSX、XLS、CSV格式",
        "upload_button": "📁 浏览Excel/CSV文件",
        "success_message": "✅ 数据成功加载！数据集有",
        "rows_text": "行",
        "columns_text": "列",
        "numerical_columns": "数值列",
        "categorical_columns": "分类列",
        "descriptive_analysis": "📈 描述性分析",
        "association_analysis": "🔗 关联分析",
        "dataset_overview": "📊 数据集概览",
        "missing_values": "🔍 缺失值",
        "numerical_stats": "🔢 数值统计",
        "data_visualization": "📊 数据可视化",
        "correlation_matrix": "🔗 相关矩阵",
        "categorical_analysis": "📋 分类分析",
        "frequency_table": "📊 频率表",
        "chi_square_test": "🎯 卡方检验",
        "correlation_analysis": "📊 相关分析",
        "anova_test": "🔄 方差分析",
        "instructions": "🚀 如何使用此应用程序",
        "upload_step": "上传Excel (.xlsx) 或 CSV (.csv) 文件",
        "analysis_step": "选择要执行的分析",
        "export_step": "以CSV格式下载分析结果",
        "features_title": "📋 主要功能",
        "descriptive_features_list": "<li>基本统计（均值、中位数、众数、标准差）</li><li>数据分布可视化</li><li>缺失值分析</li><li>相关矩阵</li>",
        "association_features_list": "<li>分类变量的卡方检验</li><li>数值变量的相关分析（皮尔逊/斯皮尔曼）</li><li>分类vs数值的方差分析</li><li>变量关系可视化</li>",
        "descriptive_features": "📈 描述性分析",
        "association_features": "🔗 关联分析",
        "supported_formats_list": "<li>Excel (.xlsx, .xls)</li><li>CSV (.csv)</li>",
        "supported_formats": "📊 支持的文件格式",
        "tip": "确保您的数据有清晰的标题和一致的格式，以获得最佳分析结果。",
        "error_no_file": "请先上传文件！",
        "select_numerical_column": "选择数值列：",
        "select_categorical_column": "选择分类列：",
        "select_variable_1": "选择变量1：",
        "select_variable_2": "选择变量2：",
        "analyze_chi_square": "分析卡方",
        "contingency_table": "列联表",
        "chi_square_results": "卡方结果",
        "significant": "显著",
        "not_significant": "不显著",
        "significant_association": "变量之间存在显著关联",
        "no_significant_association": "变量之间不存在显著关联",
        "correlation_method": "相关方法",
        "pearson": "皮尔逊",
        "spearman": "斯皮尔曼",
        "analyze_correlation": "分析相关性",
        "correlation_results": "相关结果",
        "categorical_numerical_analysis": "分类与数值分析",
        "select_categorical_variable": "选择分类变量：",
        "select_numerical_variable": "选择数值变量：",
        "analyze_categorical_numerical": "分析分类-数值",
        "anova_results": "方差分析结果",
        "significant_difference": "平均值存在显著差异",
        "mean_difference": "在类别之间",
        "no_significant_difference": "平均值不存在显著差异",
        "no_mean_difference": "在类别之间",
        "total_rows": "总行数",
        "total_columns": "总列数",
        "category": "类别",
        "frequency": "频率",
        "percentage": "百分比",
        "columns": "列",
        "file_name": "📁",
        "file_size": "大小",
        "download_summary": "下载摘要报告",
        "see_raw_data": "👀 查看原始数据",
        "export_results": "💾 导出分析结果",
        "loading_data": "加载数据...",
        "insight": "💡 洞察：",
        "significant_insight": "变量之间存在显著关联",
        "not_significant_insight": "变量之间不存在显著关联",
        "independent_variables": "这些变量彼此不独立。",
        "independent_variables_alt": "这些变量倾向于独立。",
        "correlation_strength": "非常强" if abs(0.8) >= 0.8 else "强" if abs(0.8) >= 0.6 else "中等" if abs(0.8) >= 0.4 else "弱" if abs(0.8) >= 0.2 else "非常弱",
        "positive": "正",
        "negative": "负",
        "correlation_insight": "存在",
        "between_variables": "之间",
        "statistical_significance": "这种关系在统计上是显著的。",
        "no_statistical_significance": "这种关系在统计上不显著。",
        "mean_difference_insight": "平均值存在显著差异",
        "between_categories": "在类别之间",
        "no_mean_difference_insight": "平均值不存在显著差异",
        "between_categories_alt": "在类别之间",
        "distribution": "分布",
        "frequency_chart": "频率",
        "chi_square_statistic": "卡方统计量",
        "degrees_of_freedom": "自由度",
        "significance": "显著性",
        "correlation_coefficient": "相关系数",
        "statistics_by": "{1}的{0}统计",
        "distribution_by": "{0}按{1}的分布",
        "f_statistic": "F统计量",
        "p_value": "P值"
    }
}

# Initialize session state for language
if 'language' not in st.session_state:
    st.session_state.language = 'id'

def get_translation(key):
    """Get translation for current language"""
    return TRANSLATIONS[st.session_state.language].get(key, key)

# Background image function
def get_background_image():
    """Load background image from multiple sources"""
    background_styles = []
    
    try:
        # Method 1: Try to read from current directory
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
        elif os.path.exists('background.png'):
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

# Apply background styles
background_styles = get_background_image()
for style in background_styles:
    st.markdown(f"<style>{style}</style>", unsafe_allow_html=True)

# Custom CSS with design inspired by first image
st.markdown("""
<style>
    /* Animated gradient keyframes */
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Binary rain effect */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(59, 130, 246, 0.1) 2px, rgba(59, 130, 246, 0.1) 4px),
            repeating-linear-gradient(90deg, transparent, transparent 2px, rgba(59, 130, 246, 0.1) 2px, rgba(59, 130, 246, 0.1) 4px);
        background-size: 50px 50px;
        pointer-events: none;
        z-index: -1;
        animation: binaryMove 20s linear infinite;
    }
    
    @keyframes binaryMove {
        0% { transform: translateY(0); }
        100% { transform: translateY(50px); }
    }
    
    /* Main container with glassmorphism effect */
    .main .block-container {
        background: rgba(255, 255, 255, 0.92);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        padding: 2rem;
        margin-top: 0.5rem;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        position: relative;
        z-index: 1;
        max-width: 1000px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* Sidebar with professional gradient */
    .css-1d391kg {
        background: linear-gradient(135deg, rgba(30, 64, 175, 0.95), rgba(55, 48, 163, 0.95));
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .css-1d391kg .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.95);
        color: #1e293b;
        border-radius: 8px;
    }
    
    .css-1d391kg .stFileUploader {
        background-color: rgba(255, 255, 255, 0.1);
        border: 2px dashed rgba(255, 255, 255, 0.4);
        border-radius: 10px;
        padding: 1rem;
    }
    
    .css-1d391kg .stFileUploader label {
        color: white;
        font-weight: 500;
    }
    
    /* Main header with professional blue gradient */
    .main-header {
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
    }
    
    /* Text glow animation */
    @keyframes textGlow {
        from { filter: drop-shadow(0 0 10px rgba(59, 130, 246, 0.5)); }
        to { filter: drop-shadow(0 0 20px rgba(59, 130, 246, 0.8)); }
    }
    
    /* Upload area styling - CENTERED */
    .upload-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 400px;
        margin: 1rem 0;
    }
    
    .upload-area {
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
    }
    
    .upload-area::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(59, 130, 246, 0.05), transparent);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .upload-area:hover {
        border-color: #3b82f6;
        background: linear-gradient(135deg, rgba(239, 246, 255, 0.95), rgba(219, 234, 254, 0.95));
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(59, 130, 246, 0.2);
    }
    
    .upload-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e40af;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #1e40af, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .upload-description {
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
        line-height: 1.5;
    }
    
    .upload-button {
        background: linear-gradient(135deg, #3b82f6, #1e40af);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 1rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
        position: relative;
        overflow: hidden;
        cursor: pointer;
    }
    
    .upload-button::before {
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .upload-button:hover::before {
        left: 100%;
    }
    
    .upload-button:hover {
        background: linear-gradient(135deg, #1e40af, #1e3a8a);
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(59, 130, 246, 0.6);
    }
    
    /* File info styling */
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
    
    .file-name {
        font-weight: 600;
        color: #15803d;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    .file-size {
        color: #16a34a;
        font-size: 0.9rem;
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
    
    /* Metric cards with clean design */
    .metric-card {
        background: linear-gradient(135deg, #f8fafc, #f1f5f9);
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.1), transparent);
        transition: left 0.5s ease;
    }
    
    .metric-card:hover::before {
        left: 100%;
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
        position: relative;
    }
    
    .insight-box::after {
        content: "💡";
        position: absolute;
        top: -10px;
        right: 10px;
        font-size: 1.5rem;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    /* Success messages */
    .stSuccess {
        background: linear-gradient(135deg, #f0fdf4, #dcfce7);
        border-left: 4px solid #22c55e;
        border-radius: 8px;
        border: 1px solid #bbf7d0;
    }
    
    /* Info messages */
    .stInfo {
        background: linear-gradient(135deg, #eff6ff, #dbeafe);
        border-left: 4px solid #3b82f6;
        border-radius: 8px;
        border: 1px solid #bfdbfe;
    }
    
    /* Warning messages */
    .stWarning {
        background: linear-gradient(135deg, #fffbeb, #fef3c7);
        border-left: 4px solid #f59e0b;
        border-radius: 8px;
        border: 1px solid #fde68a;
    }
    
    /* Error messages */
    .stError {
        background: linear-gradient(135deg, #fef2f2, #fee2e2);
        border-left: 4px solid #ef4444;
        border-radius: 8px;
        border: 1px solid #fecaca;
    }
    
    /* Buttons with professional blue gradient */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6, #1e40af);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1e40af, #1e3a8a);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 8px;
        border: 1px solid #d1d5db;
    }
    
    /* Radio buttons */
    .stRadio > div {
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 8px;
        padding: 1rem;
        border: 1px solid #e5e7eb;
    }
    
    /* Tabs */
    .stTabs {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 12px;
        padding: 0.5rem;
        border: 1px solid #e5e7eb;
    }
    
    /* Dataframes */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #f8fafc;
        border-radius: 8px;
        font-weight: 600;
        color: #1e40af;
        border: 1px solid #e2e8f0;
    }
    
    /* Sidebar text */
    .css-1d391kg h3 {
        color: white;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    
    .css-1d391kg p {
        color: rgba(255, 255, 255, 0.9);
        line-height: 1.5;
    }
    
    /* Spinner */
    .stSpinner {
        color: #3b82f6;
    }
    
    /* Floating elements for tech feel */
    .floating-element {
        position: fixed;
        width: 4px;
        height: 4px;
        background: rgba(59, 130, 246, 0.6);
        border-radius: 50%;
        pointer-events: none;
        animation: float 20s infinite linear;
        z-index: 0;
    }
    
    @keyframes float {
        0% {
            transform: translateY(100vh) translateX(0) rotate(0deg);
            opacity: 0;
        }
        10% {
            opacity: 1;
        }
        90% {
            opacity: 1;
        }
        100% {
            transform: translateY(-100vh) translateX(100px) rotate(360deg);
            opacity: 0;
        }
    }
    
    /* Add multiple floating elements */
    .floating-element:nth-child(2) { animation-delay: 5s; left: 20%; }
    .floating-element:nth-child(3) { animation-delay: 10s; left: 40%; }
    .floating-element:nth-child(4) { animation-delay: 15s; left: 60%; }
    .floating-element:nth-child(5) { animation-delay: 2s; left: 80%; }
    
    /* Custom file uploader styling */
    .custom-file-upload {
        position: relative;
        display: inline-block;
        cursor: pointer;
        width: 100%;
    }
    
    .custom-file-upload input[type=file] {
        position: absolute;
        left: -9999px;
    }
    
    /* Hide default Streamlit elements */
    .stHeader {
        visibility: hidden;
    }
    
    footer {
        visibility: hidden;
    }
</style>

<!-- Floating elements -->
<div class="floating-element"></div>
<div class="floating-element"></div>
<div class="floating-element"></div>
<div class="floating-element"></div>
<div class="floating-element"></div>
""", unsafe_allow_html=True)

# Global variable to store uploaded file
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None

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

def descriptive_analysis(df, numerical_cols, categorical_cols):
    """Perform descriptive analysis"""
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
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Value counts
            value_counts = df[selected_cat_col].value_counts()
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

def association_analysis(df, numerical_cols, categorical_cols):
    """Perform association analysis"""
    st.markdown(f'<div class="section-header">{get_translation("association_analysis")}</div>', unsafe_allow_html=True)
    
    # Chi-square test for categorical variables
    if len(categorical_cols) >= 2:
        st.markdown(f'<div style="font-size: 1.3rem; font-weight: 600; color: #ea580c; margin: 1rem 0;">{get_translation("chi_square_test")}</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            var1 = st.selectbox(get_translation("select_variable_1"), categorical_cols, key='cat1')
        with col2:
            var2 = st.selectbox(get_translation("select_variable_2"), [col for col in categorical_cols if col != var1], key='cat2')
        
        if st.button(get_translation("analyze_chi_square")):
            # Create contingency table
            contingency_table = pd.crosstab(df[var1], df[var2])
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f'<div style="font-size: 1.1rem; font-weight: 600; color: #dc2626; margin: 0.5rem 0;">{get_translation("contingency_table")}</div>', unsafe_allow_html=True)
                st.dataframe(contingency_table, use_container_width=True)
            
            with col2:
                # Perform chi-square test
                chi2, p_value, dof, expected = chi2_contingency(contingency_table)
                
                st.markdown(f'<div style="font-size: 1.1rem; font-weight: 600; color: #059669; margin: 0.5rem 0;">{get_translation("chi_square_results")}</div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="metric-card">
                    <strong>{get_translation("chi_square_statistic")}:</strong> {chi2:.4f}<br>
                    <strong>{get_translation("p_value")}:</strong> {p_value:.4f}<br>
                    <strong>{get_translation("degrees_of_freedom")}:</strong> {dof}<br>
                    <strong>{get_translation("significance")}:</strong> {'✅ ' + get_translation("significant") if p_value < 0.05 else '❌ ' + get_translation("not_significant")}
                </div>
                """, unsafe_allow_html=True)
                
                # Interpretation
                if p_value < 0.05:
                    st.markdown(f"""
                    <div class="insight-box">
                        <strong>{get_translation("insight")}</strong> {get_translation("significant_insight")} {var1} dan {var2}.
                        {get_translation("independent_variables")}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="insight-box">
                        <strong>{get_translation("insight")}</strong> {get_translation("not_significant_insight")} {var1} dan {var2}.
                        {get_translation("independent_variables_alt")}
                    </div>
                    """, unsafe_allow_html=True)
    
    # Correlation analysis for numerical variables
    if len(numerical_cols) >= 2:
        st.markdown(f'<div style="font-size: 1.3rem; font-weight: 600; color: #7c3aed; margin: 1rem 0;">{get_translation("correlation_analysis")}</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            var3 = st.selectbox(get_translation("select_variable_1"), numerical_cols, key='num1')
        with col2:
            var4 = st.selectbox(get_translation("select_variable_2"), [col for col in numerical_cols if col != var3], key='num2')
        
        correlation_method = st.radio(get_translation("correlation_method"), [get_translation("pearson"), get_translation("spearman")])
        
        if st.button(get_translation("analyze_correlation")):
            # Remove rows with missing values for selected variables
            clean_df = df[[var3, var4]].dropna()
            
            # Calculate correlation
            if correlation_method == get_translation("pearson"):
                corr_coef, p_value = pearsonr(clean_df[var3], clean_df[var4])
            else:
                corr_coef, p_value = spearmanr(clean_df[var3], clean_df[var4])
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f'<div style="font-size: 1.1rem; font-weight: 600; color: #0891b2; margin: 0.5rem 0;">{get_translation("correlation_results")}</div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="metric-card">
                    <strong>{get_translation("correlation_coefficient")} ({correlation_method}):</strong> {corr_coef:.4f}<br>
                    <strong>{get_translation("p_value")}:</strong> {p_value:.4f}<br>
                    <strong>{get_translation("significance")}:</strong> {'✅ ' + get_translation("significant") if p_value < 0.05 else '❌ ' + get_translation("not_significant")}
                </div>
                """, unsafe_allow_html=True)
                
                # Interpretation
                strength = get_translation("correlation_strength")
                direction = get_translation("positive") if corr_coef > 0 else get_translation("negative")
                
                st.markdown(f"""
                <div class="insight-box">
                    <strong>{get_translation("insight")}</strong> {get_translation("correlation_insight")} {direction} {strength} {get_translation("between_variables")} {var3} dan {var4}.
                    {get_translation("statistical_significance") if p_value < 0.05 else get_translation("no_statistical_significance")}
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
        st.markdown(f'<div style="font-size: 1.3rem; font-weight: 600; color: #0891b2; margin: 1rem 0;">{get_translation("categorical_numerical_analysis")}</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            cat_var = st.selectbox(get_translation("select_categorical_variable"), categorical_cols, key='cat_num')
        with col2:
            num_var = st.selectbox(get_translation("select_numerical_variable"), numerical_cols, key='num_cat')
        
        if st.button(get_translation("analyze_categorical_numerical")):
            # Group by categorical variable
            grouped_data = df.groupby(cat_var)[num_var].describe()
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f'<div style="font-size: 1.1rem; font-weight: 600; color: #0d9488; margin: 0.5rem 0;">{get_translation("statistics_by").format(num_var, cat_var)}</div>', unsafe_allow_html=True)
                st.dataframe(grouped_data.round(2), use_container_width=True)
            
            with col2:
                # Box plot by category
                fig_box_cat = px.box(df, x=cat_var, y=num_var, 
                                   title=get_translation("distribution_by").format(num_var, cat_var))
                fig_box_cat.update_layout(height=400)
                st.plotly_chart(fig_box_cat, use_container_width=True)
            
            # ANOVA test
            categories = df[cat_var].unique()
            category_groups = [df[df[cat_var] == cat][num_var].dropna() for cat in categories]
            
            # Remove empty groups
            category_groups = [group for group in category_groups if len(group) > 0]
            
            if len(category_groups) >= 2:
                f_stat, p_value = stats.f_oneway(*category_groups)
                
                st.markdown(f'<div style="font-size: 1.1rem; font-weight: 600; color: #dc2626; margin: 0.5rem 0;">{get_translation("anova_results")}</div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="metric-card">
                    <strong>{get_translation("f_statistic")}:</strong> {f_stat:.4f}<br>
                    <strong>{get_translation("p_value")}:</strong> {p_value:.4f}<br>
                    <strong>{get_translation("significance")}:</strong> {'✅ ' + get_translation("significant") if p_value < 0.05 else '❌ ' + get_translation("not_significant")}
                </div>
                """, unsafe_allow_html=True)
                
                if p_value < 0.05:
                    st.markdown(f"""
                    <div class="insight-box">
                        <strong>{get_translation("insight")}</strong> {get_translation("mean_difference_insight")} {num_var} {get_translation("between_categories")} {cat_var}.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="insight-box">
                        <strong>{get_translation("insight")}</strong> {get_translation("no_mean_difference_insight")} {num_var} {get_translation("between_categories_alt")}.
                    </div>
                    """, unsafe_allow_html=True)

def main():
    # Main header
    st.markdown(f'<h1 class="main-header">{get_translation("title")}</h1>', unsafe_allow_html=True)
    
    # Language buttons (functional) - ONLY IN TOP LEFT
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 6, 1])
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
    
    # Upload area - CENTERED IN MIDDLE
    if st.session_state.uploaded_file is None:
        st.markdown("""
        <div class="upload-container">
            <div class="upload-area">
                <div class="upload-title">""" + get_translation("upload_title") + """</div>
                <div class="upload-description">
                    """ + get_translation("upload_description") + """
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # File uploader (HIDDEN - used by JavaScript)
    uploaded_file = st.file_uploader(get_translation("upload_button"), type=['xlsx', 'xls', 'csv'], 
                                   help=get_translation("upload_step"),
                                   label_visibility="collapsed")
    
    if uploaded_file is not None:
        # Store file in session state
        st.session_state.uploaded_file = uploaded_file
        
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
                st.dataframe(df, use_container_width=True)
            
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

if __name__ == "__main__":
    main()
