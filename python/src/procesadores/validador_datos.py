"""
validador_datos.py
Valida y limpia los datos de candidatos y puestos antes de enviarlos
a la cadena de transformacion Python -> Prolog.

Reglas de validacion:
  - edad y aniosExperiencia no pueden ser negativos
  - nombre/titulo no puede estar vacio
  - habilidades y certificaciones no deben tener duplicados (se normalizan)
  - nivelEducacion debe ser uno de los 5 niveles validos
"""

NIVELES_VALIDOS = {"tecnico", "bachiller", "licenciatura", "maestria", "doctorado"}


def _normalizar_lista(lista):
    """Elimina duplicados (sin importar mayusculas/espacios) preservando el primero."""
    vistos = set()
    resultado = []
    for item in lista:
        item = item.strip()
        clave = item.lower()
        if item and clave not in vistos:
            vistos.add(clave)
            resultado.append(item)
    return resultado


def validar_candidato(candidato):
    """
    Valida y limpia un candidato. Devuelve (candidato_corregido, lista_de_avisos).
    No descarta candidatos invalidos; los corrige cuando es posible y avisa.
    """
    avisos = []
    c = dict(candidato)

    nombre = c.get("nombre", "").strip()
    if not nombre:
        avisos.append(f"[id={c.get('id')}] nombre vacio, se usara 'Sin nombre'")
        nombre = "Sin nombre"
    c["nombre"] = nombre

    edad = c.get("edad", 0)
    if edad < 0 or edad > 100:
        avisos.append(f"[{nombre}] edad invalida ({edad}), se ajusta a 0")
        edad = 0
    c["edad"] = edad

    anios = c.get("aniosExperiencia", 0)
    if anios < 0:
        avisos.append(f"[{nombre}] aniosExperiencia negativo ({anios}), se ajusta a 0")
        anios = 0
    c["aniosExperiencia"] = anios

    nivel = c.get("nivelEducacion", "").strip().lower()
    if nivel not in NIVELES_VALIDOS:
        avisos.append(f"[{nombre}] nivelEducacion invalido ('{nivel}'), se ajusta a 'tecnico'")
        nivel = "tecnico"
    c["nivelEducacion"] = nivel

    habilidades_originales = c.get("habilidades", [])
    habilidades_limpias = _normalizar_lista(habilidades_originales)
    if len(habilidades_limpias) != len(habilidades_originales):
        avisos.append(f"[{nombre}] se eliminaron habilidades duplicadas o vacias")
    c["habilidades"] = habilidades_limpias

    cert_originales = c.get("certificaciones", [])
    cert_limpias = _normalizar_lista(cert_originales)
    if len(cert_limpias) != len(cert_originales):
        avisos.append(f"[{nombre}] se eliminaron certificaciones duplicadas o vacias")
    c["certificaciones"] = cert_limpias

    return c, avisos


def validar_puesto(puesto):
    """Valida y limpia un puesto. Misma logica que validar_candidato."""
    avisos = []
    p = dict(puesto)

    titulo = p.get("titulo", "").strip()
    if not titulo:
        avisos.append(f"[id={p.get('id')}] titulo vacio, se usara 'Sin titulo'")
        titulo = "Sin titulo"
    p["titulo"] = titulo

    min_anios = p.get("minAniosExperiencia", 0)
    if min_anios < 0:
        avisos.append(f"[{titulo}] minAniosExperiencia negativo ({min_anios}), se ajusta a 0")
        min_anios = 0
    p["minAniosExperiencia"] = min_anios

    nivel = p.get("nivelEducacionRequerido", "").strip().lower()
    if nivel not in NIVELES_VALIDOS:
        avisos.append(f"[{titulo}] nivelEducacionRequerido invalido ('{nivel}'), se ajusta a 'tecnico'")
        nivel = "tecnico"
    p["nivelEducacionRequerido"] = nivel

    hab_originales = p.get("habilidadesRequeridas", [])
    hab_limpias = _normalizar_lista(hab_originales)
    if len(hab_limpias) != len(hab_originales):
        avisos.append(f"[{titulo}] se eliminaron habilidades requeridas duplicadas o vacias")
    p["habilidadesRequeridas"] = hab_limpias

    cert_originales = p.get("certificacionesDeseadas", [])
    cert_limpias = _normalizar_lista(cert_originales)
    if len(cert_limpias) != len(cert_originales):
        avisos.append(f"[{titulo}] se eliminaron certificaciones deseadas duplicadas o vacias")
    p["certificacionesDeseadas"] = cert_limpias

    return p, avisos


def validar_y_limpiar(candidatos, puestos):
    """
    Valida toda la lista de candidatos y puestos.
    Devuelve (candidatos_limpios, puestos_limpios, todos_los_avisos).
    """
    candidatos_limpios = []
    puestos_limpios = []
    todos_avisos = []

    for c in candidatos:
        c_limpio, avisos = validar_candidato(c)
        candidatos_limpios.append(c_limpio)
        todos_avisos.extend(avisos)

    for p in puestos:
        p_limpio, avisos = validar_puesto(p)
        puestos_limpios.append(p_limpio)
        todos_avisos.extend(avisos)

    return candidatos_limpios, puestos_limpios, todos_avisos
