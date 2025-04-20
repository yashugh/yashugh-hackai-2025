# -----------------------------
# FILE: rag_utils.py
# -----------------------------
def process_query(text, query):
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.vectorstores import FAISS
    from langchain.chat_models import ChatOpenAI
    from langchain.chains import RetrievalQA
    from langchain.prompts import PromptTemplate
    import os

    # Hardcoded API key (Note: this is not a best practice but required as specified)
    #os.environ['OPENAI_API_KEY'] = api_key

    try:
        # Improved text splitter for better chunking
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        chunks = text_splitter.split_text(text)
        
        # Create embeddings and vector store
        embeddings = OpenAIEmbeddings()
        vector_store = FAISS.from_texts(chunks, embeddings)
        
        # Create a retrieval system that only gets the most relevant chunks
        retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}  # Only retrieve the 5 most relevant chunks
        )
        
        # Create a custom prompt template that includes the query context
        prompt_template = """You are an Annual Report Assistant analyzing financial documents.
        Use the following context to answer the question.
        
        Context:
        {context}
        
        Question: {question}
        
        Answer the question based only on the provided context. If the context doesn't contain 
        the information needed to answer the question, just say "I don't have enough information 
        in this report to answer that question." Be specific and include relevant financial data 
        when available.
        """
        
        PROMPT = PromptTemplate(
            template=prompt_template, 
            input_variables=["context", "question"]
        )
        
        # Setup the QA chain with the custom prompt
        llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=False,
            chain_type_kwargs={"prompt": PROMPT}
        )
        
        # Get the answer
        result = qa_chain({"query": query})
        return result["result"]
        
    except Exception as e:
        return f"I encountered an error processing your question: {str(e)}. Please try uploading a smaller document or asking a more specific question about a particular section of the report."