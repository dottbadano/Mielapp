import streamlit as st
import anamnesi  # Modulo di anagrafica, anamnesi ed emocromo avanzato

# Configurazione della pagina (deve essere il primo comando Streamlit)
st.set_page_config(
    page_title="2gether - Decision Support System",
    page_icon="🩺",
    layout="wide"
)

# Iniezione di CSS personalizzato per il posizionamento e lo stile del logo in alto a destra
st.markdown(
    """
