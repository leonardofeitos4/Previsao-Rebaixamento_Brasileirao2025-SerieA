import streamlit as st
import pandas as pd
import plotly.express as px
import os

def main():
    st.title("📊 Análise Descritiva")

    # Caminho relativo
    caminho_base = os.path.join("dados", "BASE_FINAL.csv")
    df = pd.read_csv(caminho_base)

    st.subheader("📑 Visão Geral da Base")
    st.write(f"Linhas: {df.shape[0]}   Colunas: {df.shape[1]}")
    st.dataframe(df)

    # Filtro por temporada
    temporadas_disponiveis = sorted(df['Temporada'].unique())
    temporada_sel = st.selectbox("Selecione a Temporada:", temporadas_disponiveis)

    df_filtrado = df[df['Temporada'] == temporada_sel]

    st.subheader(f"📋 Estatísticas Descritivas (Ano: {temporada_sel})")
    st.write("**Resumo das variáveis numéricas considerando todos os clubes para a temporada selecionada.**")
    st.dataframe(df_filtrado.describe())

    st.subheader("📈 Distribuições das Variáveis Numéricas")
    colunas_numericas = ['Plantel', 'Idade Média', 'Estrangeiros', 'Valor de Mercado Total', 'Pontos']
    for coluna in colunas_numericas:
        fig = px.histogram(df_filtrado, x=coluna, nbins=15, title=f'Distribuição de {coluna} ({temporada_sel})')
        st.plotly_chart(fig, use_container_width=True)

    # Filtro por clube
    st.subheader("🏟️ Análises Individuais por Clube")
    clubes_disponiveis = sorted(df['Clube'].unique())
    clube_sel = st.selectbox("Selecione o Clube:", clubes_disponiveis)

    df_clube_todas = df[df['Clube'] == clube_sel][['Temporada', 'Plantel', 'Estrangeiros', 'Valor de Mercado Total', 'Pontos']]
    st.write(f"📊 Dados históricos para o **{clube_sel}**:")
    st.dataframe(df_clube_todas)

    st.subheader(f"📊 Estatísticas Descritivas por Variável — {clube_sel}")
    st.dataframe(df_clube_todas.describe())

    st.subheader(f"📊 Gráfico de Colunas Empilhadas — {clube_sel}")

    df_clube_melt = df_clube_todas.melt(id_vars='Temporada', var_name='Variável', value_name='Valor')

    fig_stack = px.bar(
        df_clube_melt,
        x="Temporada",
        y="Valor",
        color="Variável",
        text_auto=True,
        barmode="stack",
        title=f'Colunas Empilhadas para {clube_sel}'
    )
    fig_stack.update_layout(xaxis_title="Temporada", yaxis_title="Valor", legend_title="Variável")
    st.plotly_chart(fig_stack, use_container_width=True)

    st.subheader("📊 Boxplots das Variáveis Numéricas (Comparação entre Clubes)")

    col_box = st.selectbox("Selecione a Variável para o Boxplot:", colunas_numericas)

    fig_box = px.box(
        df[df['Temporada'] != 2025],
        x="Clube",
        y=col_box,
        color="Clube",
        title=f'Distribuição de {col_box} por Clube (exceto 2025)',
        points="all"
    )
    fig_box.update_layout(xaxis_title="Clube", yaxis_title=col_box)
    st.plotly_chart(fig_box, use_container_width=True)

if __name__ == "__main__":
    main()
