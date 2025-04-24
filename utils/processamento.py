import pandas as pd
import numpy as np  # Adicione esta linha
import joblib
import os
import streamlit as st

@st.cache_data
def carregar_dados():
  
    caminho = os.path.join("dados", "BASE_FINAL.csv")
    return pd.read_csv(caminho)

@st.cache_resource
def carregar_modelo():
    """
    Carrega o modelo treinado e o scaler.
    
    Returns:
        tuple: (modelo treinado, scaler)
    """
    modelo_path = os.path.join("modelos", "modelo_logit_status.pkl")
    scaler_path = os.path.join("modelos", "scaler_logit_status.pkl")
    modelo = joblib.load(modelo_path)
    scaler = joblib.load(scaler_path)
    return modelo, scaler

def fazer_previsao(dados_entrada_df):
  
    modelo, scaler = carregar_modelo()
    colunas_necessarias = ['Plantel', 'Estrangeiros', 'Valor de Mercado Total']
    dados_filtrados = dados_entrada_df[colunas_necessarias]
    dados_scaled = scaler.transform(dados_filtrados)
    previsao = modelo.predict(dados_scaled)
    probabilidade = modelo.predict_proba(dados_scaled)
    
    # Verificação da interpretação do modelo
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
    
    rico_scaled = scaler.transform(clube_rico)
    pobre_scaled = scaler.transform(clube_pobre)
    
    prob_rico = modelo.predict_proba(rico_scaled)[0]
    prob_pobre = modelo.predict_proba(pobre_scaled)[0]
    
    if prob_rico[1] > prob_pobre[1]:
        return 1 - previsao, np.column_stack((probabilidade[:, 1], probabilidade[:, 0]))
    
    return previsao, probabilidade