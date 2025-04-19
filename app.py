import streamlit as st
import hashlib
import pickle
import os
from pathlib import Path

# Configure page
st.set_page_config(page_title="📊 Annual Report Assistant", layout="centered")

# Initialize session state variables
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# Apply theme based on current selection
def apply_theme():
    if st.session_state.theme == 'dark':
        # Dark theme with improved text visibility
        st.markdown("""
        <style>
        .main {
            background-color: #121212;
            color: #FFFFFF !important;
        }
        .stApp {
            background-color: #121212;
        }
        .stTextInput > div > div > input {
            background-color: #2E2E2E;
            color: #FFFFFF;
        }
        .stButton > button {
            background-color: #0E86D4;
            color: white;
        }
        /* Ensure text elements have proper contrast */
        p, h1, h2, h3, span, label, .stMarkdown, .stText {
            color: #FFFFFF !important;
        }
        
        /* File uploader specific styling */
        .stFileUploader label {
            color: #FFFFFF !important;
        }
        .stFileUploader div[data-testid="stFileUploaderDropzone"] {
            background-color: #2E2E2E;
            border-color: #4E4E4E;
        }
        .stFileUploader div[data-testid="stFileUploaderDropzone"] p {
            color: #FFFFFF !important;
        }
        .stFileUploader div[data-testid="stFileUploaderStatusWidget"] {
            background-color: #2E2E2E;
        }
        .stFileUploader div[data-testid="stFileUploaderStatusWidget"] p {
            color: #FFFFFF !important;
        }
        
        /* Login form styling */
        .stForm {
            background-color: #1E1E1E;
            padding: 20px;
            border-radius: 10px;
        }
        
        /* Success message text fix but preserve background */
        .element-container .stAlert.success {
            background-color: rgba(0, 168, 107, 0.2);
        }
        .element-container .stAlert.success div {
            color: #FFFFFF !important;
        }
        
        .stMarkdown a {
            color: #8AB4F8 !important;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        # Light theme (default)
        st.markdown("""
        <style>
        .main {
            background-color: #FFFFFF;
            color: #31333F;
        }
        .stApp {
            background-color: #FFFFFF;
        }
        p, h1, h2, h3, span, label {
            color: #31333F !important;
        }
        /* Login form styling */
        .stForm {
            background-color: #F0F2F6;
            padding: 20px;
            border-radius: 10px;
        }
        </style>
        """, unsafe_allow_html=True)

# Function to toggle theme
def toggle_theme():
    if st.session_state.theme == 'light':
        st.session_state.theme = 'dark'
    else:
        st.session_state.theme = 'light'

# Authentication function (hardcoded for testing)
def authenticate(username, password):
    # Hardcoded credentials for testing
    if username == "admin" and password == "admin":
        return True
    return False

# Function to handle form submission - store username and password in session state
def handle_form_submit():
    st.session_state.form_username = st.session_state.username_input
    st.session_state.form_password = st.session_state.password_input
    st.session_state.form_submitted = True

# Function to logout
def logout():
    st.session_state.authenticated = False
    st.session_state.username = ""
    if 'form_submitted' in st.session_state:
        st.session_state.form_submitted = False
    if 'form_username' in st.session_state:
        del st.session_state.form_username
    if 'form_password' in st.session_state:
        del st.session_state.form_password

# Apply the theme CSS
apply_theme()

# Main application
if not st.session_state.authenticated:
    # LOGIN PAGE
    
    # Add theme toggle button at the top right
    col1, col2 = st.columns([3, 1])
    with col2:
        current_theme = "🌙 Dark" if st.session_state.theme == 'light' else "☀️ Light"
        st.button(current_theme, on_click=toggle_theme, key="theme_toggle")
    
    # Login interface
    st.title("📊 Annual Report Assistant")
    st.subheader("Login")
    
    # Create a centered login form with some padding
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            st.text_input("Username", key="username_input")
            st.text_input("Password", type="password", key="password_input")
            
            # Hint for testing
            st.caption("Use 'admin' for both username and password")
            
            submitted = st.form_submit_button("Sign In", on_click=handle_form_submit)
        
        # Process login outside the form
        if 'form_submitted' in st.session_state and st.session_state.form_submitted:
            username = st.session_state.form_username
            password = st.session_state.form_password
            
            if authenticate(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.form_submitted = False
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password")
                st.session_state.form_submitted = False
            
else:
    # HOME PAGE
    
    # Add theme toggle and logout buttons at the top
    header = st.container()
    with header:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            current_theme = "🌙 Dark" if st.session_state.theme == 'light' else "☀️ Light"
            st.button(current_theme, on_click=toggle_theme, key="theme_toggle")
        with col3:
            st.button("Logout", on_click=logout)
    
    # Main app content
    st.title("📊 Annual Report RAG Assistant")
    st.write(f"Welcome, {st.session_state.username}!")
    
    uploaded = st.file_uploader("Upload an Annual Report PDF", type="pdf")
    
    if uploaded:
        st.success("✅ PDF Uploaded!")
        
        question = st.text_input("Ask a question about the report:")
        
        if question:
            st.write("You asked:", question)
            st.write("Pretend I'm answering right now (AI coming next!)")