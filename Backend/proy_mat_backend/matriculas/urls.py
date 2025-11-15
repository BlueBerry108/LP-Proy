#URLs – indican el camino para acceder a las vistas
#Las URLs son las rutas que el cliente o navegador usa para llamar a las vistas.

from django.urls import path
from .views import (
    AlumnoListCreateView, AlumnoRetrieveUpdateDeleteView,
    CursosListCreateView, CursosRetrieveUpdateDeleteView,
    DocenteListCreateView, DocenteRetrieveUpdateDeleteView,
    SeccionListCreateView, SeccionRetrieveUpdateDeleteView,
    DetalleMatriculaListCreateView, DetalleMatriculaRetrieveUpdateDeleteView,
    MatriculaListCreateView, MatriculaRetrieveUpdateDeleteView
)

urlpatterns = [
     # ALUMNOS
    path('alumnos/', AlumnoListCreateView.as_view(), name='alumno-list'),
    path('alumnos/<int:codigo_alumno>/', AlumnoRetrieveUpdateDeleteView.as_view(), name='alumno-detail'),

    # CURSOS
    path('cursos/', CursosListCreateView.as_view(), name='curso-list'),
    path('cursos/<int:codigo_curso>/', CursosRetrieveUpdateDeleteView.as_view(), name='curso-detail'),

    # DOCENTE
    path('docentes/', DocenteListCreateView.as_view(), name='docente-list'),
    path('docentes/<int:codigo_docente>/', DocenteRetrieveUpdateDeleteView.as_view(), name='docente-detail'),

    # SECCION
    path('secciones/', SeccionListCreateView.as_view(), name='seccion-list'),
    path('secciones/<int:codigo_seccion>/', SeccionRetrieveUpdateDeleteView.as_view(), name='seccion-detail'),

    # DETALLE MATRICULA
    path('detalle-matricula/', DetalleMatriculaListCreateView.as_view(), name='detalle-list'),
    path('detalle-matricula/<int:cod_det_matricula>/', DetalleMatriculaRetrieveUpdateDeleteView.as_view(), name='detalle-detail'),

    # MATRÍCULA
    path('matriculas/', MatriculaListCreateView.as_view(), name='matricula-list'),
    path('matriculas/<int:codigo_matricula>/', MatriculaRetrieveUpdateDeleteView.as_view(), name='matricula-detail'),
]