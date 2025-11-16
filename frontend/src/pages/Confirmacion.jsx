import React from "react";

export default function Confirmacion() {
  function finalizar() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("alumno");
    window.location.href = "/";
  }
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-blue-100 to-blue-200 p-6">
      <div className="bg-white border border-blue-300 shadow-xl rounded-2xl p-10 text-center w-full max-w-lg">
        
        <h2 className="text-3xl font-bold text-blue-700 mb-4">
          Matrícula confirmada 🎉
        </h2>

        <p className="text-gray-600 mb-8">
          Tu matrícula fue registrada exitosamente.  
          Gracias por completar el proceso.
        </p>

        <button
          onClick={finalizar}
          className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-xl shadow-md transition transform hover:scale-[1.03]"
        >
          Volver al login
        </button>
      </div>
    </div>
  );
}