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


class CursosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cursos
        fields = '__all__'


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