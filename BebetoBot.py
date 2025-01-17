import streamlit as st
from main_bebeto2 import carrega_site, carrega_pdf, carrega_youtube, resposta_bot

# Título do aplicativo Streamlit
st.cache_data.clear()
st.cache_resource.clear()

st.title(f""":rainbow[BebetoBot 🤙🏻]""")

# Configuração inicial do estado da sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

if "documento" not in st.session_state:
    st.session_state.documento = ""

if "comando" not in st.session_state:
    st.session_state.comando = ""

# Exibir mensagens do histórico de conversação
st.markdown('<div class="content">', unsafe_allow_html=True)
for role, content in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(content)
st.markdown('</div>', unsafe_allow_html=True)

# Caixa de entrada para mensagens do usuário
if question := st.chat_input("Digite '1' para carregar um site, '2' para carregar um PDF, '3' para carregar um vídeo do YouTube, ou faça uma pergunta!"):
    with st.chat_message("user"):
        st.markdown(question)
    st.session_state.messages.append(("user", question))  # Adiciona mensagem do usuário ao histórico

    # Processar comando inicial ou interações com base no estado do comando
    if st.session_state.comando == '':
        if question == '1':
            st.session_state.comando = 'site'
            st.session_state.messages.append(("assistant", "Digite a URL do site aqui:"))
        elif question == '2':
            st.session_state.comando = 'pdf'
            st.session_state.messages.append(("assistant", "Faça o upload do documento PDF:"))
        elif question == '3':
            st.session_state.comando = 'youtube'
            st.session_state.messages.append(("assistant", "Digite a URL do vídeo do YouTube aqui:"))
        else:
            # Resposta do chatbot para perguntas gerais
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                with st.spinner("Determinando a melhor resposta possível..."):
                    answer = resposta_bot(st.session_state.messages, st.session_state.documento)
                    message_placeholder.markdown(f"{answer}")
                st.session_state.messages.append(("assistant", answer))
    else:
        # Processar comandos específicos
        if st.session_state.comando == 'site':
            st.session_state.documento = carrega_site(question)
            st.session_state.messages.append(("assistant", "Site carregado com sucesso! Você pode fazer perguntas sobre ele agora."))
        elif st.session_state.comando == 'youtube':
            st.session_state.documento = carrega_youtube(question)
            st.session_state.messages.append(("assistant", "Vídeo do YouTube carregado com sucesso! Você pode fazer perguntas sobre ele agora."))
        elif st.session_state.comando == 'pdf':
            st.session_state.messages.append(("assistant", "Por favor, faça o upload do documento PDF utilizando o botão abaixo."))
        st.session_state.comando = ''  # Reseta o comando após o processamento

# Gerenciar upload de PDF
if st.session_state.comando == 'pdf':
    uploaded_file = st.file_uploader("Escolha um arquivo PDF", type="pdf")
    if uploaded_file is not None:
        st.session_state.documento = carrega_pdf(uploaded_file)
        st.session_state.messages.append(("assistant", "PDF carregado com sucesso! Você pode fazer perguntas sobre ele agora."))
        st.session_state.comando = ''  # Reseta o comando

