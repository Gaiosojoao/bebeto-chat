import os
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

api_key = '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'
os.environ['GROQ_API_KEY'] = api_key

chat = ChatGroq(model='llama-3.1-70b-versatile')

def resposta_bot(mensagens):
    mensagens_modelo = [('system', 'Você é um assistente amigável chamado Bebeto')]
    mensagens_modelo += mensagens
    template = ChatPromptTemplate.from_messages(mensagens_modelo)
    chain = template | chat
    return chain.invoke({}).content