import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# CONFIGURACIÓN DE LA APP
# ==========================================
st.set_page_config(
    page_title="Visualización de Datos - Tech Employment Trends",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Transformación del empleo tech en la era de la IA")
st.markdown("""
Exploración inicial del dataset para identificar narrativas visuales relevantes
para la actividad de ingeniería de la atención y detección de anomalías.
""")

# ==========================================
# CARGA DE DATOS
# ==========================================
@st.cache_data
def load_data():
    df = pd.read_csv("tech_layoffs_hiring_trends_elite_v2.csv")
    return df

df = load_data()

# ==========================================
# INSPECCIÓN INICIAL
# ==========================================
st.header("1. Vista general del dataset")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Filas", df.shape[0])

with col2:
    st.metric("Columnas", df.shape[1])

with col3:
    st.metric("Empresas únicas", df["company_name"].nunique())

with st.expander("Ver muestra del dataset"):
    st.dataframe(df.head())

with st.expander("Columnas disponibles"):
    st.write(df.columns.tolist())

# ==========================================
# MINI ANÁLISIS EXPLORATORIO
# ==========================================
st.header("2. Mini análisis exploratorio")

# ------------------------------
# Layoffs por industria
# ------------------------------
st.subheader("Promedio de despidos por industria")

industry_layoffs = (
    df.groupby("industry")["layoff_percentage"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

fig1 = px.bar(
    industry_layoffs,
    x="layoffs_count",
    y="industry",
    orientation="h",
    title="Promedio de layoffs por industria",
    text_auto=".1f"
)

fig1.update_layout(yaxis=dict(categoryorder="total ascending"))

st.plotly_chart(fig1, use_container_width=True)

# ------------------------------
# Open roles por industria
# ------------------------------
st.subheader("Promedio de vacantes abiertas por industria")

industry_roles = (
    df.groupby("industry")["open_roles"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

fig2 = px.bar(
    industry_roles,
    x="open_roles",
    y="industry",
    orientation="h",
    title="Vacantes abiertas por industria",
    text_auto=".1f"
)

fig2.update_layout(yaxis=dict(categoryorder="total ascending"))

st.plotly_chart(fig2, use_container_width=True)

# ------------------------------
# Correlaciones
# ------------------------------
st.subheader("Correlaciones clave")

corr_cols = [
    "ai_adoption_level",
    "layoffs_count",
    "open_roles",
    "job_security_score",
    "employee_sentiment",
    "revenue_growth_percent",
    "stock_growth_percent"
]

corr = df[corr_cols].corr()

fig3 = px.imshow(
    corr,
    text_auto=True,
    aspect="auto",
    title="Mapa de correlación"
)

st.plotly_chart(fig3, use_container_width=True)

# ------------------------------
# Empresas con más despidos
# ------------------------------
st.subheader("Top 15 empresas con más despidos")

top_layoffs = df.sort_values(
    "layoffs_count",
    ascending=False
).head(15)

fig4 = px.bar(
    top_layoffs,
    x="company_name",
    y="layoffs_count",
    color="industry",
    title="Empresas con mayor volumen de despidos"
)

fig4.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig4, use_container_width=True)

# ==========================================
# INSIGHTS AUTOMÁTICOS
# ==========================================
st.header("3. Primeros hallazgos")

top_industry = industry_layoffs.iloc[0]["industry"]
top_layoff_value = industry_layoffs.iloc[0]["layoffs_count"]

st.info(
    f"""
    **Industria con mayor promedio de despidos:** {top_industry}
    
    Promedio: {top_layoff_value:.2f}
    
    Esta podría ser una candidata fuerte para la visualización de
    *Ingeniería de la Atención*.
    """
)

# ==========================================
# SIGUIENTE PASO
# ==========================================
st.success("""
Con este análisis podemos decidir:

1. Qué industria destacar
2. Qué anomalías resaltar
3. Qué narrativa visual construir
""")