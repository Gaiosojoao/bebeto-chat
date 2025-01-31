import tempfile
import streamlit as st
from langchain.memory import ConversationBufferMemory

from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

from loaders import *

TIPOS_ARQUIVOS_VALIDDOS = [ 
    'Site', 'Youtube', 'Pdf', 'Csv', 'Txt'
]

CONFIG_MODELOS = {'Groq': 
                        {'modelos': ['llama-3.3-70b-versatile', 'gemma2-9b-it', 'mixtral-8x7b-32768'],
                         'chat': ChatGroq},
                  'OpenAI': 
                        {'modelos': ['GPT-4o-mini', 'GPT-4o', 'o1 and o1-mini'],
                         'chat': ChatOpenAI}}

MEMORIA = ConversationBufferMemory()

def carrega_arquivos(tipo_arquivo, arquivo):
    if tipo_arquivo == 'Site':
        arquivo = carrega_site(arquivo)
    if tipo_arquivo == 'Youtube':
        arquivo = carrega_youtube(arquivo)
    if tipo_arquivo == 'Pdf':
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp:
            temp.write(arquivo.read())
            nome_temp = temp.name
        arquivo = carrega_pdf(nome_temp)
    if tipo_arquivo == 'Csv':
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp:
            temp.write(arquivo.read())
            nome_temp = temp.name
        arquivo = carrega_csv(nome_temp)
    if tipo_arquivo == 'Txt':
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp:
            temp.write(arquivo.read())
            nome_temp = temp.name
        arquivo = carrega_txt(nome_temp)
    return arquivo

def carrega_modelo(provedor, modelo, api_key, tipo_arquivo, arquivo):
    
    arquivo = carrega_arquivos(tipo_arquivo, arquivo)

    system_message = '''Você é um assistente amigável chamado Bebeto.
    Você possui acesso às seguintes informações vindas 
    de um documento {}: 

    ####
    {}
    ####

    Utilize as informações fornecidas para basear as suas respostas.

    Sempre que houver $ na sua saída, substita por S.

    Se a informação do documento for algo como "Just a moment...Enable JavaScript and cookies to continue" 
    sugira ao usuário carregar novamente o Oráculo!'''.format(tipo_arquivo, arquivo)
    template = ChatPromptTemplate.from_messages([
        ('system', system_message),
        ('placeholder', '{chat_history}'),
        ('user', '{input}')
    ])

    chat = CONFIG_MODELOS[provedor]['chat'](model=modelo, api_key=api_key)
    chain = template | chat

    st.session_state['chain'] = chain

def pagina_chat():
    st.header('🤖 Bem-vindo ao Bebeto', divider=True)

    chain = st.session_state.get('chain')
    if chain is None:
        st.error('Carregue o Bebeto')
        st.stop()
    memoria = st.session_state.get('memoria', MEMORIA)
    for mensagem in memoria.buffer_as_messages:
        chat = st.chat_message(mensagem.type)
        chat.markdown(mensagem.content)
        
    input_usuario = st.chat_input('Fale com o Bebeto!')
    if input_usuario:
        chat = st.chat_message('human')
        chat.markdown(input_usuario)

        chat = st.chat_message('ai')
        resposta = chat.write_stream(chain.stream({
            'input': input_usuario,
            'chat_history': memoria.buffer_as_messages
            }))

        memoria.chat_memory.add_user_message(input_usuario)
        memoria.chat_memory.add_ai_message(resposta)
        st.session_state['memoria'] = memoria

def sidebar():
    tabs = st.tabs(['Upload de Arquivos', 'Seleção de Modelos'])
    with tabs[0]:
        tipo_arquivo = st.selectbox('Tipo de Arquivo', TIPOS_ARQUIVOS_VALIDDOS)
        if tipo_arquivo == 'Site':
            arquivo = st.text_input('Digite a URL do site:')
        if tipo_arquivo == 'Youtube':
            arquivo = st.text_input('Digite a URL do video:')
        if tipo_arquivo == 'Pdf':
           arquivo = st.file_uploader('Faça o upload do arquivo pdf:', type=['pdf'])
        if tipo_arquivo == 'Csv':
           arquivo = st.file_uploader('Faça o upload do arquivo csv:', type=['.csv'])
        if tipo_arquivo == 'Txt':
           arquivo = st.file_uploader('Faça o upload do arquivo txt:', type=['.txt'])
    with tabs[1]:
        provedor = st.selectbox('Selecione o provedor do modelo', CONFIG_MODELOS.keys())
        modelo = st.selectbox('Selecione o modelo', CONFIG_MODELOS[provedor]['modelos'])
        api_key  = st.text_input(
            f'Digite sua API key para o provedor selecionado {provedor}',
            value = st.session_state.get(f'api_key_{provedor}'))

        st.session_state[f'api_key_{provedor}'] = api_key

    # Botão estilizado
    st.markdown("""
    <style>
    .stButton>button {
        background-color: #6a0dad; /* Roxo */
        color: white;
        padding: 12px 24px;
        font-size: 16px;
        border-radius: 8px;
        border: none;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #9b30b6;
    }
    </style>
    """, unsafe_allow_html=True)
    
    if st.button('Inicializar Bebeto', use_container_width=True):
        carrega_modelo(provedor, modelo, api_key, tipo_arquivo, arquivo) 

    if st.button('Apagar Histórico de Conversa', use_container_width=True):
        st.session_state['memoria'] = MEMORIA

def main(): 
    with st.sidebar:
        sidebar()
    pagina_chat()

if __name__ == '__main__':
    main()

