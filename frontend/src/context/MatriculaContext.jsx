import React, { createContext, useState } from "react";

export const MatriculaContext = createContext();

export function MatriculaProvider({ children }) {
  const [selecciones, setSelecciones] = useState([]); // array de objetos sección

  function agregarSeccion(seccionObj) {
    setSelecciones(prev => [...prev, seccionObj]);
  }
  function eliminarSeccion(codigo_seccion) {
    setSelecciones(prev => prev.filter(s => s.codigo_seccion !== codigo_seccion));
  }
  function limpiarTodo() {
    setSelecciones([]);
  }

  return (
    <MatriculaContext.Provider value={{ selecciones, agregarSeccion, eliminarSeccion, limpiarTodo }}>
      {children}
    </MatriculaContext.Provider>
  );
}