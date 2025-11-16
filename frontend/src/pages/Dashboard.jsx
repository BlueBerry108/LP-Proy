import { Link } from "react-router-dom";

export default function Dashboard() {
    return (
    <div className="min-h-screen bg-gradient-to-b from-blue-100 to-blue-200 flex items-center justify-center p-6">
      <div className="bg-white shadow-xl rounded-2xl p-10 w-full max-w-xl text-center border border-blue-300">
        
        <h1 className="text-3xl font-bold text-blue-700 mb-4">
          Bienvenido al proceso de matrícula
        </h1>

        <p className="text-gray-600 mb-8">
          Selecciona los cursos disponibles y completa tu proceso de matrícula.
        </p>

        <Link
          to="/cursos"
          className="inline-block bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-xl shadow-md transition transform hover:scale-[1.03]"
        >
          Ir a cursos disponibles
        </Link>
      </div>
    </div>
  );

}