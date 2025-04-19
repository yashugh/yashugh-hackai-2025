# rag_utils.py
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

def split_text(text: str):
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    return splitter.split_text(text)

def create_vector_db(chunks: list[str]):
    docs = [Document(page_content=chunk) for chunk in chunks]
    embeddings = OpenAIEmbeddings()
    return FAISS.from_documents(docs, embeddings)

def make_qa_chain(vector_db):
    llm = ChatOpenAI(model_name="gpt-3.5-turbo")
    return RetrievalQA.from_chain_type(llm=llm, retriever=vector_db.as_retriever())
