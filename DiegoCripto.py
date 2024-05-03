import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import timedelta
from moduloDiego import calculate_moving_averages, calculate_rsi, calculate_macd

# Carregar dados
@st.experimental_memo
def importar_dados():
    df = pd.read_csv('dadosdf_cripto.csv')
    df['tempo'] = pd.to_datetime(df['tempo'])
    return df

# Botão para recarregar os dados
if st.button('Recarregar Dados'):
    st.experimental_rerun()

df = importar_dados()

st.title('Análises de Cripto Moedas')
st.sidebar.header('Menu')

opcoes = ['Home', 'Visualização', 'Análise', 'Sobre']
escolha = st.sidebar.selectbox("Escolha uma opção", opcoes)

if escolha == 'Visualização':
    st.subheader('Visualização de Dados')
    criptomoedas = df['moeda'].unique()
    moeda_selecionada = st.selectbox('Selecione uma Moeda para Visualização:', criptomoedas)
    
    # Gráfico de linha para o preço de fechamento
    if st.button(f'Visualizar Gráfico para {moeda_selecionada}'):
        df_moeda = df[df['moeda'] == moeda_selecionada]
        fig = px.line(df_moeda, x='tempo', y='fechamento', title=f'Preço de Fechamento ao Longo do Tempo para {moeda_selecionada}')
        st.plotly_chart(fig)

if escolha == 'Análise':
    st.subheader('Análise de Indicadores de Mercado')
    criptomoedas = df['moeda'].unique()
    moeda_selecionada = st.selectbox('Selecione uma Moeda para Análise Detalhada:', criptomoedas)
    
    if st.button(f'Analisar {moeda_selecionada}'):
        df_moeda = df[df['moeda'] == moeda_selecionada]
        
        # Abas para diferentes análises
        with st.tabs(["Médias Móveis", "RSI", "MACD"]) as tabs:
            with st.tab("Médias Móveis"):
                df_moeda = calculate_moving_averages(df_moeda)
                fig = px.line(df_moeda, x='tempo', y=['fechamento', 'SMA', 'EMA'], title='Médias Móveis')
                st.plotly_chart(fig)
            
            with st.tab("RSI"):
                df_moeda = calculate_rsi(df_moeda)
                fig = px.line(df_moeda, x='tempo', y='RSI', title='Índice de Força Relativa (RSI)')
                st.plotly_chart(fig)
            
            with st.tab("MACD"):
                df_moeda = calculate_macd(df_moeda)
                fig = px.line(df_moeda, x='tempo', y=['MACD', 'signal_line'], title='MACD e Linha de Sinal')
                st.plotly_chart(fig)

# Adicione mais opções ou detalhes conforme necessário para o menu 'Sobre'
if escolha == 'Sobre':
    st.write("Esta aplicação foi desenvolvida para analisar criptomoedas.")
