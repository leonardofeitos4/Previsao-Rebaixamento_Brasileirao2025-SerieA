import streamlit as st
import pandas as pd
import plotly.express as px
import time
import io
from utils.processamento import fazer_previsao

def main():
   
    st.markdown("""
    <div class="card">
      <h3>📋 Sobre esta ferramenta</h3>
      <div style="padding: 0 10px;">
        Este aplicativo utiliza um modelo de <b>Machine Learning</b> (Regressão Logística) treinado com dados históricos do Brasileirão para prever se um clube será <b>rebaixado</b> ou <b>permanecerá</b> na Série A.<br>
        <b>O modelo considera três fatores principais:</b><br>
        • Tamanho do elenco<br>
        • Jogadores estrangeiros<br>
        • Valor de mercado
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Previsão Lote (Arquivo CSV)
    st.subheader("Previsão em Lote – Arquivo CSV")

    # Botão: Baixar template
    template_df = pd.DataFrame({
        "Plantel": [28, 24],
        "Estrangeiros": [4, 2],
        "Valor de Mercado Total": [85.0, 30.0]
    })
    csv_buffer = io.StringIO()
    template_df.to_csv(csv_buffer, index=False)
    csv_bytes = csv_buffer.getvalue().encode('utf-8')

    st.download_button(
        label="📥 Baixar exemplo de arquivo CSV",
        data=csv_bytes,
        file_name="template_dados_clubes.csv",
        mime="text/csv"
    )

    
    with st.expander("Ver formato de exemplo (clique para abrir)"):
        st.dataframe(template_df, use_container_width=True)
        st.markdown("""
        O arquivo CSV deve conter as colunas exatas:<br>
        <code>Plantel, Estrangeiros, Valor de Mercado Total</code>
        """, unsafe_allow_html=True)

    # Uploader + previsão
    uploaded_file = st.file_uploader(
        "Faça upload de um arquivo CSV para previsão em lote",
        type=["csv"]
    )

    if uploaded_file is not None:
        df_csv = pd.read_csv(uploaded_file)
        st.info("Pré-visualização dos dados enviados:")
        st.dataframe(df_csv.head(), use_container_width=True)

        with st.spinner('Analisando dados do arquivo...'):
            previsoes, probabilidades = fazer_previsao(df_csv)
            df_csv["Probabilidade Rebaixamento (%)"] = [round(p[1]*100,1) for p in probabilidades]
            df_csv["Resultado"] = ["Rebaixado" if p[1] > 0.5 else "Não Rebaixado" for p in probabilidades]
        
        st.success("Resultados das previsões no arquivo:")
        st.dataframe(df_csv, use_container_width=True)

        # Gráfico de barras lote
        if "Probabilidade Rebaixamento (%)" in df_csv.columns and "Resultado" in df_csv.columns:
            fig_batch = px.bar(
                df_csv,
                x=df_csv.index.astype(str),
                y="Probabilidade Rebaixamento (%)",
                color="Resultado",
                title="Probabilidade de Rebaixamento dos Clubes (Arquivo)",
                labels={"x": "Clube na ordem do arquivo"}
            )
            st.plotly_chart(fig_batch, use_container_width=True)

        st.markdown("---")

    # FORMULÁRIO 
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("<h3 class='subheader'>Dados do Clube</h3>", unsafe_allow_html=True)
        with st.form(key="prediction_form"):
            nome_time = st.text_input("Nome do Clube", value="Meu Time")
            plantel = st.slider("Número de Jogadores no Elenco", min_value=15, max_value=50, value=25, 
                              help="A média de jogadores nos clubes da Série A é de aproximadamente 28 atletas")
            estrangeiros = st.slider("Número de Estrangeiros", min_value=0, max_value=15, value=3,
                                  help="A média de estrangeiros nos clubes da Série A é de aproximadamente 4 atletas")
            valor_mercado_total = st.slider("Valor de Mercado (em milhões €)", min_value=5.0, max_value=300.0, value=50.0, step=5.0,
                                         help="A média de valor de mercado dos clubes da Série A é de aproximadamente €85 milhões")
            submit_button = st.form_submit_button(label="Analisar Risco de Rebaixamento")

    with col2:
        st.markdown("<h3 class='subheader'>Resultado da Análise</h3>", unsafe_allow_html=True)
        result_container = st.container()
        if submit_button:
            dados_entrada = {
                'Plantel': [plantel],
                'Estrangeiros': [estrangeiros],
                'Valor de Mercado Total': [valor_mercado_total]
            }
            dados_entrada_df = pd.DataFrame(dados_entrada)
            with st.spinner('Analisando dados...'):
                time.sleep(1)
                previsao, probabilidade = fazer_previsao(dados_entrada_df)
                prob_rebaixamento = probabilidade[0][1]
                resultado = 'Rebaixado' if prob_rebaixamento > 0.5 else 'Não Rebaixado'
                if prob_rebaixamento < 0.3:
                    cor = "green"
                    mensagem = "Baixo risco de rebaixamento"
                    emoji = "✅"
                elif prob_rebaixamento < 0.7:
                    cor = "orange"
                    mensagem = "Risco moderado de rebaixamento"
                    emoji = "⚠️"
                else:
                    cor = "red"
                    mensagem = "Alto risco de rebaixamento"
                    emoji = "🚨"

                with result_container:
                    st.markdown(f"""
                    <div style="background-color:{cor}; padding:20px; border-radius:10px; text-align:center; color:white;">
                        <h2>{nome_time}</h2>
                        <h2>{emoji} {resultado} {emoji}</h2>
                        <h4>{mensagem}</h4>
                        <h1 style="font-size:3rem;">{prob_rebaixamento:.1%}</h1>
                        <p>Probabilidade de Rebaixamento</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    
                    st.markdown('<div style="display: flex; justify-content: center;">', unsafe_allow_html=True)
                    col_pizza = st.columns([1, 2, 1])[1]
                    with col_pizza:
                        fig = px.pie(
                            values=[prob_rebaixamento, 1-prob_rebaixamento],
                            names=['Rebaixamento', 'Permanência'],
                            hole=0.7,
                            color_discrete_sequence=['#FF5A5F', '#3D9970']
                        )
                        fig.update_layout(
                            title="Probabilidades",
                            height=300,
                            width=400,
                            margin=dict(l=20, r=20, t=30, b=0),
                            showlegend=True,
                            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
                        )
                        fig.add_annotation(
                            text=f"{prob_rebaixamento:.1%}",
                            x=0.5, y=0.5,
                            font_size=24,
                            showarrow=False
                        )
                        st.plotly_chart(fig, use_container_width=False)
                    st.markdown('</div>', unsafe_allow_html=True)

                    
                    st.markdown("<br>", unsafe_allow_html=True)

                    # Criando colunas para a tabela e o gráfico radar
                    col_table, col_radar = st.columns(2)
                    comparison_data = {
                        'Clube': ['Seu Clube', 'Média Série A', 'Clube Rebaixado Típico', 'Clube Top-4 Típico'],
                        'Plantel': [plantel, 28, 24, 32],
                        'Estrangeiros': [estrangeiros, 4, 2, 7],
                        'Valor de Mercado (M€)': [valor_mercado_total, 85, 30, 150],
                        'Risco de Rebaixamento': [prob_rebaixamento, 0.5, 0.8, 0.1]
                    }
                    comp_df = pd.DataFrame(comparison_data)
                    with col_table:
                        st.markdown("### Comparação com outros clubes")
                        st.dataframe(comp_df, hide_index=True, use_container_width=True)
                    with col_radar:
                        st.markdown("### Perfil do Clube")
                        fig_radar = px.line_polar(
                            comp_df, r=[plantel/50, estrangeiros/15, valor_mercado_total/300, 1-prob_rebaixamento], 
                            theta=['Tamanho do Elenco', 'Estrangeiros', 'Valor de Mercado', 'Segurança'],
                            line_close=True,
                            range_r=[0, 1]
                        )
                        fig_radar.update_layout(height=300)
                        st.plotly_chart(fig_radar, use_container_width=True)

if __name__ == "__main__":
    main()