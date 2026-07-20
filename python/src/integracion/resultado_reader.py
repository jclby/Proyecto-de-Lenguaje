from utils.json_utils import leer_json

def leer_resultado_puntajes(ruta: str) -> list:
    """
    Lee el archivo puntajes.json que generara Prolog en la Semana 4.
    Devuelve la lista de evaluaciones con su puntaje de compatibilidad (0-100%).
    """
    datos = leer_json(ruta)
    if not datos:
        print("[resultado_reader] Sin puntajes encontrados o archivo aun no generado.")
    else:
        print(f"[resultado_reader] {len(datos)} puntajes calculados por Prolog.")
        for r in sorted(datos, key=lambda x: -x.get("puntaje", 0))[:5]:
            print(f"  {r.get('candidato')} -> {r.get('puesto')}: {r.get('puntaje')}%")
    return datos
