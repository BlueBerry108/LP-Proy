# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Alumno(models.Model):
    codigo_alumno = models.IntegerField(db_column='Codigo_alumno', primary_key=True)  # Field name made lowercase.
    nombre_alumno = models.CharField(db_column='Nombre_alumno', max_length=100, blank=True, null=True)  # Field name made lowercase.
    apellido_alumno = models.CharField(db_column='Apellido_alumno', max_length=100, blank=True, null=True)  # Field name made lowercase.
    contra_alumno = models.CharField(db_column='Contra_alumno', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ciclo_alumno = models.IntegerField(db_column='Ciclo_alumno', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Alumno'


class Cursos(models.Model):
    codigo_curso = models.IntegerField(db_column='Codigo_curso', primary_key=True)  # Field name made lowercase.
    nombre_curso = models.CharField(db_column='Nombre_curso', max_length=255, blank=True, null=True)  # Field name made lowercase.
    desc_curso = models.CharField(db_column='Desc_curso', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cant_max_alumnos = models.IntegerField(db_column='Cant_max_alumnos', blank=True, null=True)  # Field name made lowercase.
    nro_ciclo = models.IntegerField(db_column='Nro_ciclo', blank=True, null=True)  # Field name made lowercase.
    hrs_semanales_curso = models.IntegerField(db_column='Hrs_semanales_curso', blank=True, null=True)  # Field name made lowercase.
    creditos_curso = models.IntegerField(db_column='Creditos_curso', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Cursos'

class Docente(models.Model):
    codigo_docente = models.IntegerField(db_column='Codigo_docente', primary_key=True)  # Field name made lowercase.
    nombre_docente = models.CharField(db_column='Nombre_docente', max_length=100, blank=True, null=True)  # Field name made lowercase.
    apellido_docente = models.CharField(db_column='Apellido_docente', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Docente'

class Seccion(models.Model):
    codigo_seccion = models.IntegerField(db_column='Codigo_seccion', primary_key=True)  # Field name made lowercase.
    horario_seccion = models.CharField(db_column='Horario_seccion', max_length=255, blank=True, null=True)  # Field name made lowercase.
    codigo_docente = models.ForeignKey(Docente, models.DO_NOTHING, db_column='Codigo_docente', blank=True, null=True)  # Field name made lowercase.
    cant_max_alumnos = models.IntegerField(db_column='Cant_max_alumnos', blank=True, null=True)  # Field name made lowercase.
    codigo_curso = models.ForeignKey(Cursos, models.DO_NOTHING, db_column='Codigo_curso', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seccion'

class Matricula(models.Model):
    codigo_matricula = models.IntegerField(db_column='Codigo_matricula', primary_key=True)  # Field name made lowercase.
    fecha_matricula = models.DateField(db_column='Fecha_matricula', blank=True, null=True)  # Field name made lowercase.
    codigo_alumno = models.ForeignKey(Alumno, models.DO_NOTHING, db_column='Codigo_alumno', blank=True, null=True)  # Field name made lowercase.
    pago_total = models.DecimalField(db_column='Pago_total', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    pago_mensual = models.DecimalField(db_column='Pago_mensual', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    creditos_finales = models.IntegerField(db_column='Creditos_finales', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Matricula'
        

class DetalleMatricula(models.Model):
    cod_det_matricula = models.IntegerField(db_column='Cod_det_matricula', primary_key=True)  # Field name made lowercase.
    codigo_curso = models.ForeignKey(Cursos, models.DO_NOTHING, db_column='Codigo_curso', blank=True, null=True)  # Field name made lowercase.
    codigo_seccion = models.ForeignKey('Seccion', models.DO_NOTHING, db_column='Codigo_seccion', blank=True, null=True)  # Field name made lowercase.
    codigo_matricula = models.ForeignKey(Matricula, models.DO_NOTHING, db_column='Codigo_matricula', blank=True,null=True)
    
    class Meta:
        managed = False
        db_table = 'Detalle_matricula'







class Sysdiagrams(models.Model):
    name = models.CharField(max_length=128)
    principal_id = models.IntegerField()
    diagram_id = models.AutoField(primary_key=True)
    version = models.IntegerField(blank=True, null=True)
    definition = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sysdiagrams'
        unique_together = (('principal_id', 'name'),)