package app.modelos

import io.circe.generic.semiauto._
import io.circe.{Decoder, Encoder}

case class Evaluacion(
    candidato:             Candidato,
    puesto:                Puesto,
    cumpleExperiencia:     Boolean,
    cumpleEducacion:       Boolean,
    habilidadesCoinciden:  List[String],   // habilidades que el candidato tiene y el puesto pide
    habilidadesFaltantes:  List[String],   // habilidades que el puesto pide y el candidato no tiene
    certificacionesExtra:  List[String]    // certificaciones adicionales del candidato
)

object Evaluacion {
  implicit val encoder: Encoder[Evaluacion] = deriveEncoder[Evaluacion]
  implicit val decoder: Decoder[Evaluacion] = deriveDecoder[Evaluacion]
}
