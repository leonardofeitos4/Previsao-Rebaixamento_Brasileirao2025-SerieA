# Previsão de Rebaixamento - Brasileirão Série A 2025

Este projeto visa criar um aplicativo interativo para prever o risco de rebaixamento dos clubes da **Série A do Campeonato Brasileiro 2025**. O aplicativo foi desenvolvido utilizando **Streamlit** e incorporando um modelo de **Machine Learning** treinado com dados históricos, utilizando um modelo de **Regressão Logística**. O foco é tornar a análise preditiva acessível e intuitiva para usuários não técnicos.

## Objetivo

O objetivo deste projeto é fornecer uma ferramenta de **análise preditiva** para estimar o risco de rebaixamento de clubes da Série A do Campeonato Brasileiro 2025, com base em características como o tamanho do elenco, o número de estrangeiros e o valor de mercado dos clubes. O modelo de machine learning desenvolvido visa apoiar a tomada de decisões e proporcionar insights relevantes para gestores de clubes e fãs de futebol.

## Funcionalidades

O aplicativo **Streamlit** oferece as seguintes funcionalidades:

- **Entrada de Dados**: Permite que o usuário insira manualmente ou faça upload de arquivos contendo as informações dos clubes.
- **Previsão de Rebaixamento**: Com base nas informações fornecidas, o modelo faz previsões sobre a probabilidade de rebaixamento de cada clube.
- **Análise de Sensibilidade**: Exploração de como as variáveis (como o tamanho do elenco, número de estrangeiros, e valor de mercado) afetam a probabilidade de rebaixamento.
- **Visualizações Interativas**: Gráficos dinâmicos, como gráficos de linha e gráficos 3D, ajudam a interpretar as previsões e explorar os resultados de forma visual.
- **Informações sobre o Modelo**: O aplicativo contém uma seção explicativa sobre o modelo, incluindo contexto, dados utilizados, métricas de desempenho e limitações.

## Tecnologias Utilizadas

O projeto foi desenvolvido utilizando as seguintes tecnologias:

- **Streamlit**: Framework para criar o aplicativo interativo.
- **Scikit-learn**: Biblioteca para construção e treinamento do modelo de **Regressão Logística**.
- **Plotly**: Biblioteca para criar gráficos interativos e visualizações.
- **Pandas**: Biblioteca para manipulação e análise de dados.
- **NumPy**: Biblioteca para cálculos numéricos e manipulação de arrays.

## Estrutura do Projeto

O repositório contém os seguintes arquivos e pastas:

- **app.py**: Arquivo principal do Streamlit que contém a lógica para rodar o aplicativo interativo.
- **utils/processamento.py**: Funções auxiliares para carregar dados e fazer previsões com o modelo.
- **dados/**: Pasta contendo os arquivos de dados utilizados para o treinamento e testes do modelo.
- **requirements.txt**: Arquivo com as dependências necessárias para rodar o projeto.
- **README.md**: Este arquivo com informações sobre o projeto.

## Como Rodar o Projeto

### 1. Clonando o Repositório

Para clonar o repositório, use o seguinte comando:

```bash
git clone https://github.com/usuario/nome-do-repositorio.git
cd nome-do-repositorio
