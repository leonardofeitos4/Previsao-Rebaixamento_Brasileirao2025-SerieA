import streamlit as st
import pandas as pd
import plotly.express as px
import os

def main():
    st.set_page_config(layout="wide")  # Usa layout amplo
    st.title("📊 Análise Descritiva")

    # Carregando base de dados
    caminho_dados = os.path.join("dados", "BASE_FINAL.csv")
    df = pd.read_csv(caminho_dados)
    df.columns = df.columns.str.strip()  # Corrige espaços nos nomes

    # Visão Geral da Base
    st.subheader("📋 Visão Geral da Base Completa")
    st.dataframe(df, use_container_width=True)

    # Filtro de temporada
    temporadas_disponiveis = sorted(df['Temporada'].unique())
    temporada_sel = st.selectbox("Selecione o ano:", temporadas_disponiveis)
    df_filtrado = df[df['Temporada'] == temporada_sel]

    # Estatísticas Descritivas
    st.subheader(f"📊 Estatísticas Descritivas ({temporada_sel})")
    desc = df_filtrado.describe().T
    st.dataframe(desc, use_container_width=True, height=400)

    # Tabela de Distribuições das Variáveis Numéricas
    st.subheader(f"📈 Tabela de Variáveis Numéricas ({temporada_sel})")
    colunas_numericas = ['Plantel', 'Estrangeiros', 'Valor de Mercado Total', 'Pontos']
    # Exibe todas as observações para as colunas selecionadas
    if all(col in df_filtrado.columns for col in colunas_numericas):
        st.dataframe(df_filtrado[colunas_numericas], use_container_width=True)
    else:
        st.write("⚠️ Algumas colunas numéricas não estão disponíveis nesta temporada.")

    # Filtro de clube
    st.sidebar.subheader("Seleção de Clube")
    clubes_disponiveis = sorted(df['Clube'].unique())  # permite ver todos os clubes
    clube_sel = st.sidebar.selectbox("Selecione o clube:", clubes_disponiveis)

    # Dados do clube na temporada
    df_clube = df_filtrado[df_filtrado['Clube'] == clube_sel]
    st.subheader(f"📑 Dados do {clube_sel} em {temporada_sel}")
    st.dataframe(df_clube, use_container_width=True)

    # Gráfico de indicadores (única temporada)
    st.subheader(f"📊 Indicadores do {clube_sel} em {temporada_sel}")
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
            title=f'Indicadores do {clube_sel} em {temporada_sel}',
        )
        fig_stack.update_layout(barmode='stack', xaxis_title='Indicador', yaxis_title='Valor')
        st.plotly_chart(fig_stack, use_container_width=True)
    else:
        st.write("⚠️ Nenhum dado disponível para esse clube e ano.")

    # Gráfico de indicadores ao longo dos anos para o clube
    st.subheader(f"📈 Evolução de Indicadores do {clube_sel} ({min(temporadas_disponiveis)}–{max(temporadas_disponiveis)})")
    df_clube_all = df[df['Clube'] == clube_sel]
    if not df_clube_all.empty:
        df_all_melt = df_clube_all.melt(
            id_vars=['Clube', 'Temporada'],
            value_vars=colunas_numericas,
            var_name='Indicador',
            value_name='Valor'
        )
        fig_evol = px.bar(
            df_all_melt,
            x='Temporada',
            y='Valor',
            color='Indicador',
            barmode='group',
            title=f'Evolução dos Indicadores do {clube_sel} ao Longo dos Anos'
        )
        st.plotly_chart(fig_evol, use_container_width=True)
    else:
        st.write("⚠️ Não há dados históricos para esse clube.")

if __name__ == '__main__':
    main()
