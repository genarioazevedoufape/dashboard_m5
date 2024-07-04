import streamlit as st 
import pandas as pd
import plotly.express as px

# Carregar o DataFrame
path = 'database/hist_vendas_total.parquet'
df = pd.read_parquet(path)

def produtos_mais_vendidos(df, coluna, valor):
    dados_filtrados = df[df[coluna] == valor]
    dados_agrupados = dados_filtrados.groupby('id')['value'].sum()
    itens_mais_vendidos = dados_agrupados.sort_values(ascending=False).head(10)
    return itens_mais_vendidos

def create_chart(chart_type):
    if chart_type == 'Loja':
        vendas_por_loja = df.groupby('store_id')['value'].sum().reset_index()
        fig = px.bar(vendas_por_loja, x='store_id', y='value', 
                     labels={'store_id': 'Loja', 'value': 'Número de Produtos Vendidos'}, 
                     title='Número de Produtos Vendidos por Loja')

        st.plotly_chart(fig)

        # Widget para seleção da loja
        loja_selecionada = st.radio('Selecione a loja:', df['store_id'].unique(), horizontal=True)

        # Verificando se a loja selecionada existe nos dados
        if loja_selecionada in df['store_id'].unique():
            st.subheader(f'Top 10 produtos mais vendidos na Loja {loja_selecionada}')
            itens_mais_vendidos = produtos_mais_vendidos(df, 'store_id', loja_selecionada)
            # Criando uma tabela para exibir os produtos mais vendidos
            st.table(itens_mais_vendidos.reset_index().rename(columns={'id': 'ID do Produto', 'value': 'Vendas'}))

        else:
            st.warning(f'A loja {loja_selecionada} não foi encontrada nos dados.')

    elif chart_type == 'Departamento':
        vendas_por_departamento = df.groupby('dept_id')['value'].sum().reset_index()
        fig = px.bar(vendas_por_departamento, x='dept_id', y='value', 
                     labels={'dept_id': 'Departamento', 'value': 'Número de Produtos Vendidos'}, 
                     title='Número de Produtos Vendidos por Departamento')

        st.plotly_chart(fig)

        # Widget para seleção da departamento
        departamento_selecionada = st.radio('Selecione o departamento:', df['dept_id'].unique(), horizontal=True)

        # Verificando se a departamento selecionada existe nos dados
        if departamento_selecionada in df['dept_id'].unique():
            st.subheader(f'Top 10 produtos mais vendidos no Departamento {departamento_selecionada}')
            itens_mais_vendidos = produtos_mais_vendidos(df, 'dept_id', departamento_selecionada)
            # Criando uma tabela para exibir os produtos mais vendidos
            st.table(itens_mais_vendidos.reset_index().rename(columns={'id': 'ID do Produto', 'value': 'Vendas'}))

        else:
            st.warning(f'O departamento {departamento_selecionada} não foi encontrado nos dados.')

    elif chart_type == 'Categoria':
        vendas_por_categoria = df.groupby('cat_id')['value'].sum().reset_index()
        fig = px.bar(vendas_por_categoria, x='cat_id', y='value', 
                     labels={'cat_id': 'Categoria', 'value': 'Número de Produtos Vendidos'}, 
                     title='Número de Produtos Vendidos por Categoria')

        st.plotly_chart(fig)

        # Widget para seleção da categoria
        categoria_selecionada = st.radio('Selecione a categoria:', df['cat_id'].unique(), horizontal=True)

        # Verificando se a categoria selecionada existe nos dados
        if categoria_selecionada in df['cat_id'].unique():
            st.subheader(f'Top 10 produtos mais vendidos na Categoria {categoria_selecionada}')
            itens_mais_vendidos = produtos_mais_vendidos(df, 'cat_id', categoria_selecionada)
            # Criando uma tabela para exibir os produtos mais vendidos
            st.table(itens_mais_vendidos.reset_index().rename(columns={'id': 'ID do Produto', 'value': 'Vendas'}))

        else:
            st.warning(f'A categoria {categoria_selecionada} não foi encontrada nos dados.')

    elif chart_type == 'Estado':
        vendas_por_estado = df.groupby('state_id')['value'].sum().reset_index()
        fig = px.bar(vendas_por_estado, x='state_id', y='value', 
                     labels={'state_id': 'Estado', 'value': 'Número de Produtos Vendidos'}, 
                     title='Número de Produtos Vendidos por Estado')     

        st.plotly_chart(fig)

        # Widget para seleção do estado
        estado_selecionada = st.radio('Selecione o Estado:', df['state_id'].unique(), horizontal=True)

        # Verificando se o estado selecionado existe nos dados
        if estado_selecionada in df['state_id'].unique():
            st.subheader(f'Top 10 produtos mais vendidos no Estado {estado_selecionada}')
            itens_mais_vendidos = produtos_mais_vendidos(df, 'state_id', estado_selecionada)
            # Criando uma tabela para exibir os produtos mais vendidos
            st.table(itens_mais_vendidos.reset_index().rename(columns={'id': 'ID do Produto', 'value': 'Vendas'}))

        else:
            st.warning(f'O estado {estado_selecionada} não foi encontrado nos dados.')

    return fig

# Título da aplicação
st.title('Análise de Vendas | 01-2011 a 05-2016')

    # Calcular as métricas
vendas_totais = df['value'].sum()

vendas_por_loja = df.groupby('store_id')['value'].sum()
loja_top_vendas = vendas_por_loja.idxmax()
valor_top_vendas_loj = vendas_por_loja.max()

vendas_por_departamento = df.groupby('dept_id')['value'].sum()
departamento_top_vendas = vendas_por_departamento.idxmax()
valor_top_vendas_dep = vendas_por_departamento.max()

vendas_por_categoria = df.groupby('cat_id')['value'].sum()
categoria_top_vendas = vendas_por_categoria.idxmax()
valor_top_vendas_cat = vendas_por_categoria.max()

vendas_por_estado = df.groupby('state_id')['value'].sum()
estado_top_vendas = vendas_por_estado.idxmax()
valor_top_vendas_est = vendas_por_estado.max()

# Titulo
st.header("Métricas de Vendas")

# Exibir métricas em colunas
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(label="Total Produtos Vendidos", value=f"{vendas_totais:,}")

with col2:
    st.metric(label="Estado", value=estado_top_vendas)
    st.metric(label="Total de Vendas", value=f"{valor_top_vendas_est:,}")

with col3:
    st.metric(label="Categoria", value=categoria_top_vendas)
    st.metric(label="Total de Vendas", value=f"{valor_top_vendas_cat:,}")

with col4:
    st.metric(label="Departamento", value=departamento_top_vendas)
    st.metric(label="Total de Vendas", value=f"{valor_top_vendas_dep:,}")

with col5:
    st.metric(label="Loja", value=loja_top_vendas)
    st.metric(label="Total de Vendas", value=f"{valor_top_vendas_loj:,}")

#Gráfico
dados_mensais = df.groupby(['ano', 'mes'])['value'].sum().reset_index()

# Criação do gráfico com Plotly Express
fig = px.line(dados_mensais, x='mes', y='value', color='ano',
              title='Vendas Mensais por Ano',
              labels={'mes': 'Mês', 'value': 'Vendas Unitárias', 'ano': 'Ano'})

# Personalização adicional (opcional)
fig.update_layout(
    xaxis_title='Mês',
    yaxis_title='Vendas Unitárias',
    legend_title='Ano',
)

# Configuração da grade
fig.update_xaxes(showgrid=True)
fig.update_yaxes(showgrid=True)

st.plotly_chart(fig)


st.header('Número de Vendas')

# Seleção do gráfico
chart_options = ['Loja', 
                 'Departamento', 
                 'Categoria', 
                 'Estado']

selected_chart = st.selectbox('Selecione o gráfico que deseja visualizar', chart_options)

# Criar e exibir o gráfico selecionado
fig = create_chart(selected_chart)

# Análise de vendas mensais
st.header('Percentual de Vendas Mensalmente')

def create_monthly_chart(df, chart_type):
    if chart_type == 'Por Categoria':
        df_mensal = df.groupby(['cat_id', 'ano', 'mes'])['value'].sum().reset_index()
        title = 'Porcentagem de Vendas Mensais por Categoria'
        x_label = 'cat_id'
    elif chart_type == 'Por Estado':
        df_mensal = df.groupby(['state_id', 'ano', 'mes'])['value'].sum().reset_index()
        title = 'Porcentagem de Vendas Mensais por Estado'
        x_label = 'state_id'
    elif chart_type == 'Por Loja':
        df_mensal = df.groupby(['store_id', 'ano', 'mes'])['value'].sum().reset_index()
        title = 'Porcentagem de Vendas Mensais por Loja'
        x_label = 'store_id'
    
    df_mensal['ano_mes'] = df_mensal['ano'].astype(str) + '-' + df_mensal['mes'].astype(str).str.zfill(2)
    df_mensal['total_mes'] = df_mensal.groupby([x_label, 'ano'])['value'].transform('sum')
    df_mensal['percentagem'] = (df_mensal['value'] / df_mensal['total_mes']) * 100

    fig = px.line(df_mensal, x='ano_mes', y='percentagem', color=x_label, markers=True,
                  labels={'ano_mes': 'Ano-Mês', 'percentagem': 'Porcentagem de Vendas (%)', x_label: x_label},
                  title=title)
    fig.update_layout(xaxis_tickangle=90)
    return fig

# Seleção do tipo de análise
analysis_type = st.radio('Selecione o tipo de análise', ['Por Categoria', 'Por Estado', 'Por Loja'])

# Criar e exibir o gráfico selecionado
fig = create_monthly_chart(df, analysis_type)
st.plotly_chart(fig)


# 100 produtos mais vendidos
dados_agrupados = df.groupby('id')['value'].sum().sort_values(ascending=False)
itens_mais_vendidos = dados_agrupados.head(100)

# Gráfico de barras para os 100 itens mais vendidos
fig1 = px.bar(itens_mais_vendidos, x=itens_mais_vendidos.index, y=itens_mais_vendidos.values, 
              labels={'x': 'Produto', 'y': 'Vendas'}, title='100 Produtos Mais Vendidos')
fig1.update_layout(xaxis_tickangle=90)

# Cálculo da porcentagem de vendas dos top 100 itens
venda_top_100 = itens_mais_vendidos.sum()
venda_total = df['value'].sum()
porcentagem = (venda_top_100 / venda_total) * 100

# Gráfico de pizza para a porcentagem de vendas
fig2 = px.pie(values=[porcentagem, 100 - porcentagem], 
              names=[f'Top 100 Produtos ({porcentagem:.2f}%)', 'Outros'], 
              title='Porcentagem de Vendas: Top 100 Produtos vs. Outros', 
              hole=0.3)

# Streamlit para exibir os gráficos lado a lado
st.header('Itens mais vendidos')

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1)

with col2:
    st.plotly_chart(fig2)
