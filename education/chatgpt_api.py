from dotenv import load_dotenv, find_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationSummaryBufferMemory
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.runnable import RunnablePassthrough


        # PDF 파일 불러오기
loader=PyPDFLoader("./static/download/resume.pdf")
docs=loader.load()
print(len(docs))
print(docs[0])
exit()

# Chunk(block) 단위로 Split(쪼개기)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
       
docs = loader.load_and_split(text_splitter)
print(docs[0])

exit()
