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

# Adicionando alguns efeitos especiais do ponto de vista da interface do usuário
st.balloons()

# Avaliando st.chat_input e determinando se uma pergunta foi inserida
if question := st.chat_input("Digite '1' para carregar um site, '2' para carregar um PDF, '3' para carregar um vídeo do YouTube"):
    # Com o ícone do usuário, escreva a pergunta na interface
    with st.chat_message("user"):
        st.markdown(question)
    # Adicionando a pergunta e o papel (usuário) como uma mensagem ao estado da sessão
    st.session_state.messages.append(("user", question))
    
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
        if st.session_state.comando == 'site':
            st.session_state.documento = carrega_site(question)
            st.session_state.comando = ''
            st.session_state.messages.append(("assistant", "Site carregado com sucesso!"))
        elif st.session_state.comando == 'youtube':
            st.session_state.documento = carrega_youtube(question)
            st.session_state.comando = ''
            st.session_state.messages.append(("assistant", "Vídeo do YouTube carregado com sucesso!"))
        elif st.session_state.comando == 'pdf':
            st.session_state.messages.append(("assistant", "Por favor, faça o upload do documento PDF:"))
        else:
            # Respondendo como assistente com a resposta
            with st.chat_message("assistant"):
                # Garantindo que não haja mensagens presentes ao gerar a resposta
                message_placeholder = st.empty()
                # Colocando um ícone de carregamento para mostrar que a consulta está em andamento
                with st.spinner("Determinando a melhor resposta possível!"):
                    # Passando a pergunta para a função de busca, que posteriormente invoca o LLM
                    answer = resposta_bot(st.session_state.messages, st.session_state.documento)
                    # Escrevendo a resposta na interface
                    message_placeholder.markdown(f"{answer}")
            # Adicionando os resultados ao estado da sessão
            st.session_state.messages.append(("assistant", answer))

# Caixa de entrada para URLs e upload de PDF
if st.session_state.comando == 'site':
    if url := st.chat_input("Digite a URL do site:"):
        st.session_state.documento = carrega_site(url)
        st.session_state.comando = ''
        st.session_state.messages.append(("assistant", "Site carregado com sucesso!"))

if st.session_state.comando == 'youtube':
    if url := st.chat_input("Digite a URL do vídeo do YouTube:"):
        st.session_state.documento = carrega_youtube(url)
        st.session_state.comando = ''
        st.session_state.messages.append(("assistant", "Vídeo do YouTube carregado com sucesso!"))

if st.session_state.comando == 'pdf':
    uploaded_file = st.file_uploader("Escolha um arquivo PDF", type="pdf")
    if uploaded_file is not None:
        st.session_state.documento = carrega_pdf(uploaded_file)
        st.session_state.comando = ''
        st.session_state.messages.append(("assistant", "PDF carregado com sucesso!"))
