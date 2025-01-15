import streamlit as st
from main_chatbot import resposta_bot

# Título streamlit app
st.cache_data.clear()
st.cache_resource.clear()

st.title(f""":rainbow[BebetoBot 🤙🏻]""")

# Limpar cache de dados e recursos
st.cache_data.clear()
st.cache_resource.clear()

# Configurando valores para o estado da sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir mensagens
st.markdown('<div class="content">', unsafe_allow_html=True)
for role, content in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(content)
st.markdown('</div>', unsafe_allow_html=True)

# Adicionando alguns efeitos especiais do ponto de vista da interface do usuário
st.balloons()

# Avaliando st.chat_input e determinando se uma pergunta foi inserida
if question := st.chat_input("Faça uma pergunta ao BebetoBot"):
    # Com o ícone do usuário, escreva a pergunta na interface
    with st.chat_message("user"):
        st.markdown(question)
    # Adicionando a pergunta e o papel (usuário) como uma mensagem ao estado da sessão
    st.session_state.messages.append(("user", question))
    # Respondendo como assistente com a resposta
    with st.chat_message("assistant"):
        # Garantindo que não haja mensagens presentes ao gerar a resposta
        message_placeholder = st.empty()
        # Colocando um ícone de carregamento para mostrar que a consulta está em andamento
        with st.spinner("Determinando a melhor resposta possível!"):
            # Passando a pergunta para a função de busca, que posteriormente invoca o LLM
            answer = resposta_bot(st.session_state.messages)
            # Escrevendo a resposta na interface
            message_placeholder.markdown(f"{answer}")
    # Adicionando os resultados ao estado da sessão
    st.session_state.messages.append(("assistant", answer))