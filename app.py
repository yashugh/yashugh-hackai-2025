# -----------------------------
# FILE: app.py
# -----------------------------
import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv
from pdf_utils import extract_text_and_tables_from_pdf
from rag_utils import process_query

load_dotenv()

st.set_page_config(page_title="📊 Annual Report Assistant", layout="centered")

if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = ""

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
        pdf_text, pdf_tables = extract_text_and_tables_from_pdf(uploaded)

        if pdf_tables:
            with st.expander("📋 Detected Tables"):
                for idx, table in enumerate(pdf_tables):
                    st.code(table, language="text")

        question = st.text_input("Ask a question about the report:")
        if question:
            with st.spinner("Thinking..."):
                response = process_query(pdf_text + "\n" + "\n".join(pdf_tables), question)
                st.write("You asked:", question)
                st.success(response)




