% ============================================================
% validacion.pl - Punto de entrada principal de Prolog
%
% Uso desde terminal:
%   swipl -g "validar, halt" validacion.pl
%
% Uso interactivo en SWI-Prolog:
%   ?- [validacion].
%   ?- validar.
% ============================================================

:- consult(hechos).
:- consult(reglas).
:- consult(consultas).

% ------------------------------------------------------------
% Escapa comillas dobles para que el texto sea JSON valido
% ------------------------------------------------------------
escapar_json(Texto, Escapado) :-
    atom(Texto),
    atomic_list_concat(Partes, '"', Texto),
    atomic_list_concat(Partes, '\\"', Escapado).

% ------------------------------------------------------------
% Convierte un puntaje (con su explicacion) en una linea JSON
% ------------------------------------------------------------
linea_json(Candidato, Puesto, Puntaje, Clase, Explicacion, Linea) :-
    escapar_json(Explicacion, ExplicacionSegura),
    format(atom(Linea),
        '  {"candidato": "~w", "puesto": "~w", "puntaje": ~w, "clasificacion": "~w", "explicacion": "~w"}',
        [Candidato, Puesto, Puntaje, Clase, ExplicacionSegura]).

% ------------------------------------------------------------
% Exporta todos los puntajes a un archivo JSON
% (formato plano: lista de objetos, incluye explicacion textual)
% ------------------------------------------------------------
exportar_puntajes_json(RutaArchivo) :-
    findall(
        Linea,
        (
            evaluar_par(Candidato, Puesto),
            puntaje_total(Candidato, Puesto, Puntaje),
            clasificacion(Puntaje, Clase),
            explicar_compatibilidad(Candidato, Puesto, Explicacion),
            linea_json(Candidato, Puesto, Puntaje, Clase, Explicacion, Linea)
        ),
        Lineas
    ),
    atomic_list_concat(Lineas, ',\n', Cuerpo),
    format(atom(Json), '[\n~w\n]\n', [Cuerpo]),
    open(RutaArchivo, write, Stream),
    write(Stream, Json),
    close(Stream),
    length(Lineas, Total),
    format('[OK] Puntajes exportados a ~w (~w registros)~n', [RutaArchivo, Total]).

% ------------------------------------------------------------
% validar/0 - ejecuta el reporte completo en consola
% ------------------------------------------------------------
validar :-
    nl,
    write('============================================================'), nl,
    write('   SISTEMA DE SELECCION DE PERSONAL - VALIDACION'), nl,
    write('============================================================'), nl,
    nl,
    mostrar_puntajes,
    nl,
    mostrar_ranking_jerarquico,
    nl,
    mostrar_mejor_puesto_por_candidato,
    nl,
    mostrar_explicaciones,
    nl,
    exportar_puntajes_json('../data/salida/puntajes.json'),
    nl,
    write('============================================================'), nl.
