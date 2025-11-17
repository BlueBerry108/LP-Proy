#Serializers – convierten datos (Modelo ↔ JSON)
# se encarga de:
#   - Convertir objetos del modelo → JSON: Para enviar datos por API.
#   - Convertir JSON → objetos del modelo
#       Para crear o actualizar registros cuando llega un POST o PUT.
#   - Validar datos: Asegura que los datos entrantes sean correctos.

from rest_framework import serializers
from .models import Alumno, Cursos, Docente, Seccion, DetalleMatricula, Matricula

class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = '__all__'

class SimpleAlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = ['codigo_alumno', 'nombre_alumno', 'apellido_alumno', 'ciclo_alumno']

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cursos
        fields = ['codigo_curso', 'nombre_curso', 'desc_curso', 'cant_max_alumnos', 'nro_ciclo', 'hrs_semanales_curso', 'creditos_curso']

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seccion
        fields = ['codigo_seccion', 'horario_seccion', 'codigo_docente', 'cant_max_alumnos', 'codigo_curso']

class EnrollRequestSerializer(serializers.Serializer):
    codigo_alumno = serializers.IntegerField()
    secciones = serializers.ListField(child=serializers.IntegerField(), min_length=1)

class LoginSerializer(serializers.Serializer):
    codigo_alumno = serializers.IntegerField()
    contra_alumno = serializers.CharField(write_only=True)

class DocenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Docente
        fields = '__all__'


class SeccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seccion
        fields = '__all__'


class DetalleMatriculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleMatricula
        fields = '__all__'


class MatriculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matricula
        fields = '__all__'
        
