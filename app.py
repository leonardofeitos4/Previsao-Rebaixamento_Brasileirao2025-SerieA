import streamlit as st
import os, sys

# Permite importar controllers e páginas
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controllers.config import set_page_configuration, show_title
from controllers.sidebar import streamlit_menu, sidebar_content

from paginas.previsao import main as main_previsao
from paginas.dados_historicos import main as main_dados
from paginas.analise_sensibilidade import main as main_analise
from paginas.analise_descritiva import main as main_descritiva

# Configurações de página: apenas aqui, antes de qualquer st.*
set_page_configuration()
show_title()

# Menu lateral
selected_option = streamlit_menu()

# Roteamento das páginas
if selected_option == 'Previsão':
    main_previsao()
elif selected_option == 'Dados Históricos':
    main_dados()
elif selected_option == 'Análise de Sensibilidade':
    main_analise()
elif selected_option == 'Análise Descritiva':
    main_descritiva()

# Conteúdo fixo da barra lateral
sidebar_content()


