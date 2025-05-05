# app.py (ou utils/app.py, como estiver rodando)
import streamlit as st
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controllers.config import show_title, set_page_configuration
from controllers.sidebar import streamlit_menu, sidebar_content

from paginas.previsao import main as main_previsao
from paginas.dados_historicos import main as main_dados
from paginas.analise_sensibilidade import main as main_analise
from paginas.analise_descritiva import main as main_descritiva   # ← importamos a nova página

set_page_configuration()
show_title()
selected_option = streamlit_menu()

if selected_option == 'Previsão':
    main_previsao()
elif selected_option == 'Dados Históricos':
    main_dados()
elif selected_option == 'Análise de Sensibilidade':
    main_analise()
elif selected_option == 'Análise Descritiva':
    main_descritiva()

sidebar_content()

