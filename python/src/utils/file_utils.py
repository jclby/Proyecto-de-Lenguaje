import os

def asegurar_directorio(ruta: str) -> None:
    """Crea el directorio si no existe."""
    os.makedirs(ruta, exist_ok=True)

def existe_archivo(ruta: str) -> bool:
    return os.path.isfile(ruta)

def leer_texto(ruta: str) -> str:
    with open(ruta, "r", encoding="utf-8") as f:
        return f.read()

def escribir_texto(contenido: str, ruta: str) -> None:
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)
    print(f"[OK] Archivo guardado: {ruta}")
