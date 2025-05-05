import streamlit as st
import pandas as pd
import os
import plotly.express as px

# Mapeamento de nomes para exibição
COL_MAP = {
    'Plantel': 'Tamanho do Plantel',
    'Estrangeiros': 'Número de Estrangeiros',
    'Valor de Mercado Total': 'Valor de Mercado (R$)',
    'Pontos': 'Pontos Obtidos'
}

def main():
    st.header("📊 Análise Descritiva")

    # Carregar dados
    caminho = os.path.join("dados", "BASE_FINAL.xlsx")
    df = pd.read_excel(caminho)
    df.columns = df.columns.str.strip()

    # Visão geral
    st.subheader("📋 Visão Geral da Base")
    st.dataframe(df, use_container_width=True)

    # Filtro por temporada (exceto 2025)
    todas_temp = sorted(df['Temporada'].unique())
    temporadas = [t for t in todas_temp if t != 2025]
    sel_ano = st.selectbox("Selecione a temporada para análise:", temporadas)
    df_ano = df[df['Temporada'] == sel_ano]

    # Estatísticas descritivas da temporada
    st.subheader(f"📈 Estatísticas Descritivas ({sel_ano})")
    desc = df_ano.describe().T
    desc.index = [COL_MAP.get(i, i) for i in desc.index]
    desc = desc.rename(columns={
        'count': 'Contagem',
        'mean': 'Média',
        'std': 'Desvio Padrão',
        'min': 'Mínimo',
        '25%': '1º Quartil',
        '50%': 'Mediana',
        '75%': '3º Quartil',
        'max': 'Máximo'
    })
    st.dataframe(desc, use_container_width=True, height=400)

    # Tabela de variáveis numéricas por clube
    st.subheader(f"🔢 Variáveis Numéricas por Clube ({sel_ano})")
    num_cols = ['Plantel', 'Estrangeiros', 'Valor de Mercado Total', 'Pontos']
    existentes = [c for c in num_cols if c in df_ano.columns]
    if existentes:
        tabela = df_ano[['Clube'] + existentes].rename(columns=COL_MAP)
        st.dataframe(tabela, use_container_width=True)
    else:
        st.warning("Nenhuma coluna numérica disponível nesta temporada.")

    # Filtro e indicadores para clube específico
    st.subheader(f"📑 Dados e Indicadores por Clube ({sel_ano})")
    clubes = sorted(df['Clube'].unique())
    default_idx = clubes.index('Flamengo') if 'Flamengo' in clubes else 0
    sel_clube = st.selectbox("Selecione o clube:", clubes, index=default_idx)
    df_clube_ano = df_ano[df_ano['Clube'] == sel_clube]

    st.markdown(f"**Clube selecionado:** {sel_clube}")
    st.dataframe(df_clube_ano, use_container_width=True)

    if not df_clube_ano.empty:
        melt1 = df_clube_ano.melt(
            id_vars=['Clube', 'Temporada'],
            value_vars=existentes,
            var_name='Indicador',
            value_name='Valor'
        )
        melt1['Indicador'] = melt1['Indicador'].map(COL_MAP)

        st.subheader(f"📊 Indicadores de {sel_clube} em {sel_ano}")
        fig1 = px.bar(
            melt1, x='Indicador', y='Valor',
            color='Indicador', text='Valor',
            title=f"{sel_clube} — {sel_ano}"
        )
        fig1.update_layout(barmode='stack')
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("Sem dados para este clube na temporada selecionada.")

    # Evolução histórica do clube
    st.subheader(f"📈 Evolução Histórica de {sel_clube}")
    df_hist = df[df['Clube'] == sel_clube]
    if not df_hist.empty:
        melt2 = df_hist.melt(
            id_vars=['Clube', 'Temporada'],
            value_vars=existentes,
            var_name='Indicador',
            value_name='Valor'
        )
        melt2['Indicador'] = melt2['Indicador'].map(COL_MAP)
        fig2 = px.bar(
            melt2, x='Temporada', y='Valor', color='Indicador',
            barmode='group', title=f"Evolução de Indicadores - {sel_clube}"
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Sem histórico disponível para esse clube.")

    # Comparação de pontos ao longo das temporadas
    st.subheader("📊 Comparação de Pontos ao Longo dos Anos")
    default_selecao = [c for c in ['Flamengo', 'Vasco'] if c in clubes]
    sel_clubes = st.multiselect(
        "Escolha clubes para comparar:",
        clubes,
        default=default_selecao
    )
    if sel_clubes:
        df_comp = df[df['Clube'].isin(sel_clubes)]
        fig3 = px.line(
            df_comp, x='Temporada', y='Pontos',
            color='Clube', markers=True,
            title="Pontos por Temporada",
            text='Pontos'
        )
        fig3.update_traces(textposition="top center")
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.warning("Selecione ao menos um clube para comparação.")

# Execução da aplicação
if __name__ == "__main__":
    main()
