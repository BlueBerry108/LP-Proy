import React, { useState, useEffect } from "react";
import API from "../api/axios";
import SectionCard from "./SectionCard";

export default function CourseCard({ curso, inscritas }) {
  const [secciones, setSecciones] = useState([]);

  useEffect(()=> {
    API.get(`/cursos/${curso.codigo_curso}/secciones/`)
      .then(r => setSecciones(r.data))
      .catch(()=> setSecciones([]));
  }, [curso.codigo_curso]);

  return (
    <div className="
      bg-white border border-blue-200 rounded-xl p-6 mb-6 shadow-sm 
      hover:shadow-md transition
    ">
      {/* Título del curso */}
      <h3 className="text-xl font-semibold text-blue-700 mb-1">
        {curso.nombre_curso}
      </h3>

      {/* Descripción */}
      <p className="text-gray-600 mb-4">
        {curso.desc_curso}
      </p>

      {/* Listado de secciones */}
      <div className="space-y-4">
        {secciones.map(s => (
          <SectionCard 
            key={s.codigo_seccion} 
            seccion={s} 
            cursoNombre={curso.nombre_curso} 
            inscritas={inscritas} 
          />
        ))}
      </div>
    </div>
  );
}