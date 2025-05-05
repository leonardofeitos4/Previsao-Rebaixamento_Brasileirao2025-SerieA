import streamlit as st
import pandas as pd
import os
import plotly.express as px

def main():
    # Título da página
    st.header("📊 Análise Descritiva")

    # Carregando a base completa
    caminho = os.path.join("dados", "BASE_FINAL.csv")
    df = pd.read_csv(caminho)
    df.columns = df.columns.str.strip()

    # 1) Visão Geral da Base
    st.subheader("📋 Visão Geral da Base Completa")
    st.dataframe(df, use_container_width=True)

    # 2) Estatísticas Descritivas por temporada
    temporadas = sorted(df['Temporada'].unique())
    ano = st.selectbox("Selecione a temporada:", temporadas)
    df_ano = df[df['Temporada'] == ano]

    st.subheader(f"📈 Estatísticas Descritivas ({ano})")
    desc = df_ano.describe().T
    st.dataframe(desc, use_container_width=True, height=400)

    # 3) Tabela de Variáveis Numéricas
    st.subheader(f"🔢 Variáveis Numéricas ({ano})")
    num_cols = ['Plantel', 'Estrangeiros', 'Valor de Mercado Total', 'Pontos']
    existentes = [c for c in num_cols if c in df_ano.columns]
    if existentes:
        st.dataframe(df_ano[existentes], use_container_width=True)
    else:
        st.warning("Nenhuma coluna numérica disponível nesta temporada.")

    # 4) Dados do clube para comparação única
    st.subheader(f"📑 Dados do Clube em {ano}")
    clubes = sorted(df['Clube'].unique())
    clube = st.selectbox("Selecione o clube:", clubes)
    df_clube_ano = df_ano[df_ano['Clube'] == clube]
    st.dataframe(df_clube_ano, use_container_width=True)

    # Gráfico de indicadores (única temporada)
    st.subheader(f"📊 Indicadores do {clube} em {ano}")
    if not df_clube_ano.empty:
        melt1 = df_clube_ano.melt(
            id_vars=['Clube','Temporada'],
            value_vars=existentes,
            var_name='Indicador',
            value_name='Valor'
        )
        fig1 = px.bar(
            melt1,
            x='Indicador', y='Valor',
            color='Indicador',
            text='Valor',
            title=f"{clube} — {ano}"
        )
        fig1.update_layout(barmode='stack')
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("Sem dados para este clube/ano.")

    # 5) Evolução histórica do clube
    st.subheader(f"📈 Evolução de Indicadores do {clube} (Histórico)")
    df_clube_all = df[df['Clube'] == clube]
    if not df_clube_all.empty:
        melt2 = df_clube_all.melt(
            id_vars=['Clube','Temporada'],
            value_vars=existentes,
            var_name='Indicador',
            value_name='Valor'
        )
        fig2 = px.bar(
            melt2,
            x='Temporada', y='Valor',
            color='Indicador',
            barmode='group',
            title=f"Evolução de {clube}"
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Sem histórico para esse clube.")
