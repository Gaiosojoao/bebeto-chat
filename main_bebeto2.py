import os
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.document_loaders import WebBaseLoader
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
import PyPDF2

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

def carrega_pdf(file):
    reader = PyPDF2.PdfReader(file)
    documento = ''
    for page_num in range(len(reader.pages)):  # Usa len(reader.pages) no lugar de reader.numPages
        page = reader.pages[page_num]  # Usa reader.pages[page_num] no lugar de getPage(page_num)
        documento += page.extract_text()  # Mantém o método extract_text()
    return documento

def carrega_youtube(url):
    video_id = url.split("v=")[-1]
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt'], ['Português-Brasil'])
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
