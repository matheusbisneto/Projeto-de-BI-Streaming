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
    "#6cb4b1",  # azul turquesa vibrante
    "#ff8c6a",  # pêssego saturado
    "#77d5a2",  # verde menta mais vivo
    "#ff8ba7",  # rosa claro intenso
    "#9e6fd9",  # lilás forte
    "#f7a3d2",  # rosa lavanda saturado
    "#ffff80",  # amarelo claro mais vibrante
    "#98f0c5",  # verde água forte
    "#b3e0a0",  # verde menta acinzentado mais forte
    "#5ec3ff",  # azul claro brilhante
    "#ff8cb5",  # rosa chiclete intenso
    "#e4f2a7",  # verde limão mais saturado
    "#f9a99e",  # laranja rosado mais forte
    "#d0b7d9",  # cinza rosado com mais cor
    "#7bbdfb",  # azul céu intenso
]


# VISÃO GERAL DO MERCADO
if aba == "📊 Visão Geral do Mercado":
    st.title("📊 Participação de Mercado por Plataforma")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Assinantes Totais por Plataforma")
        assinantes = df_filtrado.groupby('plataforma')['usuario_id'].nunique().reset_index()
        fig = px.bar(
            assinantes, x='plataforma', y='usuario_id', color='plataforma',
            color_discrete_sequence=paleta_vibrante,
            labels={'usuario_id': 'Assinantes'}, title="Total de Assinantes"
        )
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)', font_color='black')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Crescimento Mensal de Usuários")
        crescimento = df.groupby(['data_mes', 'plataforma'])['usuario_id'].nunique().reset_index()
        fig2 = px.line(
            crescimento, x='data_mes', y='usuario_id', color='plataforma',
            color_discrete_sequence=paleta_vibrante,
            labels={'usuario_id': 'Usuários'},
            title="Crescimento ao Longo do Tempo"
        )
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                           plot_bgcolor='rgba(0,0,0,0)', font_color='black')
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Distribuição Geográfica dos Usuários")
    distribuicao = df.groupby('pais')['usuario_id'].nunique().reset_index()
    fig3 = px.pie(
        distribuicao, values='usuario_id', names='pais', title="Usuários por País",
        color_discrete_sequence=paleta_vibrante
    )
    fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='black')
    st.plotly_chart(fig3, use_container_width=True)

# ENGAJAMENTO
elif aba == "📈 Engajamento":
    st.title("📈 Engajamento por Plataforma")

    col1, col2 = st.columns(2)
    with col1:
        media_tempo = df_filtrado.groupby(['data_mes', 'plataforma'])['tempo_assistido_mensal'].mean().reset_index()
        fig = px.line(
            media_tempo, x='data_mes', y='tempo_assistido_mensal', color='plataforma',
            title='Tempo Médio Assistido por Plataforma',
            color_discrete_sequence=paleta_vibrante
        )
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)', font_color='black')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Comparativo: Tempo vs Títulos")
        comparativo = df_filtrado.groupby('plataforma')[['tempo_assistido_mensal', 'qtd_titulos_assistidos']].mean().reset_index()
        fig2 = px.bar(
            comparativo, x='plataforma', y=['tempo_assistido_mensal', 'qtd_titulos_assistidos'],
            barmode='group', title="Tempo e Títulos Médios",
            color_discrete_sequence=paleta_vibrante
        )
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                           plot_bgcolor='rgba(0,0,0,0)', font_color='black')
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Distribuição de Engajamento por Plataforma")
    fig3, ax = plt.subplots(figsize=(12, 4))
    sns.set_palette("coolwarm")
    sns.boxplot(x='plataforma', y='tempo_assistido_mensal', data=df_filtrado, ax=ax)
    ax.set_facecolor('none')
    fig3.patch.set_alpha(0.0)
    ax.set_title("Boxplot: Tempo Assistido", color='black')
    ax.tick_params(colors='black')
    ax.xaxis.label.set_color('black')
    ax.yaxis.label.set_color('black')
    st.pyplot(fig3)

# SATISFAÇÃO
elif aba == "⭐ Satisfação do Usuário":
    st.title("⭐ Satisfação e Qualidade")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Avaliação Média por Plataforma")
        aval = df_filtrado.groupby('plataforma')['avaliacao_usuario'].mean().reset_index()
        fig = px.bar(
            aval, x='plataforma', y='avaliacao_usuario', color='plataforma',
            title="Avaliação Média", labels={"avaliacao_usuario": "Nota Média"},
            color_discrete_sequence=paleta_vibrante
        )
        fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='black'),
    title_font=dict(color='black'),
    legend=dict(font=dict(color='black')),
    xaxis=dict(title_font=dict(color='black'), tickfont=dict(color='black')),
    yaxis=dict(title_font=dict(color='black'), tickfont=dict(color='black'))
)

    with col2:
        st.subheader("Correlação: Tempo vs Avaliação")
        fig2 = px.scatter(
            df_filtrado, x='tempo_assistido_mensal', y='avaliacao_usuario',
            color='plataforma', trendline="ols", title="Tempo Assistido vs Avaliação",
            color_discrete_sequence=paleta_vibrante
        )
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                           plot_bgcolor='rgba(0,0,0,0)', font_color='black')
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Distribuição das Avaliações por Plataforma")
    fig3, ax = plt.subplots(figsize=(12, 4))
    sns.set_palette("coolwarm")
    sns.boxplot(data=df_filtrado, x="plataforma", y="avaliacao_usuario", ax=ax)
    ax.set_facecolor('none')
    fig3.patch.set_alpha(0.0)
    ax.set_title("Boxplot: Avaliação por Plataforma", color='black')
    ax.tick_params(colors='black')
    ax.xaxis.label.set_color('black')
    ax.yaxis.label.set_color('black')
    st.pyplot(fig3)
