#Views – lógica de cómo responder a las peticiones
#Las views determinan qué hacer cuando alguien llama a tu API.
#En Django REST Framework puedes usar vistas genéricas como:
#   - ListCreateAPIView → listar y crear
#   - RetrieveUpdateDestroyAPIView → ver, actualizar y eliminar

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from django.shortcuts import get_object_or_404
from django.db import transaction
from datetime import datetime
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

# Helper to create jwt tokens
def get_tokens_for_user(codigo_alumno):
    refresh = RefreshToken()  # crea un token vacío SIN usuario
    refresh["codigo_alumno"] = codigo_alumno

    access = refresh.access_token
    access["codigo_alumno"] = codigo_alumno

    return {
        "refresh": str(refresh),
        "access": str(access),
    }

# --- LOGIN ---
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        codigo = serializer.validated_data['codigo_alumno']
        contra = serializer.validated_data['contra_alumno']

        try:
            alumno = Alumno.objects.get(codigo_alumno=codigo)
        except Alumno.DoesNotExist:
            return Response({"detail": "Alumno no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        stored = alumno.contra_alumno or ''
        # Si stored empieza con 'bcrypt$' -> hashed; Sino compara el plaintext y rehash
        if stored.startswith("bcrypt$"):
            hashed = stored.split("bcrypt$")[1].encode()
            if not bcrypt.checkpw(contra.encode(), hashed):
                return Response({"detail": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # plaintext comparison (legacy)
            if stored != contra:
                return Response({"detail": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)
            # re-hash and update DB (improve security)
            hashed = bcrypt.hashpw(contra.encode(), bcrypt.gensalt())
            alumno.contra_alumno = "bcrypt$" + hashed.decode()
            alumno.save()
            
        # Generar token firmado
        tokens = get_tokens_for_user(codigo)
        data = SimpleAlumnoSerializer(alumno).data
        return Response({"tokens": tokens, "alumno": data}, status=status.HTTP_200_OK)


# --- Cursos disponibles por ciclo del alumno ---
class CursosDisponiblesView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, codigo_alumno):
        alumno = get_object_or_404(Alumno, codigo_alumno=codigo_alumno)
        ciclo = alumno.ciclo_alumno
        cursos = Cursos.objects.filter(nro_ciclo=ciclo)
        ser = CursoSerializer(cursos, many=True)
        return Response(ser.data)


# --- Secciones por curso ---
class SeccionesPorCursoView(generics.ListAPIView):
    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        codigo_curso = self.kwargs.get('codigo_curso')
        return Seccion.objects.filter(codigo_curso=codigo_curso)

class AlumnosInscripcionesView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, codigo_alumno):
        detalles = DetalleMatricula.objects.raw(
            "SELECT d.* FROM Detalle_matricula d JOIN Matricula m ON d.Codigo_matricula = m.Codigo_matricula WHERE m.Codigo_alumno = %s",
            [codigo_alumno]
        )
        secciones = []
        for d in detalles:
            sec = getattr(d, 'codigo_seccion', None)
            if sec:
                # si es objeto FK
                if hasattr(sec, 'codigo_seccion'):
                    secciones.append(sec.codigo_seccion)
                else:
                    try:
                        secciones.append(int(sec))
                    except:
                        pass
        return Response({"secciones": secciones})

# --- Inscripción / Matriculación ---
class EnrollView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        ser = EnrollRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        codigo_alumno = ser.validated_data['codigo_alumno']
        secciones_ids = ser.validated_data['secciones']

        alumno = get_object_or_404(Alumno, codigo_alumno=codigo_alumno)

        # fetch sections requested
        secciones_obj = list(Seccion.objects.filter(codigo_seccion__in=secciones_ids))
        if len(secciones_obj) != len(secciones_ids):
            return Response({"detail": "Alguna sección no existe"}, status=status.HTTP_400_BAD_REQUEST)

        # validate no duplicate course names and build info
        seccion_info = []
        for s in secciones_obj:
            curso = s.codigo_curso
            nombre = (curso.nombre_curso or '').strip() if curso else ''
            seccion_info.append({'seccion': s, 'curso': curso, 'nombre': nombre})
        nombres = [si['nombre'] for si in seccion_info]
        if len(nombres) != len(set(nombres)):
            return Response({"detail": "Hay cursos repetidos (mismo nombre)."}, status=status.HTTP_400_BAD_REQUEST)

        # validate no conflicts between new sections themselves
        for i in range(len(secciones_obj)):
            for j in range(i + 1, len(secciones_obj)):
                h1 = parse_horario(secciones_obj[i].horario_seccion or "")
                h2 = parse_horario(secciones_obj[j].horario_seccion or "")
                if h1 and h2 and schedules_conflict(h1, h2):
                    return Response({"detail": "Conflicto de horario entre las secciones seleccionadas."}, status=status.HTTP_400_BAD_REQUEST)

        # get existing enrolled sections for this alumno
        detalles_alumno = DetalleMatricula.objects.raw(
            """
            SELECT d.*
            FROM Detalle_matricula d
            JOIN Matricula m ON d.Codigo_matricula = m.Codigo_matricula
            WHERE m.Codigo_alumno = %s
            """,
            [alumno.codigo_alumno]
        )
        inscritos = []
        for d in detalles_alumno:
            # d.codigo_seccion may be FK actual object or int depending on inspectdb mapping; handle both:
            sec = getattr(d, 'codigo_seccion', None)
            if sec:
                # if sec is id, try to fetch
                if hasattr(sec, 'horario_seccion'):
                    inscritos.append(sec)
                else:
                    try:
                        inscritos.append(Seccion.objects.get(codigo_seccion=sec))
                    except Seccion.DoesNotExist:
                        pass

        inscritos_horarios = []
        for sec in inscritos:
            inscritos_horarios += parse_horario(sec.horario_seccion or "")

        # check conflicts new vs existing
        for s in secciones_obj:
            h_solic = parse_horario(s.horario_seccion or "")
            if h_solic and inscritos_horarios and schedules_conflict(h_solic, inscritos_horarios):
                return Response({"detail": f"Conflicto de horario con secciones ya inscritas al intentar inscribir sección {s.codigo_seccion}"}, status=status.HTTP_400_BAD_REQUEST)

        # check capacity
        for s in secciones_obj:
            if s.cant_max_alumnos:
                count = DetalleMatricula.objects.filter(codigo_seccion=s).count()
                if count >= (s.cant_max_alumnos or 0):
                    return Response({"detail": f"La sección {s.codigo_seccion} ya está completa."}, status=status.HTTP_400_BAD_REQUEST)

        # OK — create Matricula and details (SQL insertion helpers)
        try:
            with transaction.atomic():
                nueva_matricula_id = create_matricula_and_get_id(alumno.codigo_alumno, pago_total=0, pago_mensual=0, creditos_finales=0)
                detalles_creados = []
                for s in secciones_obj:
                    det_id = create_detalle_and_get_id(nueva_matricula_id, s.codigo_curso.codigo_curso if s.codigo_curso else None, s.codigo_seccion)
                    detalles_creados.append({
                        "cod_det_matricula": det_id,
                        "codigo_curso": s.codigo_curso.codigo_curso if s.codigo_curso else None,
                        "codigo_seccion": s.codigo_seccion
                    })
                return Response({
                    "matricula_id": nueva_matricula_id,
                    "detalles": detalles_creados
                }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": f"Error creando matrícula: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)