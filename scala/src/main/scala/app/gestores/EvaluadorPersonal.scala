package app.gestores

import app.modelos.{Candidato, Puesto, Evaluacion}
import app.servicios.{CandidatoService, PuestoService}

class EvaluadorPersonal(
    candidatoService: CandidatoService,
    puestoService:    PuestoService
) {

  // Jerarquia de niveles educativos: a mayor numero, mayor nivel
  private val nivelesEducacion: Map[String, Int] = Map(
    "tecnico"      -> 1,
    "bachiller"    -> 2,
    "licenciatura" -> 3,
    "maestria"     -> 4,
    "doctorado"    -> 5
  )

  private def rangoNivel(nivel: String): Int =
    nivelesEducacion.getOrElse(nivel.toLowerCase, 0)

  /**
   * Genera una evaluacion preliminar comparando un candidato contra un puesto.
   * Esta evaluacion NO calcula el puntaje final (eso lo hara Prolog en Semana 4),
   * solo recopila los datos comparativos: que cumple, que falta, que tiene de extra.
   */
  def evaluar(candidato: Candidato, puesto: Puesto): Evaluacion = {

    val cumpleExperiencia = candidato.aniosExperiencia >= puesto.minAniosExperiencia
    val cumpleEducacion   = rangoNivel(candidato.nivelEducacion) >= rangoNivel(puesto.nivelEducacionRequerido)

    val habilidadesCandidato = candidato.habilidades.map(_.toLowerCase).toSet
    val habilidadesPuesto    = puesto.habilidadesRequeridas.map(_.toLowerCase).toSet

    val habilidadesCoinciden = puesto.habilidadesRequeridas
      .filter(h => habilidadesCandidato.contains(h.toLowerCase))

    val habilidadesFaltantes = puesto.habilidadesRequeridas
      .filterNot(h => habilidadesCandidato.contains(h.toLowerCase))

    val certificacionesCandidato = candidato.certificaciones.map(_.toLowerCase).toSet
    val certificacionesDeseadas  = puesto.certificacionesDeseadas.map(_.toLowerCase).toSet

    val certificacionesExtra = candidato.certificaciones
      .filter(c => certificacionesDeseadas.contains(c.toLowerCase))

    Evaluacion(
      candidato            = candidato,
      puesto               = puesto,
      cumpleExperiencia    = cumpleExperiencia,
      cumpleEducacion      = cumpleEducacion,
      habilidadesCoinciden = habilidadesCoinciden,
      habilidadesFaltantes = habilidadesFaltantes,
      certificacionesExtra = certificacionesExtra
    )
  }

  /**
   * Genera evaluaciones de TODOS los candidatos contra TODOS los puestos.
   * El producto cartesiano completo: cada candidato es evaluado para cada puesto.
   */
  def evaluarTodos(): List[Evaluacion] = {
    val candidatos = candidatoService.obtenerTodos
    val puestos    = puestoService.obtenerTodos

    for {
      puesto    <- puestos
      candidato <- candidatos
    } yield evaluar(candidato, puesto)
  }

  /** Reporte en consola agrupado por puesto */
  def imprimirReporte(evaluaciones: List[Evaluacion]): Unit = {
    val sep = "=" * 62
    println(s"\n$sep")
    println("    EVALUACION PRELIMINAR CANDIDATO - PUESTO")
    println(sep)

    val porPuesto = evaluaciones.groupBy(_.puesto.titulo)

    porPuesto.foreach { case (titulo, evals) =>
      println(s"\n  [Puesto: $titulo]")
      println("  " + "-" * 58)
      evals.foreach { e =>
        val expOk = if (e.cumpleExperiencia) "OK" else "NO"
        val eduOk = if (e.cumpleEducacion)   "OK" else "NO"
        println(s"  ${e.candidato.nombre.padTo(20, ' ')} Exp:$expOk  Edu:$eduOk  " +
                 s"Habilidades: ${e.habilidadesCoinciden.size}/${e.puesto.habilidadesRequeridas.size}")
        if (e.habilidadesFaltantes.nonEmpty)
          println(s"    Faltan: ${e.habilidadesFaltantes.mkString(", ")}")
      }
    }
    println(s"\n$sep")
    println(s"  Total evaluaciones generadas: ${evaluaciones.size}")
    println(sep)
  }
}
