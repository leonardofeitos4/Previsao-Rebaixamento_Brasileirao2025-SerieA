import pandas as pd
import numpy as np
import joblib
import os
import streamlit as st

# Função para carregar os dados de entrada do CSV
@st.cache_data
def carregar_dados():
    caminho = os.path.join("dados", "BASE_FINAL.csv")
    return pd.read_csv(caminho)

# Função para carregar o modelo treinado e o scaler (normalizador de dados)
@st.cache_resource
def carregar_modelo():
    """
    Carrega o modelo treinado (Logistic Regression) e o scaler para transformação de dados.
    
    Returns:
        tuple: (modelo treinado, scaler)
    """
    # Caminhos para os arquivos do modelo e do scaler
    modelo_path = os.path.join("modelos", "modelo_logit_status.pkl")
    scaler_path = os.path.join("modelos", "scaler_logit_status.pkl")
    
    # Carrega os arquivos utilizando joblib
    modelo = joblib.load(modelo_path)
    scaler = joblib.load(scaler_path)
    
    return modelo, scaler

# Função para fazer previsões com os dados de entrada
def fazer_previsao(dados_entrada_df):
    # Carrega o modelo e o scaler
    modelo, scaler = carregar_modelo()
    
    # Colunas necessárias para a previsão
    colunas_necessarias = ['Plantel', 'Estrangeiros', 'Valor de Mercado Total']
    
    # Filtra os dados de entrada para manter apenas as colunas necessárias
    dados_filtrados = dados_entrada_df[colunas_necessarias]
    
    # Aplica o scaler para normalizar os dados de entrada
    dados_scaled = scaler.transform(dados_filtrados)
    
    # Faz a previsão e calcula as probabilidades
    previsao = modelo.predict(dados_scaled)
    probabilidade = modelo.predict_proba(dados_scaled)
    
    # Verificação de interpretação do modelo utilizando dois exemplos fictícios
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
    
    # Escala os dados dos clubes fictícios
    rico_scaled = scaler.transform(clube_rico)
    pobre_scaled = scaler.transform(clube_pobre)
    
    # Calcula as probabilidades de rebaixamento para os clubes fictícios
    prob_rico = modelo.predict_proba(rico_scaled)[0]
    prob_pobre = modelo.predict_proba(pobre_scaled)[0]
    
    # Compara a probabilidade de rebaixamento para os clubes e ajusta a previsão
    if prob_rico[1] > prob_pobre[1]:
        return 1 - previsao, np.column_stack((probabilidade[:, 1], probabilidade[:, 0]))
    
    # Retorna a previsão e as probabilidades
    return previsao, probabilidade
