import streamlit as st
import base64
from PIL import Image

st.set_page_config(page_title="📊 Educational Documents Assistant", layout="wide")

# --------- SESSION STATE INIT ---------
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'pdf_uploaded' not in st.session_state:
    st.session_state.pdf_uploaded = False


# --------- BACKGROUND IMAGE FUNCTION ---------
def add_bg_from_local(image_file):
    try:
        with open(image_file, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url(data:image/png;base64,{encoded_string});
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            .stApp::before {{
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(255, 255, 255, 0.6);
                z-index: -1;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.warning("Background image not found!")


# --------- AUTH FUNCTIONS ---------
def authenticate(username, password):
    return username == "admin" and password == "admin"


def handle_form_submit():
    st.session_state.form_username = st.session_state.username_input
    st.session_state.form_password = st.session_state.password_input
    st.session_state.form_submitted = True


def logout():
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.chat_history = []
    st.session_state.pdf_uploaded = False
    st.session_state.pop('form_submitted', None)
    st.session_state.pop('form_username', None)
    st.session_state.pop('form_password', None)


def handle_chat_submit():
    if st.session_state.user_question.strip() and st.session_state.pdf_uploaded:
        st.session_state.chat_history.append(("user", st.session_state.user_question))
        st.session_state.chat_history.append(("assistant", "Pretend I'm answering right now (AI coming next!)"))
        st.session_state.user_question = ""


# --------- LOAD ASSETS ---------
add_bg_from_local("Background3.jpg")

# --------- STYLES ---------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* Main container adjustments */
.main .block-container {
    max-width: 95% !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

/* Logo container styling */
.logo-container {
    position: absolute;
    top: 20px;
    left: 20px;
    z-index: 1000;
}

/* Headings */
h1 {
    font-size: 72px !important;
    font-weight: 800;
    text-align: center;
}

h2 {
    font-size: 50px !important;
    font-weight: 700;
    text-align: center;
}

h3 {
    font-size: 35px !important;
    margin-top: 15px !important;
}

/* Login box */
div[data-testid="stForm"] {
    width: 85%;
    max-width: 1100px;
    height: 650px;
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    margin-top: 90px;
    background-color: rgba(255, 255, 255, 0.5);
    padding: 60px 50px;
    border-radius: 25px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18);
}

/* Input labels */
div[data-testid="stTextInput"] label {
    font-size: 42px !important;
    font-weight: 700 !important;
    color: black !important;
}

/* Input fields */
input[type="text"], input[type="password"] {
    font-size: 24px !important;
    padding: 18px 14px !important;
    border-radius: 12px !important;
    border: 2px solid #ccc !important;
    background: rgba(255,255,255,0.7) !important;
    color: black !important;
    height: 60px !important;
}

/* Upload box */
section[data-testid="stFileUploader"] {
    width: 95% !important;
    margin: auto;
    padding: 25px;
    font-size: 26px;
}

/* Chat bubbles */
.user-message {
    background-color: #DCF8C6;
    padding: 15px;
    border-radius: 15px;
    margin: 8px 0;
    font-size: 22px;
}

.assistant-message {
    background-color: #FFF;
    padding: 15px;
    border-radius: 15px;
    margin: 8px 0;
    font-size: 22px;
}

/* Chat input */
div[data-testid="stTextInput"] > div > div > input {
    font-size: 22px !important;
}

/* Success/Error messages */
div[data-testid="stAlert"] p {
    font-size: 24px !important;
}

/* PDF uploaded success */
div[data-testid="stAlert-success"] p {
    font-size: 44px !important;
    font-weight: bold !important;
}

/* Caption text */
.css-1vbkxwb {
    font-size: 18px !important;
}
</style>
""", unsafe_allow_html=True)

# --------- MAIN APP STRUCTURE ---------
logo_container = st.container()
with logo_container:
    logo_col, content_col = st.columns([1, 7])
    with logo_col:
        try:
            try:
                logo = Image.open("utdlogo.png")
                st.image(logo, width=220)
            except FileNotFoundError:
                try:
                    logo = Image.open("utdlogo.jpg")
                    st.image(logo, width=220)
                except FileNotFoundError:
                    st.error("Logo file not found. Please ensure 'utdlogo.png' or 'utdlogo.jpg' exists.")
        except Exception as e:
            st.error(f"Error loading logo: {e}")

if not st.session_state.authenticated:
    st.markdown("<h1>📊 Educational Documents Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<h2>🔐 Login:</h2>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 10, 1])
    with col2:
        with st.form("login_form"):
            st.markdown("<label style='font-size:42px; font-weight:700;'>Username</label>", unsafe_allow_html=True)
            st.text_input("", key="username_input")
            st.markdown("<label style='font-size:42px; font-weight:700;'>Password</label>", unsafe_allow_html=True)
            st.text_input("", type="password", key="password_input")
            st.caption("Use 'admin' for both username and password")
            st.form_submit_button("Sign In", on_click=handle_form_submit)

    if 'form_submitted' in st.session_state and st.session_state.form_submitted:
        username = st.session_state.form_username
        password = st.session_state.form_password
        if authenticate(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password")
            st.session_state.form_submitted = False
else:
    col1, col2, col3 = st.columns([1, 5, 1])
    with col3:
        st.button("Logout", on_click=logout)

    st.markdown(f"<h2>Welcome, <span style='color:#0078ff;'>{st.session_state.username}!</span></h2>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-size:35px; margin-top:15px;'>Upload Educational Document (PDF)</h3>", unsafe_allow_html=True)

    uploaded = st.file_uploader("", type="pdf",
                                on_change=lambda: st.session_state.update({"pdf_uploaded": uploaded is not None}))

    if uploaded:
        st.success("✅ PDF Uploaded!")
        st.session_state.pdf_uploaded = True

    for role, message in st.session_state.chat_history:
        if role == "user":
            st.markdown(f'<div class="user-message">{message}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="assistant-message">{message}</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([6, 1])
    with col1:
        st.text_input("Ask a question about the report...", key="user_question", on_change=handle_chat_submit)
    with col2:
        st.button("Send", on_click=handle_chat_submit)
