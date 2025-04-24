# ⚽ Previsão de Rebaixamento - Brasileirão Série A 2025

Este repositório apresenta um aplicativo interativo desenvolvido com **Streamlit**, voltado para previsão do risco de rebaixamento de clubes da Série A do Brasileirão em 2025. O app utiliza um modelo supervisionado de **Regressão Logística** treinado com dados históricos, proporcionando uma experiência acessível e visual para usuários não técnicos.

🔗 **Acesse o app online:**  
👉 [https://previsao-rebaixamentobrasileirao2025-seriea.streamlit.app/](https://previsao-rebaixamentobrasileirao2025-seriea.streamlit.app/)

## 🧭 Funcionalidades Principais
- Inserção de dados via formulário ou upload de CSV
- Predição do risco de rebaixamento (probabilidades e classificação)
- Análise de sensibilidade com diferentes cenários
- Visualizações complementares (tabelas e gráficos interativos)
- Explicação clara sobre o funcionamento do modelo e limitações

## 🧠 Sobre o Modelo
- **Tipo:** Regressão Logística
- **Variáveis:**  
  - Número de Jogadores (`Plantel`)
  - Número de Estrangeiros (`Estrangeiros`)
  - Valor de Mercado Total (`Valor de Mercado Total`)
- **Métricas de Desempenho:**  
  - Acurácia Média: **0.89** (indicando que o modelo acerta a classificação em aproximadamente 89% das vezes)
  - MAE Médio: **0.11** (erro médio absoluto entre as probabilidades previstas e reais)
  - RMSE Médio: **0.32** (raiz do erro médio quadrático, indicando a magnitude do erro)
- **Objetivo:** Apoiar decisões e análises preditivas sobre desempenho e risco de rebaixamento.  
- **Limitações:** 
  - Não inclui fatores imprevisíveis como lesões, clima ou trocas técnicas.
  - O modelo foi treinado com dados históricos e pode não refletir mudanças significativas nos times ou na dinâmica do campeonato.

## 📊 Dados Utilizados
A base de dados utilizada para treinar o modelo inclui informações sobre os clubes da Série A, como:
- `Clube`: Nome do clube
- `Plantel`: Número de jogadores no elenco
- `Estrangeiros`: Número de jogadores estrangeiros no elenco
- `Valor de Mercado Total`: Valor total de mercado do elenco
- `Pontos`: Pontuação obtida pelo clube em uma temporada
- `Situacao`: Classificação final do clube na temporada (por exemplo, Top4, Rebaixado)
- `Status`: Indicador de rebaixamento (1 para rebaixado, 0 para não rebaixado)
Exemplo das primeiras linhas da base de dados:
| Clube     | Plantel | ø Idade | Estrangeiros | ø Valor de Mercado | Valor de Mercado Total | Temporada | Pontos | Situação | Status |
|-----------|---------|---------|--------------|---------------------|-------------------------|------------|--------|----------|--------|
| São Paulo | 45      | 25      | 6            | 3.33                | 149.65                  | 2014       | 70     | Top4     | 1.0    |


## 📦 Instalação de Dependências
Para garantir que o aplicativo funcione corretamente, é essencial instalar todas as bibliotecas Python necessárias listadas no arquivo `requirements.txt`.
### 🔧 Passos para instalação:
1. **(Opcional, mas recomendado)** Crie um ambiente virtual:
   ```bash
   python -m venv venv

- No Windows:
    - venv\Scripts\activate

- No macOS/Linux:
   - source venv/bin/activate
   
## Instale as dependências do projeto

- pip install -r requirements.txt

- Execute o aplicativo com o comando:
    - streamlit run app.py


