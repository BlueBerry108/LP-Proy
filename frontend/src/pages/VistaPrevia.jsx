import React, { useContext } from "react";
import API from "../api/axios";
import { MatriculaContext } from "../context/MatriculaContext";
import { useNavigate } from "react-router-dom";

export default function VistaPrevia() {
  const { selecciones, limpiarTodo } = useContext(MatriculaContext);
  const alumno = JSON.parse(localStorage.getItem("alumno") || "{}");
  const nav = useNavigate();

  async function confirmar() {
    try {
      const ids = selecciones.map(s => s.codigo_seccion);
      // POST a /matricular/
      const res = await API.post("/matricular/", { codigo_alumno: alumno.codigo_alumno, secciones: ids });
      // res.data tiene matricula_id y detalles
      limpiarTodo();
      nav("/confirmacion");
    } catch (e) {
      alert(e.response?.data?.detail || "Error al matricular");
    }
  }

  function cancelar() {
    limpiarTodo();
    nav("/cursos");
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-sky-100 to-blue-200 p-6 flex justify-center">
      <div className="w-full max-w-3xl bg-white shadow-xl rounded-2xl p-8">
        
        {/* Título */}
        <h2 className="text-3xl font-bold text-blue-800 mb-6 text-center">
          Vista previa de matrícula
        </h2>

        {/* Resumen del alumno */}
        <div className="mb-6">
          <p className="text-blue-700 text-lg font-semibold">
            Alumno: <span className="font-normal">{alumno.nombre_alumno}</span>
          </p>
          <p className="text-blue-700 text-lg font-semibold">
            Código: <span className="font-normal">{alumno.codigo_alumno}</span>
          </p>
        </div>

        {/* Lista de cursos seleccionados */}
        <div className="bg-blue-50 rounded-xl p-5 border border-blue-200 shadow-inner">
          <h3 className="text-xl font-semibold text-blue-800 mb-3">
            Cursos seleccionados ({selecciones.length})
          </h3>

          {selecciones.length === 0 ? (
            <p className="text-blue-600">No has seleccionado ninguna sección.</p>
          ) : (
            <ul className="space-y-3">
              {selecciones.map(s => (
                <li
                  key={s.codigo_seccion}
                  className="bg-white border border-blue-200 rounded-lg p-4 shadow-sm"
                >
                  <p className="font-semibold text-blue-800">
                    {s.cursoNombre}
                  </p>
                  <p className="text-blue-700">
                    Sección: <span className="font-medium">{s.codigo_seccion}</span>
                  </p>
                  <p className="text-blue-700">
                    Horario: <span className="font-medium">{s.horario_seccion}</span>
                  </p>
                </li>
              ))}
            </ul>
          )}
        </div>

        {/* Botones */}
        <div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
          <button
            onClick={confirmar}
            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg shadow-md transition"
          >
            Confirmar matrícula
          </button>

          <button
            onClick={cancelar}
            className="px-6 py-3 bg-red-500 hover:bg-red-600 text-white font-semibold rounded-lg shadow-md transition"
          >
            Cancelar
          </button>
        </div>
      </div>
    </div>
  );
}