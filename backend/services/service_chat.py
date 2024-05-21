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

_ = load_dotenv(find_dotenv())

# 1. 이력서(pdf) -> resume.pdf
# 2. platform.openai.com -> api_key 가져오기

# llm 모델 생성(api_key, default: gpt-3.5-turbo)
llm = ChatOpenAI(
  api_key = os.getenv("OPENAI_API_KEY"),
  temperature=0.1
)
# 메모리 생성 -> 기본적으로 대화내용을 저장하지 않음
#               대화가 단절, -> 기존의 대화내용을 메모리에 저장하고
#               저장한 내용을 LLM모델에 질문할 때 함께 전달
# ConversationSummaryBufferMemory
# -> 대화기록을 모두 저장하면 좋지만 비효율적
# -> Max_token_limit까지는 모든 기록을 저장하고
#   limit가 넘어가면 요약해서 저장

memory = ConversationSummaryBufferMemory(
  llm=llm,
  max_token_limit=120.
  memory_key="chat_history",
  return_messages=True,
)


class ChatService:
  def send_chat(self, chat):
    # 사용자 질문
    question = chat["question"]

    # 1. Chroma DB 확인(Vector DB 유무 체크)
    if not os.path.isdir("./llm/chroma_db"):
        self.gen_chroma_vector()  # Vector DB 생성
    
    # 2. Chrom DB 가져오기
    db = Chroma(persist_directory="./llm/chroma_db", embedding_function=OpenAIEmbeddings())

    # 3. Semactic Search
    retriever = db.as_retriever(
       search_type="similarity",    # 코사인 유사도
       search_kwargs={
          "k":3,                    # 유사도가 가장 높은 3개만 추출
       }
    )

    # 4.Prompt
    # 4-1 System Prompt
    # 신기술(DARE PROMPT)
    qa_system_prompt = """
      지금부터 모든 답변은 한글로 출력해줘.
      너는 사용자 질문에 답변을 하는 일을 할거야.
      주어진 내용은 "김선형"이라는 인물의 정보야.
      너가 "김선형"의 입장에서 답변을 해줘.
      질문에 답변을 할 때 전달받은 내용만 사용해서 답변을 해줘.
      모르는 경우 모른다고 답변하고, 만들어서 답변하지마.
      :\n\n{context}
    """

    # 4-2. Prompt 생성
    # 1. System Prompt(역할 정의)
    # 2. Vector DB에서 검색한 내용(유사한)
    # 3. 메모리(이전 대화기록)
    # 4. 사용자 질문
    prompt = ChatPromptTemplate.from_messages(
       [
          ("system", qa_system_prompt),
          MessagesPlaceholder(variable_name="chat_history"),
          ("human", "{question}")
       ]
    )

    def load_memory(_):
       return memory.load_memory_variables({})["chat_history"]





  # 이력서(resume.pdf) -> Vector DB에 저장
  def gen_chroma_vector(self):
     # PDF 파일 불러오기
     loader = PyPDFLoader("./static/downloads/resume.pdf")
   
    # Chunk(block) 단위오 Split(쪼개기)
     text_splitter = RecursiveCharacterTextSplitter(
       chunk_size=1000,
       chunk_overlap=200
    )
  
     docs = loader.load_and_split(text_splitter)
  
    # 임베딩 -> 형태소를 숫자로 표현
    # ex) 5차원 텍스트 임베딩
    #     dog : 0.3.0.7 1.5 59 32
     embeddings = OpenAIEmbeddings()
  
cache_dir = LocalFileStore("./.cache/")
cached_embeddings = CacheBackedEmbeddings.from_bytes_store(embeddings, cache_dir)
vectorstore = Chroma.from_documents(docs, cached_embeddings)

directory = "./llm/chroma_db"
vector_index = Chroma.from_documents(
   docs,
   OpenAIEmbeddings(),
   persist_directory=directory
)
vector_index.persist()

