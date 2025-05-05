# paginas/analise_descritiva.py

import streamlit as st
from pathlib import Path
import pandas as pd
import plotly.express as px

# Define a raiz do projeto a partir deste arquivo
ROOT = Path(__file__).resolve().parent.parent

@st.cache_data

def carregar_historico():
    dados_dir = ROOT / "dados"
    csv_paths = list(dados_dir.rglob("*.csv"))
    if not csv_paths:
        st.error(f"Nenhum arquivo .csv encontrado em {dados_dir}")
        return pd.DataFrame()
    csv_path = csv_paths[0]
    rel = csv_path.relative_to(ROOT)
    st.sidebar.markdown(f"**Carregando:** `{rel}`")
    return pd.read_csv(csv_path)

def main():
    st.header("📈 Análise Descritiva da Série A")
    df = carregar_historico()
    if df.empty:
        st.stop()

    # === Filtro de Temporada (exclui 2025) ===
    if "Temporada" in df.columns:
        temporadas = sorted([s for s in df["Temporada"].unique() if s != 2025])
        temporada_sel = st.selectbox("Selecione a Temporada", temporadas, index=len(temporadas)-1)
        df_ano = df[df["Temporada"] == temporada_sel]
    else:
        temporada_sel = None
        df_ano = df.copy()

    # 1. Visão geral da base
    st.markdown(f"### 1. Visão Geral - Temporada {temporada_sel}")
    st.markdown(
        f"- **Total de clubes nesta temporada:** {df_ano['Clube'].nunique()}  \
- **Total de registros (linhas):** {df_ano.shape[0]}"
    )
    st.dataframe(df_ano, use_container_width=True)

    # 2. Estatísticas descritivas por variável
    st.markdown(f"### 2. Estatísticas Descritivas por Variável - Temporada {temporada_sel}")
    st.write("Métricas (média, mediana, desvio padrão, mínimo e máximo) para as variáveis numéricas nesta temporada.")
    stats = df_ano.describe().T.rename(columns={
        'mean': 'Média', '50%': 'Mediana',
        'std': 'Desvio Padrão', 'min': 'Mínimo', 'max': 'Máximo'
    })
    stats = stats[['Média', 'Mediana', 'Desvio Padrão', 'Mínimo', 'Máximo']]
    st.dataframe(stats, use_container_width=True)

    # 3. Distribuição Histórica por Clube (Colunas Empilhadas)
    st.markdown("### 3. Distribuição Histórica por Clube (Colunas Empilhadas)")
    clubes = sorted(df['Clube'].unique())
    clube_sel = st.selectbox("Selecione um Clube", clubes)

    df_clube_todas = df[df['Clube'] == clube_sel]
    if 'Temporada' not in df_clube_todas.columns:
        st.error("Coluna 'Temporada' não encontrada para distribuição histórica.")
    else:
        possiveis = ['Plantel', 'Estrangeiros', 'Valor de Mercado Total', 'Pontos']
        metrics = [c for c in possiveis if c in df_clube_todas.columns]
        if not metrics:
            st.warning("Nenhuma métrica numérica padrão encontrada para empilhar.")
        else:
            df_stack = df_clube_todas[['Temporada'] + metrics].set_index('Temporada')
            fig_stack = px.bar(
                df_stack,
                x=df_stack.index,
                y=metrics,
                title=f"Métricas Empilhadas por Temporada - {clube_sel}",
                labels={'value': 'Valor', 'Temporada': 'Ano', 'variable': 'Métrica'},
                text_auto=True
            )
            fig_stack.update_traces(textposition='inside')
            fig_stack.update_layout(barmode='stack', xaxis_title='Temporada', yaxis_title='Total')
            st.plotly_chart(fig_stack, use_container_width=True)

    # 4. Evolução de pontos por clube (todas as temporadas)
    st.markdown("### 4. Evolução de Pontos por Clube ao Longo das Temporadas")
    if all(col in df.columns for col in ['Clube', 'Temporada', 'Pontos']):
        lista_clubes = sorted(df['Clube'].unique().tolist())
        selecionados = st.multiselect(
            "Selecione até 5 clubes para comparar", lista_clubes, default=lista_clubes[:5], max_selections=5
        )
        if selecionados:
            df_f = df[df['Clube'].isin(selecionados)]
            fig2 = px.line(
                df_f, x='Temporada', y='Pontos', color='Clube',
                title='Pontos por Temporada para Clubes Selecionados'
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Selecione ao menos um clube para o gráfico.")
    else:
        st.warning("Colunas (Clube, Temporada, Pontos) não encontradas.")

    # Observações finais
    st.markdown("---")
    st.markdown("#### Observações e Próximos Passos")
    st.write(
        """
        - Filtro exclui 2025; escolha a temporada desejada.
        - Seção 3 exibe colunas empilhadas com rótulos de dados.
        - Seção 4 permite comparação de pontos entre clubes.
        """
    )

if __name__ == "__main__":
    main()
