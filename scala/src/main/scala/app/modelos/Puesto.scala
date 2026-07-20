package app.modelos

import io.circe.generic.semiauto._
import io.circe.{Decoder, Encoder}

case class Puesto(
    id:                      Int,
    titulo:                  String,
    minAniosExperiencia:     Int,
    nivelEducacionRequerido: String,   // nivel minimo requerido
    habilidadesRequeridas:   List[String],
    certificacionesDeseadas: List[String]
)

object Puesto {
  implicit val encoder: Encoder[Puesto] = deriveEncoder[Puesto]
  implicit val decoder: Decoder[Puesto] = deriveDecoder[Puesto]
}
