import sys
import os
import streamlit as st

# Configurazione pagina Streamlit per Mielapp
st.set_page_config(page_title="Mielapp - Mieloma Multiplo", layout="wide")

# CSS globale per ottimizzare l'interattività e ridurre i repaint superflui
st.markdown("""

""", unsafe_allow_html=True)

# Importazione del modulo di anamnesi (assicurati che il file si chiami anamnesi.py)
import anamnesi

# In futuro, quando creerai i file successivi, potrai abilitarli qui:
# import biopsia
# import followup

# Menu di navigazione laterale con brand Mielapp
st.sidebar.markdown(
    """
