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
from scipy import stats
from scipy.stats import chi2_contingency, pearsonr, spearmanr
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

# Set page config
st.set_page_config(
    page_title="Aplikasi Analisis Survey",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .insight-box {
        background-color: #e8f4fd;
        border-left: 4px solid #1f77b4;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
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
        st.markdown("### 📊 Dataset Overview")
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
            st.markdown("### 🔍 Missing Values")
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
            st.markdown("### 🔢 Statistik Numerik")
            stats_df = df[numerical_cols].describe().round(2)
            st.dataframe(stats_df, use_container_width=True)
    
    # Visualizations
    if numerical_cols:
        st.markdown("### 📊 Visualisasi Data Numerik")
        
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
            st.markdown("### 🔗 Matriks Korelasi")
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
        st.markdown("### 📋 Analisis Data Kategorikal")
        
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
        st.markdown("### 📊 Tabel Frekuensi")
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
        st.markdown("### 🎯 Uji Chi-Square (Variabel Kategorikal)")
        
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
                st.markdown("#### Tabel Kontingensi")
                st.dataframe(contingency_table, use_container_width=True)
            
            with col2:
                # Perform chi-square test
                chi2, p_value, dof, expected = chi2_contingency(contingency_table)
                
                st.markdown("#### Hasil Uji Chi-Square")
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
                    st.markdown("""
                    <div class="insight-box">
                        <strong>💡 Insight:</strong> Terdapat asosiasi yang signifikan antara variabel {} dan {}.
                        Variabel-variabel ini tidak independen satu sama lain.
                    </div>
                    """.format(var1, var2), unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="insight-box">
                        <strong>💡 Insight:</strong> Tidak terdapat asosiasi yang signifikan antara variabel {} dan {}.
                        Variabel-variabel ini cenderung independen.
                    </div>
                    """.format(var1, var2), unsafe_allow_html=True)
    
    # Correlation analysis for numerical variables
    if len(numerical_cols) >= 2:
        st.markdown("### 📊 Analisis Korelasi (Variabel Numerik)")
        
        col1, col2 = st.columns(2)
        with col1:
            var3 = st.selectbox("Pilih variabel numerik 1:", numerical_cols, key='num1')
        with col2:
            var4 = st.selectbox("Pilih variabel numerik 2:", [col for col in numerical_cols if col != var3], key='num2')
        
        correlation_method = st.radio("Metode Korelasi:", ['Pearson', 'Spearman'])
        
        if st.button("Analisis Korelasi"):
            # Remove rows with missing values for the selected variables
            clean_df = df[[var3, var4]].dropna()
            
            # Calculate correlation
            if correlation_method == 'Pearson':
                corr_coef, p_value = pearsonr(clean_df[var3], clean_df[var4])
            else:
                corr_coef, p_value = spearmanr(clean_df[var3], clean_df[var4])
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### Hasil Korelasi")
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
        st.markdown("### 🔄 Analisis Kategorikal vs Numerik")
        
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
                st.markdown(f"#### Statistik {num_var} berdasarkan {cat_var}")
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
                
                st.markdown("#### Hasil ANOVA")
                st.markdown(f"""
                <div class="metric-card">
                    <strong>F-statistic:</strong> {f_stat:.4f}<br>
                    <strong>P-value:</strong> {p_value:.4f}<br>
                    <strong>Signifikansi:</strong> {'✅ Signifikan' if p_value < 0.05 else '❌ Tidak Signifikan'}
                </div>
                """, unsafe_allow_html=True)
                
                if p_value < 0.05:
                    st.markdown("""
                    <div class="insight-box">
                        <strong>💡 Insight:</strong> Terdapat perbedaan yang signifikan dalam rata-rata {} antar kategori {}.
                    </div>
                    """.format(num_var, cat_var), unsafe_allow_html=True)

def main():
    # Main header
    st.markdown('<h1 class="main-header">📊 Aplikasi Analisis Data Survey</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.markdown("### 📋 Menu")
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
                    st.markdown("#### Kolom Numerik:")
                    for col in numerical_cols:
                        st.markdown(f"• {col}")
            
            with col2:
                if categorical_cols:
                    st.markdown("#### Kolom Kategorikal:")
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
            st.markdown("### 💾 Export Hasil Analisis")
            
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
                href = f'<a href="data:file/csv;base64,{b64}" download="survey_analysis_summary.csv">Download CSV Summary</a>'
                st.markdown(href, unsafe_allow_html=True)
    
    else:
        # Instructions
        st.markdown("""
        ## 🚀 Cara Menggunakan Aplikasi Ini
        
        1. **Upload File**: Klik tombol "Browse Files" di sidebar untuk mengupload file Excel (.xlsx) atau CSV (.csv)
        2. **Analisis Deskriptif**: Dapatkan statistik dasar, visualisasi distribusi, dan insight awal dari data Anda
        3. **Analisis Asosiasi**: Temukan hubungan antar variabel dengan uji statistik
        4. **Export Results**: Download hasil analisis dalam format CSV
        
        ### 📋 Fitur Utama:
        
        **Analisis Deskriptif:**
        - Statistik dasar (mean, median, modus, standar deviasi)
        - Visualisasi distribusi data
        - Analisis missing values
        - Matriks korelasi
        
        **Analisis Asosiasi:**
        - Uji Chi-Square untuk variabel kategorikal
        - Analisis korelasi (Pearson/Spearman) untuk variabel numerik
        - ANOVA untuk analisis kategorikal vs numerik
        - Visualisasi hubungan antar variabel
        
        ### 📊 Format File yang Didukung:
        - Excel (.xlsx)
        - CSV (.csv)
        """)
        
        # Sample data info
        st.info("💡 **Tip**: Pastikan data Anda memiliki header yang jelas dan format yang konsisten untuk hasil analisis yang optimal.")

if __name__ == "__main__":
    main()
