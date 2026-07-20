"""
preprocesador.py
Paso 0 del pipeline (se ejecuta ANTES de 'sbt run').

Flujo:
  1. Lee candidatos.json y puestos.json (datos crudos de entrada)
  2. Valida y limpia los datos (edades negativas, duplicados, campos vacios)
  3. Aplica NLP basico: detecta habilidades mencionadas en 'resumenProfesional'
     que no esten ya en la lista estructurada de habilidades
  4. Sobrescribe candidatos.json y puestos.json con los datos limpios/enriquecidos
     para que Scala trabaje siempre con datos validados

Uso:
    python preprocesador.py
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(__file__))

from procesadores.validador_datos import validar_y_limpiar
from procesadores.extractor_habilidades import enriquecer_todos

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RUTA_CANDIDATOS = os.path.join(BASE, "data", "entrada", "candidatos.json")
RUTA_PUESTOS = os.path.join(BASE, "data", "entrada", "puestos.json")


def _leer(ruta):
    if not os.path.exists(ruta):
        print(f"[ERROR] No se encontro: {ruta}")
        return []
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)


def _escribir(datos, ruta):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)


def main():
    print("=" * 50)
    print("  PREPROCESADOR - Validacion y enriquecimiento NLP")
    print("=" * 50)

    # Paso 1: leer datos crudos
    print("\n[Paso 1] Leyendo datos de entrada...")
    candidatos = _leer(RUTA_CANDIDATOS)
    puestos = _leer(RUTA_PUESTOS)

    if not candidatos or not puestos:
        print("[ERROR] No se pudo continuar: faltan candidatos o puestos.")
        return

    print(f"  {len(candidatos)} candidatos, {len(puestos)} puestos leidos")

    # Paso 2: validar y limpiar
    print("\n[Paso 2] Validando y limpiando datos...")
    candidatos, puestos, avisos_validacion = validar_y_limpiar(candidatos, puestos)

    if avisos_validacion:
        print(f"  Se encontraron {len(avisos_validacion)} aviso(s):")
        for a in avisos_validacion:
            print(f"    - {a}")
    else:
        print("  Sin observaciones. Todos los datos son validos.")

    # Paso 3: enriquecer con NLP (busca habilidades en resumenProfesional)
    print("\n[Paso 3] Buscando habilidades en texto libre (NLP basico)...")
    candidatos, avisos_nlp = enriquecer_todos(candidatos)

    if avisos_nlp:
        print(f"  Se detectaron habilidades nuevas en {len(avisos_nlp)} candidato(s):")
        for a in avisos_nlp:
            print(f"    - {a}")
    else:
        print("  No se encontraron habilidades adicionales en los resumenes.")

    # Paso 4: guardar datos limpios y enriquecidos
    print("\n[Paso 4] Guardando datos procesados...")
    _escribir(candidatos, RUTA_CANDIDATOS)
    _escribir(puestos, RUTA_PUESTOS)
    print(f"  [OK] {RUTA_CANDIDATOS}")
    print(f"  [OK] {RUTA_PUESTOS}")

    print("\n" + "=" * 50)
    print("  Preprocesamiento completo. Datos listos para Scala (sbt run).")
    print("=" * 50)


if __name__ == "__main__":
    main()
