package app.servicios

import app.modelos.Puesto
import app.util.JsonReader

class PuestoService(rutaArchivo: String) {

  private val puestos: List[Puesto] = JsonReader.leerLista[Puesto](rutaArchivo)

  def obtenerTodos: List[Puesto] = puestos

  def buscarPorId(id: Int): Option[Puesto] =
    puestos.find(_.id == id)

  def buscarPorTitulo(titulo: String): Option[Puesto] =
    puestos.find(_.titulo.equalsIgnoreCase(titulo))

  def resumen(): Unit = {
    println(s"\n--- Puestos registrados (${puestos.size}) ---")
    puestos.foreach { p =>
      println(s"  [${p.id}] ${p.titulo} — min. ${p.minAniosExperiencia} anios, ${p.nivelEducacionRequerido}")
      println(s"        Requiere: ${p.habilidadesRequeridas.mkString(", ")}")
    }
  }
}
