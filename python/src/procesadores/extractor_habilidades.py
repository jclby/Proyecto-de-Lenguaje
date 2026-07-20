"""
extractor_habilidades.py
Procesamiento de texto libre (NLP basico, sin librerias pesadas).

Si un candidato tiene un campo 'resumenProfesional' en texto libre,
se buscan menciones de habilidades conocidas que no esten ya en su
lista estructurada de 'habilidades'. Esto simula que un candidato
escribio su perfil en lenguaje natural y el sistema detecta
automaticamente competencias mencionadas.

Tecnica: coincidencia de palabras/frases (case-insensitive, por
limites de palabra) contra un catalogo de habilidades conocidas.
No requiere NLTK/spaCy; usa solo expresiones regulares.
"""

import re

# Catalogo de habilidades conocidas que el sistema sabe reconocer en texto libre.
# Se alimenta con las habilidades ya usadas en candidatos.json y puestos.json,
# mas variantes comunes de escritura.
CATALOGO_HABILIDADES = [
    "Python", "Java", "Kotlin", "Scala", "SQL", "PostgreSQL", "MySQL",
    "HTML", "CSS", "JavaScript", "R",
    "Machine Learning", "Deep Learning", "Inteligencia Artificial",
    "Comunicacion", "Liderazgo", "Trabajo en equipo", "Gestion de proyectos",
    "Excel", "Power BI", "Tableau", "Git", "Docker", "Kubernetes",
    "AWS", "AWS Certified", "Azure", "Google Cloud", "Linux",
]


def _patron_para(habilidad):
    """Crea un patron regex que detecta la habilidad como palabra/frase completa."""
    escapada = re.escape(habilidad)
    return re.compile(r"\b" + escapada + r"\b", re.IGNORECASE)


def extraer_habilidades_de_texto(texto):
    """
    Busca en el texto libre menciones de habilidades del catalogo.
    Devuelve la lista de habilidades encontradas (con su forma "oficial"
    del catalogo, no como aparecieron en el texto).
    """
    if not texto:
        return []

    encontradas = []
    for habilidad in CATALOGO_HABILIDADES:
        if _patron_para(habilidad).search(texto):
            encontradas.append(habilidad)
    return encontradas


def enriquecer_candidato_con_nlp(candidato):
    """
    Si el candidato tiene 'resumenProfesional', extrae habilidades mencionadas
    alli que no esten ya en su lista estructurada, y las agrega.
    Devuelve (candidato_enriquecido, lista_de_habilidades_agregadas).
    """
    resumen = candidato.get("resumenProfesional", "")
    if not resumen:
        return candidato, []

    detectadas = extraer_habilidades_de_texto(resumen)
    ya_tiene = set(h.lower() for h in candidato.get("habilidades", []))

    nuevas = [h for h in detectadas if h.lower() not in ya_tiene]

    if nuevas:
        candidato = dict(candidato)
        candidato["habilidades"] = candidato.get("habilidades", []) + nuevas

    return candidato, nuevas


def enriquecer_todos(candidatos):
    """
    Aplica el enriquecimiento NLP a toda la lista de candidatos.
    Devuelve (candidatos_enriquecidos, reporte_de_avisos).
    """
    resultado = []
    avisos = []

    for c in candidatos:
        c_enriquecido, nuevas = enriquecer_candidato_con_nlp(c)
        resultado.append(c_enriquecido)
        if nuevas:
            avisos.append(
                "[" + c.get("nombre", "?") + "] habilidades detectadas en resumen: " + ", ".join(nuevas)
            )

    return resultado, avisos
