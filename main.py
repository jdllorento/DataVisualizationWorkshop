import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ==========================================
# CONFIGURACIÓN DE LA APP
# ==========================================
st.set_page_config(
    page_title="Visualización de Datos - Tech Employment Trends",
    layout="wide"
)

st.title("📊 Transformación del empleo tech en la era de la IA")

# ==========================================
# CARGA DE DATOS
# ==========================================
@st.cache_data
def load_data():
    df = pd.read_csv("tech_layoffs_hiring_trends_elite_v2.csv")
    return df

df = load_data()

# Pressure Index
df["pressure_index"] = df["layoffs_count"] / (df["open_roles"] + 1)

pressure = (
    df.groupby("industry")["pressure_index"]
    .mean()
    .sort_values(ascending=False)
)


# Net Shift
df["net_shift"] = df["open_roles"] - df["layoffs_count"]

net_shift = (
    df.groupby("industry")["net_shift"]
    .mean()
    .sort_values()
)


st.header("Visualización 1")

st.markdown("""
Balance de contratación vs despidos por industria
            
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
    plot_bgcolor="black",
    paper_bgcolor="black",
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


# ==========================================
# VISUALIZACIÓN 2 — DETECCIÓN DE ANOMALÍAS
# ==========================================
st.header("Visualización 2")

st.markdown("""
Puntaje de riesgo de reemplazo por IA vs puntaje de seguridad laboral
""")

# ==========================================
# AGREGACIÓN POR INDUSTRIA
# ==========================================
industry_risk = (
    df.groupby("industry")
    .agg({
        "ai_replacement_risk": "mean",
        "job_security_score": "mean"
    })
    .reset_index()
)

# ==========================================
# SCORE DE CRITICIDAD
# ==========================================
industry_risk["criticality"] = (
    industry_risk["ai_replacement_risk"]
    - industry_risk["job_security_score"]
)

highlight = industry_risk.loc[
    industry_risk["criticality"].idxmax(),
    "industry"
]

# ==========================================
# COLORES
# ==========================================
colors = [
    "#ff2d55" if industry == highlight else "#d3d3d3"
    for industry in industry_risk["industry"]
]

# ==========================================
# GRÁFICA
# ==========================================
fig_anomaly = go.Figure()

fig_anomaly.add_trace(
    go.Scatter(
        x=industry_risk["ai_replacement_risk"],
        y=industry_risk["job_security_score"],
        mode="markers+text",
        text=industry_risk["industry"],
        textposition="top center",
        marker=dict(
            size=28,
            color=colors,
            line=dict(color="white", width=2)
        ),
        showlegend=False
    )
)

# Línea de referencia inversa
coef = np.polyfit(
    industry_risk["ai_replacement_risk"],
    industry_risk["job_security_score"],
    1
)

trend = np.poly1d(coef)

x_sorted = np.sort(industry_risk["ai_replacement_risk"])

fig_anomaly.add_trace(
    go.Scatter(
        x=x_sorted,
        y=trend(x_sorted),
        mode="lines",
        line=dict(
            dash="dash",
            color="gray",
            width=2
        ),
        name="Tendencia"
    )
)

# ==========================================
# ANOTACIÓN
# ==========================================
selected = industry_risk[
    industry_risk["industry"] == highlight
].iloc[0]

fig_anomaly.add_annotation(
    x=selected["ai_replacement_risk"],
    y=selected["job_security_score"],
    text=f"{highlight}: máxima vulnerabilidad",
    showarrow=True,
    arrowhead=2,
    ax=100,
    ay=-60,
    bgcolor="black"
)

# ==========================================
# ESTILO
# ==========================================
fig_anomaly.update_layout(
    title="Riesgo de reemplazo vs seguridad laboral",
    xaxis_title="AI Replacement Risk",
    yaxis_title="Job Security Score",
    plot_bgcolor="black",
    paper_bgcolor="black",
    font=dict(size=14),
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(fig_anomaly, use_container_width=True)




# ==========================================
# VISUALIZACIÓN 3 — COLAPSO DE CONFIANZA
# ==========================================
st.header("Visualización 3")

st.markdown("""
La seguridad laboral comparada con la estrategia de contratación de la empresa
""")

trend_order = [
    "Aggressive Hiring",
    "Moderate Hiring",
    "Hiring Freeze",
    "Downsizing"
]

hiring_security = (
    df.groupby("hiring_trend")["job_security_score"]
    .mean()
    .reindex(trend_order)
    .reset_index()
)

colors = [
    "#d3d3d3",
    "#d3d3d3",
    "#d3d3d3",
    "#ff2d55"
]

fig_trend = go.Figure()

fig_trend.add_trace(
    go.Bar(
        x=hiring_security["hiring_trend"],
        y=hiring_security["job_security_score"],
        marker_color=colors,
        text=hiring_security["job_security_score"].round(2),
        textposition="outside"
    )
)

fig_trend.add_annotation(
    x="Downsizing",
    y=hiring_security.iloc[-1]["job_security_score"],
    text="Punto crítico:\ncolapso de confianza",
    showarrow=True,
    arrowhead=2,
    ax=80,
    ay=-60
)

fig_trend.update_layout(
    title="Seguridad laboral según estrategia de contratación",
    xaxis_title="Hiring Trend",
    yaxis_title="Job Security Score",
    plot_bgcolor="black",
    paper_bgcolor="black",
    font=dict(size=14)
)

st.plotly_chart(fig_trend, use_container_width=True)
