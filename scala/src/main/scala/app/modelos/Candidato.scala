package app.modelos

import io.circe.generic.semiauto._
import io.circe.{Decoder, Encoder}

case class Candidato(
    id:               Int,
    nombre:           String,
    edad:             Int,
    aniosExperiencia: Int,
    nivelEducacion:   String,   // "tecnico", "bachiller", "licenciatura", "maestria", "doctorado"
    habilidades:      List[String],
    certificaciones:  List[String]
)

object Candidato {
  implicit val encoder: Encoder[Candidato] = deriveEncoder[Candidato]
  implicit val decoder: Decoder[Candidato] = deriveDecoder[Candidato]
}
