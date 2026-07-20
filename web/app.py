"""
app.py - Semana 6: Interfaz web Flask
Lee los archivos JSON generados por Scala/Python/Prolog y los muestra
en dos paginas: dashboard y tabla completa con filtros.

Uso:
    cd web
    python app.py
    Abrir en el navegador: http://localhost:5000
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
import re
import subprocess
import sys
from pypdf import PdfReader

app = Flask(__name__)

# ── Rutas de archivos ────────────────────────────────────────────────────────
BASE          = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RUTA_PUNTAJES   = os.path.join(BASE, "data", "salida", "puntajes.json")
RUTA_CANDIDATOS = os.path.join(BASE, "data", "entrada", "candidatos.json")
RUTA_PUESTOS    = os.path.join(BASE, "data", "entrada", "puestos.json")
RUTA_INTEGRADOR = os.path.join(BASE, "integrador.py")

# ── Helpers de carga ──────────────────────────────────────────────────────────
def cargar_json(ruta):
    if not os.path.exists(ruta):
        return []
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)

def nombre_legible(atomo):
    """Convierte 'ana_gutierrez' -> 'Ana Gutierrez' para mostrar en pantalla."""
    return " ".join(palabra.capitalize() for palabra in atomo.split("_"))

def color_clase(clasificacion):
    """Devuelve la clase CSS segun la clasificacion para el badge y la barra."""
    mapa = {
        "Excelente": "excelente",
        "Bueno":     "bueno",
        "Regular":   "regular",
        "Bajo":      "bajo",
    }
    return mapa.get(clasificacion, "bajo")

def iniciales(nombre):
    partes = nombre.split()
    if len(partes) >= 2:
        return (partes[0][0] + partes[1][0]).upper()
    return nombre[:2].upper()

def guardar_json(datos, ruta):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

def siguiente_id(lista):
    if not lista:
        return 1
    return max(item["id"] for item in lista) + 1

def parsear_lista(texto):
    """Convierte 'Python, SQL,  Machine Learning' -> ['Python', 'SQL', 'Machine Learning']"""
    if not texto:
        return []
    return [item.strip() for item in texto.split(",") if item.strip()]

def catalogo_desde_puestos(campo):
    """Recolecta valores unicos (habilidadesRequeridas o certificacionesDeseadas)
    de todos los puestos existentes, para alimentar el combobox de 'Nuevo puesto'."""
    puestos = cargar_json(RUTA_PUESTOS)
    vistos = {}
    for puesto in puestos:
        for valor in puesto.get(campo, []):
            clave = valor.strip().lower()
            if clave and clave not in vistos:
                vistos[clave] = valor.strip()
    return sorted(vistos.values(), key=lambda v: v.lower())

# ── Extraccion de datos desde CV en PDF ──────────────────────────────────────
# Plantilla fija que debe seguir el CV para que la extraccion sea confiable:
#
#   Nombre completo: Ana Gutierrez
#   Edad: 28
#   Años de experiencia: 4
#   Nivel de educación: licenciatura
#   Habilidades: Python, SQL, Machine Learning
#   Certificaciones: AWS Certified, Scrum Master
#   Resumen profesional: (texto libre, opcional, ultima seccion)
#
# Los nombres de las etiquetas no distinguen mayusculas/tildes. El orden de las
# secciones puede variar, pero "Resumen profesional" debe ir siempre al final,
# ya que se toma como el texto restante del documento.

ETIQUETAS_CV = {
    "nombre":          r"nombre(?:\s+completo)?",
    "edad":            r"edad",
    "experiencia":     r"a[nñ]os?\s+de\s+experiencia",
    "educacion":       r"nivel\s+de\s+educaci[oó]n",
    "habilidades":     r"habilidades",
    "certificaciones": r"certificaciones",
    "resumen":         r"resumen\s+profesional",
}

def _normalizar(texto):
    reemplazos = str.maketrans("áéíóúÁÉÍÓÚñÑ", "aeiouAEIOUnN")
    return texto.translate(reemplazos)

def extraer_texto_pdf(archivo):
    lector = PdfReader(archivo)
    partes = [pagina.extract_text() or "" for pagina in lector.pages]
    return "\n".join(partes)

def parsear_cv(texto):
    """Extrae los campos del candidato desde el texto del CV usando la plantilla
    de etiquetas fija. Devuelve (datos, advertencias)."""
    datos = {}
    advertencias = []

    # Construye un patron para cada etiqueta y busca "Etiqueta: valor" hasta el
    # fin de linea (o, para 'resumen', hasta el final del documento).
    posiciones = []
    for clave, patron_etiqueta in ETIQUETAS_CV.items():
        m = re.search(r"(?im)^\s*" + patron_etiqueta + r"\s*:\s*", texto)
        if m:
            posiciones.append((m.start(), m.end(), clave))
    posiciones.sort()

    for i, (inicio, fin_etiqueta, clave) in enumerate(posiciones):
        fin_valor = posiciones[i + 1][0] if i + 1 < len(posiciones) else len(texto)
        valor = texto[fin_etiqueta:fin_valor].strip()
        datos[clave] = valor

    nombre = datos.get("nombre", "").strip()
    if not nombre:
        advertencias.append("No se encontro el nombre en el CV.")

    edad = None
    if "edad" in datos:
        m = re.search(r"\d+", datos["edad"])
        if m:
            edad = int(m.group())
    if edad is None:
        advertencias.append("No se pudo leer la edad.")

    experiencia = None
    if "experiencia" in datos:
        m = re.search(r"\d+", datos["experiencia"])
        if m:
            experiencia = int(m.group())
    if experiencia is None:
        advertencias.append("No se pudieron leer los años de experiencia.")

    nivel_educacion = None
    if "educacion" in datos:
        valor_norm = _normalizar(datos["educacion"]).strip().lower()
        for nivel in NIVELES_EDUCACION:
            if nivel in valor_norm:
                nivel_educacion = nivel
                break
    if nivel_educacion is None:
        advertencias.append("No se pudo identificar el nivel de educacion (revisar manualmente).")

    habilidades = parsear_lista(datos.get("habilidades", ""))
    if not habilidades:
        advertencias.append("No se encontraron habilidades listadas.")

    certificaciones = parsear_lista(datos.get("certificaciones", ""))

    resumen = datos.get("resumen", "").strip()
    resumen = re.sub(r"\s*\n\s*", " ", resumen)

    return {
        "nombre": nombre,
        "edad": edad,
        "aniosExperiencia": experiencia,
        "nivelEducacion": nivel_educacion,
        "habilidades": habilidades,
        "certificaciones": certificaciones,
        "resumenProfesional": resumen,
    }, advertencias

# ── Ruta 1: Dashboard ─────────────────────────────────────────────────────────
@app.route("/")
def dashboard():
    puntajes = cargar_json(RUTA_PUNTAJES)

    if not puntajes:
        return render_template("dashboard.html", sin_datos=True)

    # Enriquecer con nombre legible e iniciales
    for p in puntajes:
        p["candidato_legible"] = nombre_legible(p["candidato"])
        p["puesto_legible"]    = nombre_legible(p["puesto"])
        p["iniciales"]         = iniciales(p["candidato_legible"])
        p["color"]             = color_clase(p["clasificacion"])
        if p.get("explicacion"):
            p["explicacion"] = p["explicacion"].replace(p["candidato"], p["candidato_legible"])

    total_candidatos = len(set(p["candidato"] for p in puntajes))
    total_puestos    = len(set(p["puesto"] for p in puntajes))
    promedio          = round(sum(p["puntaje"] for p in puntajes) / len(puntajes))
    excelentes        = sum(1 for p in puntajes if p["clasificacion"] == "Excelente")

    top5 = sorted(puntajes, key=lambda p: -p["puntaje"])[:5]

    # Resumen por puesto: cuantos candidatos y el mejor puntaje
    resumen_puestos = {}
    for p in puntajes:
        titulo = p["puesto_legible"]
        if titulo not in resumen_puestos:
            resumen_puestos[titulo] = {"atomo": p["puesto"], "total": 0, "mejor": 0}
        resumen_puestos[titulo]["total"] += 1
        resumen_puestos[titulo]["mejor"] = max(resumen_puestos[titulo]["mejor"], p["puntaje"])

    return render_template(
        "dashboard.html",
        sin_datos=False,
        total_candidatos=total_candidatos,
        total_puestos=total_puestos,
        promedio=promedio,
        excelentes=excelentes,
        top5=top5,
        resumen_puestos=resumen_puestos,
    )

# ── Ruta 2: Tabla completa con filtros ───────────────────────────────────────
@app.route("/todos")
def todos():
    puntajes = cargar_json(RUTA_PUNTAJES)

    for p in puntajes:
        p["candidato_legible"] = nombre_legible(p["candidato"])
        p["puesto_legible"]    = nombre_legible(p["puesto"])
        p["color"]             = color_clase(p["clasificacion"])
        if p.get("explicacion"):
            p["explicacion"] = p["explicacion"].replace(p["candidato"], p["candidato_legible"])

    # Filtros desde la URL: ?puesto=data_scientist&clasificacion=Excelente
    filtro_puesto = request.args.get("puesto", "")
    filtro_clase  = request.args.get("clasificacion", "")

    resultado = puntajes
    if filtro_puesto:
        resultado = [p for p in resultado if p["puesto"] == filtro_puesto]
    if filtro_clase:
        resultado = [p for p in resultado if p["clasificacion"] == filtro_clase]

    resultado = sorted(resultado, key=lambda p: -p["puntaje"])

    # Opciones unicas para los dropdowns
    puestos_unicos = sorted(set((p["puesto"], p["puesto_legible"]) for p in puntajes))
    clases_unicas  = ["Excelente", "Bueno", "Regular", "Bajo"]

    return render_template(
        "todos.html",
        registros=resultado,
        puestos_unicos=puestos_unicos,
        clases_unicas=clases_unicas,
        filtro_puesto=filtro_puesto,
        filtro_clase=filtro_clase,
        sin_datos=(len(puntajes) == 0),
    )

# ── Ruta 3: Formulario nuevo candidato ───────────────────────────────────────
NIVELES_EDUCACION = ["tecnico", "bachiller", "licenciatura", "maestria", "doctorado"]

@app.route("/nuevo-candidato", methods=["GET", "POST"])
def nuevo_candidato():
    if request.method == "POST":
        candidatos = cargar_json(RUTA_CANDIDATOS)

        nuevo = {
            "id": siguiente_id(candidatos),
            "nombre": request.form["nombre"].strip(),
            "edad": int(request.form["edad"]),
            "aniosExperiencia": int(request.form["aniosExperiencia"]),
            "nivelEducacion": request.form["nivelEducacion"],
            "habilidades": parsear_lista(request.form.get("habilidades", "")),
            "certificaciones": parsear_lista(request.form.get("certificaciones", "")),
        }

        resumen = request.form.get("resumenProfesional", "").strip()
        if resumen:
            nuevo["resumenProfesional"] = resumen

        candidatos.append(nuevo)
        guardar_json(candidatos, RUTA_CANDIDATOS)

        return redirect(url_for("recalcular", mensaje=f"Candidato '{nuevo['nombre']}' agregado"))

    return render_template("nuevo_candidato.html", niveles=NIVELES_EDUCACION)

# ── Ruta 3b: Extraer datos de un CV en PDF (AJAX, para precargar el formulario)
@app.route("/extraer-cv", methods=["POST"])
def extraer_cv():
    archivo = request.files.get("cv")
    if not archivo or archivo.filename == "":
        return jsonify({"error": "No se recibio ningun archivo."}), 400

    if not archivo.filename.lower().endswith(".pdf"):
        return jsonify({"error": "El archivo debe ser un PDF."}), 400

    try:
        texto = extraer_texto_pdf(archivo)
    except Exception:
        return jsonify({"error": "No se pudo leer el PDF. Verifica que no este danado o protegido."}), 400

    if not texto.strip():
        return jsonify({"error": "El PDF no tiene texto seleccionable (¿es una imagen escaneada?)."}), 400

    datos, advertencias = parsear_cv(texto)
    return jsonify({"datos": datos, "advertencias": advertencias})

# ── Ruta 4: Formulario nuevo puesto ──────────────────────────────────────────
@app.route("/nuevo-puesto", methods=["GET", "POST"])
def nuevo_puesto():
    if request.method == "POST":
        puestos = cargar_json(RUTA_PUESTOS)

        nuevo = {
            "id": siguiente_id(puestos),
            "titulo": request.form["titulo"].strip(),
            "minAniosExperiencia": int(request.form["minAniosExperiencia"]),
            "nivelEducacionRequerido": request.form["nivelEducacionRequerido"],
            "habilidadesRequeridas": parsear_lista(request.form.get("habilidadesRequeridas", "")),
            "certificacionesDeseadas": parsear_lista(request.form.get("certificacionesDeseadas", "")),
        }

        puestos.append(nuevo)
        guardar_json(puestos, RUTA_PUESTOS)

        return redirect(url_for("recalcular", mensaje=f"Puesto '{nuevo['titulo']}' agregado"))

    return render_template(
        "nuevo_puesto.html",
        niveles=NIVELES_EDUCACION,
        catalogo_habilidades=catalogo_desde_puestos("habilidadesRequeridas"),
        catalogo_certificaciones=catalogo_desde_puestos("certificacionesDeseadas"),
    )

# ── Ruta 5: Recalcular (ejecuta integrador.py) ───────────────────────────────
@app.route("/recalcular")
def recalcular():
    mensaje_previo = request.args.get("mensaje", "")

    resultado = subprocess.run(
        [sys.executable, RUTA_INTEGRADOR],
        cwd=BASE,
        capture_output=True,
        text=True,
    )

    exito = (resultado.returncode == 0)
    salida = resultado.stdout[-3000:] if resultado.stdout else resultado.stderr[-3000:]

    return render_template(
        "recalcular.html",
        exito=exito,
        salida=salida,
        mensaje_previo=mensaje_previo,
    )

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    print("=" * 50)
    print("  Servidor web iniciado")
    print(f"  Abrir en el navegador: http://localhost:{puerto}")
    print("=" * 50)
    app.run(host="0.0.0.0", port=puerto, debug=debug)
