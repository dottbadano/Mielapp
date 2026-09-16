import streamlit as st

def render_header_brand():
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("🩸 Myel-UP DSS")
        st.markdown("**Decision Support System per la Gestione Clinica del Mieloma Multiplo** (Linee Guida IMWG / NCCN)")
    with col2:
        st.markdown(
            """
