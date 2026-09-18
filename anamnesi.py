from datetime import datetime
import random
import string
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

def render_anagrafica_e_anamnesi_unificata(sigla_organo="MM", prefix="mm"):
    st.markdown("### 📋 Anagrafica & Identificazione Paziente")

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        cognome = st.text_input("Cognome Paziente", key=f"input_cognome_{prefix}")
    with col_b:
        nome = st.text_input("Nome Paziente", key=f"input_nome_{prefix}")

    id_key = f"input_id_{prefix}"
    if id_key not in st.session_state:
        st.session_state[id_key] = ""

    nuovo_id = genera_codice_univoco_organo(nome, cognome, sigla_organo)
    if nuovo_id and not st.session_state[id_key]:
        st.session_state[id_key] = nuovo_id

    with col_c:
        codice_paziente = st.text_input("Codice Univoco / ID (Richiamabile)", key=id_key)

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

    # --- CAREGIVER E SUPPORTO ---
    st.markdown("---")
    st.markdown("### 🤝 Rete di Supporto, Contesto Sociale e Caregiver")
    caregiver_supporto = st.selectbox(
        "Contesto socio-familiare e supporto:",
        ["Non valutato", "Autonomo (Senza caregiver)", "Caregiver familiare presente", "Assistenza domiciliare strutturata / RSA"],
        key=f"{prefix}_caregiver"
    )
    note_sociali = st.text_area("Note sul contesto abitativo e supporto psicologico/familiare:", key=f"{prefix}_note_sociali")

    # --- ANAMNESI PATOLOGICA REMOTA E FAMILIARE ---
    st.markdown("---")
    st.markdown("### 📜 Anamnesi Patologica Remota, Farmacologica e Familiare")
    
    col_ap1, col_ap2 = st.columns(2)
    with col_ap1:
        comorbilita_rilevanti = st.text_area(
            "Patologie croniche pregresse / Interventi chirurgici:",
            placeholder="Es. Ipertensione arteriosa, Diabete tipo 2, Pregressa Neoplasia...",
            key=f"{prefix}_comorbilita"
        )
        anamnesi_familiare = st.text_area(
            "Anamnesi familiare (patologie ematologiche o oncologiche nei consanguinei):",
            key=f"{prefix}_familiare"
        )
    with col_ap2:
        terapia_domiciliare = st.text_area(
            "Terapia domiciliare cronica in corso (Farmaci e dosaggi):",
            placeholder="Es. Cardioaspirina 100mg, Ramipril 5mg...",
            key=f"{prefix}_terapia_dom"
        )
        allergie_farmacologiche = st.text_input(
            "Allergie farmacologiche o intolleranze note:",
            key=f"{prefix}_allergie"
        )

    st.markdown("---")
    st.markdown("### 🏃‍♂️ Performance Status & Parametri Antropometrici")

    col_ant1, col_ant2 = st.columns(2)
    with col_ant1:
        peso = st.number_input("Peso (kg)", min_value=30.0, max_value=250.0, value=75.0, step=0.5, key=f"input_peso_{prefix}")
    with col_ant2:
        altezza = st.number_input("Altezza (cm)", min_value=100.0, max_value=250.0, value=175.0, step=1.0, key=f"input_altezza_{prefix}")

    altezza_m = altezza / 100.0
    bmi_valore = round(peso / (altezza_m ** 2), 1) if altezza_m > 0 else 0.0
    st.caption(f"⚖️ **BMI Calcolato:** `{bmi_valore}` kg/m²")

    ecog = st.selectbox(
        "ECOG Performance Status:",
        [
            "0 - Pienamente attivo e autonomo in ogni attività",
            "1 - Sintomatico ma ambulante, capace di attività leggere",
            "2 - Allettato o su sedia <50% del giorno, cura personale autonoma",
            "3 - Allettato o su sedia >50% del giorno, assistenza parziale",
            "4 - Completamente allettato e dipendente, non autosufficiente"
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
            "Scala IADL (Instrumental ADL):",
            ["Non valutato", "Indipendente (8/8)", "Parzialmente dipendente (4-7/8)", "Fortemente dipendente (0-3/8)"],
            key=f"{prefix}_iadl"
        )

    # --- VALUTAZIONE GERIATRICA INTERATTIVA (G8 parte da 17/17) ---
    st.markdown("---")
    st.markdown("### 🧠 Valutazione Geriatrica & Comorbilità (Compilazione Guidata)")

    with st.expander("📋 Screening G8 (Partenza base 17/17 - Riduci in base ai deficit)", expanded=False):
        st.caption("Il punteggio parte da 17 (fit ottimale). Seleziona le condizioni cliniche che comportano una riduzione del punteggio:")
        
        g8_q1 = st.selectbox(
            "1. Variazione dell'apporto di cibo negli ultimi 3 mesi:",
            [
                ("Nessuna diminuzione dell'apporto (0 punti persi)", 0),
                ("Moderata diminuzione dell'apporto (-1 punto)", 1),
                ("Grave diminuzione dell'apporto (-2 punti)", 2)
            ],
            format_func=lambda x: x[0], key=f"{prefix}_g8_1"
        )[1]

        g8_q2 = st.selectbox(
            "2. Perdita di peso recente (< 3 mesi):",
            [
                ("Nessuna perdita di peso (0 punti persi)", 0),
                ("Perdita tra 1 e 3 kg (-1 punto)", 1),
                ("Non sa / Non quantificabile (-2 punti)", 2),
                ("Perdita di peso > 3 kg (-3 punti)", 3)
            ],
            format_func=lambda x: x[0], key=f"{prefix}_g8_2"
        )[1]

        g8_q3 = st.selectbox(
            "3. Mobilità e deambulazione:",
            [
                ("Esce normalmente / Autonomo (0 punti persi)", 0),
                ("Capace di uscire ma non autosufficiente negli spostamenti (-1 punto)", 1),
                ("Costretto a letto o in poltrona (-2 punti)", 2)
            ],
            format_func=lambda x: x[0], key=f"{prefix}_g8_3"
        )[1]

        g8_q4 = st.selectbox(
            "4. Malattia acuta o stress psicologico recente (ultimi 3 mesi):",
            [
                ("No (0 punti persi)", 0),
                ("Sì (-2 punti)", 2)
            ],
            format_func=lambda x: x[0], key=f"{prefix}_g8_4"
        )[1]

        g8_q5 = st.selectbox(
            "5. Problemi neuropsicologici (demenza, depressione, decadimento):",
            [
                ("Nessun problema psicologico (0 punti persi)", 0),
                ("Demenza o depressione moderata (-1 punto)", 1),
                ("Demenza o depressione grave (-2 punti)", 2)
            ],
            format_func=lambda x: x[0], key=f"{prefix}_g8_5"
        )[1]

        g8_q6 = st.selectbox(
            "6. Indice di Massa Corporea (BMI):",
            [
                ("BMI > 23 kg/m² (0 punti persi)", 0),
                ("BMI tra 21 e 23 kg/m² (-1 punto)", 1),
                ("BMI tra 19 e 21 kg/m² (-2 punti)", 2),
                ("BMI < 19 kg/m² (-3 punti)", 3)
            ],
            format_func=lambda x: x[0], key=f"{prefix}_g8_6"
        )[1]

        if eta >= 85:
            g8_q7 = 3
            st.text("7. Età del paziente: 85 anni o più (-3 punti)")
        elif eta >= 80:
            g8_q7 = 2
            st.text("7. Età del paziente: tra 80 e 84 anni (-2 punti)")
        elif eta >= 75:
            g8_q7 = 1
            st.text("7. Età del paziente: tra 75 e 79 anni (-1 punto)")
        else:
            g8_q7 = 0
            st.text("7. Età del paziente: inferiore a 75 anni (0 punti persi)")

        g8_q8 = st.selectbox(
            "8. Numero di farmaci assunti quotidianamente:",
            [
                ("Fino a 3 farmaci al giorno (0 punti persi)", 0),
                ("Più di 3 farmaci al giorno (-1 punto)", 1)
            ],
            format_func=lambda x: x[0], key=f"{prefix}_g8_8"
        )[1]

        penalita_totale = g8_q1 + g8_q2 + g8_q3 + g8_q4 + g8_q5 + g8_q6 + g8_q7 + g8_q8
        g8_score = max(0, 17 - penalita_totale)
        st.info(f"📋 **Punteggio G8 Calcolato:** `{g8_score}/17`")

    with st.expander("🏥 Charlson Comorbidity Index (Selezione delle comorbilità)", expanded=False):
        st.write("Spunta le condizioni patologiche presenti nell'anamnesi:")
        
        c_infarto = st.checkbox("Infarto miocardico pregresso (1 pto)", key=f"{prefix}_cc_inf")
        c_scompenso = st.checkbox("Scompenso cardiaco congestizio (1 pto)", key=f"{prefix}_cc_sco")
        c_vascolare = st.checkbox("Malattia vascolare periferica (1 pto)", key=f"{prefix}_cc_vas")
        c_cereb = st.checkbox("Malattia cerebrovascolare / TIA / Ictus (1 pto)", key=f"{prefix}_cc_cer")
        c_demenza = st.checkbox("Demenza (1 pto)", key=f"{prefix}_cc_dem")
        c_bpco = st.checkbox("Malattia polmonare cronica / BPCO (1 pto)", key=f"{prefix}_cc_bpc")
        c_connettivo = st.checkbox("Malattia del tessuto connettivo / Reumatologica (1 pto)", key=f"{prefix}_cc_con")
        c_ulcera = st.checkbox("Ulcera peptica (1 pto)", key=f"{prefix}_cc_ulc")
        c_fegato_lieve = st.checkbox("Epatopatia cronica lieve (1 pto)", key=f"{prefix}_cc_feg_l")
        c_diabete = st.selectbox("Diabete mellito", [("Assente", 0), ("Senza complicanze d'organo (1 pto)", 1), ("Con complicanze d'organo (2 pti)", 2)], format_func=lambda x: x[0], key=f"{prefix}_cc_diab")
        
        c_emiplegia = st.checkbox("Emiplegia o paraplegia (2 pti)", key=f"{prefix}_cc_emi")
        c_renale = st.checkbox("Malattia renale moderata o grave (2 pti)", key=f"{prefix}_cc_ren")
        c_tumore_solido = st.checkbox("Tumore solido localizzato (2 pti)", key=f"{prefix}_cc_tum")
        c_leucemia = st.checkbox("Leucemia, Linfoma o Mieloma (2 pti)", key=f"{prefix}_cc_emato")
        c_fegato_grave = st.checkbox("Epatopatia cronica grave / Cirrosi (3 pti)", key=f"{prefix}_cc_feg_g")
        c_metastasi = st.checkbox("Tumore solido metastatico (6 pti)", key=f"{prefix}_cc_met")
        c_aids = st.checkbox("Infezione da HIV / AIDS (6 pti)", key=f"{prefix}_cc_aids")

        charlson_base = (
            (1 if c_infarto else 0) +
            (1 if c_scompenso else 0) +
            (1 if c_vascolare else 0) +
            (1 if c_cereb else 0) +
            (1 if c_demenza else 0) +
            (1 if c_bpco else 0) +
            (1 if c_connettivo else 0) +
            (1 if c_ulcera else 0) +
            (1 if c_fegato_lieve else 0) +
            c_diabete[1] +
            (2 if c_emiplegia else 0) +
            (2 if c_renale else 0) +
            (2 if c_tumore_solido else 0) +
            (2 if c_leucemia else 0) +
            (3 if c_fegato_grave else 0) +
            (6 if c_metastasi else 0) +
            (6 if c_aids else 0)
        )

    bonus_eta_charlson = 4 if eta >= 80 else (3 if eta >= 70 else (2 if eta >= 60 else (1 if eta >= 50 else 0)))
    charlson_totale = charlson_base + bonus_eta_charlson
    aspettativa_ok, charlson_ponderato = stima_aspettativa_di_vita(eta, charlson_totale, g8_score, ecog)

    st.info(f"📈 **CCI Base:** `{charlson_base}` | **Bonus Età:** `+{bonus_eta_charlson}` | **CCI Totale:** `{charlson_totale}` | **G8:** `{g8_score}/17`")

    # --- SEZIONE 1: ESAMI DI LABORATORIO (Partono NON flaggati) ---
    st.markdown("---")
    st.markdown("### 🧪 Esami di Laboratorio in Ingresso (Seleziona solo quelli eseguiti)")
    st.write("Il medico spunta esclusivamente gli esami portati in visione dal paziente per abilitarne la compilazione:")

    col_lab1, col_lab2 = st.columns(2)
    with col_lab1:
        gia_emocromo = st.checkbox("Emocromo completo", value=False, key=f"{prefix}_gia_emocromo")
        emoglobina = st.number_input("Emoglobina (g/dL)", min_value=3.0, max_value=20.0, value=13.5, step=0.1, key=f"{prefix}_hb") if gia_emocromo else 13.5
        wbc = st.number_input("WBC (10^3/uL)", min_value=0.5, max_value=100.0, value=7.0, step=0.1, key=f"{prefix}_wbc") if gia_emocromo else 7.0
        plt = st.number_input("Piastrine (10^3/uL)", min_value=10, max_value=1000, value=200, step=1, key=f"{prefix}_plt") if gia_emocromo else 200

        gia_funzione_renale = st.checkbox("Funzione Renale (Creatinina / eGFR)", value=False, key=f"{prefix}_gia_renale")
        creatinina = st.number_input("Creatinina (mg/dL)", min_value=0.2, max_value=15.0, value=0.9, step=0.1, key=f"{prefix}_creatinina") if gia_funzione_renale else 0.9
        egfr = st.number_input("eGFR (mL/min)", min_value=5, max_value=150, value=90, step=1, key=f"{prefix}_egfr") if gia_funzione_renale else 90

    with col_lab2:
        gia_chimica = st.checkbox("Chimica Clinica (Calcemia, LDH, Beta-2, Albuminemia)", value=False, key=f"{prefix}_gia_chimica")
        calcemia = st.number_input("Calcemia totale (mg/dL)", min_value=5.0, max_value=16.0, value=9.5, step=0.1, key=f"{prefix}_calcemia") if gia_chimica else 9.5
        ldh = st.number_input("LDH (U/L)", min_value=50.0, max_value=1000.0, value=200.0, step=5.0, key=f"{prefix}_ldh") if gia_chimica else 200.0
        beta2_microglobulina = st.number_input("Beta-2 Microglobulina (mg/L)", min_value=0.5, max_value=20.0, value=2.0, step=0.1, key=f"{prefix}_beta2") if gia_chimica else 2.0
        albuminemia = st.number_input("Albuminemia (g/dL)", min_value=1.0, max_value=6.0, value=4.0, step=0.1, key=f"{prefix}_albumina") if gia_chimica else 4.0

    st.markdown("#### 🔬 Profilo Monoclonale di Laboratorio")
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        flag_spep_eseguita = st.checkbox("Elettroforesi sieroproteica (SPEP) eseguita", value=False, key=f"{prefix}_spep_eseg")
        valore_picco = st.text_input("Riscontro Picco Monoclonale (es. IgG Kappa, 1.2 g/dL)", key=f"{prefix}_val_picco") if flag_spep_eseguita else ""

        flag_ife_siero_eseguita = st.checkbox("Immunofissazione sierica eseguita", value=False, key=f"{prefix}_ife_siero_eseg")
    with col_m2:
        flag_flc_eseguita = st.checkbox("Catene Leggere Libere (FLC) dosate", value=False, key=f"{prefix}_flc_eseg")
        valore_flc = st.text_input("Valori FLC / Rapporto K/L alterato", key=f"{prefix}_val_flc") if flag_flc_eseguita else ""

        flag_bence_eseguita = st.checkbox("Proteinuria di Bence-Jones / Urine 24h eseguita", value=False, key=f"{prefix}_bence_eseg")

    # --- SEZIONE 2: ESAMI DIAGNOSTICI / RADIOLOGICI CON TENDINE PARAMETRI STANDARD ---
    st.markdown("---")
    st.markdown("### 🩻 Esami Diagnostici & Radiologici (Seleziona e compila i parametri guida)")
    st.write("Spunta gli esami eseguiti per selezionare i parametri standard raccomandati dalle linee guida:")

    parametro_rx = ""
    parametro_tc = ""
    parametro_rm = ""
    parametro_ecocardio = ""
    parametro_altro = ""

    col_img1, col_img2 = st.columns(2)
    with col_img1:
        flag_rx_scheletro = st.checkbox("RX Scheletro in toto", value=False, key=f"{prefix}_rx_skel")
        if flag_rx_scheletro:
            parametro_rx = st.selectbox(
                "Parametri standard RX Scheletro:",
                ["Negativo per lesioni osteolitiche focali", "Presenza di aree di osteolisi / geodi", "Osteopenia diffusa / fratture patologiche"],
                key=f"{prefix}_p_rx"
            )

        flag_tc_low_dose = st.checkbox("TC a basso dosaggio total-body (WBLDCT)", value=False, key=f"{prefix}_tc_ld")
        if flag_tc_low_dose:
            parametro_tc = st.selectbox(
                "Parametri standard TC Total-Body:",
                ["Negativo per lesioni litiche focali", "Lesioni osteolitiche multiple (> 5mm)", "Fratture vertebrali / crolli somatici", "Infiltrazione osteomidollare diffusa"],
                key=f"{prefix}_p_tc"
            )

    with col_img2:
        flag_rm_colonna = st.checkbox("Risonanza Magnetica (RM) rachide / bacino", value=False, key=f"{prefix}_rm_col")
        if flag_rm_colonna:
            parametro_rm = st.selectbox(
                "Parametri standard RM Rachide:",
                ["Infiltrazione focale multipla / nodulare", "Infiltrazione diffusa 'salt-and-pepper'", "Assenza di lesioni focali sospette"],
                key=f"{prefix}_p_rm"
            )

        flag_ecocardio = st.checkbox("Ecocardiogramma / ECG (es. sospetta amiloidosi)", value=False, key=f"{prefix}_ecocardio")
        if flag_ecocardio:
            parametro_ecocardio = st.selectbox(
                "Parametri standard Ecocardiografia:",
                ["Ventricolo sinistro normocinetico, spessori normali", "Ipertrofia ventricolare sinistra miocardica", "Segni suggestivi di cardiopatia infiltrativa"],
                key=f"{prefix}_p_eco"
            )

    flag_altro_img = st.checkbox("Altro esame radiologico / Referto aggiuntivo", value=False, key=f"{prefix}_altro_img_chk")
    if flag_altro_img:
        parametro_altro = st.text_input("Specifica tipologia esame e reperti:", key=f"{prefix}_altro_img_txt")

    # --- INDICATORI CRAB (Connessi al contesto clinico reale) ---
    st.markdown("---")
    st.markdown("### 🎯 Indicatori Clinici di Sospetto / Criteri CRAB")
    st.write("Verifica la correlazione clinica dei criteri nel contesto del paziente:")
    
    col_cr1, col_cr2 = st.columns(2)
    with col_cr1:
        ipercalcemia = st.checkbox("Ipercalcemia (> 11 mg/dL clinicamente correlata)", value=(gia_chimica and calcemia > 11.0), key=f"{prefix}_ipercalcemia")
        insuff_renale = st.checkbox("Insufficienza renale (Creatinina > 2 o eGFR < 40 attribuita a mieloma)", value=(gia_funzione_renale and (creatinina > 2.0 or egfr < 40)), key=f"{prefix}_insuff_renale")
    with col_cr2:
        anemia_clinica = st.checkbox("Anemia marcata (Hb < 10 g/dL non spiegata da altre cause)", value=(gia_emocromo and emoglobina < 10.0), key=f"{prefix}_anemia_clinica")
        lesioni_ossee = st.checkbox("Lesioni ossee / Osteolisi refertate nell'imaging", value=(flag_rx_scheletro or flag_tc_low_dose or flag_rm_colonna), key=f"{prefix}_lesioni_ossee")

    # --- GENERAZIONE DINAMICA ESAMI CONSIGLIATI ---
    st.markdown("---")
    st.markdown("### ⚖️ Esami di Approfondimento e Completamento Consigliati")

    merita_biopsia = False
    if ipercalcemia or insuff_renale or anemia_clinica or lesioni_ossee or (flag_spep_eseguita and valore_picco != ""):
        merita_biopsia = True

    esami_finali_consigliati = []
    
    if not flag_spep_eseguita:
        esami_finali_consigliati.append("Completare Laboratorio: Elettroforesi sieroproteica (SPEP)")
    if not flag_ife_siero_eseguita:
        esami_finali_consigliati.append("Completare Laboratorio: Immunofissazione sierica")
    if not flag_flc_eseguita:
        esami_finali_consigliati.append("Completare Laboratorio: Dosaggio Catene Leggere Libere (FLC)")
    if not flag_bence_eseguita:
        esami_finali_consigliati.append("Completare Laboratorio: Proteinuria di Bence-Jones / 24 ore")

    if not flag_tc_low_dose and not flag_rx_scheletro and not flag_rm_colonna:
        esami_finali_consigliati.append("Completare Diagnostica: TC total-body a basso dosaggio (WBLDCT)")

    if merita_biopsia:
        st.success("✅ **Indicazione Ematologica:** Criteri di danno d'organo / IMWG soddisfatti. **Indicato completamento con Biopsia Osteomidollare (BOM).**")
        esami_finali_consigliati.append("Esecuzione Biopsia Osteomidollare (BOM) con aspirato per studio citofluorimetrico e FISH")
    else:
        st.warning("⚠️ **Indicazione Ematologica:** Quadro clinico iniziale / da inquadrare (escludere MGUS o Mieloma Smoldering).")
        esami_finali_consigliati.append("Controllo clinico-laboratoristico a 3-6 mesi")

    st.markdown("**📋 Lista finale degli esami prescritti / da allegare al piano di cura:**")
    for esame in esami_finali_consigliati:
        st.markdown(f"- 🔹 {esame}")

    # --- VALIDAZIONE MEDICO EMATOLOGO & ESPORTAZIONE RAPIDA ---
    st.markdown("---")
    st.markdown("### 👨‍⚕️ Validazione del Medico Ematologo & Stampa Report")
    parere_medico = st.radio(
        "Concordi con il percorso diagnostico impostato?",
        ["Concordo", "Disaccordo"],
        key=f"{prefix}_parere_medico"
    )

    opzione_terapeutica_scelta = "Nessuna (Iter diagnostico / stadiazione in corso)"
    motivazione_disaccordo = ""

    if parere_medico == "Disaccordo":
        opzioni_terapeutiche_mm = [
            "Sorveglianza attiva / Watch and Wait",
            "Terapia d'induzione con quadruplice farmaco (es. Dara-VRd)",
            "Terapia d'induzione con Bortezomib + Lenalidomide + Desametasone (VRd)",
            "Terapia per pazienti non elegibili a trapianto (es. Dara-Rd)",
            "Terapia di supporto esclusiva"
        ]
        opzione_terapeutica_scelta = st.selectbox("Seleziona opzione terapeutica alternativa:", opzioni_terapeutiche_mm, key=f"{prefix}_menu_terapie")
        motivazione_disaccordo = st.text_area("Motivazione clinica del disaccordo:", key=f"{prefix}_motivazione_testo")

    # Oggetto dizionario temporaneo per l'anteprima e la stampa immediata dell'anamnesi
    dati_correnti_temp = {
        "nome": nome.strip(),
        "cognome": cognome.strip(),
        "id_univoco": st.session_state[id_key].strip(),
        "data_nascita": str(data_nascita),
        "eta": eta,
        "peso": peso,
        "altezza": altezza,
        "bmi": bmi_valore,
        "ecog": ecog,
        "adl": adl,
        "iadl": iadl,
        "g8_score": g8_score,
        "charlson_score": charlson_totale,
        "charlson_ponderato": charlson_ponderato,
        "comorbilita": comorbilita_rilevanti,
        "terapia_domiciliare": terapia_domiciliare,
        "allergie": allergie_farmacologiche,
        "emoglobina": emoglobina if gia_emocromo else "Non dosato",
        "wbc": wbc if gia_emocromo else "Non dosato",
        "plt": plt if gia_emocromo else "Non dosato",
        "creatinina": creatinina if gia_funzione_renale else "Non dosato",
        "egfr": egfr if gia_funzione_renale else "Non dosato",
        "calcemia": calcemia if gia_chimica else "Non dosato",
        "ldh": ldh if gia_chimica else "Non dosato",
        "beta2": beta2_microglobulina if gia_chimica else "Non dosato",
        "albumina": albuminemia if gia_chimica else "Non dosato",
        "flag_spep_eseguita": flag_spep_eseguita,
        "valore_picco": valore_picco.strip(),
        "flag_flc_eseguita": flag_flc_eseguita,
        "valore_flc": valore_flc.strip(),
        "flag_tc_low_dose": flag_tc_low_dose,
        "parametro_tc": parametro_tc,
        "flag_rx_scheletro": flag_rx_scheletro,
        "parametro_rx": parametro_rx,
        "flag_rm_colonna": flag_rm_colonna,
        "parametro_rm": parametro_rm,
        "flag_ecocardio": flag_ecocardio,
        "parametro_ecocardio": parametro_ecocardio,
        "parametro_altro": parametro_altro,
        "merita_biopsia": merita_biopsia,
        "parere_medico": parere_medico,
        "opzione_terapeutica_scelta": opzione_terapeutica_scelta,
        "motivazione_disaccordo": motivazione_disaccordo.strip(),
        "caregiver": caregiver_supporto
    }

    # Pulsante per stampare/esportare il report di questa specifica sezione in autonomia
    if st.button("🖨️ Genera e Scarica Report Anamnesi & Clinica"):
        testo_report_singolo = formatta_anamnesi_per_pdf_unificata(dati_correnti_temp)
        st.text_area("Anteprima Testo Anamnesi:", value=testo_report_singolo, height=250)
        st.download_button(
            label="💾 Salva file di testo Anamnesi",
            data=testo_report_singolo,
            file_name=f"Anamnesi_{dati_correnti_temp['id_univoco']}.txt",
            mime="text/plain"
        )

    return dati_correnti_temp

def render_anamnesi_e_valutazione(sigla_organo="MM", prefix="mm"):
    return render_anagrafica_e_anamnesi_unificata(sigla_organo=sigla_organo, prefix=prefix)

def formatta_anamnesi_per_pdf_unificata(paziente_info):
    """Funzione di supporto richiesta da app.py per generare il report globale in testo/PDF."""
    if not paziente_info or not paziente_info.get("cognome"):
        return "Anamnesi non compilata o dati paziente assenti."
    
    report = f"""=== ANAGRAFICA & ANAMNESI ===
Paziente: {paziente_info.get('cognome', '')} {paziente_info.get('nome', '')}
ID Univoco: {paziente_info.get('id_univoco', '')}
Data di Nascita: {paziente_info.get('data_nascita', '')} (Età: {paziente_info.get('eta', '')} anni)
Caregiver / Supporto: {paziente_info.get('caregiver', 'Non specificato')}

PARAMETRI ANTROPOMETRICI & PERFORMANCE:
- Peso: {paziente_info.get('peso', '')} kg | Altezza: {paziente_info.get('altezza', '')} cm | BMI: {paziente_info.get('bmi', '')}
- ECOG Performance Status: {paziente_info.get('ecog', '')}
- ADL: {paziente_info.get('adl', '')} | IADL: {paziente_info.get('iadl', '')}

VALUTAZIONE GERIATRICA & COMORBILITÀ:
- Punteggio G8: {paziente_info.get('g8_score', '')}/17
- Charlson Comorbidity Index (CCI Totale): {paziente_info.get('charlson_score', '')} (Ponderato: {paziente_info.get('charlson_ponderato', '')})
- Comorbilità riferite: {paziente_info.get('comorbilita', 'Nessuna registrata')}
- Terapia domiciliare: {paziente_info.get('terapia_domiciliare', 'Non specificata')}

ESAMI DI LABORATORIO IN INGRESSO:
- Emocromo: Hb {paziente_info.get('emoglobina', '')} g/dL, WBC {paziente_info.get('wbc', '')}, Plt {paziente_info.get('plt', '')}
- Funzione Renale: Creatinina {paziente_info.get('creatinina', '')} mg/dL, eGFR {paziente_info.get('egfr', '')} mL/min
- Chimica Clinica: Calcemia {paziente_info.get('calcemia', '')} mg/dL, LDH {paziente_info.get('ldh', '')} U/L, Beta-2 {paziente_info.get('beta2', '')} mg/L, Albumina {paziente_info.get('albumina', '')} g/dL
- Profilo Monoclonale: SPEP eseguita = {paziente_info.get('flag_spep_eseguita', False)} (Picco: {paziente_info.get('valore_picco', 'N/D')})

IMAGING & ESAMI DIAGNOSTICI:
- TC Low-Dose: {paziente_info.get('flag_tc_low_dose', False)} -> {paziente_info.get('parametro_tc', '')}
- RX Scheletro: {paziente_info.get('flag_rx_scheletro', False)} -> {paziente_info.get('parametro_rx', '')}
- RM Rachide: {paziente_info.get('flag_rm_colonna', False)} -> {paziente_info.get('parametro_rm', '')}
- Ecocardiogramma: {paziente_info.get('flag_ecocardio', False)} -> {paziente_info.get('parametro_ecocardio', '')}
- Altro imaging: {paziente_info.get('parametro_altro', 'Nessuno')}

VALUTAZIONE CLINICA EMATOLOGICA:
- Indicazione Biopsia Midollare (BOM): {'Sì' if paziente_info.get('merita_biopsia', False) else 'No / Inquadramento iniziale'}
- Parere Medico: {paziente_info.get('parere_medico', 'Concordo')}
- Scelta Terapeutica Alternativa: {paziente_info.get('opzione_terapeutica_scelta', 'Nessuna')}
- Motivazione Disaccordo: {paziente_info.get('motivazione_disaccordo', 'Nessuna')}
"""
    return report
