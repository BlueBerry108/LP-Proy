LP-Proy
# Requerimientos:
- python 3.17 o superior 
- ODBC Driver 18 for SQL Server
- Tailwindcss.exe
# Pasos iniciales a seguir:
- activar el entorno virtual por la terminal (entrar a la primera carpeta --> cd Backend): .venv\Scripts\Activate
- Si aparece el error de ejecución de scripts: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
- Desactivar entorno virtual: deactivate

# Instalando dependencias
- Con el entorno activo, ejecutar --> pip install -r requirements.txt 
- En caso de no reconocer pip, probar: py -m pip install -r requirements.txt

# Variables de entorno (.env)
Crea un archivo .env al mismo nivel que la varpeta venv
Tendras que agregar los campos(Preguntar por md las credenciales):
- DJANGO_SECRET_KEY=
- DEBUG=True
- DB_NAME=
- DB_USER=
- DB_PASS=
- DB_HOST=
- DB_PORT=
# Usando el test_conn.py
Si haz seguido todos los pasos correctamente hasta ahora, deberías poder correr este archivo sin problema.

# Ejecutando el servidor Django
- Entrar a la carpeta del proyecto -> cd matriculas
- incia el servidor con -> python manage.py runserver
- El servidor se abrirá en: http://127.0.0.1:8000/

# Probar los endpoints (API REST)
Puedes usar:
- Postman
- Thunder Client
- Recomiendo -> https://app.apidog.com
En caso de usar Apidog --> crear cuenta y crear nuevo proyecto, en el modulo de endpoints crear uno nuevo y probar:
http://127.0.0.1:8000/api/docentes/
Respuesta esperada:
lista de datos correspondientes de la tabla docentes
# Notas adicionales
- Si cambias el .env, reinicia el servidor para aplicar cambios.
- Si ejecutas el proyecto con DEBUG=False, recuerda configurar ALLOWED_HOSTS correctamente.
- Para cualquier error con SQL Server, revisa:
    - Driver ODBC instalado
    - Firewall de Azure
    - Credenciales .env
