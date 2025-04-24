import streamlit as st
import pandas as pd
import plotly.express as px
from utils.processamento import carregar_dados

def main():
    st.markdown("<h3 class='subheader'>Base de Dados Histórica</h3>", unsafe_allow_html=True)
    df = carregar_dados()
    df_display = df.copy()

    # Padronize a coluna de situação
    if 'Situacao' in df_display.columns:
        df_display['Situacao'] = df_display['Situacao'].replace({'Top4': 'Top 4', 'SerieA': 'Série A', 'Serie B para Série A': 'Série B para Série A'})
        df_display['Situação'] = df_display['Situacao']
    elif 'Status' in df_display.columns:
        status_mapping = {0: "Top 4", 1: "Série A", 2: "Série B para Série A"}
        df_display['Status'] = pd.to_numeric(df_display['Status'], errors='coerce')
        df_display['Situação'] = df_display['Status'].map(lambda x: status_mapping.get(x, x) if pd.notna(x) else "Desconhecido")
    else:
        df_display['Situação'] = "Desconhecido"

    # Filtros para a tabela
    col1, col2, col3 = st.columns(3)
    with col1:
        situacao_options = df_display['Situação'].dropna().unique()
        situacao_filter = st.multiselect("Situação", options=situacao_options, default=situacao_options)
    with col2:
        min_valor = st.number_input("Valor Mínimo (M€)", value=0.0)
    with col3:
        max_valor = st.number_input("Valor Máximo (M€)", value=float(df_display['Valor de Mercado Total'].max()))

    # Aplicar filtros
    filtered_df = df_display[
        (df_display['Situação'].isin(situacao_filter)) &
        (df_display['Valor de Mercado Total'] >= min_valor) &
        (df_display['Valor de Mercado Total'] <= max_valor)
    ]

    st.dataframe(filtered_df, use_container_width=True, height=400)

    # Visualizações
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h4>Média de Valor de Mercado por Situação</h4>", unsafe_allow_html=True)
        fig_bar = px.bar(
            filtered_df.groupby('Situação')['Valor de Mercado Total'].mean().reset_index(),
            x='Situação', y='Valor de Mercado Total', color='Situação',
            labels={'Valor de Mercado Total': 'Valor Médio (M€)'}
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.markdown("<h4>Proporção de Clubes por Situação</h4>", unsafe_allow_html=True)
        fig_pie = px.pie(
            filtered_df, names='Situação',
            title='Distribuição dos Clubes',
            hole=0.5
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("<h4>Valor de Mercado vs. Pontos</h4>", unsafe_allow_html=True)
    fig_scatter = px.scatter(
        filtered_df, x='Pontos', y='Valor de Mercado Total', color='Situação',
        size='Valor de Mercado Total', hover_name='Clube',
        labels={'Valor de Mercado Total': 'Valor de Mercado (M€)'}
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

if __name__ == "__main__":
    main()