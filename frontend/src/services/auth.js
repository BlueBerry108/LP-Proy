import api from "../api/axios";

export async function loginAlumno(codigo, password) {
    const response = await api.post("/alumno/login/", {
        codigo_alumno: codigo,
        contra_alumno: password
    });
    return response.data;
}