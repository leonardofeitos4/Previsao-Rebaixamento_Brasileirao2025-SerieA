import streamlit as st
import pandas as pd
import plotly.express as px
from utils.processamento import carregar_dados

def main():
    # Título da página
    st.markdown("<h3 class='subheader'>Base de Dados Histórica</h3>", unsafe_allow_html=True)
    
    # Carregar os dados históricos
    df = carregar_dados()
    df_display = df.copy()

    # Padroniza a coluna de 'Situação' caso exista
    if 'Situacao' in df_display.columns:
        df_display['Situacao'] = df_display['Situacao'].replace({
            'Top4': 'Top 4',
            'SerieA': 'Série A',
            'SérieA': 'Série A',
            'Serie B para Série A': 'Série B para Série A',
            'SerieB_Para_SerieA': 'Série B para Série A',
            'Rebaixado': 'Rebaixado'
        })
        df_display['Situação'] = df_display['Situacao']
    elif 'Status' in df_display.columns:
        # Mapeamento dos valores de 'Status' para as categorias de situação
        status_mapping = {0: "Top 4", 1: "Série A", 2: "Série B para Série A", 3: "Rebaixado"}
        df_display['Status'] = pd.to_numeric(df_display['Status'], errors='coerce')
        df_display['Situação'] = df_display['Status'].map(lambda x: status_mapping.get(x, x) if pd.notna(x) else "Desconhecido")
    else:
        # Caso não exista nenhuma coluna 'Situacao' ou 'Status', define como "Desconhecido"
        df_display['Situação'] = "Desconhecido"

    # --- Filtros inteligentes ---
    col1, col2, col3, col4 = st.columns(4)
    
    # Filtro de situação
    with col1:
        situacao_options = sorted(df_display['Situação'].dropna().unique())
        situacao_filter = st.multiselect("Situação", options=situacao_options, default=situacao_options)
    
    # Filtro de clubes
    with col2:
        clubes_options = sorted(df_display['Clube'].dropna().unique())
        clube_filter = st.multiselect("Clube", options=["Todos"] + clubes_options, default=["Todos"])
    
    # Filtro de valor mínimo
    with col3:
        min_valor = st.number_input("Valor Mínimo (M€)", value=0.0)
    
    # Filtro de valor máximo
    with col4:
        max_valor = st.number_input("Valor Máximo (M€)", value=float(df_display['Valor de Mercado Total'].max()))

    # --- Lógica para pegar todos os dados se nada ou "Todos" for selecionado ---
    if not situacao_filter:
        situacao_filtrada = situacao_options  
    else:
        situacao_filtrada = situacao_filter

    # Filtro para clubes selecionados
    if (not clube_filter) or ("Todos" in clube_filter):
        clubes_filtrados = clubes_options
    else:
        clubes_filtrados = clube_filter

    # Aplica os filtros selecionados nos dados
    filtered_df = df_display[
        (df_display['Situação'].isin(situacao_filtrada)) &
        (df_display['Clube'].isin(clubes_filtrados)) &
        (df_display['Valor de Mercado Total'] >= min_valor) &
        (df_display['Valor de Mercado Total'] <= max_valor)
    ]

    # Exibe a tabela filtrada com os dados
    st.dataframe(filtered_df, use_container_width=True, height=400)

    # --- Visualizações ---
    col1, col2 = st.columns(2)

    # Gráfico de barras: Média de Valor de Mercado por Situação
    with col1:
        st.markdown("<h4>Média de Valor de Mercado por Situação</h4>", unsafe_allow_html=True)
        if not filtered_df.empty:
            fig_bar = px.bar(
                filtered_df.groupby('Situação')['Valor de Mercado Total'].mean().reset_index(),
                x='Situação', y='Valor de Mercado Total', color='Situação',
                labels={'Valor de Mercado Total': 'Valor Médio (M€)'}
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Nenhum dado para exibir o gráfico.")

    # Gráfico de pizza: Proporção de Clubes por Situação
    with col2:
        st.markdown("<h4>Proporção de Clubes por Situação</h4>", unsafe_allow_html=True)
        if not filtered_df.empty:
            fig_pie = px.pie(
                filtered_df, names='Situação',
                title='Distribuição dos Clubes',
                hole=0.5
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("Nenhum dado para exibir o gráfico.")

    # Gráfico de dispersão: Valor de Mercado vs. Pontos
    st.markdown("<h4>Valor de Mercado vs. Pontos</h4>", unsafe_allow_html=True)
    if not filtered_df.empty:
        fig_scatter = px.scatter(
            filtered_df, x='Pontos', y='Valor de Mercado Total', color='Situação',
            size='Valor de Mercado Total', hover_name='Clube',
            labels={'Valor de Mercado Total': 'Valor de Mercado (M€)'}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.info("Nenhum dado para exibir o gráfico.")

# Executa o aplicativo Streamlit
if __name__ == "__main__":
    main()
