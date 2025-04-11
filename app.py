import streamlit as st
import pandas as pd
import os

# Título do app
st.title("Previsão de Pontos - Brasileirão Série A")

# Carregar dados
@st.cache_data
def carregar_dados():
    caminho = os.path.join("dados", "BASE_FINAL.csv")
    return pd.read_csv(caminho)

df = carregar_dados()

# Mostrar tabela
st.subheader("Base de Dados")
st.dataframe(df)

# Filtros (exemplo)


clubes = df["Clube"].unique()
clube_selecionado = st.selectbox("Selecione um clube", clubes)

# Mostrar dados filtrados
st.subheader(f"Dados do {clube_selecionado}")
st.dataframe(df[df["Clube"] == clube_selecionado])




