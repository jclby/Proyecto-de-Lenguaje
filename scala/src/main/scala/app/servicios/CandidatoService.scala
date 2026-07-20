package app.servicios

import app.modelos.Candidato
import app.util.JsonReader

class CandidatoService(rutaArchivo: String) {

  private val candidatos: List[Candidato] = JsonReader.leerLista[Candidato](rutaArchivo)

  def obtenerTodos: List[Candidato] = candidatos

  def buscarPorId(id: Int): Option[Candidato] =
    candidatos.find(_.id == id)

  /** Candidatos con al menos N anios de experiencia */
  def conExperienciaMinima(anios: Int): List[Candidato] =
    candidatos.filter(_.aniosExperiencia >= anios)

  /** Candidatos que poseen una habilidad especifica */
  def conHabilidad(habilidad: String): List[Candidato] =
    candidatos.filter(_.habilidades.exists(_.equalsIgnoreCase(habilidad)))

  def resumen(): Unit = {
    println(s"\n--- Candidatos registrados (${candidatos.size}) ---")
    candidatos.foreach { c =>
      println(s"  [${c.id}] ${c.nombre} — ${c.aniosExperiencia} anios, ${c.nivelEducacion}")
      println(s"        Habilidades: ${c.habilidades.mkString(", ")}")
    }
  }
}
