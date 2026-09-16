from datetime import datetime
import random
import string
import re
import streamlit as st

try:
    from pypdf import PdfReader
    PYPDF_DISPONIBILE = True
except ImportError:
    PYPDF_DISPONIBILE = False

def genera_codice_univoco_organo(nome, cognome, organo_lettera="MM"):
    n = nome.strip()
    c = cognome.strip()
    if len(n) < 2 or len(c) < 2:
        return ""

    return f"{n[0].upper()}{c[1].upper()}{c[0].upper()}{n[1].upper()}-{''.join(random.choices(string.digits, k=6))}-{organo_lettera.upper()[:2]}"

def stima_aspettativa_di_vita(eta, charlson_score, g8_score, ecog_str):
    """
    Calcola l'aspettativa di vita ponderando comorbilità (Charlson), 
    stato geriatrico (G8) e performance fisica (ECOG).
    """
    bonus_fitness = 0

    if "0" in ecog_str or "1" in ecog_str:
        bonus_fitness += 2

    if g8_score >= 14:
        bonus_fitness += 2
    elif g8_score >= 11:
        bonus_fitness += 1

    charlson_ponderato = max(0, charlson_score - bonus_fitness)

    aspettativa_maggiore_di_10 = True

    if eta >= 80 and charlson_ponderato >= 5:
        aspettativa_maggiore_di_10 = False
    elif charlson_ponderato >= 6 and g8_score < 11:
        aspettativa_maggiore_di_10 = False

    return aspettativa_maggiore_di_10, charlson_ponderato

def estrai_valore_regex(pattern, testo):
    match = re.search(pattern, testo, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None

def render_anagrafica_e_anamnesi_unificata(sigla_organo="MM", prefix="mm"):
    st.markdown("### 📋 Anagrafica & Identificazione")

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        cognome = st.text_input("Cognome Paziente", key=f"input_cognome_{prefix}")
    with col_b:
        nome = st.text_input("Nome Paziente", key=f"input_nome_{prefix}")

    id_key = f"input_id_{prefix}"
    if id_key not in st.session_state:
        st.session_state[id_key] = ""

    nuovo_id = genera_codice_univoco_organo(nome, cognome, sigla_organo)
    if nuovo_id:
        st.session_state[id_key] = nuovo_id

    with col_c:
        codice_paziente = st.text_input("Codice Univoco / ID (Autogenerato)", key=id_key)

    st.markdown("**Data di Nascita (GG / MM / AAAA)**")
    col_d1, col_d2, col_d3 = st.columns(3)
    with col_d1:
        giorno_n = st.number_input("Giorno", min_value=1, max_value=31, value=1, step=1, key=f"input_giorno_{prefix}")
    with col_d2:
        mese_n = st.number_input("Mese", min_value=1, max_value=12, value=1, step=1, key=f"input_mese_{prefix}")
    with col_d3:
        anno_n = st.number_input("Anno", min_value=1900, max_value=2026, value=1960, step=1, key=f"input_anno_{prefix}")

    try:
        data_nascita = datetime(int(anno_n), int(mese_n), int(giorno_n)).date()
    except ValueError:
        data_nascita = datetime(1960, 1, 1).date()
        st.warning("Data di nascita non valida. Impostata temporaneamente a 01/01/1960.")

    oggi = datetime.today().date()
    eta = oggi.year - data_nascita.year - ((oggi.month, oggi.day) < (data_nascita.month, data_nascita.day))

    st.info(f"📊 **Età Anagrafica:** {eta} anni")

    st.markdown("---")
    st.markdown("### 🏃‍♂️ Performance Status, Parametri Antropometrici & Stile di Vita")

    col_ant1, col_ant2 = st.columns(2)
    with col_ant1:
        peso = st.number_input("Peso (kg)", min_value=30.0, max_value=250.0, value=75.0, step=0.5, key=f"input_peso_{prefix}")
    with col_ant2:
        altezza = st.number_input("Altezza (cm)", min_value=100.0, max_value=250.0, value=175.0, step=1.0, key=f"input_altezza_{prefix}")

    altezza_m = altezza / 100.0
    bmi_valore = round(peso / (altezza_m ** 2), 1) if altezza_m > 0 else 0.0
    st.caption(f"⚖️ **BMI Calcolato:** `{bmi_valore}`")

    ecog = st.selectbox(
        "ECOG Performance Status:",
        [
            "0 - Pienamente attivo e autonomo",
            "1 - Sintomatico ma ambulante",
            "2 - Allettato <50% del giorno",
            "3 - Allettato >50% del giorno",
            "4 - Completamente allettato e dipendente"
        ],
        key=f"{prefix}_ecog"
    )

    col_p1, col_p2 = st.columns(2)
    with col_p1:
        adl = st.selectbox(
            "Scala ADL (Activities of Daily Living):",
            ["Non valutato", "Indipendente (6/6)", "Parzialmente dipendente (3-5/6)", "Fortemente dipendente (0-2/6)"],
            key=f"{prefix}_adl"
        )
    with col_p2:
        iadl = st.selectbox(
            "Scala IADL (Instrumental Activities of Daily Living):",
            ["Non valutato", "Indipendente (8/8)", "Parzialmente dipendente (4-7/8)", "Fortemente dipendente (0-3/8)"],
            key=f"{prefix}_iadl"
        )

    st.markdown("#### Allergie & Tabagismo")
    ha_allergie = st.checkbox("Il paziente presenta allergie note", key=f"{prefix}_ha_allergie")
    specifica_allergie = st.text_input("Specificare allergie (es. farmaci, lattice, mdc)", key=f"{prefix}_specifica_allergie") if ha_allergie else ""

    col_t1, col_t2 = st.columns(2)
    with col_t1:
        tabagismo = st.selectbox(
            "Tabagismo:",
            ["Non fumatore", "Ex fumatore", "Fumatore attivo"],
            key=f"{prefix}_tabagismo"
        )
    with col_t2:
        sig_die = st.number_input("Numero sigarette / die", min_value=1, max_value=100, value=10, step=1, key=f"{prefix}_sig_die") if tabagismo == "Fumatore attivo" else 0

    st.markdown("---")
    st.markdown("### 🧠 Valutazione Geriatrica (G8, GDS, Mini-Mental)")

    with st.expander("Screening G8 (Valutazione a 8 voci)", expanded=False):
        g8_pesi = [
            [("0 - Grave diminuzione", 0), ("1 - Moderata diminuzione", 1), ("2 - Nessuna diminuzione", 2)],
            [("0 - > 3 kg", 0), ("1 - Non sa", 1), ("2 - Tra 1 e 3 kg", 2), ("3 - Nessuna", 3)],
            [("0 - A letto/sedia", 0), ("1 - Esce ma limitato", 1), ("2 - Normale", 2)],
            [("0 - Sì", 0), ("2 - No", 2)],
            [("0 - Demenza/Depressione grave", 0), ("1 - Demenza lieve", 1), ("2 - Nessuno", 2)],
            [("0 - < 19", 0), ("1 - 19-21", 1), ("2 - 21-23", 2), ("3 - > 23", 3)],
            [("0 - Sì", 0), ("1 - No", 1)],
            [("0 - Peggiore", 0), ("0.5 - Non sa", 0.5), ("1 - Uguale", 1), ("2 - Migliore", 2)]
        ]
        g8_labels = [
            "1. Riduzione assunzione di cibo negli ultimi 3 mesi?",
            "2. Perdita di peso recente:",
            "3. Mobilità:",
            "4. Malattia acuta o stress psicologico recente?",
            "5. Problemi neuropsicologici:",
            "6. BMI:",
            "7. Assume più di 3 farmaci al giorno?",
            "8. Stato di salute percepito rispetto ai coetanei:"
        ]
        g8_score = sum(
            st.selectbox(g8_labels[i], g8_pesi[i], index=len(g8_pesi[i]) - 1, format_func=lambda x: x[0], key=f"{prefix}_g8_{i+1}")[1]
            for i in range(8)
        )

    st.info(f"📌 **Punteggio Totale G8:** `{g8_score}/17`")

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        gds = st.selectbox(
            "Geriatric Depression Scale (GDS):",
            ["Non valutato", "Negativa (Assente)", "Positiva (Sospetta depressione / lieve-moderata)"],
            key=f"{prefix}_gds"
        )
    with col_g2:
        esegue_mmse = st.checkbox("Eseguito Mini-Mental State Examination (MMSE)", key=f"{prefix}_check_mmse")
        valore_mmse = st.text_input("Punteggio MMSE (es. 28/30)", key=f"{prefix}_valore_mmse") if esegue_mmse else ""

    st.markdown("---")
    st.markdown("### 📊 Charlson Comorbidity Index (CCI)")

    charlson_items = [
        ("Infarto miocardico pregresso (+1)", 1, "c_infarto"),
        ("Scompenso cardiaco congestizio (+1)", 1, "c_scompenso"),
        ("Malattia vascolare periferica (+1)", 1, "c_vascolare"),
        ("Malattia cerebrovascolare / TIA (+1)", 1, "c_cerebrovascolare"),
        ("Demenza (+1)", 1, "c_demenza"),
        ("Malattia polmonare cronica (BPCO) (+1)", 1, "c_bpco"),
        ("Malattia del tessuto connettivo / Reumatologica (+1)", 1, "c_connettivite"),
        ("Ulcera peptica (+1)", 1, "c_ulcera"),
        ("Malattia epatica lieve (+1)", 1, "c_fegato_l"),
        ("Diabete mellito (+1)", 1, "c_diabete"),
        ("Emiplegia o paraplegia (+2)", 2, "c_emiplegia"),
        ("Malattia renale cronica moderata-severa (+2)", 2, "c_renale"),
        ("Tumore solido localizzato (+2)", 2, "c_tumore"),
        ("Leucemia o Linfoma (+2)", 2, "c_leucemia"),
        ("Malattia epatica moderata-severa (+3)", 3, "c_fegato_g"),
        ("Tumore solido metastatico / Malattia disseminata (+6)", 6, "c_metastasi"),
        ("AIDS / HIV conclamato (+6)", 6, "c_aids")
    ]

    with st.expander("Seleziona comorbilità attive per calcolo Charlson", expanded=False):
        base_charlson = sum(
            weight if st.checkbox(label, key=f"{prefix}_{key}") else 0
            for label, weight, key in charlson_items
        )

    bonus_eta_charlson = 4 if eta >= 80 else (3 if eta >= 70 else (2 if eta >= 60 else (1 if eta >= 50 else 0)))
    charlson_totale = base_charlson + bonus_eta_charlson

    aspettativa_ok, charlson_ponderato = stima_aspettativa_di_vita(eta, charlson_totale, g8_score, ecog)

    st.info(f"📈 **Charlson Comorbidity Index (Corretto per Età):** `{charlson_totale}` (Ponderato su Fitness: `{charlson_ponderato}`)")

    st.markdown("---")
    st.markdown("### 📥 Importazione Automatica Esami di Laboratorio (PDF)")

    dati_estratti = {}
    if not PYPDF_DISPONIBILE:
        st.warning("⚠️ La libreria 'pypdf' non è installata. Inserisci i dati manualmente.")
    else:
        st.info("Carica il referto di laboratorio per estrarre automaticamente i parametri.")
        uploaded_file = st.file_uploader("Seleziona il referto PDF", type=["pdf"], key=f"uploader_lab_completo_{prefix}")

        if uploaded_file is not None:
            try:
                reader = PdfReader(uploaded_file)
                testo_pdf = ""
                for pagina in reader.pages:
                    testo_pdf += pagina.extract_text() or ""

                match_nome = re.search(r"Sig\.\s+([A-Z\s]+)", testo_pdf)
                nome_estratto = match_nome.group(1).strip() if match_nome else "Non rilevato"
                match_data = re.search(r"Data Nascita:\s*(\d{2}/\d{2}/\d{4})", testo_pdf)
                data_estratta = match_data.group(1) if match_data else ""

                st.success(f"📄 **Referto Analizzato** — Paziente: `{nome_estratto}` (Nato il: `{data_estratta}`)")

                pattern_mappa = {
                    "hb": r"Emoglobina \(Hb\)\s*\|\s*([\d\.]+)",
                    "wbc": r"Globuli bianchi \(WBC\)\s*\|\s*([\d\.]+)",
                    "plt": r"Piastrine \(PLT\)\s*\|\s*([\d\.]+)",
                    "creatinina": r"Creatinina[^\d]*([\d\.]+)",
                    "egfr": r"eGFR[^\d]*([\d\.]+)",
                    "ast": r"AST|GOT[^\d]*([\d\.]+)",
                    "alt": r"ALT|GPT[^\d]*([\d\.]+)",
                    "ggt": r"Gamma[- ]GT|GGT[^\d]*([\d\.]+)"
                }

                for chiave, pat in pattern_mappa.items():
                    val_str = estrai_valore_regex(pat, testo_pdf)
                    if val_str:
                        try:
                            dati_estratti[chiave] = float(val_str)
                        except ValueError:
                            pass
                if dati_estratti:
                    st.info(f"✅ Estratti `{len(dati_estratti)}` parametri dal PDF.")
            except Exception as e:
                st.error(f"Errore di lettura del file PDF: {e}")

    st.markdown("### 💧 Esami Ematochimici & Organi Bersaglio")
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        creatinina = st.number_input("Creatinina (mg/dL)", min_value=0.2, max_value=15.0, value=dati_estratti.get("creatinina", 0.9), step=0.1, key=f"{prefix}_creatinina")
    with col_r2:
        egfr = st.number_input("eGFR (mL/min)", min_value=5, max_value=150, value=int(dati_estratti.get("egfr", 90)), step=1, key=f"{prefix}_egfr")

    col_e1, col_e2, col_e3 = st.columns(3)
    with col_e1:
        emoglobina = st.number_input("Emoglobina (Hb g/dL)", min_value=3.0, max_value=20.0, value=dati_estratti.get("hb", 14.0), step=0.1, key=f"{prefix}_hb")
    with col_e2:
        wbc = st.number_input("WBC (10^3/uL)", min_value=0.5, max_value=100.0, value=dati_estratti.get("wbc", 7.0), step=0.1, key=f"{prefix}_wbc")
    with col_e3:
        plt = st.number_input("Piastrine (10^3/uL)", min_value=10, max_value=1000, value=int(dati_estratti.get("plt", 200)), step=1, key=f"{prefix}_plt")

    col_ep1, col_ep2, col_ep3 = st.columns(3)
    with col_ep1:
        ast = st.number_input("AST / GOT (U/L)", min_value=5.0, max_value=500.0, value=dati_estratti.get("ast", 25.0), step=1.0, key=f"{prefix}_ast")
    with col_ep2:
        alt = st.number_input("ALT / GPT (U/L)", min_value=5.0, max_value=500.0, value=dati_estratti.get("alt", 25.0), step=1.0, key=f"{prefix}_alt")
    with col_ep3:
        ggt = st.number_input("GGT (U/L)", min_value=5.0, max_value=1000.0, value=dati_estratti.get("ggt", 30.0), step=1.0, key=f"{prefix}_ggt")

    st.markdown("---")
    st.markdown("### 🤝 Caregiver & Rete di Supporto")
    caregiver_supporto = st.selectbox(
        "Rete di supporto e Caregiver:",
        ["Non valutato", "Autonomo (Senza caregiver)", "Caregiver familiare presente", "Caregiver strutturato / Assistenza domiciliare", "Supporto sociosanitario carente"],
        key=f"{prefix}_caregiver"
    )

    st.markdown("---")
    st.markdown("### 🧬 Anamnesi Familiare (Onco-Ematologia e Correlazioni)")
    st.write("Familiarità per Mieloma Multiplo e patologie plasmacellulari/ematologiche (familiari di primo grado):")

    patologie_fam = [
        ("Mieloma Multiplo", "f_mm"),
        ("MGUS / Mieloma Smoldering", "f_mgus"),
        ("Amiloidosi AL", "f_amiloidosi"),
        ("Macroglobulinemia di Waldenström", "f_wald"),
        ("Linfomi non-Hodgkin / LLC", "f_linfoma_llc"),
        ("Tumori solidi con mutazioni germinali (Mammella/Ovaio/Prostata/Pancreas)", "f_solidi_gen")
    ]
    
    cols_fam = st.columns(2)
    familiarita_attiva = []
    for idx, (label, key) in enumerate(patologie_fam):
        if cols_fam[idx % 2].checkbox(label, key=f"{prefix}_{key}"):
            familiarita_attiva.append(label)

    st.markdown("---")
    st.markdown("### 📝 Anamnesi Chirurgica & Farmacologica")
    interventi = st.text_area("Anamnesi Chirurgica (es. interventi ortopedici per fratture vertebrali)", key=f"{prefix}_interventi")
    farmacologica = st.text_area("Anamnesi Farmacologica", key=f"{prefix}_farmacologica")

    return {
        "nome": nome.strip(),
        "cognome": cognome.strip(),
        "id_univoco": codice_paziente.strip(),
        "data_nascita": str(data_nascita),
        "eta": eta,
        "peso": peso,
        "altezza": altezza,
        "bmi": bmi_valore,
        "ecog": ecog,
        "adl": adl,
        "iadl": iadl,
        "g8_score": g8_score,
        "gds": gds,
        "mmse_eseguito": esegue_mmse,
        "mmse_valore": valore_mmse.strip(),
        "charlson_score": charlson_totale,
        "charlson_ponderato": charlson_ponderato,
        "aspettativa_vita_maggiore_10_anni": aspettativa_ok,
        "ha_allergie": ha_allergie,
        "specifica_allergie": specifica_allergie.strip(),
        "tabagismo": tabagismo,
        "sig_die": sig_die,
        "creatinina": creatinina,
        "egfr": egfr,
        "emoglobina": emoglobina,
        "wbc": wbc,
        "plt": plt,
        "ast": ast,
        "alt": alt,
        "ggt": ggt,
        "caregiver": caregiver_supporto,
        "familiarita": familiarita_attiva,
        "interventi": interventi.strip(),
        "farmacologica": farmacologica.strip()
    }

def formatta_anamnesi_per_pdf_unificata(paziente_info):
    righe = [
        f"• Età: {paziente_info.get('eta', 'N/D')} anni | Peso: {paziente_info.get('peso', 'N/D')} kg | Altezza: {paziente_info.get('altezza', 'N/D')} cm | BMI: {paziente_info.get('bmi', 'N/D')}",
        f"• Performance Status (ECOG): {paziente_info.get('ecog', 'N/D')}"
    ]

    if (adl := paziente_info.get('adl')) and adl != "Non valutato":
        righe.append(f"• ADL: {adl}")
    if (iadl := paziente_info.get('iadl')) and iadl != "Non valutato":
        righe.append(f"• IADL: {iadl}")

    if paziente_info.get('ha_allergie') and (spec_all := paziente_info.get('specifica_allergie')):
        righe.append(f"• Allergie Note: {spec_all}")
    else:
        righe.append("• Allergie: Nessuna nota/riferita")

    tabagismo_str = paziente_info.get('tabagismo', 'Non fumatore')
    if tabagismo_str == "Fumatore attivo":
        tabagismo_str += f" ({paziente_info.get('sig_die', 0)} sigarette/die)"
    righe.append(f"• Tabagismo: {tabagismo_str}")

    righe.append(f"• Screening G8: {paziente_info.get('g8_score', 'N/D')}/17")

    if (gds := paziente_info.get('gds')) and gds != "Non valutato":
        righe.append(f"• GDS: {gds}")
    if paziente_info.get('mmse_eseguito') and (mmse_val := paziente_info.get('mmse_valore')):
        righe.append(f"• MMSE: {mmse_val}")

    righe.append(f"• Charlson Comorbidity Index (corretto): {paziente_info.get('charlson_score', 'N/D')} (Ponderato su Fitness: {paziente_info.get('charlson_ponderato', 'N/D')})")

    righe.append(f"• Funzionalità Renale: Creatinina {paziente_info.get('creatinina', 'N/D')} mg/dL | eGFR {paziente_info.get('egfr', 'N/D')} mL/min")
    righe.append(f"• Emocromo: Hb {paziente_info.get('emoglobina', 'N/D')} g/dL | WBC {paziente_info.get('wbc', 'N/D')} 10^3/uL | PLT {paziente_info.get('plt', 'N/D')} 10^3/uL")
    righe.append(f"• Profilo Epatico: AST {paziente_info.get('ast', 'N/D')} | ALT {paziente_info.get('alt', 'N/D')} | GGT {paziente_info.get('ggt', 'N/D')} U/L")

    if (caregiver := paziente_info.get('caregiver')) and caregiver != "Non valutato":
        righe.append(f"• Rete di Supporto / Caregiver: {caregiver}")

    if fam := paziente_info.get('familiarita', []):
        righe.append(f"• Anamnesi Familiare (Ematologia/Genetica): {', '.join(fam)}")

    if interventi := paziente_info.get('interventi', ''):
        righe.append(f"• Anamnesi Chirurgica: {interventi}")

    if farmacologica := paziente_info.get('farmacologica', ''):
        righe.append(f"• Terapia Farmacologica Attuale: {farmacologica}")

    return "\n".join(righe)
