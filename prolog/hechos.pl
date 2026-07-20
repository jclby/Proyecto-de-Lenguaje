% ============================================================
% hechos.pl - generado automaticamente por Python
% No editar manualmente; regenerar ejecutando main.py
% ============================================================

% --- Candidatos: candidato(Atom, NivelEducacion, AniosExperiencia) ---
candidato(ana_gutierrez, licenciatura, 4).   % Ana Gutierrez
candidato(carlos_mendoza, licenciatura, 5).   % Carlos Mendoza
candidato(diego_ramirez, doctorado, 12).   % Diego Ramirez
candidato(gerson_contreras, bachiller, 1).   % Gerson Contreras
candidato(luis_paredes, maestria, 8).   % Luis Paredes
candidato(maria_quispe, bachiller, 1).   % Maria Quispe
candidato(sofia_torres, licenciatura, 3).   % Sofia Torres

% --- Puestos: puesto(Atom, NivelEducacionRequerido, MinAniosExperiencia) ---
puesto(data_scientist, licenciatura, 3).   % Data Scientist
puesto(junior_developer, bachiller, 0).   % Junior Developer
puesto(programador_junior, bachiller, 0).   % Programador Junior
puesto(tech_lead, licenciatura, 6).   % Tech Lead

% --- Habilidades que posee cada candidato ---
tiene_habilidad(ana_gutierrez, comunicacion).
tiene_habilidad(ana_gutierrez, machine_learning).
tiene_habilidad(ana_gutierrez, python).
tiene_habilidad(ana_gutierrez, sql).
tiene_habilidad(carlos_mendoza, comunicacion).
tiene_habilidad(carlos_mendoza, liderazgo).
tiene_habilidad(carlos_mendoza, machine_learning).
tiene_habilidad(carlos_mendoza, python).
tiene_habilidad(carlos_mendoza, sql).
tiene_habilidad(diego_ramirez, comunicacion).
tiene_habilidad(diego_ramirez, liderazgo).
tiene_habilidad(diego_ramirez, machine_learning).
tiene_habilidad(diego_ramirez, python).
tiene_habilidad(diego_ramirez, scala).
tiene_habilidad(diego_ramirez, sql).
tiene_habilidad(gerson_contreras, java).
tiene_habilidad(gerson_contreras, python).
tiene_habilidad(gerson_contreras, sql).
tiene_habilidad(luis_paredes, comunicacion).
tiene_habilidad(luis_paredes, java).
tiene_habilidad(luis_paredes, liderazgo).
tiene_habilidad(luis_paredes, scala).
tiene_habilidad(luis_paredes, sql).
tiene_habilidad(maria_quispe, css).
tiene_habilidad(maria_quispe, docker).
tiene_habilidad(maria_quispe, excel).
tiene_habilidad(maria_quispe, git).
tiene_habilidad(maria_quispe, html).
tiene_habilidad(maria_quispe, python).
tiene_habilidad(sofia_torres, aws).
tiene_habilidad(sofia_torres, comunicacion).
tiene_habilidad(sofia_torres, java).
tiene_habilidad(sofia_torres, kotlin).
tiene_habilidad(sofia_torres, sql).

% --- Habilidades requeridas por cada puesto ---
requiere_habilidad(data_scientist, machine_learning).
requiere_habilidad(data_scientist, python).
requiere_habilidad(data_scientist, sql).
requiere_habilidad(junior_developer, python).
requiere_habilidad(junior_developer, sql).
requiere_habilidad(programador_junior, java).
requiere_habilidad(programador_junior, python).
requiere_habilidad(programador_junior, sql).
requiere_habilidad(tech_lead, comunicacion).
requiere_habilidad(tech_lead, liderazgo).
requiere_habilidad(tech_lead, sql).

% --- Certificaciones que posee cada candidato ---
tiene_certificacion(ana_gutierrez, aws_certified).
tiene_certificacion(ana_gutierrez, scrum_master).
tiene_certificacion(carlos_mendoza, aws_certified).
tiene_certificacion(carlos_mendoza, google_cloud).
tiene_certificacion(carlos_mendoza, scrum_master).
tiene_certificacion(diego_ramirez, aws_certified).
tiene_certificacion(diego_ramirez, google_cloud).
tiene_certificacion(diego_ramirez, pmp).
tiene_certificacion(diego_ramirez, scrum_master).
tiene_certificacion(gerson_contreras, cisco).
tiene_certificacion(luis_paredes, oracle_certified).
tiene_certificacion(luis_paredes, pmp).
tiene_certificacion(sofia_torres, oracle_certified).

% --- Certificaciones deseadas por cada puesto ---
desea_certificacion(data_scientist, aws_certified).
desea_certificacion(data_scientist, google_cloud).
desea_certificacion(programador_junior, cisco).
desea_certificacion(tech_lead, pmp).
desea_certificacion(tech_lead, scrum_master).

% --- Habilidades equivalentes (intercambiables para el puntaje) ---
equivale(aws_certified, google_cloud).
equivale(deep_learning, machine_learning).
equivale(java, kotlin).
equivale(mysql, sql).
equivale(pmp, scrum_master).
equivale(postgresql, sql).
equivale(python, r).

% --- Pares candidato-puesto a evaluar ---
evaluar_par(ana_gutierrez, data_scientist).
evaluar_par(ana_gutierrez, junior_developer).
evaluar_par(ana_gutierrez, programador_junior).
evaluar_par(ana_gutierrez, tech_lead).
evaluar_par(carlos_mendoza, data_scientist).
evaluar_par(carlos_mendoza, junior_developer).
evaluar_par(carlos_mendoza, programador_junior).
evaluar_par(carlos_mendoza, tech_lead).
evaluar_par(diego_ramirez, data_scientist).
evaluar_par(diego_ramirez, junior_developer).
evaluar_par(diego_ramirez, programador_junior).
evaluar_par(diego_ramirez, tech_lead).
evaluar_par(gerson_contreras, data_scientist).
evaluar_par(gerson_contreras, junior_developer).
evaluar_par(gerson_contreras, programador_junior).
evaluar_par(gerson_contreras, tech_lead).
evaluar_par(luis_paredes, data_scientist).
evaluar_par(luis_paredes, junior_developer).
evaluar_par(luis_paredes, programador_junior).
evaluar_par(luis_paredes, tech_lead).
evaluar_par(maria_quispe, data_scientist).
evaluar_par(maria_quispe, junior_developer).
evaluar_par(maria_quispe, programador_junior).
evaluar_par(maria_quispe, tech_lead).
evaluar_par(sofia_torres, data_scientist).
evaluar_par(sofia_torres, junior_developer).
evaluar_par(sofia_torres, programador_junior).
evaluar_par(sofia_torres, tech_lead).
