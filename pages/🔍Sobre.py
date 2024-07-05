import pandas as pd
import streamlit as st 
from plotly.subplots import make_subplots
import plotly.graph_objs as go

st.set_page_config(
    page_title="Walmart",
    page_icon="img\walmart.png", 
    layout="wide",
)

path = 'database/validacao_modelo.csv'
df = pd.read_csv(path)


def style_text(text, size):
    return f'<p style="font-size:{size}px;">{text}</p>'

st.title('TIME - 3')
st.markdown("<br>", unsafe_allow_html=True)

def create_profile(image_path, name, description, linkedin_url):
    col1, col2 = st.columns([1, 7], vertical_alignment='center', gap='small')
    with col1:
        st.image(image_path, width=100)
    with col2:
        st.subheader(name)
        st.write(description)
        st.link_button('Linkedin', linkedin_url)

# Profile 1
create_profile("img/genario.png", "Genário Correia de Azevedo", 
               "Bacharelando em Ciências da Computação - UFAPE", 
               'https://www.linkedin.com/in/genarioazevedo/')

# Profile 2
create_profile("img/ivan.jpeg", "Ivanilson Alves", 
               "Graduando em Análise e Desenvolvimento de Sistemas - IFPE", 
               'https://www.linkedin.com/in/ivanilson-alves-abb257201/')

# Profile 3
create_profile("img/stenio.jpeg", "Stênio Medeiros", 
               "Bacharelando em Ciências da Computação - UFAPE", 
               'https://www.linkedin.com/in/st%C3%AAnio-medeiros-b2b027227/')


st.markdown("<br>", unsafe_allow_html=True)
st.header('Sobre o Projeto')
st.write('''Este dashboard é o resultado do projeto de extensão "Formação de Cientistas de Dados no Agreste Meridional de Pernambuco", 
         promovido pela Universidade de Pernambuco e ministrado pelo professor [Dr. Eraylson Galdino](https://www.linkedin.com/in/eraylson/). 
         Durante esta formação, abordamos tópicos essenciais da Ciência de Dados, incluindo Exploração e Preparação de Dados, Análise Estatística, 
         Machine Learning e Visualização de Dados. O foco principal foi no estudo e prática de Séries Temporais, utilizando bibliotecas avançadas 
         como Nixtla que é uma ferramenta especializada em previsão de séries temporais, oferecendo suporte para múltiplos modelos estatísticos 
         e de machine learning, bem como capacidades de previsão de multisséries. Como parte integrante do projeto, enfrentamos um cenário simulado
         de Previsão de Demanda baseado em desafios reais da empresa de tecnologia Sauter. Além disso, participamos de workshops voltados para a 
         manipulação de dados no ambiente Google, ampliando nossas habilidades práticas e conhecimentos técnicos na área de Ciência de Dados.''')


st.markdown("<br>", unsafe_allow_html=True)
st.header('Instrumentos e informações da previsão de demanda')


st.write('''Para a construção dos modelos de previsão dos dados de venda do Walmart, foi realizado um processo criterioso
        de análise exploratória e transformação dos dados, a fim de extrair inferências valiosas para todo o processo. 
        Utilizou-se o framework Nixtla com a biblioteca MlForecast para a construção do modelo, onde foram avaliados os 
        modelos XGBRegressor, SVR, LinearRegression, RandomForestRegressor, utilizando as métricas RMSE, MAPE e R2. Após a avaliação e validação dos dados, 
        o modelo RandomForestRegressor foi definido como o melhor preditor.''')

link = "https://colab.research.google.com/drive/1egetnDblPccsVpVzAQSe1hOPDMopcRUD#scrollTo=vJ1171CZPQhu"
st.write("**Link to Colab Notebook:**")
st.markdown(link)


st.markdown("<br>", unsafe_allow_html=True)

with st.expander("Validação do modelo"):
    # Criar o selectbox para selecionar o unique_id
    selected_device = st.selectbox('Selecione a série', df['unique_id'].unique())

    # Filtrar o dataframe para o dispositivo selecionado
    p_device = df.loc[df['unique_id'] == selected_device]

    # Criar subplots em Plotly
    fig = make_subplots(rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.1)

    models = [
        ('XGBRegressor', 'XGBRegressor Predicted'), 
        ('SVR', 'SVR Predicted'), 
        ('LinearRegression', 'LinearRegression Predicted'), 
        ('RandomForestRegressor', 'RandomForestRegressor Predicted')
    ]

    for i, (model_col, label) in enumerate(models):
        # Adicionar linha do modelo predito
        fig.add_trace(
            go.Scatter(x=p_device['ds'], y=p_device[model_col], mode='lines', name=f'{label} - {selected_device}'),
            row=i+1, col=1
        )
        # Adicionar linha do valor real
        fig.add_trace(
            go.Scatter(x=p_device['ds'], y=p_device['y'], mode='lines', name=f'Actual - {selected_device}', line=dict(dash='dash')),
            row=i+1, col=1
        )
        # Atualizar títulos dos eixos
        fig.update_yaxes(title_text='Sessions', row=i+1, col=1)
        if i == len(models) - 1:  # Apenas o último subplot precisa do título do eixo X
            fig.update_xaxes(title_text='Date', row=i+1, col=1)

    # Atualizar layout
    fig.update_layout(height=800, width=1000, title_text=f'Previsão sob os dados de testes de {selected_device}')

    # Exibir gráfico no Streamlit
    st.plotly_chart(fig)

    metrics = {
    'Modelo': ['XGBRegressor', 'SVR', 'LinearRegression', 'RandomForestRegressor'],
    'RMSE': [5848.56, 5776.60, 5733.90, 5552.22],
    'MAPE': [0.06, 0.07, 0.06, 0.19],
    'R2': [0.99, 0.99, 0.99, 0.99]
    }

    metrics_df = pd.DataFrame(metrics)
    st.subheader('Métricas dos Modelos')
    st.write(metrics_df)
        