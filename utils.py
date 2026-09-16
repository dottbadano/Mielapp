Python
import streamlit as st

def render_header_brand():
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("🩸 Myel-UP DSS")
        st.markdown("**Decision Support System per la Gestione Clinica del Mieloma Multiplo** (Linee Guida IMWG / NCCN)")
    with col2:
        st.markdown(
            """
Versione App


v3.5 - Cloud

        """,
        unsafe_allow_html=True
    )
st.markdown("---")
def crea_box_paziente_corrente(paziente_info):
nome = paziente_info.get("nome", "N/D")
cognome = paziente_info.get("cognome", "N/D")
id_univoco = paziente_info.get("id_univoco", "MM-0001")
eta = paziente_info.get("eta", "N/D")
ecog = paziente_info.get("ecog", "N/D")
charlson = paziente_info.get("charlson_score", "N/D")
g8 = paziente_info.get("g8_score", "N/D")

st.markdown(
    f"""
Paziente in carico: {cognome} {nome} (ID: {id_univoco})


Età: {eta} anni |
ECOG PS: {ecog} |
Charlson Comorbidity Index: {charlson} |
G8 Geriatric Score: {g8}

    """,
    unsafe_allow_html=True
)
def genera_struttura_referto_unificato(moduli_per_report):
header_referto = (
"\n"
"             MYEL-UP CLINICAL REPORT             \n"
"   Decision Support System - Mieloma Multiplo     \n"
"\n\n"
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
