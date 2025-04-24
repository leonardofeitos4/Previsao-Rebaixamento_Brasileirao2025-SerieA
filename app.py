import streamlit as st
import os
import sys

# Adiciona o diretório atual ao path para importar os módulos corretamente
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importações de funções e módulos necessários para o app
from controllers.config import show_title, set_page_configuration
from controllers.sidebar import streamlit_menu, sidebar_content
from paginas.previsao import main as main_previsao
from paginas.dados_historicos import main as main_dados
from paginas.analise_sensibilidade import main as main_analise

# Configurações iniciais da página
set_page_configuration()

# Exibe o título principal do aplicativo
show_title()

# Obtém a opção escolhida no menu lateral
selected_option = streamlit_menu()

# Exibe a página correspondente à opção selecionada
if selected_option == 'Previsão':
    main_previsao()
elif selected_option == 'Dados Históricos':
    main_dados()
elif selected_option == 'Análise de Sensibilidade':
    main_analise()

# Exibe o conteúdo da sidebar
sidebar_content()
