package app.util

import io.circe.Decoder
import io.circe.parser.decode
import scala.io.Source
import scala.util.{Try, Success, Failure}

object JsonReader {

  /** Lee un archivo JSON y lo decodifica a una lista de T */
  def leerLista[T: Decoder](rutaArchivo: String): List[T] = {
    Try {
      val fuente    = Source.fromFile(rutaArchivo, "UTF-8")
      val contenido = fuente.mkString
      fuente.close()
      contenido
    } match {
      case Failure(ex) =>
        println(s"[ERROR] No se pudo leer el archivo: $rutaArchivo")
        println(s"        Detalle: ${ex.getMessage}")
        List.empty

      case Success(contenido) =>
        decode[List[T]](contenido) match {
          case Left(error) =>
            println(s"[ERROR] JSON invalido en $rutaArchivo: $error")
            List.empty
          case Right(lista) =>
            println(s"[OK] Leidos ${lista.size} registros desde $rutaArchivo")
            lista
        }
    }
  }
}
