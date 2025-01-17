import streamlit as st
from main_bebeto2 import carrega_site, carrega_pdf, carrega_youtube, resposta_bot

# Título do aplicativo Streamlit
st.cache_data.clear()
st.cache_resource.clear()

st.title(f""":rainbow[BebetoBot 🤙🏻]""")

# Limpar cache de dados e recursos
st.cache_data.clear()
st.cache_resource.clear()

# Configurando valores para o estado da sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

if "documento" not in st.session_state:
    st.session_state.documento = ""

if "comando" not in st.session_state:
    st.session_state.comando = ""

# Exibir mensagens
st.markdown('<div class="content">', unsafe_allow_html=True)
for role, content in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(content)
st.markdown('</div>', unsafe_allow_html=True)

# Avaliando st.chat_input e determinando se uma pergunta foi inserida
if question := st.chat_input("Digite '1' para carregar um site, '2' para carregar um PDF, '3' para carregar um vídeo do YouTube"):
    # Com o ícone do usuário, escreva a pergunta na interface
    with st.chat_message("user"):
        st.markdown(question)
    # Adicionando a pergunta e o papel (usuário) como uma mensagem ao estado da sessão
    st.session_state.messages.append(("user", question))
    
    # Verifica o estado do comando
    if st.session_state.comando == '':
        if question == '1':
            st.session_state.comando = 'site'
            st.session_state.messages.append(("assistant", "Digite a URL do site:"))
        elif question == '2':
            st.session_state.comando = 'pdf'
            st.session_state.messages.append(("assistant", "Faça o upload do documento PDF:"))
        elif question == '3':
            st.session_state.comando = 'youtube'
            st.session_state.messages.append(("assistant", "Digite a URL do vídeo do YouTube:"))
        else:
            st.session_state.messages.append(("assistant", "Opção inválida! Por favor, digite '1', '2' ou '3'."))
    else:
        # Processa o comando selecionado anteriormente
        if st.session_state.comando == 'site':
            st.session_state.documento = carrega_site(question)
            st.session_state.messages.append(("assistant", "Site carregado com sucesso!"))
        elif st.session_state.comando == 'youtube':
            st.session_state.documento = carrega_youtube(question)
            st.session_state.messages.append(("assistant", "Vídeo do YouTube carregado com sucesso!"))
        elif st.session_state.comando == 'pdf':
            st.session_state.messages.append(("assistant", "Por favor, faça o upload do documento PDF usando o botão abaixo."))
        st.session_state.comando = ''

# Adiciona suporte para upload de PDF
if st.session_state.comando == 'pdf':
    uploaded_file = st.file_uploader("Escolha um arquivo PDF", type="pdf")
    if uploaded_file is not None:
        st.session_state.documento = carrega_pdf(uploaded_file)
        st.session_state.messages.append(("assistant", "PDF carregado com sucesso!"))
        st.session_state.comando = ''

