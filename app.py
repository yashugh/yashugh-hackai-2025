# -----------------------------
# FILE: app.py (frontend + interaction)
# -----------------------------
import streamlit as st
import os
from pathlib import Path
from pdf_utils import extract_text_from_pdf
from rag_utils import process_query

st.set_page_config(page_title="📊 Annual Report Assistant", layout="centered")

# Session state initialization
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# Theme toggle styling
def apply_theme():
    if st.session_state.theme == 'dark':
        st.markdown("""
        <style>
        .main, .stApp { background-color: #121212; color: #FFFFFF !important; }
        .stTextInput > div > div > input { background-color: #2E2E2E; color: #FFFFFF; }
        .stButton > button { background-color: #0E86D4; color: white; }
        .stForm { background-color: #1E1E1E; padding: 20px; border-radius: 10px; }
        .element-container .stAlert.success { background-color: rgba(0, 168, 107, 0.2); }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        .main, .stApp { background-color: #FFFFFF; color: #31333F; }
        .stForm { background-color: #F0F2F6; padding: 20px; border-radius: 10px; }
        </style>
        """, unsafe_allow_html=True)

def toggle_theme():
    st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'

def authenticate(username, password):
    return username == "admin" and password == "admin"

def handle_form_submit():
    st.session_state.form_username = st.session_state.username_input
    st.session_state.form_password = st.session_state.password_input
    st.session_state.form_submitted = True

def logout():
    st.session_state.authenticated = False
    st.session_state.username = ""
    for key in ['form_submitted', 'form_username', 'form_password']:
        st.session_state.pop(key, None)

apply_theme()

if not st.session_state.authenticated:
    col1, col2 = st.columns([3, 1])
    with col2:
        current_theme = "🌙 Dark" if st.session_state.theme == 'light' else "☀️ Light"
        st.button(current_theme, on_click=toggle_theme, key="theme_toggle")

    st.title("📊 Annual Report Assistant")
    st.subheader("Login")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            st.text_input("Username", key="username_input")
            st.text_input("Password", type="password", key="password_input")
            st.caption("Use 'admin' for both username and password")
            st.form_submit_button("Sign In", on_click=handle_form_submit)

        if st.session_state.get('form_submitted', False):
            if authenticate(st.session_state.form_username, st.session_state.form_password):
                st.session_state.authenticated = True
                st.session_state.username = st.session_state.form_username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password")
                st.session_state.form_submitted = False

else:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        current_theme = "🌙 Dark" if st.session_state.theme == 'light' else "☀️ Light"
        st.button(current_theme, on_click=toggle_theme, key="theme_toggle")
    with col3:
        st.button("Logout", on_click=logout)

    st.title("📊 Annual Report RAG Assistant")
    st.write(f"Welcome, {st.session_state.username}!")

    uploaded = st.file_uploader("Upload an Annual Report PDF", type="pdf")

    if uploaded:
        st.success("✅ PDF Uploaded!")
        pdf_text = extract_text_from_pdf(uploaded)

        question = st.text_input("Ask a question about the report:")
        if question:
            with st.spinner("Thinking..."):
                response = process_query(pdf_text, question)
                st.write("You asked:", question)
                st.success(response)


# -----------------------------
# FILE: pdf_utils.py (PDF extraction)
# -----------------------------
def extract_text_from_pdf(uploaded_file):
    from PyPDF2 import PdfReader
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


# -----------------------------
# FILE: rag_utils.py (backend RAG)
# -----------------------------
def process_query(text, query):
    from langchain.text_splitter import CharacterTextSplitter
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.vectorstores import FAISS
    from langchain.chat_models import ChatOpenAI
    from langchain.chains.question_answering import load_qa_chain
    import os

    os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")  # Make sure it's set in .env

    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_text(text)

    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_texts(chunks, embeddings)

    relevant_docs = vector_store.similarity_search(query)

    llm = ChatOpenAI(temperature=0)
    chain = load_qa_chain(llm, chain_type="stuff")
    response = chain.run(input_documents=relevant_docs, question=query)
    return response

