import re
from datetime import time
from django.db import connection

# Mapea nombres de día en español -> normalizados
DAY_NAMES = {
    'lu': 'LUN', 'lun': 'LUN', 'lunes': 'LUN',
    'ma': 'MAR', 'mar': 'MAR', 'martes': 'MAR',
    'mi': 'MIE', 'mie': 'MIE', 'miercoles': 'MIE', 'miércoles': 'MIE',
    'ju': 'JUE', 'jue': 'JUE', 'jueves': 'JUE',
    'vi': 'VIE', 'vie': 'VIE', 'viernes': 'VIE',
    'sa': 'SAB', 'sab': 'SAB', 'sabado': 'SAB', 'sábado': 'SAB',
    'do': 'DOM', 'dom': 'DOM', 'domingo': 'DOM'
}

time_re = re.compile(r'(\d{1,2}):?(\d{2})')

def parse_time(tstr):
    # acepta "08:00" o "800" o "8:00"
    m = time_re.search(tstr)
    if not m:
        return None
    hour = int(m.group(1))
    minute = int(m.group(2))
    return time(hour, minute)

def parse_horario(horario_str):
    """
    Intenta parsear horario_str y devuelve lista de (dia_norm, start_time, end_time).
    Soporta formatos como:
      "Lunes 08:00-10:00"
      "Lun 08:00-10:00; Mie 09:00-11:00"
    Si no puede parsear, devuelve [] (no se puede comprobar cruce).
    """
    if not horario_str:
        return []
    entries = re.split(r'[;,/]\s*', horario_str)  # separadores ; , /
    result = []
    for e in entries:
        e = e.strip()
        if not e:
            continue
        # buscar día y horas
        parts = e.split()
        if len(parts) < 2:
            # intentar detectar "Lun08:00-10:00"
            m = re.match(r'([A-Za-z]+)\s*(\d{1,2}:\d{2}-\d{1,2}:\d{2})', e)
            if m:
                day = m.group(1)
                times = m.group(2)
            else:
                # no se puede parsear
                continue
        else:
            day = parts[0]
            times = ' '.join(parts[1:])
        # normalizar día
        day_key = day.lower()
        day_norm = DAY_NAMES.get(day_key[:3]) or DAY_NAMES.get(day_key)
        if not day_norm:
            # intentar primeros 3 letras
            day_norm = DAY_NAMES.get(day_key[:3])
        if not day_norm:
            continue
        # buscar rango horas
        m2 = re.search(r'(\d{1,2}:?\d{2})\s*-\s*(\d{1,2}:?\d{2})', times)
        if not m2:
            # intentar con sin dos puntos
            m2 = re.search(r'(\d{3,4})\s*-\s*(\d{3,4})', times)
        if not m2:
            continue
        start = parse_time(m2.group(1))
        end = parse_time(m2.group(2))
        if start and end:
            result.append((day_norm, start, end))
    return result

def intervals_overlap(a_start, a_end, b_start, b_end):
    return (a_start < b_end) and (b_start < a_end)

def schedules_conflict(h1, h2):
    """
    h1, h2: lists de (dia, start, end)
    """
    for d1, s1, e1 in h1:
        for d2, s2, e2 in h2:
            if d1 == d2 and intervals_overlap(s1, e1, s2, e2):
                return True
    return False

# DB insertion helpers (usa SQL con OUTPUT INSERTED)
def create_matricula_and_get_id(codigo_alumno, pago_total=None, pago_mensual=None, creditos_finales=None):
    """
    Inserta una fila en Matricula y devuelve el id generado.
    Ajusta nombres de columnas según tu esquema real.
    """
    with connection.cursor() as cursor:
        sql = """
        INSERT INTO Matricula (Fecha_matricula, Codigo_alumno, Pago_total, Pago_mensual, Creditos_finales)
        OUTPUT INSERTED.Codigo_matricula
        VALUES (GETDATE(), %s, %s, %s, %s)
        """
        cursor.execute(sql, [codigo_alumno, pago_total, pago_mensual, creditos_finales])
        row = cursor.fetchone()
        if row:
            return row[0]
    return None

def create_detalle_and_get_id(codigo_matricula, codigo_curso, codigo_seccion):
    with connection.cursor() as cursor:
        sql = """
        INSERT INTO Detalle_matricula (Codigo_matricula, Codigo_curso, Codigo_seccion)
        OUTPUT INSERTED.Cod_det_matricula
        VALUES (%s, %s, %s)
        """
        cursor.execute(sql, [codigo_matricula, codigo_curso, codigo_seccion])
        row = cursor.fetchone()
        if row:
            return row[0]
    return None