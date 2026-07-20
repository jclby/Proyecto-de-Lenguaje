"""
integrador.py - Integracion completa
Orquesta los tres lenguajes en secuencia:
  0. Python -> valida/limpia datos y enriquece con NLP (preprocesador.py)
  1. Scala  -> genera evaluaciones preliminares y para_python.json
  2. Python -> transforma datos, carga equivalencias y genera hechos.pl
  3. Prolog -> calcula el puntaje de compatibilidad 0-100% y exporta puntajes.json
"""

import subprocess
import sys
import os
import json
import time

# ── Rutas base ────────────────────────────────────────────────────────────────
BASE         = os.path.abspath(os.path.join(os.path.dirname(__file__)))
DIR_SCALA    = os.path.join(BASE, "scala")
DIR_PYTHON   = os.path.join(BASE, "python", "src")
DIR_PROLOG   = os.path.join(BASE, "prolog")
DIR_SALIDA   = os.path.join(BASE, "data", "salida")
RUTA_HECHOS  = os.path.join(DIR_PROLOG, "hechos.pl")
RUTA_PARES   = os.path.join(DIR_SALIDA, "para_python.json")
RUTA_PUNTAJES = os.path.join(DIR_SALIDA, "puntajes.json")

# ── Helpers de consola ────────────────────────────────────────────────────────
SEP  = "=" * 60
SEP2 = "-" * 60

def titulo(texto):
    print(f"\n{SEP}")
    print(f"  {texto}")
    print(SEP)

def paso(n, texto):
    print(f"\n[Paso {n}] {texto}...")

def ok(texto):
    print(f"  [OK] {texto}")

def error(texto):
    print(f"  [ERROR] {texto}")

def ejecutar(comando, directorio, descripcion):
    """Ejecuta un comando de sistema y devuelve True/False segun el resultado."""
    print(f"\n  > Ejecutando: {' '.join(comando)}")
    print(f"  > Directorio: {directorio}")
    print(SEP2)

    inicio = time.time()
    resultado = subprocess.run(
        comando,
        cwd=directorio,
        capture_output=False,
        text=True,
        shell=(os.name == 'nt')
    )
    duracion = round(time.time() - inicio, 1)

    print(SEP2)
    if resultado.returncode == 0:
        ok(f"{descripcion} completado en {duracion}s")
        return True
    else:
        error(f"{descripcion} fallo (codigo {resultado.returncode})")
        return False

# ── Fase 0: Preprocesamiento (validacion + NLP) ──────────────────────────────
def ejecutar_preprocesador():
    paso(0, "Ejecutando preprocesador — validando datos y buscando habilidades en texto libre")
    return ejecutar([sys.executable, "preprocesador.py"], DIR_PYTHON, "Python preprocesador.py")

# ── Fase 1: Scala ─────────────────────────────────────────────────────────────
def ejecutar_scala():
    paso(1, "Ejecutando Scala — generando evaluaciones preliminares")
    exito = ejecutar(["sbt", "run"], DIR_SCALA, "Scala sbt run")
    if not exito:
        return False

    if os.path.exists(RUTA_PARES):
        ok(f"Archivo generado: {RUTA_PARES}")
        return True
    else:
        error(f"No se encontro: {RUTA_PARES}")
        return False

# ── Fase 2: Python ────────────────────────────────────────────────────────────
def ejecutar_python():
    paso(2, "Ejecutando Python — transformando datos y generando hechos.pl")
    exito = ejecutar([sys.executable, "main.py"], DIR_PYTHON, "Python main.py")
    if not exito:
        return False

    if os.path.exists(RUTA_HECHOS):
        ok(f"Archivo generado: {RUTA_HECHOS}")
        return True
    else:
        error(f"No se genero: {RUTA_HECHOS}")
        return False

# ── Fase 3: Prolog ────────────────────────────────────────────────────────────
def ejecutar_prolog():
    paso(3, "Ejecutando Prolog — calculando puntajes de compatibilidad")
    exito = ejecutar(
        ["swipl", "-g", "validar, halt", "validacion.pl"],
        DIR_PROLOG,
        "SWI-Prolog validacion"
    )
    if not exito:
        return False

    if os.path.exists(RUTA_PUNTAJES):
        ok(f"Archivo generado: {RUTA_PUNTAJES}")
        return True
    else:
        error(f"No se genero: {RUTA_PUNTAJES}")
        return False

# ── Fase 4: Reporte final ─────────────────────────────────────────────────────
def mostrar_reporte_final(resultados):
    titulo("REPORTE FINAL DE INTEGRACION")

    fases = [
        ("Python — preprocesamiento (validacion + NLP)", resultados[0]),
        ("Scala  — evaluaciones preliminares",        resultados[1]),
        ("Python — transformacion de datos",           resultados[2]),
        ("Prolog — calculo de puntajes (0-100%)",       resultados[3]),
    ]

    todos_ok = all(resultados)

    for nombre, exito in fases:
        estado = "[OK]    " if exito else "[FALLO]"
        print(f"  {estado} {nombre}")

    print(f"\n{SEP2}")

    # Leer estadisticas de puntajes.json
    try:
        with open(RUTA_PUNTAJES, "r", encoding="utf-8") as f:
            puntajes = json.load(f)

        print(f"  Evaluaciones generadas: {len(puntajes)}")
        candidatos = len(set(p["candidato"] for p in puntajes))
        puestos    = len(set(p["puesto"]    for p in puntajes))
        print(f"  Candidatos evaluados:   {candidatos}")
        print(f"  Puestos evaluados:      {puestos}")

        promedio = round(sum(p["puntaje"] for p in puntajes) / len(puntajes), 1)
        print(f"  Puntaje promedio:       {promedio}%")

        mejor = max(puntajes, key=lambda p: p["puntaje"])
        print(f"  Mejor match:            {mejor['candidato']} -> {mejor['puesto']} ({mejor['puntaje']}%)")

        excelentes = sum(1 for p in puntajes if p["clasificacion"] == "Excelente")
        print(f"  Matches 'Excelente':    {excelentes}")

    except Exception as e:
        print(f"  [AVISO] No se pudieron leer estadisticas: {e}")

    print(f"\n{SEP2}")
    if todos_ok:
        print("  RESULTADO: INTEGRACION EXITOSA")
        print("  Los tres lenguajes trabajaron correctamente en secuencia.")
    else:
        print("  RESULTADO: INTEGRACION CON ERRORES")
        print("  Revisa los mensajes de error arriba.")
    print(SEP)

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    titulo("SISTEMA DE SELECCION DE PERSONAL")
    print("  Integracion: Scala -> Python -> Prolog")
    print(f"  Directorio base: {BASE}")

    resultados = []

    r0 = ejecutar_preprocesador()
    resultados.append(r0)
    if not r0:
        error("Preprocesador fallo. Abortando integracion.")
        mostrar_reporte_final(resultados + [False, False, False])
        sys.exit(1)

    r1 = ejecutar_scala()
    resultados.append(r1)
    if not r1:
        error("Scala fallo. Abortando integracion.")
        mostrar_reporte_final(resultados + [False, False])
        sys.exit(1)

    r2 = ejecutar_python()
    resultados.append(r2)
    if not r2:
        error("Python fallo. Abortando integracion.")
        mostrar_reporte_final(resultados + [False])
        sys.exit(1)

    r3 = ejecutar_prolog()
    resultados.append(r3)

    mostrar_reporte_final(resultados)

    sys.exit(0 if all(resultados) else 1)

if __name__ == "__main__":
    main()
