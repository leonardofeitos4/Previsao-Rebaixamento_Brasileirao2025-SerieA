import streamlit as st

def load_css():
    """
    Retorna o CSS personalizado para a aplicação.
    
    Returns:
        str: String contendo todo o CSS personalizado
    """
    return """
    <style>
        .main-header {
            font-size: 2.5rem;
            color: #1e3d59;
            text-align: center;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        .subheader {
            font-size: 1.8rem;
            color: #1e3d59;
            margin-top: 2rem;
            border-bottom: 2px solid #f5f0e1;
            padding-bottom: 0.5rem;
        }
        .card {
            background-color: #f5f0e1;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .metric-value {
            font-size: 2.5rem;
            font-weight: bold;
            text-align: center;
        }
        .metric-label {
            font-size: 1rem;
            text-align: center;
            color: #666;
        }
        .footer {
            text-align: center;
            margin-top: 3rem;
            padding: 1rem;
            background-color: #f5f0e1;
            border-radius: 10px;
        }
        .stButton>button {
            background-color: #1e3d59;
            color: white;
            font-weight: bold;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #2b5d8b;
        }
        
        /* Estilos para elementos do Streamlit */
        .stSelectbox {
            background-color: white;
            border-radius: 5px;
            border: 1px solid #ddd;
        }
        
        .stSlider {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        
        .plot-container {
            background-color: white;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        /* Estilização das tabs */
        .stTab {
            background-color: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
        }
        
        /* Estilização do dataframe */
        .dataframe {
            border: none !important;
            border-collapse: collapse !important;
        }
        
        .dataframe th {
            background-color: #1e3d59 !important;
            color: white !important;
            padding: 12px !important;
        }
        
        .dataframe td {
            padding: 10px !important;
            border: 1px solid #ddd !important;
        }
        
        /* Estilização dos gráficos */
        .js-plotly-plot {
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        /* Estilização do spinner */
        .stSpinner {
            text-align: center;
            color: #1e3d59;
        }
        
        /* Estilização das mensagens de aviso */
        .stAlert {
            background-color: #fff3cd;
            color: #856404;
            padding: 15px;
            border-radius: 5px;
            border-left: 5px solid #ffeeba;
        }
        
        /* Estilização do upload de arquivo */
        .uploadedFile {
            background-color: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
            border: 1px dashed #dee2e6;
        }

        /* Novos estilos para organização dos gráficos */
        .centered-graph {
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 20px auto;
            width: 70%;
        }

        .graph-container {
            margin: 20px 0;
            padding: 15px;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }

        .analysis-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 20px;
        }

        .comparison-table {
            background-color: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }

        .radar-chart {
            background-color: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }

        /* Estilos para centralização do gráfico de pizza */
        .pie-chart-container {
            display: flex;
            justify-content: center;
            margin: 20px 0;
        }

        /* Estilos para o layout de dois gráficos */
        .two-charts-container {
            display: flex;
            justify-content: space-between;
            margin-top: 20px;
            gap: 20px;
        }

        .chart-box {
            flex: 1;
            background-color: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
    </style>
    """

def apply_custom_css():
    """
    Aplica o CSS personalizado na aplicação
    """
    st.markdown(load_css(), unsafe_allow_html=True)