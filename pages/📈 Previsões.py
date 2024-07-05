import streamlit as st 
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Walmart",
    page_icon="img\walmart.png", 
    layout="wide",
)

path = 'database/forecast_merged.csv'
dfx = pd.read_csv(path)

# Título da aplicação
st.title('Previsão de Vendas para 6 meses')

def create_chart(chart_type):
    if chart_type == 'Estado':
        lista_estado = ['CA', 'TX', 'WI']

        # Interface para seleção do estado
        estado_selecionado = st.radio('Selecione o estado:', lista_estado, index=0, horizontal=True)

        # Filtrar os dados pelo unique_id selecionado
        filtered_df = dfx[dfx['unique_id'] == (estado_selecionado)]

        # Criar o gráfico com Plotly Express
        fig = px.line(filtered_df, x='ds', y='y', title=f'Previsão de Demanda para Estado: {estado_selecionado}', labels={'ds': 'Data', 'y': 'Demanda'})

        # Adicionar uma linha vertical para marcar a data de início das previsões
        fig.add_vline(x='2016-06-30', line_width=3, line_dash='dash', line_color='red')

        # Configuração adicional do gráfico (opcional)
        fig.update_layout(xaxis_title='Data', yaxis_title='Demanda', legend_title='Tipo de Dados')

        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig)

        metrics = {
        'Métricas': ['RMSE', 'MAPE', 'R2'],
        'Valores': [5552.22, 0.19, 0.99]
        }
        metrics_df = pd.DataFrame(metrics)       

        col1, col2 = st.columns(2)
        with col1:
            st.write('Métricas')
            st.write(metrics_df)
        with col2:
            st.write('Dataframe')
            columns_to_display = ['ds', 'y', 'unique_id']
            filtered_df = filtered_df[columns_to_display]
            st.write(filtered_df)

    elif chart_type == 'Loja':
        lista_lojas = ['CA_1', 'CA_2', 'CA_3', 'CA_4', 'TX_1', 'TX_2', 'TX_3', 'WI_1', 'WI_2', 'WI_3']

        # Interface para seleção da loja
        loja_selecionada = st.radio('Selecione a loja:', lista_lojas, index=4, horizontal=True)

        # Filtrar os dados pelo unique_id selecionado
        filtered_df = dfx[dfx['unique_id'] == loja_selecionada]

        # Criar o gráfico com Plotly Express
        fig = px.line(filtered_df, x='ds', y='y', title=f'Previsão de Demanda para Loja: {loja_selecionada}', labels={'ds': 'Data', 'y': 'Demanda'})

        # Adicionar uma linha vertical para marcar a data de início das previsões
        fig.add_vline(x='2016-06-30', line_width=3, line_dash='dash', line_color='red')

        # Configuração adicional do gráfico (opcional)
        fig.update_layout(xaxis_title='Data', yaxis_title='Demanda', legend_title='Tipo de Dados')

        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig)

        metrics = {
        'Métricas': ['RMSE', 'MAPE', 'R2'],
        'Valores': [5552.22, 0.19, 0.99]
        }
        metrics_df = pd.DataFrame(metrics)        

        col1, col2 = st.columns(2)
        with col1:
            st.write('Métricas')
            st.write(metrics_df)
        with col2:
            st.write('Dataframe')
            columns_to_display = ['ds', 'y', 'unique_id']
            filtered_df = filtered_df[columns_to_display]
            st.write(filtered_df)

    elif chart_type == 'Produto':
        # Listas de estados e departamentos
        list_est = ['CA', 'TX', 'WI']
        list_dept = ['FOODS', 'HOBBIES', 'HOUSEHOLD']

        # Interface para seleção de estado e departamento
        col1, col2 = st.columns(2)
        with col1:
            estado_selecionado = st.radio('Selecione o estado:', ['Todos'] + list_est, horizontal=True)
        with col2:
            departamento_selecionado = st.radio('Selecione o departamento:', ['Todos'] + list_dept, horizontal=True)

        # Filtrar o DataFrame com base na seleção de estado e departamento
        filtered_df = dfx[dfx['unique_id'].str.contains('evaluation')]

        if estado_selecionado != 'Todos':
            filtered_df = filtered_df[filtered_df['unique_id'].str.contains(estado_selecionado)]
        if departamento_selecionado != 'Todos':
            filtered_df = filtered_df[filtered_df['unique_id'].str.contains(departamento_selecionado)]

        # Interface de seleção do produto
        produto_selecionado = st.selectbox('Selecione o produto:', filtered_df['unique_id'].unique().tolist())

        # Filtrar o DataFrame com base no produto selecionado
        filtered_data = filtered_df[filtered_df['unique_id'] == produto_selecionado]

        # Criar o gráfico com Plotly Express
        fig = px.line(filtered_data, x='ds', y='y', title=f'Gráfico para {produto_selecionado}', labels={'ds': 'Data', 'y': 'Valor'})

        fig.add_vline(x='2016-06-30', line_width=3, line_dash='dash', line_color='red')

        # Configuração adicional do gráfico (opcional)
        fig.update_layout(xaxis_title='Data', yaxis_title='Valor', legend_title='Tipo de Dados')

        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig)

        metrics = {
        'Métricas': ['RMSE', 'MAPE', 'R2'],
        'Valores': [5552.22, 0.19, 0.99]
        }
        metrics_df = pd.DataFrame(metrics)         

        col1, col2 = st.columns(2)
        with col1:
            st.write('Métricas')
            st.write(metrics_df)
        with col2:
            st.write('Dataframe')
            columns_to_display = ['ds', 'y', 'unique_id']
            filtered_df = filtered_df[columns_to_display]
            st.write(filtered_df)
    else:
        st.warning('Selecione um gráfico para visualizar')

# Opções de gráficos disponíveis
chart_options = ['Estado', 'Loja', 'Produto']

# Selecionar o tipo de gráfico
selected_chart = st.selectbox('Selecione o gráfico que deseja visualizar', chart_options)

# Chamar a função para criar o gráfico selecionado
create_chart(selected_chart)

# filtered_df = dfx[dfx['unique_id'].str.contains('evaluation')]
# st.write(filtered_df['unique_id'].unique().tolist())

