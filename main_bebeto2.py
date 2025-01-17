import os
from langchain-groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.document_loaders import WebBaseLoader
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound

api_key = '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'
os.environ['GROQ_API_KEY'] = api_key

chat = ChatGroq(model='llama-3.1-70b-versatile')

def carrega_site(url):
    loader = WebBaseLoader(url)
    lista_documentos = loader.load()
    documento = ''
    for doc in lista_documentos:
        documento += doc.page_content
    return documento

def carrega_pdf():
    # Função para carregar conteúdo de um PDF
    # Substitua este código pelo código real para carregar o conteúdo do PDF
    return "Conteúdo do PDF"

def carrega_youtube(url):
    video_id = url.split("v=")[-1]
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt'])
    except NoTranscriptFound:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'pt-PT'])
    documento = ' '.join([item['text'] for item in transcript])
    return documento

def resposta_bot(mensagens, documento):
    mensagem_system = '''Você é um assistente amigável chamado Bebeto.
    Você utiliza as seguintes informações para formular suas respostas: {informacoes}'''
    mensagens_modelo = [('system', mensagem_system)]
    mensagens_modelo += mensagens
    template = ChatPromptTemplate.from_messages(mensagens_modelo)
    chain = template | chat
    return chain.invoke({'informacoes': documento}).content
