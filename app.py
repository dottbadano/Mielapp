import sys
import os
import streamlit as st

# Configurazione della pagina Streamlit
st.set_page_config(
    page_title="Mielapp - Mieloma Multiplo", 
    page_layout="wide",
    initial_sidebar_state="expanded"
)

# CSS globale per ottimizzare i componenti dell'interfaccia
st.markdown("""

""", unsafe_allow_html=True)

# Tentativo sicuro di importazione del modulo anamnesi
try:
    import anamnesi
    MODULO_ANAMNESI_DISPONIBILE = True
except ImportError:
    MODULO_ANAMNESI_DISPONIBILE = False

# --- BARRA LATERALE (MENU DI NAVIGAZIONE) ---
st.sidebar.markdown(
    """
