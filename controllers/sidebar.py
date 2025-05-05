import streamlit as st

def streamlit_menu():
    # Criação do menu lateral com opções para navegação
    with st.sidebar:
        selected = st.selectbox(
            "Menu Principal",  # Título do menu
            [
                "Previsão",
                "Dados Históricos",
                "Análise de Sensibilidade",
                "Análise Descritiva"      # ← nova opção
            ],
            format_func=lambda x: f"📊 {x}"  # Adiciona um ícone à frente de cada opção
        )
    return selected  # Retorna a opção selecionada pelo usuário

def sidebar_content():
    # Informações sobre o modelo na barra lateral
    st.sidebar.title("📌 Sobre o Modelo")
    st.sidebar.markdown("""
    **Modelo:** Regressão Logística  # Tipo de modelo utilizado  
    **Features utilizadas:**  # Principais variáveis usadas no modelo  
    - Número de Jogadores no Clube  
    - Número de Estrangeiros no Clube  
    - Valor do Clube no Mercado  

    **Métricas de desempenho:**  # Métricas que avaliam o desempenho do modelo  
    - Acurácia Média: **0.89**  
    - MAE Médio: **0.11**  
    - RMSE Médio: **0.32**  

    **Finalidade:**  # Objetivo do modelo  
    Apoiar análises preditivas sobre risco de rebaixamento com base em características dos clubes.  

    **Limitações:**  # Limitações do modelo  
    O modelo é baseado em dados históricos e pode não capturar fatores externos ou imprevisíveis.
    """)
