import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import base64

# Configurações da página
st.set_page_config(page_title="Dashboard Streaming", layout="wide")

# Fundo com CSS e correções visuais
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
        }}
        [data-testid="stSidebar"] {{
            background-color: #84c2cd;
        }}
        [data-testid="stSidebar"] * {{
            color: black !important;
        }}
        .stSelectbox div, .stRadio > div {{
            background-color: rgba(255, 255, 255, 0.1) !important;
        }}
        .css-18e3th9 {{
            background-color: rgba(255,255,255,0.1) !important;
            border-radius: 10px;
            padding: 10px;
        }}
        .st-bb {{
            background-color: rgba(255,255,255,0.1) !important;
            border: none;
            color: black !important;
        }}
        .stPlotlyChart > div {{
            background-color: rgba(0,0,0,0) !important;
        }}
        .stTitle, .stHeader, .stSubheader, .markdown-text-container, 
        h1, h2, h3, h4, h5, h6 {{
            color: black !important;
        }}
        .stTextInput > div > div > input {{
            color: black !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_local("assets/background.jpg")

# Leitura dos dados
@st.cache_data
def carregar_dados():
    df = pd.read_csv("dados_streaming_realista_2018_2024.csv")
    df["data_mes"] = pd.to_datetime(df["data"]).dt.to_period("M").astype(str)
    return df

df = carregar_dados()

# NAVBAR
aba = st.sidebar.radio("🔍 Selecione a seção:", [
    "📊 Visão Geral do Mercado",
    "📈 Engajamento",
    "⭐ Satisfação do Usuário"
])

# Filtros
anos = sorted(df['data_mes'].unique())
paises = ['Todos'] + sorted(df['pais'].unique())
filtro_pais = st.sidebar.selectbox("🌎 País", paises)
filtro_ano = st.sidebar.selectbox("🗓 Mês/Ano", ['Todos'] + anos)

df_filtrado = df.copy()
if filtro_pais != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['pais'] == filtro_pais]
if filtro_ano != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['data_mes'] == filtro_ano]

# Paleta vibrante com máxima variedade
paleta_vibrante = [
    "#6cb4b1", "#ff8c6a", "#77d5a2", "#ff8ba7", "#9e6fd9", "#f7a3d2", "#ffff80",
    "#98f0c5", "#b3e0a0", "#5ec3ff", "#ff8cb5", "#e4f2a7", "#f9a99e", "#d0b7d9", "#7bbdfb"
]

# Função para configurar gráficos com textos pretos
def ajustar_layout(fig):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='black')
    )

# VISÃO GERAL DO MERCADO
if aba == "📊 Visão Geral do Mercado":
    st.title("📊 Participação de Mercado por Plataforma")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Assinantes Totais por Plataforma")
        assinantes = df_filtrado.groupby('plataforma')['usuario_id'].nunique().reset_index()
        fig = px.bar(assinantes, x='plataforma', y='usuario_id', color='plataforma',
                     color_discrete_sequence=paleta_vibrante, labels={'usuario_id': 'Assinantes'})
        ajustar_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Crescimento Mensal de Usuários")
        crescimento = df.groupby(['data_mes', 'plataforma'])['usuario_id'].nunique().reset_index()
        fig2 = px.line(crescimento, x='data_mes', y='usuario_id', color='plataforma',
                       color_discrete_sequence=paleta_vibrante, labels={'usuario_id': 'Usuários'})
        ajustar_layout(fig2)
        st.plotly_chart(fig2, use_container_width=True)

# ENGAJAMENTO
elif aba == "📈 Engajamento":
    st.title("📈 Engajamento por Plataforma")

    col1, col2 = st.columns(2)
    with col1:
        media_tempo = df_filtrado.groupby(['data_mes', 'plataforma'])['tempo_assistido_mensal'].mean().reset_index()
        fig = px.line(media_tempo, x='data_mes', y='tempo_assistido_mensal', color='plataforma',
                      color_discrete_sequence=paleta_vibrante, title='Tempo Médio Assistido por Plataforma')
        ajustar_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

# SATISFAÇÃO
elif aba == "⭐ Satisfação do Usuário":
    st.title("⭐ Satisfação e Qualidade")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Avaliação Média por Plataforma")
        aval = df_filtrado.groupby('plataforma')['avaliacao_usuario'].mean().reset_index()
        fig = px.bar(aval, x='plataforma', y='avaliacao_usuario', color='plataforma',
                     labels={"avaliacao_usuario": "Nota Média"}, color_discrete_sequence=paleta_vibrante)
        ajustar_layout(fig)
        st.plotly_chart(fig, use_container_width=True)
