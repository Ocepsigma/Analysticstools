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

# Background image function - WORKING SOLUTION
def get_background_image():
    """Load background image from multiple sources"""
    background_styles = []
    
    # Try to load from different sources
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
        margin-top: 2rem;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        position: relative;
        z-index: 1;
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
        margin-bottom: 2rem;
        text-shadow: 0px 2px 4px rgba(0,0,0,0.1);
        animation: textGlow 3s ease-in-out infinite alternate;
    }
    
    /* Text glow animation */
    @keyframes textGlow {
        from { filter: drop-shadow(0 0 10px rgba(59, 130, 246, 0.5)); }
        to { filter: drop-shadow(0 0 20px rgba(59, 130, 246, 0.8)); }
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
    
    /* Upload area styling */
    .upload-area {
        background: linear-gradient(135deg, #f8fafc, #f1f5f9);
        border: 2px dashed #cbd5e1;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
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
        background: linear-gradient(135deg, #eff6ff, #dbeafe);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.15);
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
    
    /* Language buttons styling */
    .lang-button {
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
    }
    
    .lang-button:hover {
        background: #3b82f6;
        color: white;
        border-color: #3b82f6;
        transform: translateY(-1px);
    }
    
    .lang-button.active {
        background: #3b82f6;
        color: white;
        border-color: #3b82f6;
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
</style>

<!-- Floating elements -->
<div class="floating-element"></div>
<div class="floating-element"></div>
<div class="floating-element"></div>
<div class="floating-element"></div>
<div class="floating-element"></div>
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
            st.error("File tidak didukung. Harap upload file Excel (.xlsx) atau CSV (.csv)")
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
    st.markdown('<div class="section-header">📈 Analisis Deskriptif</div>', unsafe_allow_html=True)
    
    # Basic Statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div style="font-size: 1.3rem; font-weight: 600; color: #1e40af; margin: 1rem 0;">📊 Dataset Overview</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="metric-card">
            <strong>Jumlah Baris:</strong> {df.shape[0]:,}<br>
            <strong>Jumlah Kolom:</strong> {df.shape[1]}<br>
            <strong>Kolom Numerik:</strong> {len(numerical_cols)}<br>
            <strong>Kolom Kategorikal:</strong> {len(categorical_cols)}
        </div>
        """, unsafe_allow_html=True)
        
        # Missing values
        missing_data = df.isnull().sum()
        if missing_data.sum() > 0:
            st.markdown('<div style="font-size: 1.3rem; font-weight: 600; color: #f59e0b; margin: 1rem 0;">🔍 Missing Values</div>', unsafe_allow_html=True)
            missing_df = pd.DataFrame({
                'Kolom': missing_data.index,
                'Jumlah Missing': missing_data.values,
                'Persentase': (missing_data.values / len(df) * 100).round(2)
            })
            missing_df = missing_df[missing_df['Jumlah Missing'] > 0]
            st.dataframe(missing_df, use_container_width=True)
    
    with col2:
        # Numerical columns statistics
        if numerical_cols:
            st.markdown('<div style="font-size: 1.3rem; font-weight: 600; color: #059669; margin: 1rem 0;">🔢 Statistik Numerik</div>', unsafe_allow_html=True)
            stats_df = df[numerical_cols].describe().round(2)
            st.dataframe(stats_df, use_container_width=True)
    
    # Visualizations
    if numerical_cols:
        st.markdown('<div style="font-size: 1.3rem; font-weight: 600; color: #1e40af; margin: 1rem 0;">📊 Visualisasi Data Numerik</div>', unsafe_allow_html=True)
        
        # Distribution plots
        selected_num_col = st.selectbox("Pilih kolom numerik untuk distribusi:", numerical_cols)
        
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
            st.markdown('<div style="font-size: 1.3rem; font-weight: 600; color: #7c3aed; margin: 1rem 0;">🔗 Matriks Korelasi</div>', unsafe_allow_html=True)
            correlation_matrix = df[numerical_cols].corr()
            
            fig_corr = px.imshow(correlation_matrix, 
                                text_auto=True, 
                                aspect="auto",
                                color_continuous_scale='RdBu_r',
                                title='Matriks Korelasi Variabel Numerik')
            fig_corr.update_layout(height=500)
            st.plotly_chart(fig_corr, use_container_width=True)
    
    # Categorical analysis
    if categorical_cols:
        st.markdown('<div style="font-size: 1.3rem; font-weight: 600; color: #dc2626; margin: 1rem 0;">📋 Analisis Data Kategorikal</div>', unsafe_allow_html=True)
        
        selected_cat_col = st.selectbox("Pilih kolom kategorikal:", categorical_cols)
        
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
        st.markdown('<div style="font-size: 1.3rem; font-weight: 600; color: #0891b2; margin: 1rem 0;">📊 Tabel Frekuensi</div>', unsafe_allow_html=True)
        freq_table = pd.DataFrame({
            'Kategori': value_counts.index,
            'Frekuensi': value_counts.values,
            'Persentase': (value_counts.values / len(df) * 100).round(2)
        })
        st.dataframe(freq_table, use_container_width=True)

def association_analysis(df, numerical_cols, categorical_cols):
    """Perform association analysis"""
    st.markdown('<div class="section-header">🔗 Analisis Asosiasi</div>', unsafe_allow_html=True)
    
    # Chi-square test for categorical variables
    if len(categorical_cols) >= 2:
        st.markdown('<div style="font-size: 1.3rem; font-weight: 600; color: #ea580c; margin: 1rem 0;">🎯 Uji Chi-Square (Variabel Kategorikal)</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            var1 = st.selectbox("Pilih variabel 1:", categorical_cols, key='cat1')
        with col2:
            var2 = st.selectbox("Pilih variabel 2:", [col for col in categorical_cols if col != var1], key='cat2')
        
        if st.button("Analisis Chi-Square"):
            # Create contingency table
            contingency_table = pd.crosstab(df[var1], df[var2])
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div style="font-size: 1.1rem; font-weight: 600; color: #dc2626; margin: 0.5rem 0;">Tabel Kontingensi</div>', unsafe_allow_html=True)
                st.dataframe(contingency_table, use_container_width=True)
            
            with col2:
                # Perform chi-square test
                chi2, p_value, dof, expected = chi2_contingency(contingency_table)
                
                st.markdown('<div style="font-size: 1.1rem; font-weight: 600; color: #059669; margin: 0.5rem 0;">Hasil Uji Chi-Square</div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="metric-card">
                    <strong>Chi-Square Statistic:</strong> {chi2:.4f}<br>
                    <strong>P-value:</strong> {p_value:.4f}<br>
                    <strong>Degrees of Freedom:</strong> {dof}<br>
                    <strong>Signifikansi:</strong> {'✅ Signifikan' if p_value < 0.05 else '❌ Tidak Signifikan'}
                </div>
                """, unsafe_allow_html=True)
                
                # Interpretation
                if p_value < 0.05:
                    st.markdown(f"""
                    <div class="insight-box">
                        <strong>💡 Insight:</strong> Terdapat asosiasi yang signifikan antara variabel {var1} dan {var2}.
                        Variabel-variabel ini tidak independen satu sama lain.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="insight-box">
                        <strong>💡 Insight:</strong> Tidak terdapat asosiasi yang signifikan antara variabel {var1} dan {var2}.
                        Variabel-variabel ini cenderung independen.
                    </div>
                    """, unsafe_allow_html=True)
    
    # Correlation analysis for numerical variables
    if len(numerical_cols) >= 2:
        st.markdown('<div style="font-size: 1.3rem; font-weight: 600; color: #7c3aed; margin: 1rem 0;">📊 Analisis Korelasi (Variabel Numerik)</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            var3 = st.selectbox("Pilih variabel numerik 1:", numerical_cols, key='num1')
        with col2:
            var4 = st.selectbox("Pilih variabel numerik 2:", [col for col in numerical_cols if col != var3], key='num2')
        
        correlation_method = st.radio("Metode Korelasi:", ['Pearson', 'Spearman'])
        
        if st.button("Analisis Korelasi"):
            # Remove rows with missing values for selected variables
            clean_df = df[[var3, var4]].dropna()
            
            # Calculate correlation
            if correlation_method == 'Pearson':
                corr_coef, p_value = pearsonr(clean_df[var3], clean_df[var4])
            else:
                corr_coef, p_value = spearmanr(clean_df[var3], clean_df[var4])
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div style="font-size: 1.1rem; font-weight: 600; color: #0891b2; margin: 0.5rem 0;">Hasil Korelasi</div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="metric-card">
                    <strong>Koefisien Korelasi ({correlation_method}):</strong> {corr_coef:.4f}<br>
                    <strong>P-value:</strong> {p_value:.4f}<br>
                    <strong>Signifikansi:</strong> {'✅ Signifikan' if p_value < 0.05 else '❌ Tidak Signifikan'}
                </div>
                """, unsafe_allow_html=True)
                
                # Interpretation
                strength = "sangat kuat" if abs(corr_coef) >= 0.8 else "kuat" if abs(corr_coef) >= 0.6 else "sedang" if abs(corr_coef) >= 0.4 else "lemah" if abs(corr_coef) >= 0.2 else "sangat lemah"
                direction = "positif" if corr_coef > 0 else "negatif"
                
                st.markdown(f"""
                <div class="insight-box">
                    <strong>💡 Insight:</strong> Terdapat hubungan {direction} yang {strength} antara {var3} dan {var4}.
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
        st.markdown('<div style="font-size: 1.3rem; font-weight: 600; color: #0891b2; margin: 1rem 0;">🔄 Analisis Kategorikal vs Numerik</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            cat_var = st.selectbox("Pilih variabel kategorikal:", categorical_cols, key='cat_num')
        with col2:
            num_var = st.selectbox("Pilih variabel numerik:", numerical_cols, key='num_cat')
        
        if st.button("Analisis Kategorikal-Numerik"):
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
                
                st.markdown('<div style="font-size: 1.1rem; font-weight: 600; color: #dc2626; margin: 0.5rem 0;">Hasil ANOVA</div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="metric-card">
                    <strong>F-statistic:</strong> {f_stat:.4f}<br>
                    <strong>P-value:</strong> {p_value:.4f}<br>
                    <strong>Signifikansi:</strong> {'✅ Signifikan' if p_value < 0.05 else '❌ Tidak Signifikan'}
                </div>
                """, unsafe_allow_html=True)
                
                if p_value < 0.05:
                    st.markdown(f"""
                    <div class="insight-box">
                        <strong>💡 Insight:</strong> Terdapat perbedaan yang signifikan dalam rata-rata {num_var} antar kategori {cat_var}.
                    </div>
                    """, unsafe_allow_html=True)

def main():
    # Language selector
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; margin: 1rem 0;">
            <span class="lang-button active">🇮🇩 Indonesia</span>
            <span class="lang-button">🇬🇧 English</span>
            <span class="lang-button">🇨🇳 中文</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Main header
    st.markdown('<h1 class="main-header">Analisis Data Survei</h1>', unsafe_allow_html=True)
    
    # Upload area - inspired by first image
    st.markdown("""
    <div class="upload-area">
        <h3 style="color: #1e40af; margin-bottom: 1rem;">Unggah File Excel Anda untuk memulai analisis</h3>
        <p style="color: #64748b; margin-bottom: 1rem;">Drag and drop file here<br>Limit 200MB per file • XLSX, XLS</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.markdown('<div style="font-size: 1.3rem; font-weight: 600; color: white; margin: 1rem 0;">📋 Menu</div>', unsafe_allow_html=True)
    st.sidebar.markdown("Upload file Excel/CSV survey Anda untuk memulai analisis.")
    
    # File upload
    uploaded_file = st.sidebar.file_uploader("Upload File Survey", type=['xlsx', 'csv'])
    
    if uploaded_file is not None:
        # Load data
        with st.spinner("Memuat data..."):
            df = load_data(uploaded_file)
        
        if df is not None:
            # Success message
            st.success(f"✅ Data berhasil dimuat! Dataset memiliki {df.shape[0]} baris dan {df.shape[1]} kolom.")
            
            # Show raw data
            with st.expander("👀 Lihat Data Mentah"):
                st.dataframe(df, use_container_width=True)
            
            # Get column types
            numerical_cols, categorical_cols = get_column_types(df)
            
            # Show column information
            col1, col2 = st.columns(2)
            with col1:
                if numerical_cols:
                    st.markdown('<div style="font-size: 1.1rem; font-weight: 600; color: #1e40af; margin: 0.5rem 0;">Kolom Numerik:</div>', unsafe_allow_html=True)
                    for col in numerical_cols:
                        st.markdown(f"• {col}")
            
            with col2:
                if categorical_cols:
                    st.markdown('<div style="font-size: 1.1rem; font-weight: 600; color: #dc2626; margin: 0.5rem 0;">Kolom Kategorikal:</div>', unsafe_allow_html=True)
                    for col in categorical_cols:
                        st.markdown(f"• {col}")
            
            # Analysis tabs
            tab1, tab2 = st.tabs(["📈 Analisis Deskriptif", "🔗 Analisis Asosiasi"])
            
            with tab1:
                descriptive_analysis(df, numerical_cols, categorical_cols)
            
            with tab2:
                association_analysis(df, numerical_cols, categorical_cols)
            
            # Export functionality
            st.markdown("---")
            st.markdown('<div style="font-size: 1.3rem; font-weight: 600; color: #059669; margin: 1rem 0;">💾 Export Hasil Analisis</div>', unsafe_allow_html=True)
            
            if st.button("Download Summary Report"):
                # Create a summary report
                summary_data = {
                    'Metric': ['Total Rows', 'Total Columns', 'Numerical Columns', 'Categorical Columns', 'Missing Values'],
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
        st.markdown("""
<div style="background: rgba(255, 255, 255, 0.9); padding: 2rem; border-radius: 15px; border: 1px solid #e5e7eb; margin: 1rem 0;">
<h2 style="color: #1e40af; margin-bottom: 1rem;">🚀 Cara Menggunakan Aplikasi Ini</h2>
<ol style="color: #374151; line-height: 1.6;">
    <li><strong style="color: #3b82f6;">Upload File</strong>: Klik tombol "Browse Files" di sidebar untuk mengupload file Excel (.xlsx) atau CSV (.csv)</li>
    <li><strong style="color: #7c3aed;">Analisis Deskriptif</strong>: Dapatkan statistik dasar, visualisasi distribusi, dan insight awal dari data Anda</li>
    <li><strong style="color: #dc2626;">Analisis Asosiasi</strong>: Temukan hubungan antar variabel dengan uji statistik</li>
    <li><strong style="color: #059669;">Export Results</strong>: Download hasil analisis dalam format CSV</li>
</ol>

<h3 style="color: #1e40af; margin: 1.5rem 0 1rem 0;">📋 Fitur Utama:</h3>

<div style="background: #f8fafc; padding: 1rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #3b82f6;">
<h4 style="color: #1e40af; margin-bottom: 0.5rem;">📈 Analisis Deskriptif:</h4>
<ul style="color: #374151; line-height: 1.5;">
    <li>Statistik dasar (mean, median, modus, standar deviasi)</li>
    <li>Visualisasi distribusi data</li>
    <li>Analisis missing values</li>
    <li>Matriks korelasi</li>
</ul>
</div>

<div style="background: #f8fafc; padding: 1rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #dc2626;">
<h4 style="color: #dc2626; margin-bottom: 0.5rem;">🔗 Analisis Asosiasi:</h4>
<ul style="color: #374151; line-height: 1.5;">
    <li>Uji Chi-Square untuk variabel kategorikal</li>
    <li>Analisis korelasi (Pearson/Spearman) untuk variabel numerik</li>
    <li>ANOVA untuk analisis kategorikal vs numerik</li>
    <li>Visualisasi hubungan antar variabel</li>
</ul>
</div>

<h3 style="color: #ea580c; margin: 1.5rem 0 1rem 0;">📊 Format File yang Didukung:</h3>
<ul style="color: #374151; line-height: 1.5;">
    <li>Excel (.xlsx)</li>
    <li>CSV (.csv)</li>
</ul>

<div style="background: linear-gradient(135deg, #eff6ff, #dbeafe); padding: 1rem; border-radius: 10px; border-left: 4px solid #3b82f6; margin: 1rem 0;">
<p style="color: #1e40af; margin: 0; font-weight: 600;">💡 <strong>Tip</strong>: Pastikan data Anda memiliki header yang jelas dan format yang konsisten untuk hasil analisis yang optimal.</p>
</div>
</div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
