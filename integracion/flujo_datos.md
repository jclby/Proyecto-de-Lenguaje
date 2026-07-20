# Flujo de datos — Integracion completa

## Diagrama

```
integrador.py (orquestador)
       |
       |-- [1] sbt run
       |         Scala lee:  data/entrada/candidatos.json
       |                     data/entrada/puestos.json
       |         Scala genera: data/salida/evaluaciones_preliminares.json
       |                       data/salida/para_python.json  <-- clave
       |
       |-- [2] python main.py
       |         Python lee:   data/salida/para_python.json
       |         Python genera: prolog/hechos.pl             <-- clave
       |
       |-- [3] swipl validacion.pl
                 Prolog carga: prolog/hechos.pl
                               prolog/reglas.pl
                               prolog/consultas.pl
                 Prolog calcula: puntaje de 0 a 100% por cada par candidato-puesto
                 Prolog exporta: data/salida/puntajes.json    <-- usado por Flask en Semana 6
```

## Formato de cada archivo clave

### data/salida/para_python.json
Generado por ExportadorDatos.scala. Un registro por cada par (candidato, puesto):
```json
[
  {
    "candidato": "Ana Gutierrez",
    "puesto": "Data Scientist",
    "aniosExperiencia": 4,
    "minAniosExperiencia": 3,
    "nivelEducacion": "licenciatura",
    "nivelEducacionReq": "licenciatura",
    "habilidadesCandidato": ["Python", "SQL", "Machine Learning", "Comunicacion"],
    "habilidadesRequeridas": ["Python", "Machine Learning", "SQL"],
    "certCandidato": ["AWS Certified", "Scrum Master"],
    "certDeseadas": ["AWS Certified", "Google Cloud"]
  }
]
```

### prolog/hechos.pl
Generado por prolog_writer.py. Hechos Prolog listos para calcular el puntaje:
```prolog
candidato(ana_gutierrez, licenciatura, 4).
puesto(data_scientist, licenciatura, 3).
tiene_habilidad(ana_gutierrez, python).
requiere_habilidad(data_scientist, python).
evaluar_par(ana_gutierrez, data_scientist).
```

### data/salida/puntajes.json
Generado por validacion.pl. Resultado final del calculo:
```json
[
  {"candidato": "ana_gutierrez", "puesto": "data_scientist", "puntaje": 100, "clasificacion": "Excelente"}
]
```

## Como ejecutar

### Integracion completa (recomendado)
```bash
# Desde la raiz del proyecto
python integrador.py
```

### Por partes (manual)
```bash
# 1. Scala
cd scala && sbt run

# 2. Python
cd python/src && python main.py

# 3. Prolog
cd prolog && swipl -g "validar, halt" validacion.pl
```
