import streamlit as st 
import pandas as pd
import plotly.express as px

# Carregar o DataFrame
path = 'database/forecast_merged.csv'
dfx = pd.read_csv(path)

st.set_page_config(
    page_title="Walmart",
    page_icon="img\walmart.png", 
    layout="wide",
)

col1, col2 = st.columns([1, 8])  
with col1:
    st.image("img/walmart.png", width=100)
with col2:
    st.title("Walmart - Números de Vendas")



with st.expander("Saiba mais"):
        st.write('''O Walmart é um dos maiores varejistas e uma das lojas de varejo preferidas para compras domésticas. 
        Conhecida pelos preços mais baixos e economia de custos em todas as categorias de produtos, uma visita às suas lojas 
        físicas é uma experiência por si só. É um negócio de varejo que teve 66.927,173 vendas de janeiro de 2011 a maio de 2016.''')


# Calcular as métricas
filtered_total = dfx[(dfx['ds'] >= '2016-06-30') & (dfx['unique_id'].isin(['Total']))]
vendas_totais = int(filtered_total['y'].sum())

#Estado
df_filtered_est = dfx[(dfx['ds'] >= '2016-06-30') & (dfx['unique_id'].isin(['CA', 'TX', 'WI']))]
sales_by_state = df_filtered_est.groupby('unique_id')['y'].sum().reset_index()
top_state = sales_by_state.loc[sales_by_state['y'].idxmax()]

#Loja
df_filtered_loja = dfx[(dfx['ds'] >= '2016-06-30') & (dfx['unique_id'].isin(['CA_1', 'CA_2', 'CA_3', 'CA_4', 'TX_1', 'TX_2', 'TX_3', 'WI_1', 'WI_2', 'WI_3']))]
sales_by_loja = df_filtered_loja.groupby('unique_id')['y'].sum().reset_index()
top_loja = sales_by_loja.loc[sales_by_loja['y'].idxmax()]

#Produto
df_filtered_produto = dfx[(dfx['ds'] >= '2016-06-30') & (dfx['unique_id'].str.contains('evaluation'))]
sales_by_produto = df_filtered_produto.groupby('unique_id')['y'].sum().reset_index()
top_produto = sales_by_produto.loc[sales_by_produto['y'].idxmax()]

# Titulo
st.header("Previsão de Vendas para 6 meses")

# Exibir métricas em colunas
col1, col2, col3, col4 = st.columns(4)

col1.metric(label="Total Produtos Vendidos", value=f"{vendas_totais:,}")

with col2:
    st.metric(label="Estado", value=top_state['unique_id'])
    st.metric(label="Total de Vendas", value=f"{int(top_state['y']):,}")

with col3:
    st.metric(label="Loja", value=top_loja['unique_id'])
    st.metric(label="Total de Vendas", value=f"{int(top_loja['y']):,}")

with col4:
    st.metric(label="Produto", value=top_produto['unique_id'])
    st.metric(label="Total de Vendas", value=f"{int(top_produto['y']):,}")


filtered_df = dfx[dfx['unique_id'] == 'Total']

# Criar o gráfico com Plotly Express
fig = px.line(filtered_df, x='ds', y='y', title=f'Previsão de Demanda para Total de Vendas', labels={'ds': 'Data', 'y': 'Demanda'})

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