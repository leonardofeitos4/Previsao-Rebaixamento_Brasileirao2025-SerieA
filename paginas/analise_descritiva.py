import streamlit as st
import pandas as pd
import plotly.express as px
import os

def main():
    st.title("Análise Descritiva – Campeonato Brasileiro Série A")

    # Carregar dados de forma segura (sem caminho absoluto)
    caminho_base = os.path.join('dados', 'todos_clubes_serieA.csv')
    df = pd.read_csv(caminho_base)

    # Converter Temporada pra inteiro
    df['Temporada'] = df['Temporada'].astype(int)

    # Remover ano 2025 da análise
    df = df[df['Temporada'] != 2025]

    st.subheader("Visão Geral da Base")

    # Filtro de ano
    anos_disponiveis = sorted(df['Temporada'].unique())
    ano_sel = st.selectbox("Selecione o ano", anos_disponiveis, index=len(anos_disponiveis)-1)

    df_ano = df[df['Temporada'] == ano_sel]

    st.write(f"**Base de Dados – Temporada {ano_sel}**")
    st.write(f"Linhas: {df_ano.shape[0]}   Colunas: {df_ano.shape[1]}")
    st.dataframe(df_ano)

    st.subheader("Estatísticas Descritivas por Variável")

    # Estatísticas por variável numérica, com ano
    stats = df_ano.describe().transpose()
    st.dataframe(stats)

    st.subheader("Distribuições das Variáveis Numéricas")

    num_cols = ['Plantel', 'Estrangeiros', 'Valor de Mercado Total', 'Pontos']

    for col in num_cols:
        fig = px.histogram(df, x=col, color='Temporada', nbins=20, title=f'Distribuição de {col} por Temporada')
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Análise de um Clube Específico")

    clubes_disponiveis = sorted(df['Clube'].unique())
    clube_sel = st.selectbox("Selecione o clube", clubes_disponiveis)

    df_clube = df[df['Clube'] == clube_sel]

    st.write(f"**Dados do clube {clube_sel}**")
    st.dataframe(df_clube)

    # Gráfico colunas empilhadas verticais com rótulos
    st.subheader(f"Métricas Empilhadas – {clube_sel}")

    metrics = ['Plantel', 'Estrangeiros', 'Valor de Mercado Total', 'Pontos']
    df_stack = df_clube[['Temporada'] + metrics]
    df_stack_melted = df_stack.melt(id_vars='Temporada', value_vars=metrics, var_name='Métrica', value_name='Valor')

    fig_stack = px.bar(
        df_stack_melted,
        x='Temporada',
        y='Valor',
        color='Métrica',
        barmode='stack',
        title=f"Métricas Empilhadas – {clube_sel}",
        text_auto=True
    )

    fig_stack.update_traces(textposition='inside')
    fig_stack.update_layout(xaxis_title='Temporada', yaxis_title='Valor Total')
    st.plotly_chart(fig_stack, use_container_width=True)

if __name__ == "__main__":
    main()
