from utils.json_utils import leer_json

def leer_pares_candidato_puesto(ruta: str) -> list:
    """
    Lee el archivo para_python.json generado por ExportadorDatos.scala.
    Cada registro representa un par (candidato, puesto) con todos los
    datos crudos necesarios para que Prolog calcule el puntaje.
    """
    pares = leer_json(ruta)
    if pares:
        print(f"[scala_reader] {len(pares)} pares candidato-puesto cargados desde Scala.")
    return pares
