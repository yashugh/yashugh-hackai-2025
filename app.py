import streamlit as st

st.set_page_config(page_title="📊 Annual Report Assistant")

st.title("📊 Annual Report RAG Assistant")

uploaded = st.file_uploader("Upload an Annual Report PDF", type="pdf")

if uploaded:
    st.success("✅ PDF Uploaded!")

    question = st.text_input("Ask a question about the report:")

    if question:
        st.write("You asked:", question)
        st.write("Pretend I'm answering right now (AI coming next!)")
