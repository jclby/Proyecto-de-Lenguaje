# Sistema de Seleccion de Personal

Sistema que evalua la compatibilidad entre candidatos y puestos de trabajo,
generando un puntaje de 0 a 100%, mediante tres lenguajes de programacion
integrados.

## Arquitectura

```
Candidatos/Puestos (JSON)
        |
        v
     SCALA (gestion de datos, evaluacion preliminar)
        |
        v
     PYTHON (transformacion de datos)
        |
        v
     PROLOG (calculo de puntaje de compatibilidad 0-100%)
        |
        v
     PYTHON (lee resultados)
        |
        v
     FLASK + HTML (interfaz visual)
```

## Tecnologias

| Capa   | Lenguaje | Rol                                          |
|--------|----------|-----------------------------------------------|
| 1      | Scala    | Modelos, servicios, evaluacion preliminar     |
| 2      | Python   | Transformacion de datos JSON <-> Prolog       |
| 3      | Prolog   | Calculo de compatibilidad candidato-puesto    |
| 4      | Python/Flask | Interfaz web para visualizar resultados   |

## Estructura

```
seleccion-personal/
├── scala/       -> Nucleo del sistema (SBT + Circe)
├── python/      -> Capa de integracion
├── prolog/      -> Motor de reglas de compatibilidad
├── web/         -> Interfaz Flask + HTML
├── data/        -> Archivos de entrada y salida
├── docs/        -> Documentacion
└── integracion/ -> Guias de comunicacion entre capas
```

## Requisitos

- Scala 2.13 + SBT 1.9
- Python 3.10+
- SWI-Prolog 9+
- Flask (pip install flask)

## Fases de desarrollo

- [x] **Semana 1** — Estructura + configuracion + modelos Scala
- [ ] **Semana 2** — Servicios Scala + evaluacion preliminar + JSON
- [ ] **Semana 3** — Modulo Python + transformacion de datos
- [ ] **Semana 4** — Reglas Prolog: puntaje de compatibilidad 0-100%
- [ ] **Semana 5** — Integracion completa
- [ ] **Semana 6** — Interfaz Flask + HTML, pruebas y documentacion
