import streamlit as st

def set_page_configuration():
    st.set_page_config(
        page_title="Previsão de Rebaixamento - Série A",
        page_icon="⚽",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def show_title():
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