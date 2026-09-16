import streamlit as st
from datetime import datetime

def render_header_brand():
    """
    Rende l'intestazione brandizzata di Myel-UP in alto a destra:
    - 'M' in giallo miele, 'yel-UP' in nero.
    - Box elegante con bordi sfumati/arrotondati.
    - '2' di 2getus in rosso e 'getus s.r.l.' in nero.
    """
    st.markdown(
        """""",
    unsafe_allow_html=True
)st.markdown(
    f"""""",
    unsafe_allow_html=True
)header_documento = (
    "==================================================\n"
    "             MYEL-UP - REPORT CLINICO             \n"
    "           engineered by 2getus s.r.l.            \n"
    f"   Data generazione: {data_corrente}             \n"
    "==================================================\n\n"
)

documento_completo = header_documento
for nome_modulo, testo_modulo in selezioni_moduli_testo.items():
    if testo_modulo:
        documento_completo += f"--- [{nome_modulo.upper()}] ---\n{testo_modulo}\n\n"
        
return documento_completo
