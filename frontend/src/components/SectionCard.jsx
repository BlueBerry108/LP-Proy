import React, { useContext } from "react";
import { MatriculaContext } from "../context/MatriculaContext";
import { parseHorario, schedulesConflict } from "../utils/horario";

export default function SectionCard({ seccion, cursoNombre, inscritas }) {
  const { selecciones, agregarSeccion } = useContext(MatriculaContext);
  const id = seccion.codigo_seccion;

  // si alumno ya inscrito en esta sección => deshabilitado
  const yaInscrito = inscritas.includes(id);

  // si curso ya seleccionado en el carrito => bloquear (misma regla que backend)
  const mismoCursoSeleccionado = selecciones.some(s => s.cursoNombre === cursoNombre);

  // verificar cruce horario con las selecciones actuales
  const selHorarios = [].concat(...selecciones.map(s => parseHorario(s.horario_seccion || "")));
  const thisHorarios = parseHorario(seccion.horario_seccion || "");
  const hayConflicto = selHorarios.length && schedulesConflict(selHorarios, thisHorarios);

  function onAdd() {
    if (yaInscrito) return alert("Ya estás inscrito en esta sección.");
    if (mismoCursoSeleccionado) return alert("Ya seleccionaste una sección de este curso.");
    if (hayConflicto) return alert("Conflicto de horario con una sección seleccionada.");
    // agregar objeto con la info necesaria
    agregarSeccion({
      codigo_seccion: seccion.codigo_seccion,
      horario_seccion: seccion.horario_seccion,
      codigo_curso: seccion.codigo_curso,
      cursoNombre,
    });
  }

  return (
    <div className="
      border border-blue-200 bg-white rounded-xl shadow-sm p-5 mb-4 
      hover:shadow-md transition
    ">
      <div className="flex justify-between items-center mb-3">
        <h3 className="text-lg font-semibold text-blue-700">
          Sección {id}
        </h3>
        {yaInscrito && (
          <span className="text-xs bg-green-100 text-green-700 px-3 py-1 rounded-full">
            Inscrito
          </span>
        )}
        {hayConflicto && (
          <span className="text-xs bg-red-100 text-red-700 px-3 py-1 rounded-full">
            Conflicto
          </span>
        )}
      </div>

      <p className="text-gray-600 mb-1">
        <span className="font-medium">Horario:</span> {seccion.horario_seccion}
      </p>

      <p className="text-gray-600 mb-4">
        <span className="font-medium">Docente:</span> {seccion.codigo_docente}
      </p>

      <button
  onClick={onAdd}
  disabled={yaInscrito || mismoCursoSeleccionado || hayConflicto}
  className={`w-full mt-2 py-2 rounded-lg font-medium transition-colors
    ${yaInscrito
      ? "bg-green-400 text-white cursor-not-allowed"
      : (mismoCursoSeleccionado || hayConflicto)
        ? "bg-gray-300 text-gray-500 cursor-not-allowed"
        : "bg-blue-500 text-white hover:bg-blue-600"
    }
  `}
>
        {yaInscrito ? "Inscrito" : "Agregar"}
      </button>
    </div>
  );
}