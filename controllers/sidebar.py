import streamlit as st

def streamlit_menu():
    with st.sidebar:
        selected = st.selectbox(
            "Menu Principal",
            ["Previsão", "Dados Históricos", "Análise de Sensibilidade"],
            format_func=lambda x: f"📊 {x}"
        )
    return selected

def sidebar_content():
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
    O modelo é baseado em dados históricos e pode não capturar fatores externos ou imprevisíveis.
    """)