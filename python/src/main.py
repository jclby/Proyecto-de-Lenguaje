"""
main.py - Modulo Python (post-Scala)
Flujo:
  1. Lee para_python.json exportado por Scala
  2. Transforma cada par candidato-puesto a atomos Prolog validos
  3. Carga equivalencias_habilidades.json y las convierte a atomos
  4. Genera prolog/hechos.pl automaticamente con todo lo anterior
"""

import sys
import os
import json

# Permite importar modulos desde src/
sys.path.insert(0, os.path.dirname(__file__))

from integracion.scala_reader        import leer_pares_candidato_puesto
from procesadores.transformador_datos import transformar_pares, transformar_equivalencias
from integracion.prolog_writer        import generar_hechos

# ── Rutas (relativas al archivo main.py) ─────────────────────────────────────
# src -> python -> seleccion-personal (2 niveles arriba)
BASE              = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RUTA_ENTRADA      = os.path.join(BASE, "data", "salida", "para_python.json")
RUTA_EQUIVALENCIAS = os.path.join(BASE, "data", "entrada", "equivalencias_habilidades.json")
RUTA_HECHOS       = os.path.join(BASE, "prolog", "hechos.pl")


def _leer_equivalencias():
    if not os.path.exists(RUTA_EQUIVALENCIAS):
        return []
    with open(RUTA_EQUIVALENCIAS, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    print("=" * 50)
    print("  MODULO PYTHON - Transformacion de datos")
    print("=" * 50)

    # Paso 1: leer pares candidato-puesto desde Scala
    print("\n[Paso 1] Leyendo pares candidato-puesto de Scala...")
    pares = leer_pares_candidato_puesto(RUTA_ENTRADA)

    if not pares:
        print("[ERROR] No hay datos. Ejecuta primero 'sbt run' en scala/")
        return

    # Paso 2: transformar a formato Prolog
    print("\n[Paso 2] Transformando datos a atomos Prolog...")
    datos = transformar_pares(pares)

    # Mostrar preview de la transformacion
    print("\n  Preview de atomos generados:")
    for atom, original, anios, nivel in datos["candidatos"][:3]:
        print(f"    candidato({atom}, {nivel}, {anios})   <- '{original}'")
    for atom, original, min_anios, nivel in datos["puestos"]:
        print(f"    puesto({atom}, {nivel}, {min_anios})   <- '{original}'")

    # Paso 3: cargar y transformar equivalencias de habilidades
    print("\n[Paso 3] Cargando equivalencias de habilidades...")
    equivalencias_crudas = _leer_equivalencias()
    equivalencias = transformar_equivalencias(equivalencias_crudas)
    print(f"  {len(equivalencias)} equivalencias cargadas:")
    for a, b in equivalencias:
        print(f"    equivale({a}, {b})")

    # Paso 4: generar hechos.pl
    print("\n[Paso 4] Generando hechos.pl para Prolog...")
    generar_hechos(datos, RUTA_HECHOS, equivalencias=equivalencias)

    print("\n" + "=" * 50)
    print("  Listo. Archivo generado:")
    print(f"  {RUTA_HECHOS}")
    print("=" * 50)
    print("\nLas reglas en prolog/reglas.pl calcularan el puntaje 0-100%")

if __name__ == "__main__":
    main()
