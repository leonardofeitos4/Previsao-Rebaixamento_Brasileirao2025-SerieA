import os
import joblib
import pandas as pd
import numpy as np            # ← Não esqueça dessa linha!
import streamlit as st

@st.cache_data
def carregar_dados():
    caminho = os.path.join("dados", "BASE_FINAL.csv")
    return pd.read_csv(caminho)

@st.cache_resource
def carregar_modelo():
    modelo_path = os.path.join("modelos", "modelo_logit_status.pkl")
    scaler_path = os.path.join("modelos", "scaler_logit_status.pkl")
    modelo = joblib.load(modelo_path)
    scaler = joblib.load(scaler_path)
    return modelo, scaler

def fazer_previsao(dados_entrada_df):
    modelo, scaler = carregar_modelo()
    colunas = ['Plantel','Estrangeiros','Valor de Mercado Total']
    X = dados_entrada_df[colunas]
    Xs = scaler.transform(X)
    preds = modelo.predict(Xs)
    probs = modelo.predict_proba(Xs)

    # teste de interpretação
    clube_rico = pd.DataFrame({'Plantel':[35], 'Estrangeiros':[10], 'Valor de Mercado Total':[200]})
    clube_pobre = pd.DataFrame({'Plantel':[20], 'Estrangeiros':[2],  'Valor de Mercado Total':[15]})
    pr = modelo.predict_proba(scaler.transform(clube_rico))[0][1]
    pp = modelo.predict_proba(scaler.transform(clube_pobre))[0][1]

    if pr > pp:
        # inverte a interpretação (classe 1 vira "rebaixado")
        preds = 1 - preds
        # troca a coluna de probabilidades
        probs = np.column_stack((probs[:, 1], probs[:, 0]))

    return preds, probs