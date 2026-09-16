import streamlit as st

def render_esame_istologico(prefix="istologico"):
    """
    Rende l'interfaccia per la registrazione e l'analisi del referto istologico, 
    citologico midollare, immunofenotipico e citogenetico (FISH) per il Mieloma Multiplo.
    """
    st.subheader("📋 Referto Biopsia / Aspirato Midollare & Diagnosi Istologica")
    
    # 1. Cellularità e Infiltrazione Plasmacellulare
    st.markdown("#### 1. Cellularità Midollare e Infiltrato Neoplastico")
    col1, col2 = st.columns(2)
    with col1:
        cellularita = st.selectbox(
            "Cellularità Midollare Globale:",
            ["Normocellulare", "Ipercellulare", "Ipocellulare / Atrofico"],
            key=f"{prefix}_cellularita"
        )
    with col2:
        infiltrazione_pc = st.number_input(
            "Infiltrazione Plasmacellulare (%) sul totale delle cellule midollari:",
            min_value=0.0, max_value=100.0, value=10.0, step=1.0,
            key=f"{prefix}_infiltrazione_pc"
        )

    # 2. Morfologia e Fenotipo (Citometria a flusso / Immunoistochimica)
    st.markdown("#### 2. Caratteristiche Morfologiche e Profilo Immunofenotipico")
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        morfologia_pc = st.selectbox(
            "Morfologia delle Plasmacellule:",
            [
                "Mature / Tipiche",
                "Plasmablastiche / Immature",
                "Pleomorfiche / Anaplastiche",
                "Miste (Mature e Plasmablastiche)"
            ],
            key=f"{prefix}_morfologia"
        )
    with col_m2:
        restrizione_catene = st.selectbox(
            "Restrizione Catene Leggere (Clonilità):",
            [
                "Restrizione Kappa (Monoclonale)",
                "Restrizione Lambda (Monoclonale)",
                "Biclonalità / Altro",
                "Non determinabile / Negativa"
            ],
            key=f"{prefix}_catene"
        )

    # Marcatori di superficie tipici
    st.markdown("**Espressione Antigenica (Immunofenotipo):**")
    col_a1, col_a2, col_a3, col_a4 = st.columns(4)
    with col_a1:
        cd138 = st.selectbox("CD138", ["Positivo", "Negativo", "Non eseguito"], key=f"{prefix}_cd138")
    with col_a2:
        cd38 = st.selectbox("CD38", ["Positivo", "Negativo", "Non eseguito"], key=f"{prefix}_cd38")
    with col_a3:
        cd56 = st.selectbox("CD56", ["Positivo (Aberrante)", "Negativo", "Non eseguito"], key=f"{prefix}_cd56")
    with col_a4:
        cd19 = st.selectbox("CD19", ["Negativo (Aberrante)", "Positivo", "Non eseguito"], key=f"{prefix}_cd19")

    # 3. Fibrosi e Citogenetica / FISH
    st.markdown("#### 3. Fibrosi Midollare e Assetto Citogenetico (FISH)")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        fibrosi = st.selectbox(
            "Grado di Fibrosi Reticolinica:",
            ["Assente (MF-0)", "Lieve (MF-1)", "Moderata (MF-2)", "Severa (MF-3)"],
            key=f"{prefix}_fibrosi"
        )
    with col_f2:
        fish_rischio = st.multiselect(
            "Anomalie Citogenetiche / FISH ad Alto Rischio rilevate:",
            [
                "Nessuna anomalia ad alto rischio rilevata (Standard Risk)",
                "del(17p) / TP53 persa",
                "t(4;14)",
                "t(14;16)",
                "t(14;20)",
                "Guadagno / Amplificazione 1q (1q21 amp)",
                "Monosomia 13 / del(13q)"
            ],
            default=["Nessuna anomalia ad alto rischio rilevata (Standard Risk)"],
            key=f"{prefix}_fish"
        )

    # 4. Conclusione Diagnostica Istologica
    st.markdown("#### 4. Conclusione Diagnostica del Referto")
    conclusione_istologica = st.selectbox(
        "Inquadramento Nosologico finale del reperto:",
        [
            "Mieloma Multiplo Sintomatico (attivo)",
            "Mieloma Multiplo Asintomatico (Smoldering - SMM)",
            "MGUS (Monoclonal Gammopathy of Undetermined Significance)",
            "Plasmacitoma solitario osseo / extramedollare",
            "Midollo indenne da infiltrazione di malattia plasmacellulare"
        ],
        key=f"{prefix}_conclusione_istologica"
    )

    note_libere_istologo = st.text_area(
        "Note descrittive aggiuntive del patologo / ematologo:",
        placeholder="Inserire eventuali dettagli microscopici rilevanti o referto testuale esteso...",
        key=f"{prefix}_note"
    )

    # Compilazione del dizionario strutturato da passare al cervellone (app.py)
    esito_istologico_info = {
        "cellularita": cellularita,
        "infiltrazione_pc": infiltrazione_pc,
        "morfologia_pc": morfologia_pc,
        "restrizione_catene": restrizione_catene,
        "immunofenotipo": {
            "cd138": cd138,
            "cd38": cd38,
            "cd56": cd56,
            "cd19": cd19
        },
        "fibrosi": fibrosi,
        "fish_rischio": fish_rischio,
        "conclusione_istologica": conclusione_istologica,
        "note_libere": note_libere_istologo
    }

    return esito_istologico_info


def formatta_istologico_per_pdf(esito_istologico_info):
    """
    Formatta in testo ordinato i dati dell'esame istologico e midollare per l'inclusione nel referto clinico/PDF.
    """
    immuno = esito_istologico_info.get("immunofenotipo", {})
    fish_str = ", ".join(esito_istologico_info.get("fish_rischio", []))
    
    testo = (
        f"Referto Biopsia / Aspirato Midollare & Citogenetica:\n"
        f"• Cellularità Globale: {esito_istologico_info.get('cellularita')}\n"
        f"• Infiltrazione Plasmacellulare: {esito_istologico_info.get('infiltrazione_pc')}%\n"
        f"• Morfologia: {esito_istologico_info.get('morfologia_pc')} | Clonilità: {esito_istologico_info.get('restrizione_catene')}\n"
        f"• Immunoistochimica/Flow: CD138 ({immuno.get('cd138')}), CD38 ({immuno.get('cd38')}), CD56 ({immuno.get('cd56')}), CD19 ({immuno.get('cd19')})\n"
        f"• Fibrosi Reticolinica: {esito_istologico_info.get('fibrosi')}\n"
        f"• Assetto Citogenetico FISH: {fish_str}\n"
        f"• Conclusione Diagnostica: {esito_istologico_info.get('conclusione_istologica')}\n"
        f"• Note del Medico: {esito_istologico_info.get('note_libere')}"
    )
    return testo
