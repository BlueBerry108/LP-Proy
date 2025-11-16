import os
import sys
import django
from django.contrib.auth.hashers import make_password
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "proy_mat_backend.proy_mat_backend.settings"
)

django.setup()

from proy_mat_backend.matriculas.models import Alumno


def migrate_passwords():
    alumnos = Alumno.objects.all()

    for alumno in alumnos:
        if alumno.contra_alumno:
            alumno.contra_alumno = make_password(alumno.contra_alumno)
            alumno.save()
            print(f"Contraseña migrada para alumno: {alumno.codigo_alumno}")

    print("Migración completada.")


if __name__ == "__main__":
    migrate_passwords()