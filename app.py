# =============================================================================
# 📊 DATA SCIENCE JOB POSTS 2025 - VISUALIZATION DASHBOARD
# =============================================================================
# Gece modu uyumlu, profesyonel veri görselleştirme uygulaması
# =============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import ast
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# 🎨 SAYFA AYARLARI
# =============================================================================
st.set_page_config(
    page_title="📊 Data Science Jobs 2025 Veri Setii Analiz Dashboardu",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================================================================
# 🎨 GECE MODU UYUMLU CSS
# =============================================================================
st.markdown("""
<style>
    /* Ana arka plan */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    /* Başlık stilleri */
    .main-header {
        font-size: 10rem;
        font-weight: bold;
        color: #00d4ff;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.6);
    }
    .sub-header {
        font-size: 1.8rem;
        color: #a0a0a0;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Yorum kutusu */
    .insight-box {
        background-color: #1a1f2e;
        border-left: 4px solid #00d4ff;
        padding: 1rem 1.2rem;
        margin: 1rem 0;
        border-radius: 0 8px 8px 0;
        color: #e0e0e0;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    .insight-box strong {
        color: #00d4ff;
    }
    
    /* Bölüm ayırıcı */
    .section-divider {
        border-top: 1px solid #2d3748;
        margin: 2.5rem 0;
    }
    
    /* DataFrame tabloları için koyu tema */
    .stDataFrame {
        background-color: #1a1f2e !important;
    }
    .stDataFrame [data-testid="stDataFrameResizable"] {
        background-color: #1a1f2e !important;
    }
    
    /* Metrik kartları */
    div[data-testid="stMetricValue"] {
        color: #00d4ff;
        font-size: 1.8rem;
    }
    div[data-testid="stMetricLabel"] {
        color: #a0a0a0;
    }
    
    /* Tab butonları - büyütülmüş */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1a1f2e;
        color: #e0e0e0;
        border-radius: 8px;
        padding: 12px 24px;
        font-size: 1rem;
        font-weight: 500;
        border: 1px solid #2d3748;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #2d3748;
        border-color: #00d4ff;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00d4ff !important;
        color: #0e1117 !important;
        font-weight: 600;
    }
    
    /* Başlıklar */
    h1, h2, h3, h4, h5, h6 {
        color: #fafafa !important;
    }
    
    /* Tablo başlıkları ve içeriği */
    .dataframe {
        background-color: #1a1f2e !important;
        color: #e0e0e0 !important;
    }
    .dataframe th {
        background-color: #252d3d !important;
        color: #00d4ff !important;
    }
    .dataframe td {
        background-color: #1a1f2e !important;
        color: #e0e0e0 !important;
    }
    
    /* Özel tablo stili */
    .dark-table {
        width: 100%;
        border-collapse: collapse;
        background-color: #1a1f2e;
        border-radius: 8px;
        overflow: hidden;
        margin: 1rem 0;
    }
    .dark-table th {
        background-color: #252d3d;
        color: #00d4ff;
        padding: 12px 16px;
        text-align: left;
        font-weight: 600;
        border-bottom: 2px solid #3d4a5c;
    }
    .dark-table td {
        padding: 10px 16px;
        color: #e0e0e0;
        border-bottom: 1px solid #2d3748;
    }
    .dark-table tr:hover {
        background-color: #252d3d;
    }
    
    /* Selectbox ve diğer input'lar */
    .stSelectbox label, .stMultiSelect label {
        color: #e0e0e0 !important;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# 📂 VERİ YÜKLEME FONKSİYONLARI
# =============================================================================
@st.cache_data
def load_data():
    """Veri setini yükle"""
    df = pd.read_csv('data_science_job_posts_2025.csv')
    return df

@st.cache_data
def parse_salary(salary_str):
    """Maaş değerini sayısala çevir"""
    if pd.isna(salary_str) or salary_str == '':
        return np.nan
    salary_str = str(salary_str).replace('€', '').replace(',', '')
    if ' - ' in salary_str:
        try:
            parts = salary_str.split(' - ')
            return (float(parts[0].strip()) + float(parts[1].strip())) / 2
        except:
            return np.nan
    try:
        return float(salary_str.strip())
    except:
        return np.nan

@st.cache_data
def parse_skills(skills_str):
    """Skills listesini parse et"""
    if pd.isna(skills_str) or skills_str == '[]':
        return []
    try:
        return ast.literal_eval(skills_str)
    except:
        return []

@st.cache_data
def parse_company_size(size_str):
    """Şirket büyüklüğünü sayısala çevir"""
    if pd.isna(size_str):
        return np.nan
    size_str = str(size_str).replace(',', '').replace('€', '').strip()
    try:
        return float(size_str)
    except:
        return np.nan

# HTML tablo oluşturucu (gece modu uyumlu)
def create_dark_table(df, max_rows=None):
    """Gece moduna uygun HTML tablo oluştur"""
    if max_rows:
        df = df.head(max_rows)
    
    html = '<table class="dark-table">'
    # Başlık satırı
    html += '<thead><tr>'
    for col in df.columns:
        html += f'<th>{col}</th>'
    html += '</tr></thead>'
    # Veri satırları
    html += '<tbody>'
    for _, row in df.iterrows():
        html += '<tr>'
        for val in row:
            html += f'<td>{val}</td>'
        html += '</tr>'
    html += '</tbody></table>'
    return html

# =============================================================================
# VERİ YÜKLEME VE ÖN İŞLEME
# =============================================================================
try:
    df = load_data()
    # Veri ön işleme
    df['salary_numeric'] = df['salary'].apply(parse_salary)
    df['company_size_numeric'] = df['company_size'].apply(parse_company_size)
    df['skills_list'] = df['skills'].apply(parse_skills)
    df['skills_count'] = df['skills_list'].apply(len)
    data_loaded = True
except FileNotFoundError:
    data_loaded = False
    st.error("❌ 'data_science_job_posts_2025.csv' dosyası bulunamadı!")

# =============================================================================
# 1️⃣ BAŞLIK + AÇIKLAMA
# =============================================================================
st.markdown('<h1 style="font-size: 4rem; font-weight: bold; color: #00d4ff; text-align: center; margin-bottom: 0.5rem; text-shadow: 3px 3px 6px rgba(0,0,0,0.6);">📊 Data Science Job Posts 2025</h1>', unsafe_allow_html=True)
st.markdown('<p style="font-size: 2rem; color: #a0a0a0; text-align: center; margin-bottom: 2rem;">2025 Yılı Veri Bilimi İş İlanları Analiz Dashboardu</p>', unsafe_allow_html=True)

st.markdown("""
<div class="insight-box">
    <strong>🎯 Bu Dashboard ile:</strong> Veri bilimi iş piyasasındaki trendleri keşfedin, 
    maaş dağılımlarını analiz edin, en çok aranan becerileri görün ve sektörel karşılaştırmalar yapın.
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

if data_loaded:
    # ==========================================================================
    # 2️⃣ ÖRNEK VERİLER VE SÜTUN BİLGİSİ
    # ==========================================================================
    st.header("📁 Örnek Veriler ve Sütun Bilgisi")
    
    # Metrikler
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 Toplam İlan", f"{df.shape[0]:,}")
    with col2:
        st.metric("📋 Özellik Sayısı", 13)
    with col3:
        st.metric("💰 Ort. Maaş", f"€{df['salary_numeric'].mean():,.0f}")
    with col4:
        st.metric("🏢 Şirket Sayısı", df['company'].nunique())
    
    st.subheader("🔍 Örnek Veriler")
    display_cols = ['job_title', 'seniority_level', 'status', 'company', 'location', 'industry', 'salary']
    sample_df = df[display_cols].head(10).copy()
    sample_df.columns = ['Pozisyon', 'Kıdem', 'Durum', 'Şirket', 'Lokasyon', 'Sektör', 'Maaş']
    st.markdown(create_dark_table(sample_df), unsafe_allow_html=True)
    
    # Sütun bilgileri
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Sütunlar")
        original_cols = [col for col in df.columns if col not in ['salary_numeric', 'company_size_numeric', 'skills_list', 'skills_count']]
        columns_info = pd.DataFrame({
            'Sütun Adı': original_cols,
            'Veri Tipi': [str(df[col].dtype) for col in original_cols]
        })
        st.markdown(create_dark_table(columns_info), unsafe_allow_html=True)
    
    with col2:
        st.subheader("📊 Değişken Özeti")
        summary_df = pd.DataFrame({
            'Metrik': ['Sayısal Değişken', 'Kategorik Değişken', 'Toplam Satır', 'Toplam Sütun'],
            'Değer': [3, 10, df.shape[0], 13]
        })
        st.markdown(create_dark_table(summary_df), unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box">
        <strong>💡 Yorum:</strong> Veri seti 946 iş ilanı içermektedir. Her ilan için pozisyon, 
        kıdem seviyesi, lokasyon, sektör, maaş ve gereken beceriler gibi detaylı bilgiler bulunmaktadır.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # ==========================================================================
    # 3️⃣ EKSİK DEĞER ANALİZİ
    # ==========================================================================
    st.header("🔍 Eksik Değer Analizi")
    
    # Eksik değer hesaplama
    original_cols = [col for col in df.columns if col not in ['salary_numeric', 'company_size_numeric', 'skills_list', 'skills_count']]
    missing_data = []
    for col in original_cols:
        null_count = df[col].isnull().sum()
        empty_count = (df[col] == '').sum() if df[col].dtype == 'object' else 0
        total_missing = null_count + empty_count
        missing_data.append({
            'Sütun': col,
            'Eksik Sayı': total_missing,
            'Oran (%)': round(total_missing / len(df) * 100, 2)
        })
    
    missing_df = pd.DataFrame(missing_data).sort_values('Eksik Sayı', ascending=False)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(create_dark_table(missing_df), unsafe_allow_html=True)
    
    with col2:
        # Eksik değer grafiği - daha yüksek boyut
        missing_filtered = missing_df[missing_df['Eksik Sayı'] > 0]
        
        if len(missing_filtered) > 0:
            fig_missing = px.bar(
                missing_filtered,
                x='Sütun',
                y='Eksik Sayı',
                color='Oran (%)',
                title='<b>Sütunlara Göre Eksik Değer Dağılımı</b>',
                template='plotly_dark',
                color_continuous_scale='Reds',
                height=450  # Daha yüksek
            )
            fig_missing.update_layout(
                title_font=dict(size=18, color='#00d4ff'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e0e0e0'),
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig_missing, use_container_width=True)
        else:
            st.success("✅ Veri setinde eksik değer bulunmamaktadır!")
    
    st.markdown("""
    <div class="insight-box">
        <strong>💡 Yorum:</strong> Eksik değerler analiz edildiğinde, seniority_level ve status 
        sütunlarında en fazla eksiklik görülmektedir. Bu durum, bazı iş ilanlarında bu bilgilerin 
        paylaşılmadığını göstermektedir. Model geliştirme aşamasında bu eksiklikler dikkate alınmalıdır.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # ==========================================================================
    # 3.5️⃣ AYKIRI DEĞER ANALİZİ
    # ==========================================================================
    st.header("📉 Aykırı Değer Analizi")
    
    st.markdown("""
    <div class="insight-box">
        <strong>🎯 Aykırı Değer Tespiti:</strong> IQR (Interquartile Range) yöntemi kullanılarak 
        aykırı değerler tespit edilmiştir. Q1 - 1.5*IQR alt sınır, Q3 + 1.5*IQR üst sınır olarak belirlenir.
    </div>
    """, unsafe_allow_html=True)
    
    # Aykırı değer hesaplama fonksiyonu
    def detect_outliers_iqr(data):
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = data[(data < lower_bound) | (data > upper_bound)]
        return outliers, lower_bound, upper_bound, Q1, Q3, IQR
    
    # Maaş için aykırı değer analizi
    salary_clean = df['salary_numeric'].dropna()
    outliers_salary, lb_salary, ub_salary, q1_salary, q3_salary, iqr_salary = detect_outliers_iqr(salary_clean)
    
    # Şirket büyüklüğü için aykırı değer analizi
    company_size_clean = df['company_size_numeric'].dropna()
    outliers_size, lb_size, ub_size, q1_size, q3_size, iqr_size = detect_outliers_iqr(company_size_clean)
    
    # Beceri sayısı için aykırı değer analizi (tablo için)
    skills_count_data = df['skills_count'].dropna()
    outliers_skills_data, lb_skills_data, ub_skills_data, q1_skills_data, q3_skills_data, iqr_skills_data = detect_outliers_iqr(skills_count_data)
    
    # Aykırı değer istatistikleri tablosu
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Aykırı Değer İstatistikleri")
        outlier_stats = pd.DataFrame({
            'Metrik': ['Q1 (25%)', 'Q3 (75%)', 'IQR', 'Alt Sınır', 'Üst Sınır', 'Aykırı Değer Sayısı', 'Aykırı Oran (%)'],
            'Maaş (€)': [
                f"{q1_salary:,.0f}",
                f"{q3_salary:,.0f}",
                f"{iqr_salary:,.0f}",
                f"{lb_salary:,.0f}",
                f"{ub_salary:,.0f}",
                f"{len(outliers_salary)}",
                f"{len(outliers_salary)/len(salary_clean)*100:.1f}%"
            ],
            'Şirket Büyüklüğü': [
                f"{q1_size:,.0f}" if len(company_size_clean) > 0 else "N/A",
                f"{q3_size:,.0f}" if len(company_size_clean) > 0 else "N/A",
                f"{iqr_size:,.0f}" if len(company_size_clean) > 0 else "N/A",
                f"{lb_size:,.0f}" if len(company_size_clean) > 0 else "N/A",
                f"{ub_size:,.0f}" if len(company_size_clean) > 0 else "N/A",
                f"{len(outliers_size)}" if len(company_size_clean) > 0 else "N/A",
                f"{len(outliers_size)/len(company_size_clean)*100:.1f}%" if len(company_size_clean) > 0 else "N/A"
            ],
            'Beceri Sayısı': [
                f"{q1_skills_data:.0f}",
                f"{q3_skills_data:.0f}",
                f"{iqr_skills_data:.0f}",
                f"{lb_skills_data:.0f}",
                f"{ub_skills_data:.0f}",
                f"{len(outliers_skills_data)}",
                f"{len(outliers_skills_data)/len(skills_count_data)*100:.1f}%"
            ]
        })
        st.markdown(create_dark_table(outlier_stats), unsafe_allow_html=True)
    
    with col2:
        st.subheader("📝 Özet")
        total_outliers = len(outliers_salary) + len(outliers_size) + len(outliers_skills_data)
        summary_outlier = pd.DataFrame({
            'Değişken': ['Maaş', 'Şirket Büyüklüğü', 'Beceri Sayısı', 'Toplam'],
            'Aykırı Sayısı': [len(outliers_salary), len(outliers_size), len(outliers_skills_data), total_outliers],
            'Durum': [
                '⚠️ Yüksek' if len(outliers_salary) > 50 else '✅ Normal',
                '⚠️ Yüksek' if len(outliers_size) > 50 else '✅ Normal',
                '⚠️ Yüksek' if len(outliers_skills_data) > 50 else '✅ Normal',
                '⚠️ Dikkat' if total_outliers > 100 else '✅ Kabul Edilebilir'
            ]
        })
        st.markdown(create_dark_table(summary_outlier), unsafe_allow_html=True)
    
    # Aykırı değer grafikleri - ÖNCE ve SONRA
    st.subheader("📊 Maaş Dağılımı: Aykırı Değer Öncesi vs Sonrası")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # ÖNCE - Aykırı değerler dahil
        fig_before = go.Figure()
        fig_before.add_trace(go.Box(
            y=salary_clean,
            name='Maaş (Önce)',
            boxpoints='outliers',
            marker_color='#ff6b6b',
            line_color='#ff6b6b'
        ))
        fig_before.update_layout(
            title='<b>🟥 Aykırı Değerler DAHİL</b>',
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            title_font=dict(size=16, color='#ff6b6b'),
            font=dict(color='#e0e0e0'),
            yaxis_title='Maaş (€)',
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig_before, use_container_width=True)
        
        st.markdown(f"""
        <div class="insight-box">
            <strong>🟥 Önce:</strong> Toplam {len(salary_clean):,} kayıt<br>
            Min: €{salary_clean.min():,.0f} | Max: €{salary_clean.max():,.0f}<br>
            Aykırı Değer: {len(outliers_salary)} adet
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # SONRA - Aykırı değerler hariç
        salary_no_outliers = salary_clean[(salary_clean >= lb_salary) & (salary_clean <= ub_salary)]
        
        fig_after = go.Figure()
        fig_after.add_trace(go.Box(
            y=salary_no_outliers,
            name='Maaş (Sonra)',
            boxpoints='outliers',
            marker_color='#00d4ff',
            line_color='#00d4ff'
        ))
        fig_after.update_layout(
            title='<b>🟦 Aykırı Değerler HARİÇ</b>',
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            title_font=dict(size=16, color='#00d4ff'),
            font=dict(color='#e0e0e0'),
            yaxis_title='Maaş (€)',
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig_after, use_container_width=True)
        
        st.markdown(f"""
        <div class="insight-box">
            <strong>🟦 Sonra:</strong> Toplam {len(salary_no_outliers):,} kayıt<br>
            Min: €{salary_no_outliers.min():,.0f} | Max: €{salary_no_outliers.max():,.0f}<br>
            Silinen: {len(salary_clean) - len(salary_no_outliers)} kayıt
        </div>
        """, unsafe_allow_html=True)
    
    # Histogram karşılaştırması
    st.subheader("📊 Histogram Karşılaştırması")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_hist_before = px.histogram(
            x=salary_clean,
            nbins=50,
            title='<b>🟥 Maaş Histogramı (Önce)</b>',
            template='plotly_dark',
            labels={'x': 'Maaş (€)', 'y': 'Frekans'}
        )
        fig_hist_before.update_traces(marker_color='#ff6b6b')
        fig_hist_before.update_layout(
            title_font=dict(size=16, color='#ff6b6b'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0'),
            height=350
        )
        st.plotly_chart(fig_hist_before, use_container_width=True)
    
    with col2:
        fig_hist_after = px.histogram(
            x=salary_no_outliers,
            nbins=50,
            title='<b>🟦 Maaş Histogramı (Sonra)</b>',
            template='plotly_dark',
            labels={'x': 'Maaş (€)', 'y': 'Frekans'}
        )
        fig_hist_after.update_traces(marker_color='#00d4ff')
        fig_hist_after.update_layout(
            title_font=dict(size=16, color='#00d4ff'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0'),
            height=350
        )
        st.plotly_chart(fig_hist_after, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box">
        <strong>💡 Yorum:</strong> Aykırı değerler temizlendikten sonra maaş dağılımı daha homojen 
        bir yapıya kavuşmuştur. Sol taraftaki grafiklerde (kırmızı) aşırı yüksek maaş değerleri 
        görülürken, sağ taraftaki temizlenmiş verilerde (mavi) daha tutarlı bir dağılım elde edilmiştir.
    </div>
    """, unsafe_allow_html=True)
    
    # ŞİRKET BÜYÜKLÜĞÜ AYKIRI DEĞER ANALİZİ
    if len(company_size_clean) > 0:
        st.subheader("🏢 Şirket Büyüklüğü: Aykırı Değer Öncesi vs Sonrası")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # ÖNCE - Aykırı değerler dahil
            fig_size_before = go.Figure()
            fig_size_before.add_trace(go.Box(
                y=company_size_clean,
                name='Şirket Büyüklüğü (Önce)',
                boxpoints='outliers',
                marker_color='#ff6b6b',
                line_color='#ff6b6b'
            ))
            fig_size_before.update_layout(
                title='<b>🟥 Aykırı Değerler DAHİL</b>',
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                title_font=dict(size=16, color='#ff6b6b'),
                font=dict(color='#e0e0e0'),
                yaxis_title='Şirket Büyüklüğü (Çalışan Sayısı)',
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig_size_before, use_container_width=True)
            
            st.markdown(f"""
            <div class="insight-box">
                <strong>🟥 Önce:</strong> Toplam {len(company_size_clean):,} kayıt<br>
                Min: {company_size_clean.min():,.0f} | Max: {company_size_clean.max():,.0f}<br>
                Aykırı Değer: {len(outliers_size)} adet
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # SONRA - Aykırı değerler hariç
            size_no_outliers = company_size_clean[(company_size_clean >= lb_size) & (company_size_clean <= ub_size)]
            
            fig_size_after = go.Figure()
            fig_size_after.add_trace(go.Box(
                y=size_no_outliers,
                name='Şirket Büyüklüğü (Sonra)',
                boxpoints='outliers',
                marker_color='#00d4ff',
                line_color='#00d4ff'
            ))
            fig_size_after.update_layout(
                title='<b>🟦 Aykırı Değerler HARİÇ</b>',
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                title_font=dict(size=16, color='#00d4ff'),
                font=dict(color='#e0e0e0'),
                yaxis_title='Şirket Büyüklüğü (Çalışan Sayısı)',
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig_size_after, use_container_width=True)
            
            st.markdown(f"""
            <div class="insight-box">
                <strong>🟦 Sonra:</strong> Toplam {len(size_no_outliers):,} kayıt<br>
                Min: {size_no_outliers.min():,.0f} | Max: {size_no_outliers.max():,.0f}<br>
                Silinen: {len(company_size_clean) - len(size_no_outliers)} kayıt
            </div>
            """, unsafe_allow_html=True)
        
        # Şirket büyüklüğü histogram karşılaştırması
        st.subheader("📊 Şirket Büyüklüğü Histogram Karşılaştırması")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_size_hist_before = px.histogram(
                x=company_size_clean,
                nbins=50,
                title='<b>🟥 Şirket Büyüklüğü Histogramı (Önce)</b>',
                template='plotly_dark',
                labels={'x': 'Şirket Büyüklüğü', 'y': 'Frekans'}
            )
            fig_size_hist_before.update_traces(marker_color='#ff6b6b')
            fig_size_hist_before.update_layout(
                title_font=dict(size=16, color='#ff6b6b'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e0e0e0'),
                height=350
            )
            st.plotly_chart(fig_size_hist_before, use_container_width=True)
        
        with col2:
            fig_size_hist_after = px.histogram(
                x=size_no_outliers,
                nbins=50,
                title='<b>🟦 Şirket Büyüklüğü Histogramı (Sonra)</b>',
                template='plotly_dark',
                labels={'x': 'Şirket Büyüklüğü', 'y': 'Frekans'}
            )
            fig_size_hist_after.update_traces(marker_color='#00d4ff')
            fig_size_hist_after.update_layout(
                title_font=dict(size=16, color='#00d4ff'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e0e0e0'),
                height=350
            )
            st.plotly_chart(fig_size_hist_after, use_container_width=True)
        
        st.markdown("""
        <div class="insight-box">
            <strong>💡 Yorum:</strong> Şirket büyüklüğü değişkeninde de aykırı değerler tespit edilmiştir. 
            Çok büyük şirketler (dev kuruluşlar) aykırı değer olarak belirlenmiş olup, temizleme sonrası 
            daha dengeli bir dağılım elde edilmiştir.
        </div>
        """, unsafe_allow_html=True)
    
    # BECERİ SAYISI AYKIRI DEĞER ANALİZİ
    skills_count_clean = df['skills_count'].dropna()
    outliers_skills, lb_skills, ub_skills, q1_skills, q3_skills, iqr_skills = detect_outliers_iqr(skills_count_clean)
    
    if len(outliers_skills) > 0:
        st.subheader("🛠️ Beceri Sayısı: Aykırı Değer Öncesi vs Sonrası")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # ÖNCE - Aykırı değerler dahil
            fig_skills_before = go.Figure()
            fig_skills_before.add_trace(go.Box(
                y=skills_count_clean,
                name='Beceri Sayısı (Önce)',
                boxpoints='outliers',
                marker_color='#ff6b6b',
                line_color='#ff6b6b'
            ))
            fig_skills_before.update_layout(
                title='<b>🟥 Aykırı Değerler DAHİL</b>',
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                title_font=dict(size=16, color='#ff6b6b'),
                font=dict(color='#e0e0e0'),
                yaxis_title='Beceri Sayısı',
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig_skills_before, use_container_width=True)
            
            st.markdown(f"""
            <div class="insight-box">
                <strong>🟥 Önce:</strong> Toplam {len(skills_count_clean):,} kayıt<br>
                Min: {skills_count_clean.min():.0f} | Max: {skills_count_clean.max():.0f}<br>
                Aykırı Değer: {len(outliers_skills)} adet
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # SONRA - Aykırı değerler hariç
            skills_no_outliers = skills_count_clean[(skills_count_clean >= lb_skills) & (skills_count_clean <= ub_skills)]
            
            fig_skills_after = go.Figure()
            fig_skills_after.add_trace(go.Box(
                y=skills_no_outliers,
                name='Beceri Sayısı (Sonra)',
                boxpoints='outliers',
                marker_color='#00d4ff',
                line_color='#00d4ff'
            ))
            fig_skills_after.update_layout(
                title='<b>🟦 Aykırı Değerler HARİÇ</b>',
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                title_font=dict(size=16, color='#00d4ff'),
                font=dict(color='#e0e0e0'),
                yaxis_title='Beceri Sayısı',
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig_skills_after, use_container_width=True)
            
            st.markdown(f"""
            <div class="insight-box">
                <strong>🟦 Sonra:</strong> Toplam {len(skills_no_outliers):,} kayıt<br>
                Min: {skills_no_outliers.min():.0f} | Max: {skills_no_outliers.max():.0f}<br>
                Silinen: {len(skills_count_clean) - len(skills_no_outliers)} kayıt
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="insight-box">
            <strong>💡 Yorum:</strong> Beceri sayısı değişkeninde bazı ilanlar aşırı fazla beceri gerektirmektedir. 
            Bu ilanlar aykırı değer olarak tespit edilmiştir. Normal ilanlar ortalama 5-10 beceri ararken, 
            bazı ilanlar 20+ beceri talep etmektedir.
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # ==========================================================================
    # 4️⃣ BETİMSEL İSTATİSTİKLER
    # ==========================================================================
    st.header("📈 Betimsel İstatistikler")
    
    # Sayısal değişkenler tablosu
    st.subheader("🔢 Sayısal Değişkenler")
    
    numeric_stats = pd.DataFrame({
        'İstatistik': ['Ortalama', 'Medyan', 'Std Sapma', 'Min', 'Max', 'Geçerli Değer'],
        'Maaş (€)': [
            f"{df['salary_numeric'].mean():,.0f}",
            f"{df['salary_numeric'].median():,.0f}",
            f"{df['salary_numeric'].std():,.0f}",
            f"{df['salary_numeric'].min():,.0f}",
            f"{df['salary_numeric'].max():,.0f}",
            f"{df['salary_numeric'].notna().sum():,}"
        ],
        'Şirket Büyüklüğü': [
            f"{df['company_size_numeric'].mean():,.0f}" if df['company_size_numeric'].notna().any() else "N/A",
            f"{df['company_size_numeric'].median():,.0f}" if df['company_size_numeric'].notna().any() else "N/A",
            f"{df['company_size_numeric'].std():,.0f}" if df['company_size_numeric'].notna().any() else "N/A",
            f"{df['company_size_numeric'].min():,.0f}" if df['company_size_numeric'].notna().any() else "N/A",
            f"{df['company_size_numeric'].max():,.0f}" if df['company_size_numeric'].notna().any() else "N/A",
            f"{df['company_size_numeric'].notna().sum():,}"
        ],
        'Beceri Sayısı': [
            f"{df['skills_count'].mean():.1f}",
            f"{df['skills_count'].median():.0f}",
            f"{df['skills_count'].std():.1f}",
            f"{df['skills_count'].min()}",
            f"{df['skills_count'].max()}",
            f"{len(df):,}"
        ]
    })
    st.markdown(create_dark_table(numeric_stats), unsafe_allow_html=True)
    
    # Kategorik değişken dağılımları - TABLO FORMATINDA
    st.subheader("📝 Kategorik Değişken Dağılımları")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**İş Pozisyonları**")
        job_counts = df['job_title'].value_counts().head(5).reset_index()
        job_counts.columns = ['Pozisyon', 'Sayı']
        st.markdown(create_dark_table(job_counts), unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Kıdem Seviyeleri**")
        seniority_data = df[df['seniority_level'].notna() & (df['seniority_level'] != '')]['seniority_level'].value_counts().reset_index()
        seniority_data.columns = ['Kıdem', 'Sayı']
        st.markdown(create_dark_table(seniority_data), unsafe_allow_html=True)
    
    with col3:
        st.markdown("**Çalışma Modeli**")
        status_data = df[df['status'].notna() & (df['status'] != '')]['status'].value_counts().reset_index()
        status_data.columns = ['Model', 'Sayı']
        st.markdown(create_dark_table(status_data), unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box">
        <strong>💡 Yorum:</strong> Data Scientist pozisyonu en yaygın iş türüdür. Senior seviye 
        pozisyonlar çoğunluğu oluştururken, hybrid ve on-site çalışma modelleri en çok tercih 
        edilen seçeneklerdir.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # ==========================================================================
    # 5️⃣ DAĞILIM GRAFİKLERİ (COUNTPLOTS)
    # ==========================================================================
    st.header("📊 Dağılım Grafikleri")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 1. Seniority Level Distribution - Countplot
        st.subheader("👔 Kıdem Seviyesi Dağılımı")
        seniority_valid = df[df['seniority_level'].notna() & (df['seniority_level'] != '')]
        seniority_counts = seniority_valid['seniority_level'].value_counts().reset_index()
        seniority_counts.columns = ['Kıdem', 'Sayı']
        
        fig_seniority = px.bar(
            seniority_counts,
            x='Kıdem',
            y='Sayı',
            title='<b>Kıdem Seviyesi Dağılımı (Countplot)</b>',
            template='plotly_dark',
            height=400
        )
        fig_seniority.update_traces(marker_color='#00d4ff')
        fig_seniority.update_layout(
            title_font=dict(size=16, color='#00d4ff'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0'),
            showlegend=False
        )
        st.plotly_chart(fig_seniority, use_container_width=True)
        
        st.markdown("""
        <div class="insight-box">
            <strong>💡 Yorum:</strong> Senior pozisyonlar en yüksek talep gören kıdem seviyesidir. 
            Junior pozisyonlar nispeten daha az ilan içermektedir.
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # 2. Work Model Distribution - Countplot
        st.subheader("🏢 Çalışma Modeli Dağılımı")
        status_valid = df[df['status'].notna() & (df['status'] != '')]
        status_counts = status_valid['status'].value_counts().reset_index()
        status_counts.columns = ['Model', 'Sayı']
        
        fig_status = px.bar(
            status_counts,
            x='Model',
            y='Sayı',
            title='<b>Çalışma Modeli Dağılımı (Countplot)</b>',
            template='plotly_dark',
            height=400
        )
        fig_status.update_traces(marker_color='#00d4ff')
        fig_status.update_layout(
            title_font=dict(size=16, color='#00d4ff'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0'),
            showlegend=False
        )
        st.plotly_chart(fig_status, use_container_width=True)
        
        st.markdown("""
        <div class="insight-box">
            <strong>💡 Yorum:</strong> Hybrid ve on-site çalışma modelleri en yaygın tercihlerdir. 
            Remote pozisyonlar da önemli bir pay almaktadır.
        </div>
        """, unsafe_allow_html=True)
    
    # 11. Work Status Distribution - Pie Chart
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🥧 Çalışma Modeli Oranları (Pie Chart)")
        
        fig_pie = px.pie(
            status_counts,
            values='Sayı',
            names='Model',
            title='<b>Remote / Hybrid / On-site Oranları</b>',
            template='plotly_dark',
            color_discrete_sequence=px.colors.qualitative.Set3,
            hole=0.4
        )
        fig_pie.update_layout(
            title_font=dict(size=16, color='#00d4ff'),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0')
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
        
        st.markdown("""
        <div class="insight-box">
            <strong>💡 Yorum:</strong> Pasta grafiği, çalışma modellerinin oransal dağılımını gösterir. 
            Şirketlerin çoğu hibrit veya ofis bazlı çalışmayı tercih etmektedir.
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # 4. Industry Distribution - Countplot (Top 15)
        st.subheader("🏭 Sektör Dağılımı (Top 15)")
        industry_counts = df['industry'].value_counts().head(15).reset_index()
        industry_counts.columns = ['Sektör', 'Sayı']
        
        fig_industry = px.bar(
            industry_counts,
            y='Sektör',
            x='Sayı',
            orientation='h',
            title='<b>İlk 15 Sektörün İlan Sayısı</b>',
            template='plotly_dark',
            height=450
        )
        fig_industry.update_traces(marker_color='#00d4ff')
        fig_industry.update_layout(
            title_font=dict(size=16, color='#00d4ff'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0'),
            yaxis={'categoryorder': 'total ascending'}
        )
        st.plotly_chart(fig_industry, use_container_width=True)
        
        st.markdown("""
        <div class="insight-box">
            <strong>💡 Yorum:</strong> Technology sektörü veri bilimi ilanlarında açık ara lider konumdadır. 
            Finance ve Healthcare sektörleri de önemli istihdam kaynakları arasındadır.
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # ==========================================================================
    # 6️⃣ KORELASYON ANALİZİ
    # ==========================================================================
    st.header("🔗 Korelasyon Analizi")
    
    numeric_for_corr = df[['salary_numeric', 'company_size_numeric', 'skills_count']].dropna()
    
    if len(numeric_for_corr) > 10:
        corr_matrix = numeric_for_corr.corr()
        
        # Küçültülmüş korelasyon grafiği
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            fig_corr, ax = plt.subplots(figsize=(6, 5))  # Küçültülmüş boyut
            fig_corr.patch.set_facecolor('#0e1117')
            ax.set_facecolor('#0e1117')
            
            sns.heatmap(
                corr_matrix,
                annot=True,
                cmap='coolwarm',
                center=0,
                fmt='.2f',
                linewidths=0.5,
                ax=ax,
                annot_kws={'color': 'white', 'fontsize': 11},
                cbar_kws={'shrink': 0.8}
            )
            
            labels = ['Maaş', 'Şirket Büyüklüğü', 'Beceri Sayısı']
            ax.set_xticklabels(labels, color='white', fontsize=10)
            ax.set_yticklabels(labels, color='white', rotation=0, fontsize=10)
            ax.set_title('Korelasyon Isı Haritası', fontsize=14, fontweight='bold', color='#00d4ff', pad=15)
            
            plt.tight_layout()
            st.pyplot(fig_corr)
            plt.close()
    
    st.markdown("""
    <div class="insight-box">
        <strong>💡 Yorum:</strong> Korelasyon analizi, değişkenler arasındaki doğrusal ilişkileri gösterir. 
        +1'e yakın değerler güçlü pozitif, -1'e yakın değerler güçlü negatif ilişkiyi ifade eder.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # ==========================================================================
    # 6️⃣ MAAŞ DAĞILIMI (Histogram + KDE)
    # ==========================================================================
    st.header("📊 Maaş Dağılımı (Histogram + KDE)")
    
    salary_data = df['salary_numeric'].dropna()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Plotly Histogram
        fig_hist = px.histogram(
            x=salary_data,
            nbins=40,
            title='<b>Maaş Dağılımı (Histogram)</b>',
            template='plotly_dark',
            labels={'x': 'Maaş (€)', 'y': 'Frekans'}
        )
        fig_hist.update_layout(
            title_font=dict(size=16, color='#00d4ff'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0'),
            showlegend=False,
            height=400
        )
        fig_hist.update_traces(marker_color='#00d4ff')
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col2:
        # Matplotlib + Seaborn KDE
        fig_kde, ax = plt.subplots(figsize=(10, 5.5))
        fig_kde.patch.set_facecolor('#0e1117')
        ax.set_facecolor('#0e1117')
        
        sns.histplot(salary_data, kde=True, ax=ax, color='#00d4ff', alpha=0.7, edgecolor='#1a1f2e')
        ax.set_title('Maaş Dağılımı (Histogram + KDE)', fontweight='bold', color='#00d4ff', fontsize=14)
        ax.set_xlabel('Maaş (€)', color='white', fontsize=11)
        ax.set_ylabel('Frekans', color='white', fontsize=11)
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('#3d4a5c')
        ax.spines['left'].set_color('#3d4a5c')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(True, alpha=0.2, color='#3d4a5c')
        
        plt.tight_layout()
        st.pyplot(fig_kde)
        plt.close()
    
    # İstatistikler
    skewness = salary_data.skew()
    
    st.markdown(f"""
    <div class="insight-box">
        <strong>💡 Yorum:</strong> Maaş dağılımı analiz edildiğinde; Ortalama: €{salary_data.mean():,.0f}, 
        Medyan: €{salary_data.median():,.0f}, Çarpıklık: {skewness:.2f}. 
        {'Sağa çarpık dağılım yüksek maaşlı pozisyonların azlığını gösterir.' if skewness > 0.5 else 'Dağılım nispeten simetriktir.'}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # ==========================================================================
    # 8️⃣ SEKTÖR VE ŞİRKET ANALİZLERİ
    # ==========================================================================
    st.header("🏢 Sektör ve Şirket Analizleri")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 9. Average Salary by Industry - Bar Plot
        st.subheader("💰 Sektöre Göre Ortalama Maaş")
        
        industry_salary = df.groupby('industry')['salary_numeric'].mean().reset_index()
        industry_salary.columns = ['Sektör', 'Ortalama Maaş']
        industry_salary = industry_salary.dropna().sort_values('Ortalama Maaş', ascending=True).tail(12)
        
        fig_ind_salary = px.bar(
            industry_salary,
            x='Ortalama Maaş',
            y='Sektör',
            orientation='h',
            title='<b>Sektöre Göre Ortalama Maaş</b>',
            template='plotly_dark',
            height=450
        )
        fig_ind_salary.update_traces(marker_color='#00d4ff')
        fig_ind_salary.update_layout(
            title_font=dict(size=16, color='#00d4ff'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0'),
            yaxis={'categoryorder': 'total ascending'}
        )
        st.plotly_chart(fig_ind_salary, use_container_width=True)
        
        st.markdown("""
        <div class="insight-box">
            <strong>💡 Yorum:</strong> Sektörler arasında maaş farklılıkları belirgindir. 
            Teknoloji ve finans sektörleri en yüksek ortalama maaşları sunmaktadır.
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # 7. Salary vs Company Size - Scatter Plot
        st.subheader("📈 Şirket Büyüklüğü vs Maaş")
        
        # Outlier filtreleme
        scatter_df = df[['company_size_numeric', 'salary_numeric', 'industry', 'company', 'status']].dropna()
        # Aşırı değerleri filtrele
        q1_size = scatter_df['company_size_numeric'].quantile(0.05)
        q3_size = scatter_df['company_size_numeric'].quantile(0.95)
        q1_salary = scatter_df['salary_numeric'].quantile(0.05)
        q3_salary = scatter_df['salary_numeric'].quantile(0.95)
        scatter_df = scatter_df[
            (scatter_df['company_size_numeric'] >= q1_size) & 
            (scatter_df['company_size_numeric'] <= q3_size) &
            (scatter_df['salary_numeric'] >= q1_salary) &
            (scatter_df['salary_numeric'] <= q3_salary)
        ]
        
        if len(scatter_df) > 0:
            fig_scatter = px.scatter(
                scatter_df,
                x='company_size_numeric',
                y='salary_numeric',
                color='industry',
                size='salary_numeric',
                hover_data=['company', 'status'],
                title='<b>Şirket Büyüklüğü ve Maaş İlişkisi</b>',
                template='plotly_dark',
                labels={'company_size_numeric': 'Şirket Büyüklüğü', 'salary_numeric': 'Maaş (€)'},
                height=450
            )
            fig_scatter.update_layout(
                title_font=dict(size=16, color='#00d4ff'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e0e0e0'),
                legend=dict(font=dict(size=9))
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        st.markdown("""
        <div class="insight-box">
            <strong>💡 Yorum:</strong> Şirket büyüklüğü ile maaş arasındaki ilişki sektöre göre değişkenlik gösterir. 
            Büyük şirketler genellikle daha yüksek maaş sunma eğilimindedir.
        </div>
        """, unsafe_allow_html=True)
    
    # 10. Daily Job Posting Trend - Line Chart
    st.subheader("📅 Günlük İlan Yayınlama Trendi")
    
    # post_date'i parse et
    def parse_post_date(date_str):
        """post_date'i gün sayısına çevir"""
        if pd.isna(date_str):
            return np.nan
        date_str = str(date_str).lower()
        if 'day' in date_str:
            try:
                return int(date_str.split()[0])
            except:
                return np.nan
        elif 'month' in date_str:
            try:
                return int(date_str.split()[0]) * 30
            except:
                return np.nan
        elif 'year' in date_str:
            try:
                return int(date_str.split()[0]) * 365
            except:
                return np.nan
        return np.nan
    
    df['days_ago'] = df['post_date'].apply(parse_post_date)
    trend_df = df[df['days_ago'].notna()].groupby('days_ago').size().reset_index(name='İlan Sayısı')
    trend_df = trend_df.sort_values('days_ago')
    trend_df['Gün'] = trend_df['days_ago'].astype(int)
    
    if len(trend_df) > 0:
        fig_trend = px.line(
            trend_df,
            x='Gün',
            y='İlan Sayısı',
            title='<b>İlan Yayınlama Trendi (Gün Bazında)</b>',
            template='plotly_dark',
            markers=True,
            height=400
        )
        fig_trend.update_layout(
            title_font=dict(size=16, color='#00d4ff'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0'),
            xaxis_title='Kaç Gün Önce',
            yaxis_title='İlan Sayısı'
        )
        fig_trend.update_traces(line_color='#00d4ff', marker_color='#ff6b6b')
        st.plotly_chart(fig_trend, use_container_width=True)
        
        st.markdown("""
        <div class="insight-box">
            <strong>💡 Yorum:</strong> İlan yayınlama trendi, piyasadaki işe alım aktivitesini gösterir. 
            Son günlerde yoğunlaşan ilanlar, aktif bir işe alım dönemini işaret etmektedir.
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # ==========================================================================
    # 9️⃣ ETKİLEŞİMLİ ANALİZLER
    # ==========================================================================
    st.header("🎨 Etkileşimli Analizler")
    
    tab1, tab2, tab3 = st.tabs(["📦 Kıdem vs Maaş", "🛠️ Beceri Analizi", "🌍 Lokasyon"])
    
    # TAB 1: Kıdem vs Maaş
    with tab1:
        st.subheader("📦 Kıdem Seviyesine Göre Maaş Dağılımı")
        
        valid_seniority = df[df['seniority_level'].notna() & (df['seniority_level'] != '')]
        
        # Yatay boxplot - daha net görünüm
        fig_box = px.box(
            valid_seniority,
            y='seniority_level',
            x='salary_numeric',
            title='<b>Kıdem Seviyesine Göre Maaş Boxplot</b>',
            template='plotly_dark',
            color='seniority_level',
            labels={'seniority_level': 'Kıdem Seviyesi', 'salary_numeric': 'Maaş (€)'},
            orientation='h',
            height=500
        )
        fig_box.update_layout(
            title_font=dict(size=16, color='#00d4ff'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0'),
            showlegend=False,
            yaxis=dict(tickfont=dict(size=12), categoryorder='total ascending'),
            boxgap=0.3,
            boxgroupgap=0.4
        )
        fig_box.update_traces(width=0.6)
        st.plotly_chart(fig_box, use_container_width=True)
        
        # Kıdem istatistikleri tablosu
        st.subheader("📊 Kıdem Bazlı İstatistikler")
        seniority_stats = valid_seniority.groupby('seniority_level')['salary_numeric'].agg(['mean', 'median', 'count']).reset_index()
        seniority_stats.columns = ['Kıdem', 'Ortalama (€)', 'Medyan (€)', 'İlan Sayısı']
        seniority_stats['Ortalama (€)'] = seniority_stats['Ortalama (€)'].apply(lambda x: f"{x:,.0f}")
        seniority_stats['Medyan (€)'] = seniority_stats['Medyan (€)'].apply(lambda x: f"{x:,.0f}")
        st.markdown(create_dark_table(seniority_stats), unsafe_allow_html=True)
        
        st.markdown("""
        <div class="insight-box">
            <strong>💡 Yorum:</strong> Lead pozisyonlar en yüksek maaş aralığına sahipken, 
            junior pozisyonlar giriş seviyesi maaşlarla başlamaktadır. Senior pozisyonlar 
            geniş bir maaş aralığına sahiptir.
        </div>
        """, unsafe_allow_html=True)
    
    # TAB 2: Beceri Analizi
    with tab2:
        st.subheader("🛠️ En Çok Aranan Beceriler")
        
        # Tüm becerileri topla
        all_skills = []
        for skills in df['skills_list']:
            all_skills.extend(skills)
        
        if len(all_skills) > 0:
            skill_counts = pd.Series(all_skills).value_counts().head(20)
            
            # 5. Top 20 Most Requested Skills - Barplot
            fig_skills = px.bar(
                x=skill_counts.values,
                y=skill_counts.index,
                orientation='h',
                title='<b>En Çok Aranan 20 Beceri</b>',
                template='plotly_dark',
                labels={'x': 'İlan Sayısı', 'y': 'Beceri'},
                height=500
            )
            fig_skills.update_traces(marker_color='#00d4ff')
            fig_skills.update_layout(
                title_font=dict(size=16, color='#00d4ff'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e0e0e0'),
                showlegend=False,
                yaxis={'categoryorder': 'total ascending'}
            )
            st.plotly_chart(fig_skills, use_container_width=True)
            
            # 8. Top 30 Most Requested Skills - Horizontal Bar Chart
            st.subheader("📊 En Çok Aranan 30 Beceri")
            skill_counts_30 = pd.Series(all_skills).value_counts().head(30)
            
            fig_skills_30 = px.bar(
                x=skill_counts_30.values,
                y=skill_counts_30.index,
                orientation='h',
                title='<b>En Çok Aranan 30 Beceri (Detaylı)</b>',
                template='plotly_dark',
                labels={'x': 'İlan Sayısı', 'y': 'Beceri'},
                height=700
            )
            fig_skills_30.update_traces(marker_color='#00d4ff')
            fig_skills_30.update_layout(
                title_font=dict(size=16, color='#00d4ff'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e0e0e0'),
                showlegend=False,
                yaxis={'categoryorder': 'total ascending'}
            )
            st.plotly_chart(fig_skills_30, use_container_width=True)
            
            st.markdown("""
            <div class="insight-box">
                <strong>💡 Yorum:</strong> Python, SQL ve Machine Learning en kritik becerilerdir. 
                Cloud ve DevOps becerileri de giderek önem kazanmaktadır.
            </div>
            """, unsafe_allow_html=True)
            
            # Beceri grupları tabloları
            st.subheader("📋 Beceri Grupları")
            
            col1, col2, col3 = st.columns(3)
            
            programming = ['python', 'r', 'sql', 'java', 'scala']
            ml_tools = ['machine learning', 'deep learning', 'tensorflow', 'pytorch', 'keras', 'scikit-learn']
            cloud_tools = ['aws', 'gcp', 'azure', 'docker', 'kubernetes']
            
            with col1:
                st.markdown("**💻 Programlama**")
                prog_data = []
                for skill in programming:
                    count = all_skills.count(skill)
                    if count > 0:
                        prog_data.append({'Beceri': skill, 'Sayı': count})
                if prog_data:
                    st.markdown(create_dark_table(pd.DataFrame(prog_data)), unsafe_allow_html=True)
            
            with col2:
                st.markdown("**🤖 ML/DL**")
                ml_data = []
                for skill in ml_tools:
                    count = all_skills.count(skill)
                    if count > 0:
                        ml_data.append({'Beceri': skill, 'Sayı': count})
                if ml_data:
                    st.markdown(create_dark_table(pd.DataFrame(ml_data)), unsafe_allow_html=True)
            
            with col3:
                st.markdown("**☁️ Cloud/DevOps**")
                cloud_data = []
                for skill in cloud_tools:
                    count = all_skills.count(skill)
                    if count > 0:
                        cloud_data.append({'Beceri': skill, 'Sayı': count})
                if cloud_data:
                    st.markdown(create_dark_table(pd.DataFrame(cloud_data)), unsafe_allow_html=True)
            
            st.markdown("""
            <div class="insight-box">
                <strong>💡 Yorum:</strong> Python ve SQL en çok aranan becerilerdir. Machine Learning 
                bilgisi neredeyse tüm pozisyonlarda beklenmektedir. Cloud platformları da giderek 
                daha önemli hale gelmektedir.
            </div>
            """, unsafe_allow_html=True)
            
            # ==================================================================
            # 🔗 BECERİ BİRLİKTELİK ANALİZİ (YENİ BÖLÜM)
            # ==================================================================
            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
            st.subheader("🔗 Beceri Birliktelik Analizi")
            
            st.markdown("""
            <div class="insight-box">
                <strong>📌 Beceri Birlikteliği Nedir?</strong> Hangi becerilerin birlikte arandığını 
                gösterir. Örneğin, Python arayan ilanların kaçında aynı zamanda Machine Learning de aranıyor?
            </div>
            """, unsafe_allow_html=True)
            
            # İkili beceri kombinasyonları hesaplama
            from itertools import combinations
            
            skill_pairs = []
            for skills in df['skills_list']:
                if len(skills) >= 2:
                    for pair in combinations(sorted(set(skills)), 2):
                        skill_pairs.append(pair)
            
            pair_counts = pd.Series(skill_pairs).value_counts().head(15)
            
            # İkili kombinasyon grafiği
            st.markdown("**👫 En Sık Birlikte Aranan İkili Beceriler (Top 15)**")
            
            pair_df = pd.DataFrame({
                'Beceri Çifti': [f"{p[0]} + {p[1]}" for p in pair_counts.index],
                'İlan Sayısı': pair_counts.values
            })
            
            fig_pairs = px.bar(
                pair_df,
                x='İlan Sayısı',
                y='Beceri Çifti',
                orientation='h',
                title='<b>En Sık Birlikte Aranan Beceri Çiftleri</b>',
                template='plotly_dark',
                height=500
            )
            fig_pairs.update_traces(marker_color='#00d4ff')
            fig_pairs.update_layout(
                title_font=dict(size=16, color='#00d4ff'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e0e0e0'),
                yaxis={'categoryorder': 'total ascending'}
            )
            st.plotly_chart(fig_pairs, use_container_width=True)
            
            # Üçlü beceri kombinasyonları
            st.markdown("**👨‍👩‍👧 En Sık Birlikte Aranan Üçlü Beceriler (Top 10)**")
            
            skill_triplets = []
            for skills in df['skills_list']:
                if len(skills) >= 3:
                    for triplet in combinations(sorted(set(skills)), 3):
                        skill_triplets.append(triplet)
            
            triplet_counts = pd.Series(skill_triplets).value_counts().head(10)
            
            triplet_df = pd.DataFrame({
                'Beceri Üçlüsü': [f"{t[0]} + {t[1]} + {t[2]}" for t in triplet_counts.index],
                'İlan Sayısı': triplet_counts.values
            })
            
            fig_triplets = px.bar(
                triplet_df,
                x='İlan Sayısı',
                y='Beceri Üçlüsü',
                orientation='h',
                title='<b>En Sık Birlikte Aranan Beceri Üçlüleri</b>',
                template='plotly_dark',
                height=450
            )
            fig_triplets.update_traces(marker_color='#48bb78')
            fig_triplets.update_layout(
                title_font=dict(size=16, color='#48bb78'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e0e0e0'),
                yaxis={'categoryorder': 'total ascending'}
            )
            st.plotly_chart(fig_triplets, use_container_width=True)
            
            # Özel kombinasyon analizi
            st.markdown("**🎯 Popüler Beceri Kombinasyonları Detayı**")
            
            # Belirli kombinasyonları say
            def count_combination(skills_list, combo):
                count = 0
                for skills in skills_list:
                    skills_lower = [s.lower() for s in skills]
                    if all(c.lower() in skills_lower for c in combo):
                        count += 1
                return count
            
            popular_combos = [
                ('Python', 'Machine Learning'),
                ('Python', 'SQL'),
                ('Python', 'Machine Learning', 'Deep Learning'),
                ('Python', 'SQL', 'Machine Learning'),
                ('Python', 'TensorFlow', 'PyTorch'),
                ('AWS', 'Python', 'Machine Learning'),
                ('Python', 'Spark', 'SQL'),
                ('R', 'Python', 'SQL'),
            ]
            
            combo_results = []
            total_jobs = len(df)
            
            for combo in popular_combos:
                count = count_combination(df['skills_list'], combo)
                combo_name = ' + '.join(combo)
                percentage = (count / total_jobs) * 100
                combo_results.append({
                    'Kombinasyon': combo_name,
                    'İlan Sayısı': count,
                    'Oran (%)': f"{percentage:.1f}%"
                })
            
            combo_df = pd.DataFrame(combo_results).sort_values('İlan Sayısı', ascending=False)
            st.markdown(create_dark_table(combo_df), unsafe_allow_html=True)
            
            # Python merkezli analiz
            st.markdown("**🐍 Python ile Birlikte En Çok Aranan Beceriler**")
            
            python_cooccurrence = {}
            for skills in df['skills_list']:
                if 'python' in [s.lower() for s in skills]:
                    for skill in skills:
                        if skill.lower() != 'python':
                            python_cooccurrence[skill] = python_cooccurrence.get(skill, 0) + 1
            
            python_co_df = pd.DataFrame({
                'Beceri': list(python_cooccurrence.keys()),
                'Python ile Birlikte': list(python_cooccurrence.values())
            }).sort_values('Python ile Birlikte', ascending=False).head(10)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                fig_python_co = px.bar(
                    python_co_df,
                    x='Python ile Birlikte',
                    y='Beceri',
                    orientation='h',
                    title='<b>Python ile Birlikte En Çok Aranan 10 Beceri</b>',
                    template='plotly_dark',
                    height=400
                )
                fig_python_co.update_traces(marker_color='#ed8936')
                fig_python_co.update_layout(
                    title_font=dict(size=16, color='#ed8936'),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#e0e0e0'),
                    yaxis={'categoryorder': 'total ascending'}
                )
                st.plotly_chart(fig_python_co, use_container_width=True)
            
            with col2:
                st.markdown(create_dark_table(python_co_df), unsafe_allow_html=True)
            
            st.markdown("""
            <div class="insight-box">
                <strong>💡 Yorum:</strong> Python + Machine Learning en popüler ikili kombinasyondur. 
                Üçlü kombinasyonlarda Python + SQL + Machine Learning öne çıkmaktadır. 
                Bu, veri bilimi pozisyonlarının temel beklentilerini net şekilde ortaya koymaktadır. 
                Deep Learning ve TensorFlow/PyTorch gibi ileri düzey beceriler de sıkça birlikte aranmaktadır.
            </div>
            """, unsafe_allow_html=True)
    
    # TAB 3: Lokasyon
    with tab3:
        st.subheader("🌍 Lokasyon Bazlı Analiz")
        
        # Headquarter bazlı analiz - BARPLOT
        hq_data = df.groupby('headquarter').agg({
            'salary_numeric': 'mean',
            'job_title': 'count'
        }).reset_index()
        hq_data.columns = ['Merkez', 'Ortalama Maaş', 'İlan Sayısı']
        hq_data = hq_data.dropna().sort_values('İlan Sayısı', ascending=False).head(12)
        
        fig_location = px.bar(
            hq_data,
            x='Merkez',
            y='İlan Sayısı',
            title='<b>Şirket Merkezine Göre İlan Sayısı</b>',
            template='plotly_dark',
            height=500
        )
        fig_location.update_traces(marker_color='#00d4ff')
        fig_location.update_layout(
            title_font=dict(size=16, color='#00d4ff'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0'),
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_location, use_container_width=True)
        
        # Lokasyon tablosu
        st.subheader("📊 Lokasyon Detayları")
        location_table = hq_data.copy()
        location_table['Ortalama Maaş'] = location_table['Ortalama Maaş'].apply(lambda x: f"€{x:,.0f}")
        st.markdown(create_dark_table(location_table.head(10)), unsafe_allow_html=True)
        
        st.markdown("""
        <div class="insight-box">
            <strong>💡 Yorum:</strong> San Francisco, New York ve Seattle gibi teknoloji merkezleri 
            hem en fazla iş ilanına hem de en yüksek maaşlara sahiptir. Coğrafi konum, maaş 
            beklentilerini önemli ölçüde etkilemektedir.
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # ==========================================================================
    # 🎯 İLERİ DÜZEY GRAFİKLER
    # ==========================================================================
    st.header("🎯 İleri Düzey Görselleştirmeler")
    
    # --------------------------------------------------------------------------
    # 1️⃣ DUMBBELL CHART - Kıdem Seviyelerine Göre Min-Max Maaş Karşılaştırması
    # --------------------------------------------------------------------------
    st.subheader("🏋️ Dumbbell Chart: Kıdem Seviyelerine Göre Maaş Aralığı")
    
    st.markdown("""
    <div class="insight-box">
        <strong>📌 Dumbbell Chart Nedir?</strong> Her kıdem seviyesi için minimum ve maksimum maaş 
        değerlerini gösterir. İki nokta arasındaki çizgi, maaş aralığının genişliğini temsil eder.
    </div>
    """, unsafe_allow_html=True)
    
    # Kıdem seviyesine göre min-max maaş hesaplama
    seniority_salary = df[df['seniority_level'].notna() & (df['seniority_level'] != '')].groupby('seniority_level').agg({
        'salary_numeric': ['min', 'max', 'mean', 'count']
    }).reset_index()
    seniority_salary.columns = ['Kıdem', 'Min Maaş', 'Max Maaş', 'Ort Maaş', 'İlan Sayısı']
    seniority_salary = seniority_salary.dropna()
    seniority_salary = seniority_salary.sort_values('Ort Maaş', ascending=True)
    
    fig_dumbbell = go.Figure()
    
    # Çizgiler (min-max arası)
    for i, row in seniority_salary.iterrows():
        fig_dumbbell.add_trace(go.Scatter(
            x=[row['Min Maaş'], row['Max Maaş']],
            y=[row['Kıdem'], row['Kıdem']],
            mode='lines',
            line=dict(color='#4a5568', width=3),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Min noktaları (kırmızı)
    fig_dumbbell.add_trace(go.Scatter(
        x=seniority_salary['Min Maaş'],
        y=seniority_salary['Kıdem'],
        mode='markers',
        marker=dict(color='#ff6b6b', size=14, symbol='circle'),
        name='Min Maaş',
        hovertemplate='<b>%{y}</b><br>Min Maaş: €%{x:,.0f}<extra></extra>'
    ))
    
    # Max noktaları (mavi)
    fig_dumbbell.add_trace(go.Scatter(
        x=seniority_salary['Max Maaş'],
        y=seniority_salary['Kıdem'],
        mode='markers',
        marker=dict(color='#00d4ff', size=14, symbol='circle'),
        name='Max Maaş',
        hovertemplate='<b>%{y}</b><br>Max Maaş: €%{x:,.0f}<extra></extra>'
    ))
    
    # Ortalama noktaları (yeşil)
    fig_dumbbell.add_trace(go.Scatter(
        x=seniority_salary['Ort Maaş'],
        y=seniority_salary['Kıdem'],
        mode='markers',
        marker=dict(color='#48bb78', size=10, symbol='diamond'),
        name='Ortalama Maaş',
        hovertemplate='<b>%{y}</b><br>Ort Maaş: €%{x:,.0f}<extra></extra>'
    ))
    
    fig_dumbbell.update_layout(
        title='<b>Kıdem Seviyesine Göre Maaş Aralığı (Min - Ort - Max)</b>',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_font=dict(size=18, color='#00d4ff'),
        font=dict(color='#e0e0e0'),
        xaxis_title='Maaş (€)',
        yaxis_title='',
        height=450,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5)
    )
    st.plotly_chart(fig_dumbbell, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box">
        <strong>💡 Yorum:</strong> Lead pozisyonlar en geniş maaş aralığına sahipken, Junior pozisyonlar 
        daha dar bir aralıkta kalmaktadır. Kırmızı noktalar minimum, mavi noktalar maksimum, yeşil 
        elmaslar ise ortalama maaşı göstermektedir.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # --------------------------------------------------------------------------
    # 2️⃣ RIDGELINE PLOT - Lokasyona Göre Maaş Dağılımı
    # --------------------------------------------------------------------------
    st.subheader("🌊 Ridgeline Plot: Lokasyona Göre Maaş Dağılımı")
    
    st.markdown("""
    <div class="insight-box">
        <strong>📌 Ridgeline Plot Nedir?</strong> Farklı kategorilerin dağılımlarını üst üste 
        yerleştirerek karşılaştırmayı kolaylaştırır. Her lokasyonun maaş dağılımını görmek için idealdir.
    </div>
    """, unsafe_allow_html=True)
    
    # En çok ilan veren lokasyonları seç (headquarter kullanarak)
    top_locations = df['headquarter'].value_counts().head(8).index.tolist()
    ridgeline_data = df[df['headquarter'].isin(top_locations) & df['salary_numeric'].notna()]
    
    # Ridgeline için violin plot kullanma (Plotly'de ridge yerine)
    fig_ridge = go.Figure()
    
    colors = ['#00d4ff', '#ff6b6b', '#48bb78', '#ed8936', '#9f7aea', '#f687b3', '#68d391', '#fc8181']
    
    for i, location in enumerate(top_locations):
        location_data = ridgeline_data[ridgeline_data['headquarter'] == location]['salary_numeric']
        
        fig_ridge.add_trace(go.Violin(
            x=location_data,
            y=[location] * len(location_data),
            name=location,
            orientation='h',
            side='positive',
            width=1.5,
            line_color=colors[i % len(colors)],
            fillcolor=colors[i % len(colors)],
            opacity=0.7,
            meanline_visible=True,
            box_visible=False,
            points=False,
            showlegend=False
        ))
    
    fig_ridge.update_layout(
        title='<b>Lokasyona Göre Maaş Dağılımı (Ridgeline Tarzı)</b>',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_font=dict(size=18, color='#00d4ff'),
        font=dict(color='#e0e0e0'),
        xaxis_title='Maaş (€)',
        yaxis_title='',
        height=550,
        violingap=0,
        violinmode='overlay'
    )
    st.plotly_chart(fig_ridge, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box">
        <strong>💡 Yorum:</strong> San Francisco ve New York gibi teknoloji merkezleri en geniş ve yüksek 
        maaş dağılımına sahiptir. Farklı lokasyonlar arasındaki maaş farkları açıkça görülmektedir. 
        Silikon Vadisi lokasyonları diğer bölgelere göre belirgin şekilde yüksek maaş sunmaktadır.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # --------------------------------------------------------------------------
    # 3️⃣ ERROR BAR CHART - Çalışma Modeline Göre Maaş (Ortalama ± Std)
    # --------------------------------------------------------------------------
    st.subheader("📊 Error Bar Chart: Çalışma Modeline Göre Maaş Dağılımı")
    
    st.markdown("""
    <div class="insight-box">
        <strong>📌 Error Bar Chart Nedir?</strong> Ortalama değerleri ve belirsizlik/varyans 
        aralığını gösterir. Hata çubukları, standart sapma veya güven aralığını temsil eder.
    </div>
    """, unsafe_allow_html=True)
    
    # Çalışma modeline göre maaş istatistikleri
    status_stats = df[df['status'].notna() & (df['status'] != '')].groupby('status').agg({
        'salary_numeric': ['mean', 'std', 'count']
    }).reset_index()
    status_stats.columns = ['Çalışma Modeli', 'Ortalama', 'Std Sapma', 'Sayı']
    status_stats = status_stats.dropna()
    status_stats['Std Sapma'] = status_stats['Std Sapma'].fillna(0)
    
    fig_error = go.Figure()
    
    fig_error.add_trace(go.Bar(
        x=status_stats['Çalışma Modeli'],
        y=status_stats['Ortalama'],
        error_y=dict(
            type='data',
            array=status_stats['Std Sapma'],
            visible=True,
            color='#ff6b6b',
            thickness=2,
            width=8
        ),
        marker_color='#00d4ff',
        name='Ortalama Maaş',
        text=[f"€{x:,.0f}" for x in status_stats['Ortalama']],
        textposition='outside',
        textfont=dict(color='#e0e0e0')
    ))
    
    fig_error.update_layout(
        title='<b>Çalışma Modeline Göre Ortalama Maaş (± Standart Sapma)</b>',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_font=dict(size=18, color='#00d4ff'),
        font=dict(color='#e0e0e0'),
        xaxis_title='Çalışma Modeli',
        yaxis_title='Maaş (€)',
        height=450,
        showlegend=False
    )
    st.plotly_chart(fig_error, use_container_width=True)
    
    # İstatistik tablosu
    error_table = status_stats.copy()
    error_table['Ortalama'] = error_table['Ortalama'].apply(lambda x: f"€{x:,.0f}")
    error_table['Std Sapma'] = error_table['Std Sapma'].apply(lambda x: f"€{x:,.0f}")
    st.markdown(create_dark_table(error_table), unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box">
        <strong>💡 Yorum:</strong> Remote pozisyonlar en yüksek ortalama maaşa sahipken, aynı zamanda 
        en yüksek standart sapmaya da sahiptir. Bu, remote pozisyonlarda maaş çeşitliliğinin 
        daha fazla olduğunu göstermektedir.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # --------------------------------------------------------------------------
    # 4️⃣ VIOLIN PLOT - Sektör ve Kıdem Seviyesine Göre Maaş
    # --------------------------------------------------------------------------
    st.subheader("🎻 Violin Plot: Sektör ve Kıdem Seviyesine Göre Maaş Dağılımı")
    
    st.markdown("""
    <div class="insight-box">
        <strong>📌 Violin Plot Nedir?</strong> Box plot ve KDE (yoğunluk grafiği) birleşimidir. 
        Dağılımın şeklini, medyanı ve çeyreklikleri aynı anda gösterir.
    </div>
    """, unsafe_allow_html=True)
    
    # İlk olarak sektöre göre violin plot
    top_5_industries = df['industry'].value_counts().head(5).index.tolist()
    violin_data = df[df['industry'].isin(top_5_industries) & df['salary_numeric'].notna()]
    
    fig_violin1 = px.violin(
        violin_data,
        x='industry',
        y='salary_numeric',
        color='industry',
        box=True,
        points='outliers',
        title='<b>Sektöre Göre Maaş Dağılımı (Violin Plot)</b>',
        template='plotly_dark',
        labels={'industry': 'Sektör', 'salary_numeric': 'Maaş (€)'},
        color_discrete_sequence=['#00d4ff', '#ff6b6b', '#48bb78', '#ed8936', '#9f7aea']
    )
    fig_violin1.update_layout(
        title_font=dict(size=18, color='#00d4ff'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e0e0e0'),
        height=500,
        showlegend=False,
        xaxis_tickangle=-30
    )
    st.plotly_chart(fig_violin1, use_container_width=True)
    
    # Kıdem seviyesine göre violin plot
    seniority_violin = df[df['seniority_level'].notna() & (df['seniority_level'] != '') & df['salary_numeric'].notna()]
    
    fig_violin2 = px.violin(
        seniority_violin,
        x='seniority_level',
        y='salary_numeric',
        color='seniority_level',
        box=True,
        points='outliers',
        title='<b>Kıdem Seviyesine Göre Maaş Dağılımı (Violin Plot)</b>',
        template='plotly_dark',
        labels={'seniority_level': 'Kıdem Seviyesi', 'salary_numeric': 'Maaş (€)'},
        color_discrete_sequence=['#00d4ff', '#ff6b6b', '#48bb78', '#ed8936']
    )
    fig_violin2.update_layout(
        title_font=dict(size=18, color='#00d4ff'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e0e0e0'),
        height=500,
        showlegend=False
    )
    st.plotly_chart(fig_violin2, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box">
        <strong>💡 Yorum:</strong> Violin plotlar, maaş dağılımının şeklini net bir şekilde ortaya koyar. 
        Technology sektöründe çift tepeli (bimodal) bir dağılım görülürken, Lead pozisyonlarda 
        maaşlar geniş bir aralığa yayılmaktadır. Junior pozisyonlar ise dar ve düşük bir aralıkta 
        yoğunlaşmıştır.
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# FOOTER
# =============================================================================
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p style="color: #a0a0a0;">📊 Data Science Job Posts 2025 Dashboard</p>
    <p style="color: #666; font-size: 0.9rem;">Streamlit | Plotly | Seaborn | Matplotlib</p>
</div>
""", unsafe_allow_html=True)
