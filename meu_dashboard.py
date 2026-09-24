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
        color: white;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #151821;
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    /* Títulos */
    h1, h2, h3 {
        color: white;
    }

    /* Métricas */
    div[data-testid="stMetric"] {
        background-color: #181c26;
        border: 1px solid #292e3a;
        border-left: 4px solid #0070cc;
        border-radius: 8px;
        padding: 15px;
    }

    div[data-testid="stMetricLabel"] {
        color: #b8bec9;
    }

    div[data-testid="stMetricValue"] {
        color: white;
    }

    /* Botão */
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

                preco = np.random.uniform(
                    3500,
                    5500
                )

            elif categoria == "Jogos":

                preco = np.random.uniform(
                    150,
                    400
                )

            elif categoria == "Acessórios":

                preco = np.random.uniform(
                    100,
                    800
                )

            elif categoria == "PlayStation Plus":

                preco = np.random.uniform(
                    40,
                    500
                )

            else:

                preco = np.random.uniform(
                    3000,
                    5000
                )

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
    options=sorted(
        df["Plataforma"].unique()
    ),
    default=sorted(
        df["Plataforma"].unique()
    )
)


categorias_selecionadas = st.sidebar.multiselect(
    "Categoria de Produto",
    options=sorted(
        df["Categoria"].unique()
    ),
    default=sorted(
        df["Categoria"].unique()
    )
)


# ============================================================
# FILTROS
# ============================================================

df_filtrado = df[
    (df["Plataforma"].isin(
        plataformas_selecionadas
    ))
    &
    (df["Categoria"].isin(
        categorias_selecionadas
    ))
].copy()


# ============================================================
# TÍTULO
# ============================================================

st.title(
    "PlayStation Global Sales & Services"
)

st.caption(
    "Painel de Inteligência Operacional e "
    "Desempenho do Ecossistema PlayStation"
)

st.divider()


# ============================================================
# CÁLCULO DOS KPIs
# ============================================================

receita_total = df_filtrado[
    "Receita"
].sum()


volume_pedidos = df_filtrado[
    "Quantidade"
].sum()


if volume_pedidos > 0:

    ticket_medio = (
        receita_total /
        volume_pedidos
    )

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
# FORMATAÇÃO DOS VALORES
# ============================================================

def formatar_moeda(valor):

    valor_formatado = f"{valor:,.2f}"

    valor_formatado = (
        valor_formatado
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

    return f"R$ {valor_formatado}"


def formatar_numero(valor):

    return f"{int(valor):,}".replace(
        ",",
        "."
    )


# ============================================================
# KPIs
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        label="💰 Receita Acumulada",
        value=formatar_moeda(
            receita_total
        )
    )


with col2:

    st.metric(
        label="📦 Volume de Pedidos",
        value=formatar_numero(
            volume_pedidos
        )
    )


with col3:

    st.metric(
        label="🎫 Ticket Médio",
        value=formatar_moeda(
            ticket_medio
        )
    )


with col4:

    st.metric(
        label="🏆 Categoria Líder",
        value=categoria_lider
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
# ABA 1 - EVOLUÇÃO MENSAL
# ============================================================

with tab1:

    st.subheader(
        "Evolução Mensal da Receita"
    )

    if not df_filtrado.empty:

        df_mensal = df_filtrado.copy()

        df_mensal["Mês"] = (
            df_mensal["Data"]
            .dt
            .to_period("M")
            .astype(str)
        )

        df_mensal = (
            df_mensal
            .groupby(
                "Mês",
                as_index=False
            )["Receita"]
            .sum()
        )


        grafico_mensal = (
            alt.Chart(
                df_mensal
            )
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
            "Nenhum dado encontrado "
            "para os filtros selecionados."
        )


# ============================================================
# ABA 2 - PLATAFORMAS
# ============================================================

with tab2:

    st.subheader(
        "Receita por Plataforma"
    )

    if not df_filtrado.empty:

        df_plataforma = (
            df_filtrado
            .groupby(
                "Plataforma",
                as_index=False
            )["Receita"]
            .sum()
            .sort_values(
                "Receita",
                ascending=False
            )
        )


        grafico_plataforma = (
            alt.Chart(
                df_plataforma
            )
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
            "Nenhum dado encontrado "
            "para os filtros selecionados."
        )


# ============================================================
# ABA 3 - REGISTROS
# ============================================================

with tab3:

    st.subheader(
        "Registros Filtrados"
    )


    st.dataframe(
        df_filtrado,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # DOWNLOAD CSV
    # ========================================================

    csv = df_filtrado.to_csv(
        index=False
    ).encode("utf-8")


    st.download_button(
        label="⬇️ Baixar dados filtrados em CSV",
        data=csv,
        file_name=(
            "vendas_playstation_filtradas.csv"
        ),
        mime="text/csv"
    )
