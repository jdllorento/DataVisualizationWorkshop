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
    df.groupby("industry")["layoffs_count"]
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


st.subheader("Métricas alternativas")

# Pressure Index
df["pressure_index"] = df["layoffs_count"] / (df["open_roles"] + 1)

pressure = (
    df.groupby("industry")["pressure_index"]
    .mean()
    .sort_values(ascending=False)
)

st.write("Pressure Index")
st.dataframe(pressure)

# Net Shift
df["net_shift"] = df["open_roles"] - df["layoffs_count"]

net_shift = (
    df.groupby("industry")["net_shift"]
    .mean()
    .sort_values()
)

st.write("Net Employment Shift")
st.dataframe(net_shift)

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


st.header("4. Visualización 1 — Ingeniería de la Atención")

st.markdown("""
### AI: la excepción en un mercado tech en contracción

Cambio neto de empleo por industria  
(vacantes abiertas - despidos)
""")

industry_net = (
    df.groupby("industry")["net_shift"]
    .mean()
    .sort_values()
    .reset_index()
)

colors = [
    "#d3d3d3" if industry != "AI" else "#0066ff"
    for industry in industry_net["industry"]
]

fig_attention = go.Figure()

fig_attention.add_trace(
    go.Bar(
        x=industry_net["net_shift"],
        y=industry_net["industry"],
        orientation="h",
        marker_color=colors,
        text=industry_net["net_shift"].round(0),
        textposition="outside"
    )
)

fig_attention.update_layout(
    title="Cambio neto de empleo por industria",
    xaxis_title="Open Roles - Layoffs",
    yaxis_title="",
    showlegend=False,
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(size=14),
    margin=dict(l=20, r=20, t=60, b=20)
)

fig_attention.add_vline(
    x=0,
    line_width=2,
    line_dash="dash",
    line_color="gray"
)

fig_attention.add_annotation(
    x=industry_net[industry_net["industry"] == "AI"]["net_shift"].values[0],
    y="AI",
    text="Única industria\ncon crecimiento neto",
    showarrow=True,
    arrowhead=2,
    ax=80,
    ay=-40
)

st.plotly_chart(fig_attention, use_container_width=True)

st.info("""
**Insight:** Mientras la mayoría de industrias tecnológicas presentan contracción neta,
AI aparece como la única categoría con expansión laboral sostenida.
""")


st.header("5. Visualización 2 — Detección de Anomalías")

st.markdown("""
### Crecimiento financiero con despidos masivos

Detección de empresas que contradicen la intuición:
crecen financieramente mientras reducen plantilla.
""")

# ==========================================
# UMBRALES DE ANOMALÍA
# ==========================================
revenue_threshold = df["revenue_growth_percent"].quantile(0.85)
layoffs_threshold = df["layoffs_count"].quantile(0.85)

df["is_anomaly"] = (
    (df["revenue_growth_percent"] > revenue_threshold) &
    (df["layoffs_count"] > layoffs_threshold)
)

normal_df = df[~df["is_anomaly"]]
anomaly_df = df[df["is_anomaly"]]

# ==========================================
# GRÁFICA
# ==========================================
fig_anomaly = go.Figure()

# Contexto neutro
fig_anomaly.add_trace(
    go.Scatter(
        x=normal_df["revenue_growth_percent"],
        y=normal_df["layoffs_count"],
        mode="markers",
        marker=dict(
            color="lightgray",
            size=8,
            opacity=0.45
        ),
        name="Contexto"
    )
)

# Anomalías destacadas
fig_anomaly.add_trace(
    go.Scatter(
        x=anomaly_df["revenue_growth_percent"],
        y=anomaly_df["layoffs_count"],
        mode="markers+text",
        text=anomaly_df["company_name"],
        textposition="top center",
        marker=dict(
            color="#ff2d55",
            size=14,
            line=dict(color="white", width=2)
        ),
        name="Anomalías"
    )
)

# Líneas de referencia
fig_anomaly.add_vline(
    x=revenue_threshold,
    line_dash="dash",
    line_color="gray"
)

fig_anomaly.add_hline(
    y=layoffs_threshold,
    line_dash="dash",
    line_color="gray"
)

# Anotación principal
if not anomaly_df.empty:
    first = anomaly_df.iloc[0]

    fig_anomaly.add_annotation(
        x=first["revenue_growth_percent"],
        y=first["layoffs_count"],
        text="Crecimiento alto + despidos masivos",
        showarrow=True,
        arrowhead=2,
        ax=80,
        ay=-50
    )

fig_anomaly.update_layout(
    title="Anomalías corporativas en el mercado tech",
    xaxis_title="Revenue Growth (%)",
    yaxis_title="Layoffs Count",
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(size=14)
)

st.plotly_chart(fig_anomaly, use_container_width=True)

st.warning(f"""
Se detectaron **{len(anomaly_df)} anomalías**:
empresas con crecimiento financiero elevado y despidos simultáneamente altos.
""")