import re

def _a_atom(texto: str) -> str:
    """
    Convierte un texto a atomo Prolog valido:
      - minusculas
      - espacios y guiones -> guion bajo
      - elimina caracteres no alfanumericos (excepto _)
    Ejemplos:
      'Ana Gutierrez'   ->  ana_gutierrez
      'Data Scientist'  ->  data_scientist
      'Machine Learning'->  machine_learning
    """
    texto = texto.lower()
    texto = re.sub(r'[\s\-]+', '_', texto)
    texto = re.sub(r'[^a-z0-9_]', '', texto)
    return texto

def transformar_pares(pares: list) -> dict:
    """
    Convierte cada par candidato-puesto al formato que usara prolog_writer.py.
    Devuelve un dict con:
      - candidatos: set de (atom, nombre_original, anios_exp, nivel_edu)
      - puestos:    set de (atom, titulo_original, min_anios, nivel_edu_req)
      - habilidades_candidato: lista de (candidato_atom, habilidad_atom)
      - habilidades_puesto:    lista de (puesto_atom, habilidad_atom)
      - cert_candidato:        lista de (candidato_atom, cert_atom)
      - cert_puesto:           lista de (puesto_atom, cert_atom)
      - pares:                 lista de (candidato_atom, puesto_atom) unicos
    """
    candidatos = set()
    puestos    = set()
    habilidades_candidato = set()
    habilidades_puesto    = set()
    cert_candidato        = set()
    cert_puesto           = set()
    pares_unicos          = set()

    for p in pares:
        c_atom = _a_atom(p["candidato"])
        p_atom = _a_atom(p["puesto"])

        candidatos.add((c_atom, p["candidato"], p["aniosExperiencia"], _a_atom(p["nivelEducacion"])))
        puestos.add((p_atom, p["puesto"], p["minAniosExperiencia"], _a_atom(p["nivelEducacionReq"])))

        for h in p["habilidadesCandidato"]:
            habilidades_candidato.add((c_atom, _a_atom(h)))
        for h in p["habilidadesRequeridas"]:
            habilidades_puesto.add((p_atom, _a_atom(h)))

        for c in p["certCandidato"]:
            cert_candidato.add((c_atom, _a_atom(c)))
        for c in p["certDeseadas"]:
            cert_puesto.add((p_atom, _a_atom(c)))

        pares_unicos.add((c_atom, p_atom))

    return {
        "candidatos":             sorted(candidatos),
        "puestos":                sorted(puestos),
        "habilidades_candidato":  sorted(habilidades_candidato),
        "habilidades_puesto":     sorted(habilidades_puesto),
        "cert_candidato":         sorted(cert_candidato),
        "cert_puesto":            sorted(cert_puesto),
        "pares":                  sorted(pares_unicos),
    }


def transformar_equivalencias(equivalencias):
    """
    Convierte la lista de pares [habilidad_a, habilidad_b] (texto original)
    a pares de atomos Prolog unicos y ordenados.
    Cada par se normaliza para evitar duplicados invertidos:
    (java, kotlin) y (kotlin, java) se consideran el mismo par.
    """
    pares_atom = set()
    for a, b in equivalencias:
        atom_a = _a_atom(a)
        atom_b = _a_atom(b)
        if atom_a == atom_b:
            continue
        par = tuple(sorted((atom_a, atom_b)))
        pares_atom.add(par)
    return sorted(pares_atom)
