import React, { useState, useEffect, useContext } from "react";
import API from "../api/axios";
import CourseCard from "../components/CourseCard";
import { MatriculaContext } from "../context/MatriculaContext";

export default function CursosDisponibles() {
  const alumno = JSON.parse(localStorage.getItem("alumno") || "{}");
  const [cursos, setCursos] = useState([]);
  const [inscritas, setInscritas] = useState([]); // secciones ya inscritas
  const { selecciones } = useContext(MatriculaContext);

  useEffect(()=> {
    if (!alumno.codigo_alumno) return;
    API.get(`/alumnos/${alumno.codigo_alumno}/cursos/`).then(r=>setCursos(r.data));
    // obtener inscripciones existentes (si añadiste endpoint)
    API.get(`/alumnos/${alumno.codigo_alumno}/inscripciones/`)
      .then(r => setInscritas(r.data.secciones || []))
      .catch(() => setInscritas([]));
  }, [alumno.codigo_alumno]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100 p-6">

      {/* Contenedor principal */}
      <div className="max-w-6xl mx-auto">
        
        {/* Encabezado */}
        <h2 className="text-3xl font-bold text-blue-800 mb-6 text-center">
          Cursos disponibles — Ciclo {alumno.ciclo_alumno}
        </h2>

        {/* Sección principal con cursos */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
          {cursos.map(c => (
            <CourseCard 
              key={c.codigo_curso} 
              curso={c} 
              inscritas={inscritas}
            />
          ))}
        </div>

        {/* Panel lateral inferior para las selecciones */}
        <div className="
          bg-white shadow-md border border-blue-200 rounded-xl p-6 
          max-w-xl mx-auto
        ">
          <h3 className="text-xl font-semibold text-blue-700 mb-3">
            Selecciones ({selecciones.length})
          </h3>

          {selecciones.length === 0 ? (
            <p className="text-gray-500">No has seleccionado ninguna sección.</p>
          ) : (
            <ul className="space-y-2 mb-4">
              {selecciones.map(s => (
                <li 
                  key={s.codigo_seccion} 
                  className="bg-blue-50 border border-blue-200 rounded-lg p-3"
                >
                  <span className="font-medium text-blue-700">{s.cursoNombre}</span>
                  <span className="text-gray-600"> — Sección {s.codigo_seccion}</span>
                </li>
              ))}
            </ul>
          )}

          <a 
            href="/vista-previa"
            className="
              block text-center bg-blue-600 text-white 
              py-2 rounded-lg font-medium 
              hover:bg-blue-700 transition
            "
          >
            Ir a vista previa
          </a>
        </div>
      </div>
    </div>
  );
}