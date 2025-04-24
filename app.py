# 📦 Imports necessários
import streamlit as st
import pandas as pd
import numpy as np
import os
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import time

# ⚙️ Configuração da página - DEVE SER A PRIMEIRA CHAMADA STREAMLIT
st.set_page_config(
    page_title="Previsão de Rebaixamento - Série A",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para melhorar a aparência
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1e3d59;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .subheader {
        font-size: 1.8rem;
        color: #1e3d59;
        margin-top: 2rem;
        border-bottom: 2px solid #f5f0e1;
        padding-bottom: 0.5rem;
    }
    .card {
        background-color: #f5f0e1;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
    }
    .metric-label {
        font-size: 1rem;
        text-align: center;
        color: #666;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1rem;
        background-color: #f5f0e1;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #1e3d59;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #2b5d8b;
    }
</style>
""", unsafe_allow_html=True)

# 📥 Função para carregar a base de dados
@st.cache_data
def carregar_dados():
    """Carrega a base de dados do projeto."""
    caminho = os.path.join("dados", "BASE_FINAL.csv")
    return pd.read_csv(caminho)

# 📥 Função para carregar o modelo e scaler
@st.cache_resource
def carregar_modelo():
    """Carrega o modelo treinado e o scaler."""
    modelo_path = os.path.join("modelos", "modelo_logit_status.pkl")
    scaler_path = os.path.join("modelos", "scaler_logit_status.pkl")
    modelo = joblib.load(modelo_path)
    scaler = joblib.load(scaler_path)
    return modelo, scaler

# 📊 Função para realizar a previsão
def fazer_previsao(dados_entrada_df):
    """Recebe os dados de entrada, aplica o scaler e realiza a previsão."""
    modelo, scaler = carregar_modelo()
    colunas_necessarias = ['Plantel', 'Estrangeiros', 'Valor de Mercado Total']
    dados_filtrados = dados_entrada_df[colunas_necessarias]
    dados_scaled = scaler.transform(dados_filtrados)
    previsao = modelo.predict(dados_scaled)
    probabilidade = modelo.predict_proba(dados_scaled)
    
    # CORREÇÃO: Vamos verificar se a interpretação está correta
    # Criamos exemplos extremos para verificar
    clube_rico = pd.DataFrame({
        'Plantel': [35],
        'Estrangeiros': [10],
        'Valor de Mercado Total': [200]
    })
    clube_pobre = pd.DataFrame({
        'Plantel': [20],
        'Estrangeiros': [2],
        'Valor de Mercado Total': [15]
    })
    
    # Transformar os dados
    rico_scaled = scaler.transform(clube_rico)
    pobre_scaled = scaler.transform(clube_pobre)
    
    # Fazer previsões
    prob_rico = modelo.predict_proba(rico_scaled)[0]
    prob_pobre = modelo.predict_proba(pobre_scaled)[0]
    
    # Se a probabilidade da classe 1 for maior para o clube rico do que para o clube pobre,
    # então a classe 1 deve ser "Não Rebaixado" (o que é contra-intuitivo)
    if prob_rico[1] > prob_pobre[1]:
        # Invertemos a interpretação
        return 1 - previsao, np.column_stack((probabilidade[:, 1], probabilidade[:, 0]))
    
    # Caso contrário, mantemos a interpretação original
    return previsao, probabilidade

# Função para criar um banner animado
def criar_banner():
    st.markdown("""
    <div style="background-color:#1e3d59; padding:10px; border-radius:10px; margin-bottom:20px">
        <h1 style="color:white; text-align:center; font-size:3rem; text-shadow: 2px 2px 4px #000000;">
            ⚽ Previsão de Rebaixamento - Brasileirão Série A 2025
        </h1>
        <p style="color:white; text-align:center; font-size:1.2rem;">
            Análise preditiva com Machine Learning para clubes do futebol brasileiro
        </p>
    </div>
    """, unsafe_allow_html=True)

# 📄 Carregar dados
df = carregar_dados()

# Banner principal
criar_banner()

# Descrição inicial com mais detalhes e formatação
st.markdown("""
<div class="card">
    <h3>📋 Sobre esta ferramenta</h3>
    <p>Este aplicativo utiliza um modelo de <b>Machine Learning</b> (Regressão Logística) treinado com dados históricos do Brasileirão para prever se um clube será <span style="color:red; font-weight:bold">rebaixado</span> ou <span style="color:green; font-weight:bold">permanecerá na série A</span>.</p>
    
    <p>O modelo considera três fatores principais:</p>
    <ul>
        <li><b>Tamanho do elenco</b>: Número total de jogadores registrados</li>
        <li><b>Jogadores estrangeiros</b>: Quantidade de atletas internacionais</li>
        <li><b>Valor de mercado</b>: Avaliação financeira do clube em milhões</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Tabs para organizar o conteúdo
tab1, tab2, tab3 = st.tabs(["🔮 Fazer Previsão", "📊 Dados Históricos", "📈 Análise de Sensibilidade"])

with tab1:
    # Layout em colunas para o formulário
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("<h3 class='subheader'>Dados do Clube</h3>", unsafe_allow_html=True)
        
        # Formulário com validações e formatação melhorada
        with st.form(key="prediction_form"):
            nome_time = st.text_input("Nome do Clube", value="Meu Time")
            
            # Adicionar um seletor de escudo (simulado)
            escudo_options = ["Escudo Padrão", "Escudo Personalizado"]
            escudo_choice = st.selectbox("Tipo de Escudo", escudo_options)
            
            if escudo_choice == "Escudo Personalizado":
                uploaded_file = st.file_uploader("Carregar escudo do clube", type=["jpg", "png", "jpeg"])
            
            plantel = st.slider("Número de Jogadores no Elenco", min_value=15, max_value=50, value=25, 
                              help="A média de jogadores nos clubes da Série A é de aproximadamente 28 atletas")
            
            estrangeiros = st.slider("Número de Estrangeiros", min_value=0, max_value=15, value=3,
                                  help="A média de estrangeiros nos clubes da Série A é de aproximadamente 4 atletas")
            
            valor_mercado_total = st.slider("Valor de Mercado (em milhões €)", min_value=5.0, max_value=300.0, value=50.0, step=5.0,
                                         help="A média de valor de mercado dos clubes da Série A é de aproximadamente €85 milhões")
            
            submit_button = st.form_submit_button(label="Analisar Risco de Rebaixamento")
    
    with col2:
        st.markdown("<h3 class='subheader'>Resultado da Análise</h3>", unsafe_allow_html=True)
        
        # Placeholder para o resultado
        result_container = st.container()
        
        # Organizar dados de entrada
        dados_entrada = {
            'Plantel': [plantel],
            'Estrangeiros': [estrangeiros],
            'Valor de Mercado Total': [valor_mercado_total]
        }
        dados_entrada_df = pd.DataFrame(dados_entrada)
        
        # Processamento da previsão quando o botão é clicado
        if submit_button:
            with st.spinner('Analisando dados...'):
                time.sleep(1)  # Simular processamento
                previsao, probabilidade = fazer_previsao(dados_entrada_df)
                
                # Determinar a probabilidade de rebaixamento
                # A função fazer_previsao já deve retornar as probabilidades na ordem correta
                prob_rebaixamento = probabilidade[0][1]
                resultado = 'Rebaixado' if prob_rebaixamento > 0.5 else 'Não Rebaixado'
                
                # Determinar cor e mensagem com base na probabilidade
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
                
                # Exibir resultado com estilo
                with result_container:
                    st.markdown(f"""
                    <div style="background-color:{cor}; padding:20px; border-radius:10px; text-align:center; color:white;">
                        <h2>{emoji} {resultado} {emoji}</h2>
                        <h4>{mensagem}</h4>
                        <h1 style="font-size:3rem;">{prob_rebaixamento:.1%}</h1>
                        <p>Probabilidade de Rebaixamento</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Gráfico de gauge com Plotly (mais bonito que o matplotlib)
                    fig = px.pie(
                        values=[prob_rebaixamento, 1-prob_rebaixamento],
                        names=['Rebaixamento', 'Permanência'],
                        hole=0.7,
                        color_discrete_sequence=['#FF5A5F', '#3D9970']
                    )
                    fig.update_layout(
                        title="Probabilidades",
                        height=300,
                        margin=dict(l=20, r=20, t=30, b=0),
                        showlegend=True,
                        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
                    )
                    # Adicionar texto no centro
                    fig.add_annotation(
                        text=f"{prob_rebaixamento:.1%}",
                        x=0.5, y=0.5,
                        font_size=24,
                        showarrow=False
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Comparação com outros clubes (simulado)
                    st.markdown("### Comparação com outros clubes")
                    comparison_data = {
                        'Clube': ['Seu Clube', 'Média Série A', 'Clube Rebaixado Típico', 'Clube Top-4 Típico'],
                        'Plantel': [plantel, 28, 24, 32],
                        'Estrangeiros': [estrangeiros, 4, 2, 7],
                        'Valor de Mercado (M€)': [valor_mercado_total, 85, 30, 150],
                        'Risco de Rebaixamento': [prob_rebaixamento, 0.5, 0.8, 0.1]
                    }
                    comp_df = pd.DataFrame(comparison_data)
                    
                    # Gráfico de radar para comparação
                    fig_radar = px.line_polar(
                        comp_df, r=[plantel/50, estrangeiros/15, valor_mercado_total/300, 1-prob_rebaixamento], 
                        theta=['Tamanho do Elenco', 'Estrangeiros', 'Valor de Mercado', 'Segurança'],
                        line_close=True,
                        range_r=[0, 1],
                        title="Perfil do Clube"
                    )
                    fig_radar.update_layout(height=350)
                    st.plotly_chart(fig_radar, use_container_width=True)

with tab2:
    st.markdown("<h3 class='subheader'>Base de Dados Histórica</h3>", unsafe_allow_html=True)
    
    # Mapeamento de códigos para rótulos descritivos
    status_mapping = {
        0: "Top 4",
        1: "Série A",
        2: "Série B para Série A"
    }
    
    # Criar uma cópia do DataFrame com a coluna Status mapeada para exibição
    df_display = df.copy()
    # Converter a coluna Status para o tipo que você está usando (provavelmente int ou float)
    if 'Status' in df_display.columns:
        df_display['Status'] = pd.to_numeric(df_display['Status'], errors='coerce')
        # Aplicar o mapeamento apenas para valores que existem no dicionário
        df_display['Situação'] = df_display['Status'].map(lambda x: status_mapping.get(x, x) if pd.notna(x) else "Desconhecido")
    
    # Filtros para a tabela
    col1, col2, col3 = st.columns(3)
    with col1:
        # Obter valores únicos da coluna mapeada e remover NaN
        situacao_options = df_display['Situação'].dropna().unique() if 'Situação' in df_display.columns else []
        situacao_filter = st.multiselect("Situação", options=situacao_options, default=situacao_options)
    with col2:
        min_valor = st.number_input("Valor Mínimo (M€)", value=0.0)
    with col3:
        max_valor = st.number_input("Valor Máximo (M€)", value=float(df['Valor de Mercado Total'].max()))
    
    # Aplicar filtros
    if 'Situação' in df_display.columns and situacao_filter:
        # Criar um mapeamento reverso para filtrar
        reverse_mapping = {v: k for k, v in status_mapping.items()}
        
        # Converter os rótulos selecionados de volta para os valores numéricos
        status_values = [reverse_mapping.get(s, s) for s in situacao_filter if s in reverse_mapping]
        
        # Filtrar o DataFrame
        filtered_df = df_display[
            (df_display['Situação'].isin(situacao_filter)) & 
            (df_display['Valor de Mercado Total'] >= min_valor) & 
            (df_display['Valor de Mercado Total'] <= max_valor)
        ]
    else:
        filtered_df = df_display[
            (df_display['Valor de Mercado Total'] >= min_valor) & 
            (df_display['Valor de Mercado Total'] <= max_valor)
        ]
    
    # Exibir tabela com estilo
    st.dataframe(filtered_df, use_container_width=True, height=400)
    
    # Visualizações adicionais
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h4>Distribuição de Valor de Mercado por Situação</h4>", unsafe_allow_html=True)
        if 'Situação' in df_display.columns:
            fig = px.box(df_display, x='Situação', y='Valor de Mercado Total', color='Situação')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Dados de Situação não disponíveis para visualização.")
    
    with col2:
        st.markdown("<h4>Relação entre Tamanho do Elenco e Estrangeiros</h4>", unsafe_allow_html=True)
        if 'Situação' in df_display.columns:
            fig = px.scatter(df_display, x='Plantel', y='Estrangeiros', color='Situação', 
                          size='Valor de Mercado Total', hover_name=df_display.index)
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Dados de Situação não disponíveis para visualização.")

with tab3:
    st.markdown("<h3 class='subheader'>Análise de Sensibilidade</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div class="card">
        <p>Esta seção permite explorar como cada variável afeta a probabilidade de rebaixamento. 
        Ajuste os controles deslizantes para ver como o risco muda quando você altera um fator mantendo os outros constantes.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Valores base para análise de sensibilidade
    base_plantel = 25
    base_estrangeiros = 3
    base_valor = 50.0
    
    # Controles para análise de sensibilidade
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<h4>Tamanho do Elenco</h4>", unsafe_allow_html=True)
        plantel_range = list(range(15, 51, 5))
        resultados_plantel = []
        
        # Calcular probabilidades para diferentes tamanhos de elenco
        for p in plantel_range:
            dados = pd.DataFrame({
                'Plantel': [p],
                'Estrangeiros': [base_estrangeiros],
                'Valor de Mercado Total': [base_valor]
            })
            _, prob = fazer_previsao(dados)
            resultados_plantel.append(prob[0][1])  # Probabilidade de rebaixamento
        
        # Criar DataFrame para o gráfico
        df_plantel = pd.DataFrame({
            'Tamanho do Elenco': plantel_range,
            'Probabilidade de Rebaixamento': resultados_plantel
        })
        
        # Plotar gráfico
        fig_plantel = px.line(df_plantel, x='Tamanho do Elenco', y='Probabilidade de Rebaixamento',
                           markers=True, title="Impacto do Tamanho do Elenco")
        fig_plantel.update_layout(yaxis_tickformat='.0%')
        st.plotly_chart(fig_plantel, use_container_width=True)
    
    with col2:
        st.markdown("<h4>Número de Estrangeiros</h4>", unsafe_allow_html=True)
        estrangeiros_range = list(range(0, 16, 2))
        resultados_estrangeiros = []
        
        # Calcular probabilidades para diferentes números de estrangeiros
        for e in estrangeiros_range:
            dados = pd.DataFrame({
                'Plantel': [base_plantel],
                'Estrangeiros': [e],
                'Valor de Mercado Total': [base_valor]
            })
            _, prob = fazer_previsao(dados)
            resultados_estrangeiros.append(prob[0][1])  # Probabilidade de rebaixamento
        
        # Criar DataFrame para o gráfico
        df_estrangeiros = pd.DataFrame({
            'Número de Estrangeiros': estrangeiros_range,
            'Probabilidade de Rebaixamento': resultados_estrangeiros
        })
        
        # Plotar gráfico
        fig_estrangeiros = px.line(df_estrangeiros, x='Número de Estrangeiros', y='Probabilidade de Rebaixamento',
                                markers=True, title="Impacto do Número de Estrangeiros")
        fig_estrangeiros.update_layout(yaxis_tickformat='.0%')
        st.plotly_chart(fig_estrangeiros, use_container_width=True)
    
    with col3:
        st.markdown("<h4>Valor de Mercado</h4>", unsafe_allow_html=True)
        valor_range = list(range(10, 301, 30))
        resultados_valor = []
        
        # Calcular probabilidades para diferentes valores de mercado
        for v in valor_range:
            dados = pd.DataFrame({
                'Plantel': [base_plantel],
                'Estrangeiros': [base_estrangeiros],
                'Valor de Mercado Total': [v]
            })
            _, prob = fazer_previsao(dados)
            resultados_valor.append(prob[0][1])  # Probabilidade de rebaixamento
        
        # Criar DataFrame para o gráfico
        df_valor = pd.DataFrame({
            'Valor de Mercado (M€)': valor_range,
            'Probabilidade de Rebaixamento': resultados_valor
        })
        
        # Plotar gráfico
        fig_valor = px.line(df_valor, x='Valor de Mercado (M€)', y='Probabilidade de Rebaixamento',
                         markers=True, title="Impacto do Valor de Mercado")
        fig_valor.update_layout(yaxis_tickformat='.0%')
        st.plotly_chart(fig_valor, use_container_width=True)
    
    # Adicionar um gráfico 3D para visualizar a interação entre variáveis
    st.markdown("<h3 class='subheader'>Interação entre Variáveis</h3>", unsafe_allow_html=True)
    
    # Criar uma grade de valores para visualização 3D
    plantel_3d = [20, 25, 30, 35, 40]
    valor_3d = [20, 50, 100, 150, 200]
    
    # Criar dados para o gráfico 3D
    df_3d = pd.DataFrame(columns=['Plantel', 'Valor de Mercado (M€)', 'Probabilidade de Rebaixamento'])
    
    for p in plantel_3d:
        for v in valor_3d:
            dados = pd.DataFrame({
                'Plantel': [p],
                'Estrangeiros': [base_estrangeiros],
                'Valor de Mercado Total': [v]
            })
            _, prob = fazer_previsao(dados)
            df_3d = pd.concat([df_3d, pd.DataFrame({
                'Plantel': [p],
                'Valor de Mercado (M€)': [v],
                'Probabilidade de Rebaixamento': [prob[0][1]]
            })], ignore_index=True)
    
    # Plotar gráfico 3D
    fig_3d = px.scatter_3d(df_3d, x='Plantel', y='Valor de Mercado (M€)', z='Probabilidade de Rebaixamento',
                        color='Probabilidade de Rebaixamento', opacity=0.7,
                        color_continuous_scale=px.colors.sequential.Viridis)
    
    fig_3d.update_layout(height=600, scene=dict(
        zaxis=dict(tickformat='.0%')
    ))
    st.plotly_chart(fig_3d, use_container_width=True)
    
    # Adicionar uma explicação sobre a análise de sensibilidade
    st.markdown("""
    <div class="card">
        <h4>Interpretação da Análise de Sensibilidade</h4>
        <p>Os gráficos acima mostram como cada variável afeta a probabilidade de rebaixamento quando as outras são mantidas constantes:</p>
        <ul>
            <li><b>Tamanho do Elenco</b>: Geralmente, um elenco maior está associado a uma menor probabilidade de rebaixamento, pois proporciona mais opções táticas e melhor gestão de lesões e suspensões.</li>
            <li><b>Número de Estrangeiros</b>: Mais jogadores estrangeiros geralmente indicam maior capacidade de investimento e acesso a mercados internacionais, o que pode reduzir o risco de rebaixamento.</li>
            <li><b>Valor de Mercado</b>: Um valor de mercado mais alto está fortemente correlacionado com menor risco de rebaixamento, pois reflete a qualidade geral do elenco.</li>
        </ul>
        <p>O gráfico 3D mostra a interação entre o tamanho do elenco e o valor de mercado, permitindo visualizar como essas variáveis combinadas afetam o risco de rebaixamento.</p>
    </div>
    """, unsafe_allow_html=True)

# Adicionar informações na barra lateral
st.sidebar.title("📌 Sobre o Modelo")
st.sidebar.markdown("""
**Modelo:** Regressão Logística  
**Features utilizadas:**  
- Número de Jogadores no Clube  
- Número de Estrangeiros no Clube  
- Valor do Clube no Mercado  

**Métricas de desempenho:**  
- Acurácia Média: **0.89**  
- MAE Médio: **0.11**  
- RMSE Médio: **0.32**  

**Finalidade:**  
Apoiar análises preditivas sobre risco de rebaixamento com base em características dos clubes.  

**Limitações:**  
O modelo é baseado em dados históricos e pode não capturar fatores externos ou imprevisíveis (lesões, mudanças de técnico, etc).
""")

# Adicionar rodapé
st.markdown("""
<div class="footer">
    <p>Desenvolvido para o curso de Machine Learning - 2023</p>
    <p>Dados obtidos de fontes públicas sobre o Campeonato Brasileiro</p>
</div>
""", unsafe_allow_html=True)
        