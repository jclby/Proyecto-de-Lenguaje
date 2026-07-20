from utils.file_utils import escribir_texto

def generar_hechos(datos, ruta_salida, equivalencias=None):
    """
    Genera el archivo hechos.pl con todos los hechos Prolog
    derivados de los pares candidato-puesto exportados por Scala.

    Predicados generados:
      candidato(Atom, NivelEducacion, AniosExperiencia).
      puesto(Atom, NivelEducacionReq, MinAniosExperiencia).
      tiene_habilidad(CandidatoAtom, HabilidadAtom).
      requiere_habilidad(PuestoAtom, HabilidadAtom).
      tiene_certificacion(CandidatoAtom, CertAtom).
      desea_certificacion(PuestoAtom, CertAtom).
      evaluar_par(CandidatoAtom, PuestoAtom).
      equivale(HabilidadAtomA, HabilidadAtomB).
    """
    if equivalencias is None:
        equivalencias = []

    lineas = []
    lineas.append("% ============================================================")
    lineas.append("% hechos.pl - generado automaticamente por Python")
    lineas.append("% No editar manualmente; regenerar ejecutando main.py")
    lineas.append("% ============================================================")
    lineas.append("")

    # --- Candidatos: candidato(Atom, NivelEducacion, AniosExperiencia) ---
    lineas.append("% --- Candidatos: candidato(Atom, NivelEducacion, AniosExperiencia) ---")
    for atom, original, anios, nivel in datos["candidatos"]:
        lineas.append(f"candidato({atom}, {nivel}, {anios}).   % {original}")
    lineas.append("")

    # --- Puestos: puesto(Atom, NivelEducacionRequerido, MinAniosExperiencia) ---
    lineas.append("% --- Puestos: puesto(Atom, NivelEducacionRequerido, MinAniosExperiencia) ---")
    for atom, original, min_anios, nivel in datos["puestos"]:
        lineas.append(f"puesto({atom}, {nivel}, {min_anios}).   % {original}")
    lineas.append("")

    # --- Habilidades del candidato ---
    lineas.append("% --- Habilidades que posee cada candidato ---")
    for c_atom, h_atom in datos["habilidades_candidato"]:
        lineas.append(f"tiene_habilidad({c_atom}, {h_atom}).")
    lineas.append("")

    # --- Habilidades requeridas por el puesto ---
    lineas.append("% --- Habilidades requeridas por cada puesto ---")
    for p_atom, h_atom in datos["habilidades_puesto"]:
        lineas.append(f"requiere_habilidad({p_atom}, {h_atom}).")
    lineas.append("")

    # --- Certificaciones del candidato ---
    lineas.append("% --- Certificaciones que posee cada candidato ---")
    for c_atom, cert_atom in datos["cert_candidato"]:
        lineas.append(f"tiene_certificacion({c_atom}, {cert_atom}).")
    lineas.append("")

    # --- Certificaciones deseadas por el puesto ---
    lineas.append("% --- Certificaciones deseadas por cada puesto ---")
    for p_atom, cert_atom in datos["cert_puesto"]:
        lineas.append(f"desea_certificacion({p_atom}, {cert_atom}).")
    lineas.append("")

    # --- Equivalencias de habilidades ---
    lineas.append("% --- Habilidades equivalentes (intercambiables para el puntaje) ---")
    for atom_a, atom_b in equivalencias:
        lineas.append(f"equivale({atom_a}, {atom_b}).")
    lineas.append("")

    # --- Pares a evaluar ---
    lineas.append("% --- Pares candidato-puesto a evaluar ---")
    for c_atom, p_atom in datos["pares"]:
        lineas.append(f"evaluar_par({c_atom}, {p_atom}).")
    lineas.append("")

    contenido = "\n".join(lineas)
    escribir_texto(contenido, ruta_salida)
    print(f"[prolog_writer] hechos.pl generado en: {ruta_salida}")
    print(f"  Candidatos: {len(datos['candidatos'])}")
    print(f"  Puestos:    {len(datos['puestos'])}")
    print(f"  Pares a evaluar: {len(datos['pares'])}")
    print(f"  Equivalencias de habilidades: {len(equivalencias)}")
