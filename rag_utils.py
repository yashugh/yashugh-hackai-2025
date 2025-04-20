# -----------------------------
# FILE: rag_utils.py
# -----------------------------
def process_query(text, query):
    from langchain.text_splitter import CharacterTextSplitter
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.vectorstores import FAISS
    from langchain.chat_models import ChatOpenAI
    from langchain.chains.question_answering import load_qa_chain
    import os

    os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_text(text)

    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_texts(chunks, embeddings)

    relevant_docs = vector_store.similarity_search(query)

    llm = ChatOpenAI(temperature=0)
    chain = load_qa_chain(llm, chain_type="stuff")
    response = chain.run(input_documents=relevant_docs, question=query)
    return response



