#Views – lógica de cómo responder a las peticiones
#Las views determinan qué hacer cuando alguien llama a tu API.
#En Django REST Framework puedes usar vistas genéricas como:
#   - ListCreateAPIView → listar y crear
#   - RetrieveUpdateDestroyAPIView → ver, actualizar y eliminar

from rest_framework import generics
from .models import Alumno, Cursos, Docente, Seccion, DetalleMatricula, Matricula
from .serializers import (
    AlumnoSerializer, CursosSerializer, DocenteSerializer,
    SeccionSerializer, DetalleMatriculaSerializer, MatriculaSerializer
)

# ---- ALUMNO ----
class AlumnoListCreateView(generics.ListCreateAPIView):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer

class AlumnoRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer
    lookup_field = 'codigo_alumno'


# ---- CURSOS ----
class CursosListCreateView(generics.ListCreateAPIView):
    queryset = Cursos.objects.all()
    serializer_class = CursosSerializer

class CursosRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cursos.objects.all()
    serializer_class = CursosSerializer
    lookup_field = 'codigo_curso'


# ---- DOCENTE ----
class DocenteListCreateView(generics.ListCreateAPIView):
    queryset = Docente.objects.all()
    serializer_class = DocenteSerializer

class DocenteRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Docente.objects.all()
    serializer_class = DocenteSerializer
    lookup_field = 'codigo_docente'


# ---- SECCIÓN ----
class SeccionListCreateView(generics.ListCreateAPIView):
    queryset = Seccion.objects.all()
    serializer_class = SeccionSerializer

class SeccionRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Seccion.objects.all()
    serializer_class = SeccionSerializer
    lookup_field = 'codigo_seccion'


# ---- DETALLE MATRÍCULA ----
class DetalleMatriculaListCreateView(generics.ListCreateAPIView):
    queryset = DetalleMatricula.objects.all()
    serializer_class = DetalleMatriculaSerializer

class DetalleMatriculaRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DetalleMatricula.objects.all()
    serializer_class = DetalleMatriculaSerializer
    lookup_field = 'cod_det_matricula'


# ---- MATRÍCULA ----
class MatriculaListCreateView(generics.ListCreateAPIView):
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer

class MatriculaRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer
    lookup_field = 'codigo_matricula'