#URLs – indican el camino para acceder a las vistas
#Las URLs son las rutas que el cliente o navegador usa para llamar a las vistas.

from django.urls import path
from .views import (
    LoginView, CursosDisponiblesView, SeccionesPorCursoView, EnrollView, AlumnosInscripcionesView
)

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='login'),
    path('alumnos/<int:codigo_alumno>/cursos/', CursosDisponiblesView.as_view(), name='cursos-por-alumno'),
    path('cursos/<int:codigo_curso>/secciones/', SeccionesPorCursoView.as_view(), name='secciones-por-curso'),
    path('matricular/', EnrollView.as_view(), name='matricular'),
    path('alumnos/<int:codigo_alumno>/inscripciones/', AlumnosInscripcionesView.as_view(), name='inscripciones-alumno'),
]