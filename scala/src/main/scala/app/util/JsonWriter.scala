package app.util

import io.circe.Encoder
import io.circe.syntax._
import java.io.{File, PrintWriter}
import scala.util.{Try, Success, Failure}

object JsonWriter {

  /** Serializa una lista de T a JSON y la escribe en rutaArchivo */
  def escribirLista[T: Encoder](lista: List[T], rutaArchivo: String): Unit = {
    val archivo = new File(rutaArchivo)
    Option(archivo.getParentFile).foreach(_.mkdirs())

    val json = lista.asJson.spaces2

    Try {
      val writer = new PrintWriter(archivo, "UTF-8")
      writer.write(json)
      writer.close()
    } match {
      case Success(_) =>
        println(s"[OK] Archivo guardado: $rutaArchivo (${lista.size} registros)")
      case Failure(ex) =>
        println(s"[ERROR] No se pudo escribir: $rutaArchivo")
        println(s"        Detalle: ${ex.getMessage}")
    }
  }
}
