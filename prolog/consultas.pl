% ============================================================
% consultas.pl - Consultas del sistema de seleccion
% ============================================================

% ------------------------------------------------------------
% Mostrar todos los puntajes calculados
% ------------------------------------------------------------
mostrar_puntajes :-
    write('=== PUNTAJES DE COMPATIBILIDAD ==='), nl,
    forall(
        evaluar_par(Candidato, Puesto),
        (
            puntaje_total(Candidato, Puesto, Puntaje),
            clasificacion(Puntaje, Clase),
            format('  ~w -> ~w : ~w% (~w)~n', [Candidato, Puesto, Puntaje, Clase])
        )
    ).

% ------------------------------------------------------------
% Mostrar el ranking de candidatos para cada puesto
% ------------------------------------------------------------
mostrar_ranking_por_puesto :-
    write('=== RANKING DE CANDIDATOS POR PUESTO ==='), nl,
    forall(
        puesto(Puesto, _, _),
        (
            nl,
            format('  [Puesto: ~w]~n', [Puesto]),
            findall(
                Puntaje-Candidato,
                (evaluar_par(Candidato, Puesto), puntaje_total(Candidato, Puesto, Puntaje)),
                Pares
            ),
            sort(0, @>=, Pares, Ordenados),
            forall(
                member(P-C, Ordenados),
                (clasificacion(P, Clase), format('    ~w : ~w% (~w)~n', [C, P, Clase]))
            )
        )
    ).

% ------------------------------------------------------------
% Mostrar el mejor puesto para cada candidato
% ------------------------------------------------------------
mostrar_mejor_puesto_por_candidato :-
    write('=== MEJOR PUESTO PARA CADA CANDIDATO ==='), nl,
    forall(
        candidato(Candidato, _, _),
        (
            mejor_puesto_para(Candidato, Puesto, Puntaje),
            format('  ~w -> ~w (~w%)~n', [Candidato, Puesto, Puntaje])
        )
    ).

% ------------------------------------------------------------
% Mostrar detalle de un par especifico (desglose del puntaje)
% ------------------------------------------------------------
mostrar_detalle(Candidato, Puesto) :-
    format('=== DETALLE: ~w -> ~w ===~n', [Candidato, Puesto]),
    puntaje_experiencia(Candidato, Puesto, PExp),
    puntaje_educacion(Candidato, Puesto, PEdu),
    puntaje_habilidades(Candidato, Puesto, PHab),
    puntaje_certificaciones(Candidato, Puesto, PCert),
    puntaje_total(Candidato, Puesto, Total),
    format('  Experiencia:      ~w/25~n', [PExp]),
    format('  Educacion:        ~w/25~n', [PEdu]),
    format('  Habilidades:      ~w/35~n', [PHab]),
    format('  Certificaciones:  ~w/15~n', [PCert]),
    format('  TOTAL:            ~w/100~n', [Total]).

% ------------------------------------------------------------
% Mostrar la explicacion en lenguaje natural de cada evaluacion
% ------------------------------------------------------------
mostrar_explicaciones :-
    write('=== EXPLICACION DE CADA EVALUACION ==='), nl,
    forall(
        evaluar_par(Candidato, Puesto),
        (
            explicar_compatibilidad(Candidato, Puesto, Explicacion),
            format('  [~w -> ~w]~n', [Candidato, Puesto]),
            format('    ~w~n', [Explicacion])
        )
    ).

% ------------------------------------------------------------
% Mostrar ranking jerarquico por puesto usando mejor_que/3
% (ordena por puntaje, y para empates explica por que uno
%  esta antes que otro usando el razonamiento en cascada)
% ------------------------------------------------------------
mostrar_ranking_jerarquico :-
    write('=== RANKING JERARQUICO (con desempate logico) ==='), nl,
    forall(
        puesto(Puesto, _, _),
        (
            nl,
            format('  [Puesto: ~w]~n', [Puesto]),
            findall(C, evaluar_par(C, Puesto), Candidatos),
            predsort(comparar_para_ranking(Puesto), Candidatos, Ordenados),
            forall(
                member(C, Ordenados),
                (
                    puntaje_total(C, Puesto, P),
                    format('    ~w : ~w%~n', [C, P])
                )
            ),
            mostrar_desempates(Ordenados, Puesto)
        )
    ).

% Comparador para predsort: ordena de mejor a peor usando mejor_que/3
comparar_para_ranking(Puesto, Orden, C1, C2) :-
    (   mejor_que(C1, C2, Puesto) -> Orden = (<)
    ;   mejor_que(C2, C1, Puesto) -> Orden = (>)
    ;   Orden = (=)
    ).

% Muestra la razon de desempate entre candidatos consecutivos con puntaje igual
mostrar_desempates([C1, C2 | Resto], Puesto) :-
    puntaje_total(C1, Puesto, P1),
    puntaje_total(C2, Puesto, P2),
    (   P1 =:= P2, mejor_que(C1, C2, Puesto)
    ->  razon_mejor_que(C1, C2, Puesto, Razon),
        format('      (~w queda sobre ~w: ~w)~n', [C1, C2, Razon])
    ;   true
    ),
    mostrar_desempates([C2 | Resto], Puesto).
mostrar_desempates(_, _).
