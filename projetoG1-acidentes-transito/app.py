import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

st.set_page_config(
    page_title="Acidentes de Trânsito no Brasil",
    page_icon="🚗",
    layout="wide"
)

sns.set_theme(style="whitegrid")

DATA_PATH = Path(__file__).parent / "dados" / "simulacao_acidentes_transito_brasil.csv"


@st.cache_data
def carregar_dados():
    df = pd.read_csv(DATA_PATH)

    df.columns = [col.strip().lower() for col in df.columns]

    df["data"] = pd.to_datetime(df["data"], errors="coerce")

    colunas_numericas = [
        "ano", "mes", "acidentes", "feridos", "mortes",
        "chuva_mm", "veiculos_envolvidos"
    ]

    for coluna in colunas_numericas:
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

    return df


df = carregar_dados()

# =========================================================
# TÍTULO
# =========================================================

st.title("🚗 Acidentes de Trânsito no Brasil")
st.markdown(
    """
    **Análise de dados de acidentes de trânsito entre 2015 e 2024**

    Este dashboard busca identificar padrões temporais, geográficos e
    relacionados às características dos acidentes, além de analisar
    feridos, mortes, clima, visibilidade e gravidade.
    """
)

st.divider()

# =========================================================
# FILTROS
# =========================================================

st.sidebar.header("🔎 Filtros")

anos = sorted(df["ano"].dropna().unique())
meses = sorted(df["mes"].dropna().unique())
regioes = sorted(df["regiao"].dropna().unique())
ufs = sorted(df["uf"].dropna().unique())
tipos = sorted(df["tipo_acidente"].dropna().unique())
periodos = sorted(df["periodo_dia"].dropna().unique())
gravidades = sorted(df["nivel_gravidade"].dropna().unique())

ano_selecionado = st.sidebar.multiselect(
    "Ano",
    anos,
    default=anos
)

mes_selecionado = st.sidebar.multiselect(
    "Mês",
    meses,
    default=meses
)

regiao_selecionada = st.sidebar.multiselect(
    "Região",
    regioes,
    default=regioes
)

uf_selecionada = st.sidebar.multiselect(
    "Estado",
    ufs,
    default=ufs
)

tipo_selecionado = st.sidebar.multiselect(
    "Tipo de acidente",
    tipos,
    default=tipos
)

periodo_selecionado = st.sidebar.multiselect(
    "Período do dia",
    periodos,
    default=periodos
)

gravidade_selecionada = st.sidebar.multiselect(
    "Nível de gravidade",
    gravidades,
    default=gravidades
)

dados = df[
    df["ano"].isin(ano_selecionado)
    & df["mes"].isin(mes_selecionado)
    & df["regiao"].isin(regiao_selecionada)
    & df["uf"].isin(uf_selecionada)
    & df["tipo_acidente"].isin(tipo_selecionado)
    & df["periodo_dia"].isin(periodo_selecionado)
    & df["nivel_gravidade"].isin(gravidade_selecionada)
].copy()

if dados.empty:
    st.warning("Nenhum registro corresponde aos filtros selecionados.")
    st.stop()

# =========================================================
# KPIs
# =========================================================

st.header("📊 Indicadores principais")

total_acidentes = dados["acidentes"].sum()
total_feridos = dados["feridos"].sum()
total_mortes = dados["mortes"].sum()

estado_critico = (
    dados.groupby("uf")["acidentes"]
    .sum()
    .idxmax()
)

periodo_critico = (
    dados.groupby("periodo_dia")["acidentes"]
    .sum()
    .idxmax()
)

tipo_frequente = (
    dados.groupby("tipo_acidente")["acidentes"]
    .sum()
    .idxmax()
)

c1, c2, c3, c4, c5, c6 = st.columns(6)

c1.metric(
    "Total de acidentes",
    f"{total_acidentes:,.0f}".replace(",", ".")
)

c2.metric(
    "Total de feridos",
    f"{total_feridos:,.0f}".replace(",", ".")
)

c3.metric(
    "Total de mortes",
    f"{total_mortes:,.0f}".replace(",", ".")
)

c4.metric(
    "Estado mais crítico",
    estado_critico
)

c5.metric(
    "Período mais perigoso",
    periodo_critico
)

c6.metric(
    "Tipo mais frequente",
    tipo_frequente
)

st.divider()

# =========================================================
# EVOLUÇÃO TEMPORAL
# =========================================================

st.header("📈 Evolução temporal")

temporal = (
    dados.groupby("data", as_index=False)
    .agg(
        acidentes=("acidentes", "sum"),
        feridos=("feridos", "sum"),
        mortes=("mortes", "sum")
    )
    .sort_values("data")
)

fig, ax = plt.subplots(figsize=(12, 5))

sns.lineplot(
    data=temporal,
    x="data",
    y="acidentes",
    ax=ax
)

ax.set_title("Evolução dos acidentes ao longo do tempo")
ax.set_xlabel("Data")
ax.set_ylabel("Quantidade de acidentes")

st.pyplot(fig, use_container_width=True)
plt.close(fig)

# =========================================================
# ANÁLISE TEMPORAL AVANÇADA
# =========================================================

st.subheader("📅 Análise temporal avançada")

mensal = (
    dados.set_index("data")
    .resample("ME")
    .agg({
        "acidentes": "sum",
        "feridos": "sum",
        "mortes": "sum"
    })
    .reset_index()
)

if len(mensal) >= 3:
    mensal["media_movel_3m"] = (
        mensal["acidentes"]
        .rolling(3)
        .mean()
    )

    fig, ax = plt.subplots(figsize=(12, 5))

    sns.lineplot(
        data=mensal,
        x="data",
        y="acidentes",
        label="Acidentes",
        ax=ax
    )

    sns.lineplot(
        data=mensal,
        x="data",
        y="media_movel_3m",
        label="Média móvel de 3 meses",
        linewidth=3,
        ax=ax
    )

    ax.set_title("Série temporal com média móvel")
    ax.set_xlabel("Data")
    ax.set_ylabel("Acidentes")

    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

# =========================================================
# ESTADOS E REGIÕES
# =========================================================

col1, col2 = st.columns(2)

with col1:
    st.subheader("🇧🇷 Acidentes por estado")

    por_uf = (
        dados.groupby("uf", as_index=False)["acidentes"]
        .sum()
        .sort_values("acidentes", ascending=False)
    )

    fig, ax = plt.subplots(figsize=(8, 6))

    sns.barplot(
        data=por_uf,
        x="acidentes",
        y="uf",
        ax=ax
    )

    ax.set_title("Ranking de acidentes por estado")
    ax.set_xlabel("Acidentes")
    ax.set_ylabel("Estado")

    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

with col2:
    st.subheader("🌎 Acidentes por região")

    por_regiao = (
        dados.groupby("regiao", as_index=False)["acidentes"]
        .sum()
        .sort_values("acidentes", ascending=False)
    )

    fig, ax = plt.subplots(figsize=(8, 6))

    sns.barplot(
        data=por_regiao,
        x="regiao",
        y="acidentes",
        ax=ax
    )

    ax.set_title("Comparação entre regiões")
    ax.set_xlabel("Região")
    ax.set_ylabel("Acidentes")
    ax.tick_params(axis="x", rotation=20)

    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

# =========================================================
# TIPO DE ACIDENTE
# =========================================================

st.header("🚘 Tipos de acidente")

por_tipo = (
    dados.groupby("tipo_acidente", as_index=False)["acidentes"]
    .sum()
    .sort_values("acidentes", ascending=False)
)

fig, ax = plt.subplots(figsize=(10, 5))

sns.barplot(
    data=por_tipo,
    x="acidentes",
    y="tipo_acidente",
    ax=ax
)

ax.set_title("Tipos de acidente mais frequentes")
ax.set_xlabel("Acidentes")
ax.set_ylabel("Tipo de acidente")

st.pyplot(fig, use_container_width=True)
plt.close(fig)

# =========================================================
# HEATMAP
# =========================================================

st.header("🔥 Horários e períodos críticos")

heatmap = pd.pivot_table(
    dados,
    values="acidentes",
    index="mes",
    columns="periodo_dia",
    aggfunc="sum",
    fill_value=0
)

fig, ax = plt.subplots(figsize=(10, 5))

sns.heatmap(
    heatmap,
    annot=True,
    fmt=".0f",
    cmap="YlOrRd",
    ax=ax
)

ax.set_title("Acidentes por mês e período do dia")
ax.set_xlabel("Período do dia")
ax.set_ylabel("Mês")

st.pyplot(fig, use_container_width=True)
plt.close(fig)

# =========================================================
# CLIMA / CHUVA
# =========================================================

st.header("🌧️ Condições climáticas")

col1, col2 = st.columns(2)

with col1:

    chuva = (
        dados.groupby("visibilidade", as_index=False)["acidentes"]
        .sum()
        .sort_values("acidentes", ascending=False)
    )

    fig, ax = plt.subplots(figsize=(7, 5))

    ax.pie(
        chuva["acidentes"],
        labels=chuva["visibilidade"],
        autopct="%1.1f%%",
        startangle=90
    )

    ax.set_title("Acidentes por condição de visibilidade")

    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

with col2:

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.scatterplot(
        data=dados,
        x="chuva_mm",
        y="acidentes",
        hue="visibilidade",
        ax=ax
    )

    ax.set_title("Relação entre chuva e acidentes")
    ax.set_xlabel("Chuva (mm)")
    ax.set_ylabel("Acidentes")

    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

# =========================================================
# GRAVIDADE
# =========================================================

st.header("⚠️ Gravidade dos acidentes")

gravidade = (
    dados.groupby("nivel_gravidade", as_index=False)
    .agg(
        acidentes=("acidentes", "sum"),
        feridos=("feridos", "sum"),
        mortes=("mortes", "sum")
    )
    .sort_values("acidentes", ascending=False)
)

fig, ax = plt.subplots(figsize=(9, 5))

sns.barplot(
    data=gravidade,
    x="nivel_gravidade",
    y="acidentes",
    ax=ax
)

ax.set_title("Acidentes por nível de gravidade")
ax.set_xlabel("Nível de gravidade")
ax.set_ylabel("Acidentes")

st.pyplot(fig, use_container_width=True)
plt.close(fig)

st.dataframe(
    gravidade,
    use_container_width=True,
    hide_index=True
)

# =========================================================
# CORRELAÇÃO ESTATÍSTICA
# =========================================================

st.header("📐 Correlação entre variáveis")

colunas_correlacao = [
    "acidentes",
    "feridos",
    "mortes",
    "chuva_mm",
    "veiculos_envolvidos"
]

matriz = dados[colunas_correlacao].corr()

fig, ax = plt.subplots(figsize=(9, 6))

sns.heatmap(
    matriz,
    annot=True,
    cmap="coolwarm",
    vmin=-1,
    vmax=1,
    ax=ax
)

ax.set_title("Matriz de correlação")

st.pyplot(fig, use_container_width=True)
plt.close(fig)

st.info(
    """
    A correlação mede a associação linear entre duas variáveis.
    Valores próximos de 1 indicam associação positiva, valores próximos
    de -1 indicam associação negativa e valores próximos de 0 indicam
    pouca associação linear. Correlação, por si só, não significa causalidade.
    """
)

# =========================================================
# MUNICÍPIOS
# =========================================================

st.header("🏙️ Ranking de cidades críticas")

cidades = (
    dados.groupby("cidade", as_index=False)
    .agg(
        acidentes=("acidentes", "sum"),
        feridos=("feridos", "sum"),
        mortes=("mortes", "sum")
    )
    .sort_values("acidentes", ascending=False)
)

st.dataframe(
    cidades.head(15),
    use_container_width=True,
    hide_index=True
)

# =========================================================
# INTERPRETAÇÃO
# =========================================================

st.header("🧠 Interpretação dos resultados")

primeiro = temporal.iloc[0]["acidentes"]
ultimo = temporal.iloc[-1]["acidentes"]

if ultimo > primeiro:
    tendencia = "aumento"
elif ultimo < primeiro:
    tendencia = "redução"
else:
    tendencia = "estabilidade"

st.info(
    f"""
    **Principais resultados do recorte selecionado:**

    - O estado com maior número de acidentes é **{estado_critico}**.
    - O período do dia com maior concentração é **{periodo_critico}**.
    - O tipo de acidente mais frequente é **{tipo_frequente}**.
    - Foram registrados **{total_acidentes:,.0f} acidentes**.
    - Foram registrados **{total_feridos:,.0f} feridos**.
    - Foram registradas **{total_mortes:,.0f} mortes**.
    - No período analisado, observa-se **{tendencia}** entre o primeiro
      e o último ponto da série temporal.
    """
)

# =========================================================
# TABELA DETALHADA
# =========================================================

st.header("📋 Dados detalhados")

st.dataframe(
    dados.sort_values(["ano", "mes", "uf"]),
    use_container_width=True,
    hide_index=True
)

# =========================================================
# CONCLUSÃO
# =========================================================

st.header("🎯 Conclusão executiva")

st.markdown(
    f"""
    A análise dos acidentes de trânsito permite identificar padrões
    temporais, geográficos e relacionados às condições das ocorrências.

    No recorte selecionado, **{estado_critico}** apresenta a maior quantidade
    de acidentes, enquanto **{periodo_critico}** concentra a maior quantidade
    de ocorrências entre os períodos do dia.

    A análise também permite observar a distribuição dos acidentes entre
    os diferentes tipos de ocorrência, níveis de gravidade e condições de
    visibilidade. Além disso, a série temporal e a média móvel ajudam a
    identificar tendências ao longo do período estudado.

    Os indicadores de feridos e mortes complementam a análise ao demonstrar
    o impacto dos acidentes, enquanto a matriz de correlação permite explorar
    associações entre acidentes, vítimas, chuva e veículos envolvidos.
    """
)

st.markdown("""
<div style="text-align: left;">
    Projeto G1 — Análise e Visualização de Dados com Python<br>
    Aluno: Yago Amaro Zamborlini<br>
    Professor: Alexandre Louzada
</div>
""", unsafe_allow_html=True)
