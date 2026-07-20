% ============================================================
% reglas.pl - Motor de calculo de compatibilidad
% Puntaje de 0 a 100% por cada par (Candidato, Puesto)
% ============================================================

:- use_module(library(lists)).
:- dynamic(equivale/2).

% Jerarquia de niveles educativos (mayor numero = mayor nivel)
nivel_valor(tecnico,      1).
nivel_valor(bachiller,    2).
nivel_valor(licenciatura, 3).
nivel_valor(maestria,     4).
nivel_valor(doctorado,    5).

% ------------------------------------------------------------
% CRITERIO 1: Experiencia (25 puntos)
% Cumple si los anios del candidato >= minimo requerido
% ------------------------------------------------------------
cumple_experiencia(Candidato, Puesto) :-
    candidato(Candidato, _, AniosCand),
    puesto(Puesto, _, MinAnios),
    AniosCand >= MinAnios.

puntaje_experiencia(Candidato, Puesto, 25) :-
    cumple_experiencia(Candidato, Puesto), !.
puntaje_experiencia(_, _, 0).

% ------------------------------------------------------------
% CRITERIO 2: Educacion (25 puntos)
% Cumple si el nivel del candidato >= nivel requerido
% ------------------------------------------------------------
cumple_educacion(Candidato, Puesto) :-
    candidato(Candidato, NivelCand, _),
    puesto(Puesto, NivelReq, _),
    nivel_valor(NivelCand, ValorCand),
    nivel_valor(NivelReq, ValorReq),
    ValorCand >= ValorReq.

puntaje_educacion(Candidato, Puesto, 25) :-
    cumple_educacion(Candidato, Puesto), !.
puntaje_educacion(_, _, 0).

% ------------------------------------------------------------
% Equivalencia de habilidades (simetrica)
% equivale/2 se carga desde hechos.pl en una sola direccion;
% aqui se vuelve simetrica para poder consultarla en cualquier orden.
% ------------------------------------------------------------
son_equivalentes(H, H).
son_equivalentes(H1, H2) :- equivale(H1, H2).
son_equivalentes(H1, H2) :- equivale(H2, H1).

% ------------------------------------------------------------
% CRITERIO 3: Habilidades (35 puntos, proporcional)
% (habilidades que coinciden / habilidades requeridas) * 35
% Una habilidad requerida se considera cubierta si el candidato
% la tiene exactamente, o tiene una habilidad equivalente.
% ------------------------------------------------------------
habilidades_requeridas(Puesto, Lista) :-
    findall(H, requiere_habilidad(Puesto, H), Lista).

habilidades_candidato(Candidato, Lista) :-
    findall(H, tiene_habilidad(Candidato, H), Lista).

% Una requerida esta cubierta si coincide exacto o por equivalencia
requerida_cubierta(Candidato, Requerida) :-
    tiene_habilidad(Candidato, DelCandidato),
    son_equivalentes(Requerida, DelCandidato),
    !.

habilidades_coincidentes(Candidato, Puesto, Coincidentes) :-
    habilidades_requeridas(Puesto, Requeridas),
    include(requerida_cubierta(Candidato), Requeridas, Coincidentes).

puntaje_habilidades(Candidato, Puesto, Puntaje) :-
    habilidades_requeridas(Puesto, Requeridas),
    length(Requeridas, TotalReq),
    TotalReq > 0,
    !,
    habilidades_coincidentes(Candidato, Puesto, Coincidentes),
    length(Coincidentes, TotalCoinciden),
    Puntaje is round((TotalCoinciden / TotalReq) * 35).
% Si el puesto no requiere ninguna habilidad, otorgar el puntaje completo
puntaje_habilidades(_, _, 35).

% ------------------------------------------------------------
% CRITERIO 4: Certificaciones (15 puntos, proporcional)
% (certificaciones extra que coinciden / certificaciones deseadas) * 15
% Si el puesto no desea ninguna certificacion, otorgar el puntaje completo
% ------------------------------------------------------------
certificaciones_deseadas(Puesto, Lista) :-
    findall(C, desea_certificacion(Puesto, C), Lista).

certificaciones_candidato(Candidato, Lista) :-
    findall(C, tiene_certificacion(Candidato, C), Lista).

certificaciones_coincidentes(Candidato, Puesto, Coincidentes) :-
    certificaciones_deseadas(Puesto, Deseadas),
    certificaciones_candidato(Candidato, DelCandidato),
    intersection(Deseadas, DelCandidato, Coincidentes).

puntaje_certificaciones(Candidato, Puesto, Puntaje) :-
    certificaciones_deseadas(Puesto, Deseadas),
    length(Deseadas, TotalDeseadas),
    TotalDeseadas > 0,
    !,
    certificaciones_coincidentes(Candidato, Puesto, Coincidentes),
    length(Coincidentes, TotalCoinciden),
    Puntaje is round((TotalCoinciden / TotalDeseadas) * 15).
puntaje_certificaciones(_, _, 15).

% ------------------------------------------------------------
% PUNTAJE TOTAL: suma de los 4 criterios (0-100%)
% ------------------------------------------------------------
puntaje_total(Candidato, Puesto, Total) :-
    puntaje_experiencia(Candidato, Puesto, PExp),
    puntaje_educacion(Candidato, Puesto, PEdu),
    puntaje_habilidades(Candidato, Puesto, PHab),
    puntaje_certificaciones(Candidato, Puesto, PCert),
    Total is PExp + PEdu + PHab + PCert.

% ------------------------------------------------------------
% Clasificacion textual segun el puntaje
% ------------------------------------------------------------
clasificacion(Puntaje, 'Excelente')  :- Puntaje >= 85, !.
clasificacion(Puntaje, 'Bueno')      :- Puntaje >= 65, Puntaje < 85, !.
clasificacion(Puntaje, 'Regular')    :- Puntaje >= 45, Puntaje < 65, !.
clasificacion(_,       'Bajo').

% ------------------------------------------------------------
% Mejor candidato para un puesto especifico
% ------------------------------------------------------------
mejor_candidato_para(Puesto, MejorCandidato, MejorPuntaje) :-
    findall(
        Puntaje-Candidato,
        (evaluar_par(Candidato, Puesto), puntaje_total(Candidato, Puesto, Puntaje)),
        Pares
    ),
    sort(0, @>=, Pares, [MejorPuntaje-MejorCandidato|_]).

% ------------------------------------------------------------
% Mejor puesto para un candidato especifico
% ------------------------------------------------------------
mejor_puesto_para(Candidato, MejorPuesto, MejorPuntaje) :-
    findall(
        Puntaje-Puesto,
        (evaluar_par(Candidato, Puesto), puntaje_total(Candidato, Puesto, Puntaje)),
        Pares
    ),
    sort(0, @>=, Pares, [MejorPuntaje-MejorPuesto|_]).

% ============================================================
% COMPARACION JERARQUICA ENTRE CANDIDATOS (mejor_que/3)
% Compara dos candidatos para el MISMO puesto en cascada de
% criterios: primero experiencia, luego educacion, luego
% habilidades. Esto desempata casos donde el puntaje numerico
% es igual, mostrando un razonamiento logico explicito en vez
% de solo comparar el total.
% ============================================================

anios_de(Candidato, Anios) :-
    candidato(Candidato, _, Anios).

nivel_de(Candidato, Valor) :-
    candidato(Candidato, Nivel, _),
    nivel_valor(Nivel, Valor).

cantidad_habilidades_coincidentes(Candidato, Puesto, Cantidad) :-
    habilidades_coincidentes(Candidato, Puesto, Lista),
    length(Lista, Cantidad).

% C1 es mejor que C2 para Puesto si tiene mas anios de experiencia
mejor_que(C1, C2, Puesto) :-
    evaluar_par(C1, Puesto),
    evaluar_par(C2, Puesto),
    anios_de(C1, A1),
    anios_de(C2, A2),
    A1 > A2,
    !.

% Si empatan en experiencia, gana quien tiene mayor nivel educativo
mejor_que(C1, C2, Puesto) :-
    evaluar_par(C1, Puesto),
    evaluar_par(C2, Puesto),
    anios_de(C1, A1),
    anios_de(C2, A1),
    nivel_de(C1, N1),
    nivel_de(C2, N2),
    N1 > N2,
    !.

% Si tambien empatan en educacion, gana quien tiene mas habilidades coincidentes
mejor_que(C1, C2, Puesto) :-
    evaluar_par(C1, Puesto),
    evaluar_par(C2, Puesto),
    anios_de(C1, A1),
    anios_de(C2, A1),
    nivel_de(C1, N1),
    nivel_de(C2, N1),
    cantidad_habilidades_coincidentes(C1, Puesto, H1),
    cantidad_habilidades_coincidentes(C2, Puesto, H2),
    H1 > H2.

% ------------------------------------------------------------
% Razon textual de por que C1 es mejor que C2 (para mostrar al usuario)
% ------------------------------------------------------------
razon_mejor_que(C1, C2, Puesto, Razon) :-
    anios_de(C1, A1), anios_de(C2, A2),
    (   A1 > A2
    ->  format(atom(Razon), 'tiene mas experiencia (~w vs ~w años)', [A1, A2])
    ;   nivel_de(C1, N1), nivel_de(C2, N2),
        (   N1 > N2
        ->  Razon = 'tiene mayor nivel educativo, con experiencia equivalente'
        ;   cantidad_habilidades_coincidentes(C1, Puesto, H1),
            cantidad_habilidades_coincidentes(C2, Puesto, H2),
            format(atom(Razon), 'tiene mas habilidades relevantes (~w vs ~w), con experiencia y educacion equivalentes', [H1, H2])
        )
    ).

% ============================================================
% EXPLICACION DEL PORQUE (sistema experto simple)
% Genera un texto que justifica el puntaje obtenido, encadenando
% el resultado de cada criterio en lenguaje natural.
% ============================================================
explicar_compatibilidad(Candidato, Puesto, Explicacion) :-
    puntaje_experiencia(Candidato, Puesto, PExp),
    puntaje_educacion(Candidato, Puesto, PEdu),
    puntaje_certificaciones(Candidato, Puesto, PCert),

    % Frase de experiencia
    (   PExp > 0
    ->  FraseExp = 'cumple con la experiencia minima requerida'
    ;   candidato(Candidato, _, AniosCand),
        puesto(Puesto, _, MinAnios),
        format(atom(FraseExp), 'no cumple la experiencia minima (tiene ~w, se requieren ~w años)', [AniosCand, MinAnios])
    ),

    % Frase de educacion
    (   PEdu > 0
    ->  FraseEdu = 'su nivel educativo es igual o superior al requerido'
    ;   FraseEdu = 'su nivel educativo es inferior al requerido'
    ),

    % Frase de habilidades
    habilidades_requeridas(Puesto, Requeridas),
    length(Requeridas, TotalReq),
    habilidades_coincidentes(Candidato, Puesto, Coincidentes),
    length(Coincidentes, TotalCoinciden),
    habilidades_faltantes(Candidato, Puesto, Faltantes),
    (   TotalReq =:= 0
    ->  FraseHab = 'el puesto no exige habilidades especificas'
    ;   Faltantes == []
    ->  format(atom(FraseHab), 'cubre todas las habilidades requeridas (~w/~w)', [TotalCoinciden, TotalReq])
    ;   atomic_list_concat(Faltantes, ', ', FaltantesTexto),
        format(atom(FraseHab), 'cubre ~w de ~w habilidades requeridas; le faltan: ~w', [TotalCoinciden, TotalReq, FaltantesTexto])
    ),

    % Frase de certificaciones (proporcional, igual que habilidades, para
    % que el texto refleje el mismo numero que aporto al puntaje real)
    certificaciones_deseadas(Puesto, Deseadas),
    length(Deseadas, TotalDeseadas),
    certificaciones_coincidentes(Candidato, Puesto, CertCoincidentes),
    length(CertCoincidentes, TotalCertCoinciden),
    (   TotalDeseadas =:= 0
    ->  FraseCert = 'el puesto no exige certificaciones especificas'
    ;   TotalCertCoinciden =:= TotalDeseadas
    ->  format(atom(FraseCert), 'aporta todas las certificaciones valoradas (~w/~w, ~w puntos)', [TotalCertCoinciden, TotalDeseadas, PCert])
    ;   TotalCertCoinciden =:= 0
    ->  format(atom(FraseCert), 'no aporta certificaciones valoradas (0/~w, 0 puntos)', [TotalDeseadas])
    ;   format(atom(FraseCert), 'aporta ~w de ~w certificaciones valoradas (~w puntos)', [TotalCertCoinciden, TotalDeseadas, PCert])
    ),

    format(atom(Explicacion),
        'El candidato ~w: ~w. Ademas, ~w. En cuanto a habilidades, ~w. Por ultimo, ~w.',
        [Candidato, FraseExp, FraseEdu, FraseHab, FraseCert]).

% Lista de habilidades requeridas que el candidato NO cubre (ni exacto ni equivalente)
habilidades_faltantes(Candidato, Puesto, Faltantes) :-
    habilidades_requeridas(Puesto, Requeridas),
    exclude(requerida_cubierta(Candidato), Requeridas, Faltantes).
