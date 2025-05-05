import streamlit as st
import pandas as pd
import plotly.express as px
import os

def main():
    st.title("📊 Análise Descritiva")

    # Carregando base de dados
    caminho_dados = os.path.join("dados", "BASE_FINAL.csv")
    df = pd.read_csv(caminho_dados)

    # Corrigindo nomes de colunas (caso haja espaços)
    df.columns = df.columns.str.strip()

    st.subheader("📋 Visão Geral da Base")
    st.write(f"Linhas: {df.shape[0]} | Colunas: {df.shape[1]}")
    st.dataframe(df.head())

    # Filtro de temporada
    temporadas_disponiveis = sorted(df['Temporada'].unique())
    temporada_sel = st.selectbox("Selecione o ano:", temporadas_disponiveis)

    df_filtrado = df[df['Temporada'] == temporada_sel]

    st.subheader(f"📊 Estatísticas Descritivas ({temporada_sel})")
    st.dataframe(df_filtrado.describe())

    # Distribuições das variáveis numéricas
    st.subheader(f"📈 Distribuições das Variáveis Numéricas ({temporada_sel})")
    colunas_numericas = ['Plantel', 'Estrangeiros', 'Valor de Mercado Total', 'Pontos']

    for coluna in colunas_numericas:
        if coluna in df_filtrado.columns and not df_filtrado.empty:
            fig = px.histogram(df_filtrado, x=coluna, nbins=15, title=f'Distribuição de {coluna} ({temporada_sel})')
            st.plotly_chart(fig)
        else:
            st.write(f"⚠️ Dados de **{coluna}** não disponíveis para {temporada_sel}.")

    # Filtro de clube
    clubes_disponiveis = sorted(df_filtrado['Clube'].unique())
    clube_sel = st.selectbox("Selecione o clube:", clubes_disponiveis)

    df_clube = df_filtrado[df_filtrado['Clube'] == clube_sel]

    st.subheader(f"📑 Dados do {clube_sel} ({temporada_sel})")
    st.dataframe(df_clube)

    # Gráfico de barras empilhadas
    st.subheader(f"📊 Indicadores do {clube_sel} ({temporada_sel})")

    if not df_clube.empty:
        df_clube_melt = df_clube.melt(
            id_vars=['Clube', 'Temporada'],
            value_vars=colunas_numericas,
            var_name='Indicador',
            value_name='Valor'
        )

        fig_stack = px.bar(
            df_clube_melt,
            x='Indicador',
            y='Valor',
            color='Indicador',
            text='Valor',
            title=f'Indicadores do {clube_sel} ({temporada_sel})',
        )
        fig_stack.update_layout(barmode='stack', xaxis_title='Indicador', yaxis_title='Valor')
        st.plotly_chart(fig_stack)
    else:
        st.write("⚠️ Nenhum dado disponível para esse clube e ano.")

