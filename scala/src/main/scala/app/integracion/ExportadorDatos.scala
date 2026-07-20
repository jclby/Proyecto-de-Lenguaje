package app.integracion

import app.modelos.Evaluacion
import app.util.JsonWriter
import io.circe.generic.semiauto._
import io.circe.Encoder

/**
 * Exporta las evaluaciones en un formato plano que Python convertira
 * a hechos Prolog en la Semana 3. Prolog usara estos datos crudos
 * (no el resultado preliminar) para calcular el puntaje de 0 a 100%.
 *
 * Formato de salida:
 * {
 *   "candidato":             "Ana Gutierrez",
 *   "puesto":                "Data Scientist",
 *   "aniosExperiencia":      4,
 *   "minAniosExperiencia":   3,
 *   "nivelEducacion":        "licenciatura",
 *   "nivelEducacionReq":     "licenciatura",
 *   "habilidadesCandidato":  ["Python", "SQL", ...],
 *   "habilidadesRequeridas": ["Python", "Machine Learning", "SQL"],
 *   "certCandidato":         ["AWS Certified", ...],
 *   "certDeseadas":          ["AWS Certified", "Google Cloud"]
 * }
 */
object ExportadorDatos {

  case class ParCandidatoPuesto(
      candidato:             String,
      puesto:                String,
      aniosExperiencia:      Int,
      minAniosExperiencia:   Int,
      nivelEducacion:        String,
      nivelEducacionReq:     String,
      habilidadesCandidato:  List[String],
      habilidadesRequeridas: List[String],
      certCandidato:         List[String],
      certDeseadas:          List[String]
  )

  implicit val encoder: Encoder[ParCandidatoPuesto] = deriveEncoder[ParCandidatoPuesto]

  def exportar(evaluaciones: List[Evaluacion], rutaSalida: String): Unit = {
    val pares = evaluaciones.map { e =>
      ParCandidatoPuesto(
        candidato             = e.candidato.nombre,
        puesto                = e.puesto.titulo,
        aniosExperiencia      = e.candidato.aniosExperiencia,
        minAniosExperiencia   = e.puesto.minAniosExperiencia,
        nivelEducacion        = e.candidato.nivelEducacion,
        nivelEducacionReq     = e.puesto.nivelEducacionRequerido,
        habilidadesCandidato  = e.candidato.habilidades,
        habilidadesRequeridas = e.puesto.habilidadesRequeridas,
        certCandidato         = e.candidato.certificaciones,
        certDeseadas          = e.puesto.certificacionesDeseadas
      )
    }
    JsonWriter.escribirLista(pares, rutaSalida)
    println(s"[Exportador] Datos listos para Python en: $rutaSalida")
  }
}
