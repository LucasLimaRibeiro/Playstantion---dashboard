import streamlit as st
import pandas as pd
import numpy as np
import altair as alt


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="PlayStation Analytics Hub",
    page_icon="🎮",
    layout="wide"
)


# ============================================================
# CSS - VISUAL PLAYSTATION
# ============================================================

st.markdown("""
<style>

    /* Fundo principal */
    .stApp {
        background-color: #0f1015;
        color: #ffffff;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #151821;
    }

    section[data-testid="stSidebar"] * {
        color: #ffffff;
    }

    /* Título principal */
    h1 {
        color: #ffffff;
        font-weight: 800;
    }

    /* Cards dos KPIs */
    .kpi-card {
        background: #181c26;
        border: 1px solid #292e3a;
        border-left: 4px solid #0070cc;
        border-radius: 8px;
        padding: 20px;
        min-height: 150px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    }

    .kpi-title {
        font-size: 15px;
        color: #b8bec9;
        margin-bottom: 10px;
        font-weight: 600;
    }

    .kpi-value {
        font-size: 25px;
        color: #ffffff;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .kpi-sub {
        font-size: 13px;
        color: #8f96a3;
    }

    /* Botões */
    .stDownloadButton button {
        background-color: #0070cc;
        color: white;
        border: none;
    }

    .stDownloadButton button:hover {
        background-color: #005da8;
        color: white;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# GERAÇÃO DOS DADOS
# ============================================================

@st.cache_data
def gerar_dados():

    np.random.seed(42)

    datas = pd.date_range(
        start="2023-01-01",
        end="2023-12-31",
        freq="D"
    )

    categorias = [
        "Consoles",
        "Jogos",
        "Acessórios",
        "PlayStation Plus",
        "PS VR2"
    ]

    plataformas = [
        "PlayStation 5",
        "PlayStation 4",
        "PlayStation Store",
        "PlayStation VR2"
    ]

    dados = []

    for data in datas:

        for _ in range(3):

            categoria = np.random.choice(categorias)
            plataforma = np.random.choice(plataformas)

            quantidade = np.random.randint(1, 8)

            if categoria == "Consoles":
                preco = np.random.uniform(3500, 5500)

            elif categoria == "Jogos":
                preco = np.random.uniform(150, 400)

            elif categoria == "Acessórios":
                preco = np.random.uniform(100, 800)

            elif categoria == "PlayStation Plus":
                preco = np.random.uniform(40, 500)

            else:
                preco = np.random.uniform(3000, 5000)

            receita = quantidade * preco

            dados.append({
                "Data": data,
                "Plataforma": plataforma,
                "Categoria": categoria,
                "Quantidade": quantidade,
                "Receita": receita
            })

    return pd.DataFrame(dados)


df = gerar_dados()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🎮 Filtros Analíticos")

st.sidebar.write(
    "Selecione os parâmetros para recalcular os indicadores:"
)

plataformas_selecionadas = st.sidebar.multiselect(
    "Plataforma",
    options=sorted(df["Plataforma"].unique()),
    default=sorted(df["Plataforma"].unique())
)

categorias_selecionadas = st.sidebar.multiselect(
    "Categoria de Produto",
    options=sorted(df["Categoria"].unique()),
    default=sorted(df["Categoria"].unique())
)


# ============================================================
# FILTROS
# ============================================================

df_filtrado = df[
    (df["Plataforma"].isin(plataformas_selecionadas)) &
    (df["Categoria"].isin(categorias_selecionadas))
].copy()


# ============================================================
# TÍTULO
# ============================================================

st.title("PlayStation Global Sales & Services")

st.caption(
    "Painel de Inteligência Operacional e Desempenho do Ecossistema PlayStation"
)

st.divider()


# ============================================================
# CÁLCULO DOS KPIs
# ============================================================

receita_total = df_filtrado["Receita"].sum()

volume_pedidos = df_filtrado["Quantidade"].sum()

if volume_pedidos > 0:
    ticket_medio = receita_total / volume_pedidos
else:
    ticket_medio = 0


if not df_filtrado.empty:
    categoria_lider = (
        df_filtrado
        .groupby("Categoria")["Receita"]
        .sum()
        .idxmax()
    )
else:
    categoria_lider = "Nenhuma"


# ============================================================
# CARDS DOS KPIs
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">
                Receita Acumulada
            </div>

            <div class="kpi-value">
                R$ {receita_total:,.2f}
            </div>

            <div class="kpi-sub">
                ● Vendas e Serviços
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">
                Volume de Pedidos
            </div>

            <div class="kpi-value">
                {volume_pedidos:,}
            </div>

            <div class="kpi-sub">
                ● Transações Processadas
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">
                Ticket Médio
            </div>

            <div class="kpi-value">
                R$ {ticket_medio:,.2f}
            </div>

            <div class="kpi-sub">
                ● Valor Médio por Pedido
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col4:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">
                Categoria Líder
            </div>

            <div class="kpi-value">
                {categoria_lider}
            </div>

            <div class="kpi-sub">
                ● Maior Faturamento
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.write("")


# ============================================================
# ABAS
# ============================================================

tab1, tab2, tab3 = st.tabs([
    "📈 Evolução e Segmentação",
    "📊 Desempenho por Plataforma",
    "📋 Registros Brutos"
])


# ============================================================
# ABA 1 - EVOLUÇÃO
# ============================================================

with tab1:

    st.subheader("Evolução Mensal da Receita")

    if not df_filtrado.empty:

        df_mensal = (
            df_filtrado
            .assign(Mês=df_filtrado["Data"].dt.to_period("M").astype(str))
            .groupby("Mês", as_index=False)["Receita"]
            .sum()
        )

        grafico_mensal = (
            alt.Chart(df_mensal)
            .mark_area(
                line=True,
                opacity=0.7
            )
            .encode(
                x=alt.X(
                    "Mês:N",
                    title="Mês",
                    sort=None
                ),
                y=alt.Y(
                    "Receita:Q",
                    title="Receita (R$)"
                ),
                tooltip=[
                    alt.Tooltip(
                        "Mês:N",
                        title="Mês"
                    ),
                    alt.Tooltip(
                        "Receita:Q",
                        title="Receita",
                        format=",.2f"
                    )
                ]
            )
            .properties(
                height=400
            )
        )

        st.altair_chart(
            grafico_mensal,
            use_container_width=True
        )

    else:

        st.warning(
            "Nenhum dado encontrado para os filtros selecionados."
        )


# ============================================================
# ABA 2 - PLATAFORMAS
# ============================================================

with tab2:

    st.subheader("Receita por Plataforma")

    if not df_filtrado.empty:

        df_plataforma = (
            df_filtrado
            .groupby("Plataforma", as_index=False)["Receita"]
            .sum()
            .sort_values(
                "Receita",
                ascending=False
            )
        )

        grafico_plataforma = (
            alt.Chart(df_plataforma)
            .mark_bar()
            .encode(
                x=alt.X(
                    "Receita:Q",
                    title="Receita (R$)"
                ),
                y=alt.Y(
                    "Plataforma:N",
                    title="Plataforma",
                    sort="-x"
                ),
                tooltip=[
                    alt.Tooltip(
                        "Plataforma:N",
                        title="Plataforma"
                    ),
                    alt.Tooltip(
                        "Receita:Q",
                        title="Receita",
                        format=",.2f"
                    )
                ]
            )
            .properties(
                height=350
            )
        )

        st.altair_chart(
            grafico_plataforma,
            use_container_width=True
        )

    else:

        st.warning(
            "Nenhum dado encontrado para os filtros selecionados."
        )


# ============================================================
# ABA 3 - REGISTROS
# ============================================================

with tab3:

    st.subheader("Registros Filtrados")

    st.dataframe(
        df_filtrado,
        use_container_width=True,
        hide_index=True
    )

    csv = df_filtrado.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Baixar dados filtrados em CSV",
        data=csv,
        file_name="vendas_playstation_filtradas.csv",
        mime="text/csv"
    )
