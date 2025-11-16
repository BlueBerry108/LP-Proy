import React, { useState } from "react";
import API from "../api/axios";

export default function Login() {
  const [codigo, setCodigo] = useState("");
  const [pass, setPass] = useState("");
  const [err, setErr] = useState("");

  async function submit(e) {
    e.preventDefault();
    setErr("");
    try {
      const r = await API.post("/auth/login/", { codigo_alumno: Number(codigo), contra_alumno: pass });
      const { tokens, alumno } = r.data;
      localStorage.setItem("access_token", tokens.access);
      localStorage.setItem("refresh_token", tokens.refresh);
      localStorage.setItem("alumno", JSON.stringify(alumno));
      window.location.href = "/dashboard";
    } catch (error) {
      setErr(error.response?.data?.detail || "Error login");
    }
  }

  return (
   <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-sky-100 to-blue-200 p-6">
      <div className="w-full max-w-md bg-white shadow-xl rounded-2xl p-8">

        {/* Título */}
        <h2 className="text-3xl font-bold text-center text-blue-800 mb-6">
          Ingreso de Alumno
        </h2>

        {/* Formulario */}
        <form onSubmit={submit} className="space-y-5">

          <div>
            <label className="block mb-1 text-blue-700 font-semibold">
              Código de Alumno
            </label>
            <input
              value={codigo}
              onChange={(e) => setCodigo(e.target.value)}
              placeholder="Ej: 20231045"
              className="w-full px-4 py-2 border border-blue-300 rounded-lg focus:ring-2 focus:ring-blue-400 outline-none"
            />
          </div>

          <div>
            <label className="block mb-1 text-blue-700 font-semibold">
              Contraseña
            </label>
            <input
              type="password"
              value={pass}
              onChange={(e) => setPass(e.target.value)}
              placeholder="Ingresar contraseña"
              className="w-full px-4 py-2 border border-blue-300 rounded-lg focus:ring-2 focus:ring-blue-400 outline-none"
            />
          </div>

          {/* Botón */}
          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 rounded-lg transition"
          >
            Entrar
          </button>
        </form>

        {/* Error */}
        {err && (
          <div className="mt-4 text-center text-red-600 font-semibold">
            {err}
          </div>
        )}
      </div>
    </div>
  );
}