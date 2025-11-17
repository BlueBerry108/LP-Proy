#Views – lógica de cómo responder a las peticiones
#Las views determinan qué hacer cuando alguien llama a tu API.
#En Django REST Framework puedes usar vistas genéricas como:
#   - ListCreateAPIView → listar y crear
#   - RetrieveUpdateDestroyAPIView → ver, actualizar y eliminar

import base64
import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics, authentication 
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken
import bcrypt

from .models import Alumno, Cursos, Seccion, Matricula, DetalleMatricula
from .serializers import (
    LoginSerializer, SimpleAlumnoSerializer,
    CursoSerializer, SectionSerializer, EnrollRequestSerializer
)
from .utils_enroll import (
    parse_horario, schedules_conflict,
    create_matricula_and_get_id, create_detalle_and_get_id
)

logger = logging.getLogger(__name__)

# --- Fake user para JWT ---
class FakeUser:
    """Objeto temporal para generar tokens JWT usando SimpleJWT."""
    def __init__(self, user_id):
        self.id = user_id
        self.is_active = True   # SimpleJWT requiere esto

# Helper to create jwt tokens
def get_tokens_for_user(alumno):
    """
    SimpleJWT exige un objeto tipo User. Como Alumno no hereda de User,
    usamos un FakeUser para poder generar tokens válidos.
    """
    fake = FakeUser(alumno.codigo_alumno)
    
    refresh = RefreshToken.for_user(fake)

    # Guardamos el código del alumno en el token
    refresh["codigo_alumno"] = alumno.codigo_alumno

    access = refresh.access_token
    access["codigo_alumno"] = alumno.codigo_alumno

    return {
        "refresh": str(refresh),
        "access": str(access),
    }

# --- LOGIN ---
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        codigo = serializer.validated_data['codigo_alumno']
        contra = serializer.validated_data['contra_alumno']

        # Buscar alumno
        try:
            alumno = Alumno.objects.get(codigo_alumno=codigo)
        except Alumno.DoesNotExist:
            return Response({"detail": "Alumno no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        stored = alumno.contra_alumno or ""

        # --- Contraseña en bcrypt ---
        if stored.startswith("bcrypt$"):
            hashed = stored.replace("bcrypt$", "").encode()

            if not bcrypt.checkpw(contra.encode(), hashed):
                return Response({"detail": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)

        # --- Contraseña antigua en texto plano ---
        else:
            if stored != contra:
                return Response({"detail": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)

            # Actualizar a bcrypt
            hashed = bcrypt.hashpw(contra.encode(), bcrypt.gensalt())
            alumno.contra_alumno = "bcrypt$" + hashed.decode()
            alumno.save()

        # Generar tokens JWT válidos
        tokens = get_tokens_for_user(alumno)

        # Serializar datos del alumno
        data = SimpleAlumnoSerializer(alumno).data

        return Response({"tokens": tokens, "alumno": data}, status=status.HTTP_200_OK)


# --- Cursos disponibles por ciclo del alumno ---
class CursosDisponiblesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, codigo_alumno):
        alumno = get_object_or_404(Alumno, codigo_alumno=codigo_alumno)
        cursos = Cursos.objects.filter(nro_ciclo=alumno.ciclo_alumno)
        return Response(CursoSerializer(cursos, many=True).data)


# --- Secciones por curso ---
class SeccionesPorCursoView(generics.ListAPIView):
    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Seccion.objects.filter(codigo_curso=self.kwargs.get("codigo_curso"))

# --- Lista Secciones Inscritas ---
class AlumnosInscripcionesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, codigo_alumno):
        detalles = DetalleMatricula.objects.raw(
            """
            SELECT d.*
            FROM Detalle_matricula d
            JOIN Matricula m ON d.Codigo_matricula = m.Codigo_matricula
            WHERE m.Codigo_alumno = %s
            """,
            [codigo_alumno],
        )
        secciones = []
        for d in detalles:
            sec = getattr(d, "codigo_seccion", None)
            if hasattr(sec, "codigo_seccion"):  # FK objeto
                secciones.append(sec.codigo_seccion)
            else:
                try:
                    secciones.append(int(sec))
                except Exception:
                    # ignorar si no convertible
                    pass

        return Response({"secciones": secciones})

# --- Inscripción / Matriculación ---
class EnrollView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        ser = EnrollRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        codigo_alumno = ser.validated_data["codigo_alumno"]
        secciones_ids = ser.validated_data["secciones"]

        alumno = get_object_or_404(Alumno, codigo_alumno=codigo_alumno)

        secciones_obj = list(Seccion.objects.filter(codigo_seccion__in=secciones_ids))
        if len(secciones_obj) != len(secciones_ids):
            return Response({"detail": "Alguna sección no existe"}, status=400)

        # Verificar duplicados de cursos
        nombres = [((s.codigo_curso.nombre_curso or "").strip() if s.codigo_curso else "") for s in secciones_obj]
        if len(nombres) != len(set(nombres)):
            return Response({"detail": "Hay cursos repetidos."}, status=400)

        # Conflictos entre nuevos
        for i in range(len(secciones_obj)):
            for j in range(i + 1, len(secciones_obj)):
                h1 = parse_horario(secciones_obj[i].horario_seccion or "")
                h2 = parse_horario(secciones_obj[j].horario_seccion or "")
                if h1 and h2 and schedules_conflict(h1, h2):
                    return Response({"detail": "Conflicto de horario entre las secciones seleccionadas."}, status=400)

        # Buscar inscripciones previas
        detalles_previos = DetalleMatricula.objects.raw(
            """
            SELECT d.*
            FROM Detalle_matricula d
            JOIN Matricula m ON d.Codigo_matricula = m.Codigo_matricula
            WHERE m.Codigo_alumno = %s
            """,
            [codigo_alumno],
        )

        inscritos = []
        for d in detalles_previos:
            sec = getattr(d, "codigo_seccion", None)
            if hasattr(sec, "horario_seccion"):
                inscritos.append(sec)
            else:
                try:
                    inscritos.append(Seccion.objects.get(codigo_seccion=sec))
                except Exception:
                    pass

        horarios_previos = []
        for sec in inscritos:
            horarios_previos += parse_horario(sec.horario_seccion or "")

        # Conflicto con previos
        for s in secciones_obj:
            h = parse_horario(s.horario_seccion or "")
            if h and horarios_previos and schedules_conflict(h, horarios_previos):
                return Response({"detail": f"Conflicto con sección ya inscrita: {s.codigo_seccion}"}, status=400)

        # Aforo
        for s in secciones_obj:
            count = DetalleMatricula.objects.filter(codigo_seccion=s).count()
            if count >= (s.cant_max_alumnos or 0):
                return Response({"detail": f"La sección {s.codigo_seccion} está llena."}, status=400)

        # Crear matrícula
        try:
            matricula_id = create_matricula_and_get_id(
                alumno.codigo_alumno, pago_total=0, pago_mensual=0, creditos_finales=0
            )

            detalles_creados = []
            for s in secciones_obj:
                det_id = create_detalle_and_get_id(
                    matricula_id,
                    s.codigo_curso.codigo_curso if s.codigo_curso else None,
                    s.codigo_seccion,
                )
                detalles_creados.append(
                    {
                        "cod_det_matricula": det_id,
                        "codigo_curso": s.codigo_curso.codigo_curso if s.codigo_curso else None,
                        "codigo_seccion": s.codigo_seccion,
                    }
                )

            return Response({"matricula_id": matricula_id, "detalles": detalles_creados}, status=201)

        except Exception as e:
            logger.exception("Error creando matrícula")
            return Response({"detail": f"Error creando matrícula: {str(e)}"}, status=500)