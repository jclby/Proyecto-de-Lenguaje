package app

import app.servicios.{CandidatoService, PuestoService}
import app.gestores.EvaluadorPersonal
import app.integracion.ExportadorDatos
import app.util.JsonWriter

object Main extends App {

  println("=== Sistema de Seleccion de Personal ===\n")

  // ── Rutas de archivos ────────────────────────────────────────────────────
  // Ajusta esta ruta base segun donde tengas el proyecto en tu maquina
  val rutaBase = "../data"

  val rutaCandidatos = s"$rutaBase/entrada/candidatos.json"
  val rutaPuestos     = s"$rutaBase/entrada/puestos.json"
  val rutaSalida      = s"$rutaBase/salida/evaluaciones_preliminares.json"
  val rutaExportado   = s"$rutaBase/salida/para_python.json"

  // ── Fase 1: Cargar datos ─────────────────────────────────────────────────
  println("[ Fase 1 ] Cargando datos de entrada...")
  val candidatoService = new CandidatoService(rutaCandidatos)
  val puestoService    = new PuestoService(rutaPuestos)

  candidatoService.resumen()
  puestoService.resumen()

  // ── Fase 2: Generar evaluaciones preliminares ────────────────────────────
  println("\n[ Fase 2 ] Generando evaluaciones preliminares...")
  val evaluador    = new EvaluadorPersonal(candidatoService, puestoService)
  val evaluaciones = evaluador.evaluarTodos()

  evaluador.imprimirReporte(evaluaciones)

  // ── Fase 3: Guardar resultados ───────────────────────────────────────────
  println("\n[ Fase 3 ] Guardando resultados...")
  JsonWriter.escribirLista(evaluaciones, rutaSalida)

  // ── Fase 4: Exportar para Python (Semana 3) ──────────────────────────────
  println("\n[ Fase 4 ] Exportando datos para Python...")
  ExportadorDatos.exportar(evaluaciones, rutaExportado)

  println("\nProceso completado! Revisa data/salida/ para ver los resultados.")
}

