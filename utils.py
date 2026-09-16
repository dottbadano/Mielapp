import streamlit as st

def render_header_brand():
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("🩸 Myel-UP DSS")
        st.markdown("**Decision Support System per la Gestione Clinica del Mieloma Multiplo** (Linee Guida IMWG / NCCN)")
    with col2:
        st.markdown(
            """
st.markdown(
        f"""
            st.markdown(
        f"""
        <div style="padding: 12px 18px; background-color: #e8f4fd; border-left: 5px solid #0d6efd; border-radius: 4px; margin-bottom: 20px;">
            <span style="font-size: 14px; color: #084298;"><b>Paziente in carico:</b> {cognome} {nome} (ID: <b>{id_univoco}</b>)</span><br>
            <span style="font-size: 13px; color: #333;">
                Età: <b>{eta} anni</b> | 
                ECOG PS: <b>{ecog}</b> | 
                Charlson Comorbidity Index: <b>{charlson}</b> | 
                G8 Geriatric Score: <b>{g8}</b>
            </span>
        </div>
        """,
        unsafe_allow_html=True
                def genera_struttura_referto_unificato(moduli_per_report):
    header_referto = (
        "==================================================\n"
        "             MYEL-UP CLINICAL REPORT             \n"
        "   Decision Support System - Mieloma Multiplo     \n"
        "==================================================\n\n"
    )
    
    corpo_referto = ""
    for titolo_sezione, contenuto_testuale in moduli_per_report.items():
        corpo_referto += f"--- {titolo_sezione.upper()} ---\n"
        corpo_referto += f"{contenuto_testuale}\n\n"
        
    footer_referto = (
        "==================================================\n"
        "  Report generato automaticamente tramite Myel-UP  \n"
        "  Conforme agli standard IMWG / NCCN            \n"
        "=================================================="
    )
    
    return header_referto + corpo_referto + footer_referto
    )
