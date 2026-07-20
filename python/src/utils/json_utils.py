import json
import os

def leer_json(ruta: str) -> list:
    """Lee un archivo JSON y devuelve su contenido como lista."""
    if not os.path.exists(ruta):
        print(f"[ERROR] Archivo no encontrado: {ruta}")
        return []
    with open(ruta, "r", encoding="utf-8") as f:
        datos = json.load(f)
    print(f"[OK] Leidos {len(datos)} registros desde {ruta}")
    return datos

def escribir_json(datos, ruta: str) -> None:
    """Escribe datos (lista o dict) como JSON formateado."""
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    print(f"[OK] Archivo guardado: {ruta}")
