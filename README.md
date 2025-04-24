# ⚽ Previsão de Rebaixamento - Brasileirão Série A 2025

Este repositório apresenta um aplicativo interativo desenvolvido com **Streamlit**, voltado para previsão do risco de rebaixamento de clubes da Série A do Brasileirão em 2025. O app utiliza um modelo supervisionado de **Regressão Logística** treinado com dados históricos, proporcionando uma experiência acessível e visual para usuários não técnicos.

🔗 **Acesse o app online:**  
👉 [https://previsao-rebaixamentobrasileirao2025-seriea.streamlit.app/](https://previsao-rebaixamentobrasileirao2025-seriea.streamlit.app/)

---

## 🧭 Funcionalidades Principais

- Inserção de dados via formulário ou upload de CSV
- Predição do risco de rebaixamento (probabilidades e classificação)
- Análise de sensibilidade com diferentes cenários
- Visualizações complementares (tabelas e gráficos interativos)
- Explicação clara sobre o funcionamento do modelo e limitações

---

## 🧠 Sobre o Modelo

- **Tipo:** Regressão Logística
- **Variáveis:**  
  - Número de Jogadores  
  - Número de Estrangeiros  
  - Valor de Mercado Total  
- **Métricas de Desempenho:**  
  - Acurácia Média: **0.89**  
  - MAE Médio: **0.11**  
  - RMSE Médio: **0.32**  
- **Objetivo:** Apoiar decisões e análises preditivas sobre desempenho e risco de rebaixamento.  
- **Limitações:** Não inclui fatores imprevisíveis como lesões, clima ou trocas técnicas.

---

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

- Instale as dependências do projeto:
pip install -r requirements.txt



