import { BrowserRouter, Routes, Route } from "react-router-dom";
import { MatriculaProvider } from "./context/MatriculaContext";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import CursosDisponibles from "./pages/CursosDisponibles";
import VistaPrevia from "./pages/VistaPrevia";
import Confirmacion from "./pages/Confirmacion";

export default function App() {
    return (
        <BrowserRouter>
                <Routes>
                    <Route path="/" element={<Login />} />
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="/cursos" element={<CursosDisponibles />} />
                    <Route path="/vista-previa" element={<VistaPrevia />} />
                    <Route path="/confirmacion" element={<Confirmacion />} />
                </Routes>
        </BrowserRouter>
    );
}