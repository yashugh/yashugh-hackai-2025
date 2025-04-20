
import streamlit as st
import base64
from PIL import Image

st.set_page_config(page_title="📊 Annual Report Assistant", layout="wide")

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
add_bg_from_local("background2.jpg")

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
    font-size: 72px !important;  /* Increased from 60px */
    font-weight: 800;
    text-align: center;
}

h2 {
    font-size: 50px !important;  /* Increased from 40px */
    font-weight: 700;
    text-align: center;
}

h3 {
    font-size: 35px !important;  /* Increased from 28px */
    margin-top: 15px !important;
}

/* Login box */
div[data-testid="stForm"] {
    width: 85%;  /* Increased from 80% */
    max-width: 1100px;  /* Increased from 1000px */
    height: 650px;  /* Increased from 550px */
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    margin-top: 90px;
    background-color: rgba(255, 255, 255, 0.5);
    padding: 60px 50px;  /* Increased padding */
    border-radius: 25px;  /* Increased from 20px */
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18);  /* Enhanced shadow */
}

/* Input labels */
div[data-testid="stTextInput"] label {
    font-size: 28px !important;  /* Increased from 22px */
    font-weight: 600 !important;
    color: black !important;
}

/* Input fields */
input[type="text"], input[type="password"] {
    font-size: 24px !important;  /* Increased from 18px */
    padding: 18px 14px !important;  /* Increased padding */
    border-radius: 12px !important;  /* Increased radius */
    border: 2px solid #ccc !important;  /* Increased border */
    background: rgba(255,255,255,0.7) !important;
    color: black !important;
    height: 60px !important;  /* Added height */
}

/* Upload box */
section[data-testid="stFileUploader"] {
    width: 95% !important;
    margin: auto;
    padding: 25px;  /* Increased from 20px */
    font-size: 26px;  /* Increased from 22px */
}

/* Chat bubbles */
.user-message {
    background-color: #DCF8C6;
    padding: 15px;  /* Increased from 10px */
    border-radius: 15px;  /* Increased from 10px */
    margin: 8px 0;  /* Increased from 5px */
    font-size: 22px;  /* Added font size */
}

.assistant-message {
    background-color: #FFF;
    padding: 15px;  /* Increased from 10px */
    border-radius: 15px;  /* Increased from 10px */
    margin: 8px 0;  /* Increased from 5px */
    font-size: 22px;  /* Added font size */
}

/* Chat input */
div[data-testid="stTextInput"] > div > div > input {
    font-size: 22px !important;  /* Increased font size */
}

/* Logout Button */
div.stButton > button {
    font-size: 26px !important;  /* Increased from 22px */
    padding: 16px 35px !important;  /* Increased padding */
    border-radius: 12px !important;  /* Increased radius */
    background-color: #ff4b4b !important;
    color: white !important;
    font-weight: 600 !important;
}

div.stButton > button:hover {
    background-color: #cc0000 !important;
}

/* Success/Error messages */
div[data-testid="stAlert"] p {
    font-size: 24px !important;  /* Increased font size */
}

/* Caption text */
.css-1vbkxwb {
    font-size: 18px !important;  /* Increased caption font size */
}
</style>
""", unsafe_allow_html=True)

# --------- MAIN APP STRUCTURE ---------
# Create a container for the logo that will appear at the top of every page
logo_container = st.container()
with logo_container:
    # Create two columns - smaller ratio for the logo to make it bigger visually
    logo_col, content_col = st.columns([1, 7])
    with logo_col:
        try:
            # Try to load the logo with both extensions
            try:
                logo = Image.open("TarkFinance.png")
                st.image(logo, width=220)  # Increased from 180
            except FileNotFoundError:
                try:
                    logo = Image.open("TarkFinance.jpg")
                    st.image(logo, width=220)  # Increased from 180
                except FileNotFoundError:
                    st.error("Logo file not found. Please ensure 'TarkFinance.png' or 'TarkFinance.jpg' exists.")
        except Exception as e:
            st.error(f"Error loading logo: {e}")

# Continue with the rest of the app
if not st.session_state.authenticated:
    st.markdown("<h1>📊 Financial Report Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<h2>🔐 Login:</h2>", unsafe_allow_html=True)

    # Wider login form with fewer empty columns on sides
    col1, col2, col3 = st.columns([1, 10, 1])
    with col2:
        with st.form("login_form"):
            st.markdown("<label style='font-size:42px; font-weight:700;'>Username</label>",
                        unsafe_allow_html=True)  # Increased from 36px
            st.text_input("", key="username_input")
            st.markdown("<label style='font-size:42px; font-weight:700;'>Password</label>",
                        unsafe_allow_html=True)  # Increased from 36px
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
    # Adjusted column ratios to make content wider
    col1, col2, col3 = st.columns([1, 5, 1])
    with col3:
        st.button("Logout", on_click=logout)

    st.markdown(f"<h2>Welcome, <span style='color:#0078ff;'>{st.session_state.username}!</span></h2>",
                unsafe_allow_html=True)
    st.markdown("<h3 style='font-size:35px; margin-top:15px;'>Upload Financial Reports (PDF)</h3>", unsafe_allow_html=True)

    uploaded = st.file_uploader("", type="pdf",
                                on_change=lambda: st.session_state.update({"pdf_uploaded": uploaded is not None}))

    if uploaded:
        st.success("✅ PDF Uploaded!")
        st.session_state.pdf_uploaded = True

    for role, message in st.session_state.chat_history:
        if role == "user":
            st.markdown(
                f'<div class="user-message">{message}</div>',
                unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div class="assistant-message">{message}</div>',
                unsafe_allow_html=True)

    # Wider chat input with 6:1 ratio instead of 5:1
    col1, col2 = st.columns([6, 1])
    with col1:
        st.text_input("Ask a question about the report...", key="user_question", on_change=handle_chat_submit)
    with col2:
        st.button("Send", on_click=handle_chat_submit)