# -*- coding: utf-8 -*-
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)

class Profile(models.Model):
    ADMINISTRADOR = 1
    GERENTE = 2
    TESORERO = 3
    REVISORFISCAL = 4
    INSPECTORZONA = 5
    SUPERVISOR = 6
    CONSULTA = 7
    ROLE_CHOICES = (
        (ADMINISTRADOR, 'Administrador'),
        (GERENTE, 'Gerente'),
        (TESORERO, 'Tesorero'),
        (REVISORFISCAL, 'Revisor Fiscal'),
        (INSPECTORZONA, 'Inspector de riego'),
        (SUPERVISOR, 'Supervisor'),
        (CONSULTA, 'Consulta'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    cargo = models.CharField(max_length=30, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)

    def __unicode__(self):  # __unicode__ for Python 2
        return self.user.username

class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DjangoSite(models.Model):
    domain = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'django_site'

class TipoIdentificacion(models.Model):
    nombre = models.CharField(max_length=50)

    def __unicode__(self):  # __unicode__ for Python 2
        return self.nombre

class Tercero(models.Model):
    identificacion = models.CharField(primary_key=True, max_length=25)
    tipo_identificacion = models.ForeignKey(TipoIdentificacion, on_delete=models.DO_NOTHING)
    pirme_nombre = models.CharField(max_length=50)
    segundo_nombre = models.CharField(max_length=50, null=True, blank=True)
    primer_apellido = models.CharField(max_length=50)
    segundo_apellido = models.CharField(max_length=50, null=True, blank=True)
    telefono = models.CharField(max_length=9)
    celular = models.CharField(max_length=12,null=True, blank=True)
    correo = models.CharField(max_length=50, null=True, blank=True)
    direccion = models.CharField(max_length=50,null=True, blank=True)
    razon_social = models.CharField(max_length=50,null=True, blank=True)
    identificacion_representante = models.CharField(max_length=25,null=True, blank=True)
    tipo_identificacion_representante = models.ForeignKey(TipoIdentificacion, related_name='TPRazonSocial',null=True, blank=True)
    telefono_razon_social = models.CharField(max_length=9,null=True, blank=True)
    celular_razon_social = models.CharField(max_length=12,null=True, blank=True)
    correo_razon_social = models.CharField(max_length=50, null=True, blank=True)
    direccion_razon_social = models.CharField(max_length=50,null=True, blank=True)
    activo = models.BooleanField ()
    usuario_registro = models.ForeignKey(User, related_name='Tusuarioregistro',null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    usuario_modifica = models.ForeignKey(User, related_name='Tusuariomodifica', null=True, blank=True)
    fecha_modifica = models.DateTimeField(auto_now=True, null=True, blank=True)

    @property
    def json(self):
        if self.activo == True:
            return {
                    'tipo_identificacion' : self.tipo_identificacion.nombre,
                    'identificacion': self.identificacion,
                    'razon_social' : self.razon_social,
                    'pirme_nombre': self.pirme_nombre,
                    'segundo_nombre' : self.segundo_nombre,
                    'primer_apellido' : self.primer_apellido,
                    'segundo_apellido' : self.segundo_apellido,
                    'telefono' : self.telefono,
                    'celular' : self.celular,
                    'correo': self.correo,
                    'activo' : '<p><span class="glyphicon glyphicon glyphicon-ok btn btn-success btn-xs"></span></p>',

                    }
        else:
            return {
                    'tipo_identificacion' : self.tipo_identificacion.nombre,
                    'identificacion': self.identificacion,
                    'razon_social' : self.razon_social,
                    'pirme_nombre': self.pirme_nombre,
                    'segundo_nombre' : self.segundo_nombre,
                    'primer_apellido' : self.primer_apellido,
                    'segundo_apellido' : self.segundo_apellido,
                    'telefono' : self.telefono,
                    'celular' : self.celular,
                    'correo': self.correo,
                    'activo' : '<p><span class="glyphicon glyphicon glyphicon glyphicon-remove btn btn-danger btn-xs"></span></p>',
                    }

class Zonas(models.Model):
    codigo_zona = models.CharField(primary_key=True, max_length=25)
    nombre_zona = models.CharField(max_length=50)
    usuario_registro = models.ForeignKey(User, related_name='Zonausuarioregistro',null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    usuario_modifica = models.ForeignKey(User, related_name='Zonausuariomodifica', null=True, blank=True)
    fecha_modifica = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __unicode__(self):  # __unicode__ for Python 2
        return self.codigo_zona

class Predio(models.Model):
    codigo_predio = models.CharField(primary_key=True, max_length=25)
    cedula_catastral = models.CharField(max_length=50, null=True, blank=True)
    matricula_inmobiliaria = models.CharField(max_length=100, null=True, blank=True)
    area_total = models.DecimalField(max_digits=11, decimal_places=4, validators=[MinValueValidator(1)])
    area_beneficiada = models.DecimalField(max_digits=11, decimal_places=4, validators=[MinValueValidator(1)])
    area_cultivada = models.DecimalField(max_digits=11, decimal_places=4, validators=[MinValueValidator(1)])
    latitud = models.DecimalField(max_digits=10, decimal_places=6)
    logitud = models.DecimalField(max_digits=10, decimal_places=6)
    nombre_predio = models.CharField(max_length=100, null=True, blank=True)
    ubicacion_predio = models.CharField(max_length=100, null=True, blank=True)
    ruta_escritura = models.FileField(upload_to='archivos/', null=True, blank=True)
    ruta_matricula_inmobiliaria = models.FileField(upload_to='archivos/',  null=True, blank=True)
    usuario_registro = models.ForeignKey(User, related_name='usuarioregistro',null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    usuario_modifica = models.ForeignKey(User, related_name='usuariomodifica', null=True, blank=True)
    fecha_modifica = models.DateTimeField(auto_now=True, null=True, blank=True)


class PredioPropietario(models.Model):
    codigo_predio = models.ForeignKey(Predio, on_delete=models.DO_NOTHING)
    identificacion_propietario = models.ForeignKey(Tercero, related_name='propietario', on_delete=models.DO_NOTHING)
    identificacion_usuario = models.ForeignKey(Tercero, related_name='usuario', on_delete=models.DO_NOTHING)
    derecho = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    usuario_registro = models.ForeignKey(User, related_name='Pusuarioregistro',null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    usuario_modifica = models.ForeignKey(User, related_name='Pusuariomodifica', null=True, blank=True)
    fecha_modifica = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        unique_together = (('codigo_predio', 'identificacion_propietario','identificacion_usuario'),)

    @property
    def json(self):
        return {
                'codigo_predio' : self.codigo_predio_id,
                'identificacion_propietario': self.identificacion_propietario_id,
                'primernombreP': self.identificacion_propietario.pirme_nombre,
                'segundonombreP' : self.identificacion_propietario.segundo_nombre,
                'primerapellidoP' : self.identificacion_propietario.primer_apellido,
                'segundoapellidoP' : self.identificacion_propietario.segundo_apellido,
                'identificacion_usuario' : self.identificacion_usuario_id,
                'primernombreU' : self.identificacion_usuario.pirme_nombre,
                'segundonombreU' : self.identificacion_usuario.segundo_nombre,
                'primerapellidoU' : self.identificacion_usuario.primer_apellido, 
                'segundoapellidoU' : self.identificacion_usuario.segundo_apellido,
                'nombre_predio' : self.codigo_predio.nombre_predio,
                }

class TipoCultivo(models.Model):
    nombre_cultivo = models.CharField(max_length=100)

    def __unicode__(self):  # __unicode__ for Python 2
        return self.nombre_cultivo
        
class Cultivo(models.Model):
    id_cultivo =  models.OneToOneField(TipoCultivo, on_delete=models.DO_NOTHING)
    consumo_aguaF1 = models.DecimalField(max_digits=11, decimal_places=4)
    consumo_aguaF2 = models.DecimalField(max_digits=11, decimal_places=4)
    consumo_aguaF3 = models.DecimalField(max_digits=11, decimal_places=4, null=True, blank=True)
    consumo_aguaF4 = models.DecimalField(max_digits=11, decimal_places=4, null=True, blank=True)
    longitud_raizF1 = models.DecimalField(max_digits=5, decimal_places=2)
    longitud_raizF2 = models.DecimalField(max_digits=5, decimal_places=2)
    longitud_raizF3 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    longitud_raizF4 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    duracion = models.DecimalField(max_digits=5, decimal_places=2)
    usuario_registro = models.ForeignKey(User, related_name='Cusuarioregistro',null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    usuario_modifica = models.ForeignKey(User, related_name='Cusuariomodifica', null=True, blank=True)
    fecha_modifica = models.DateTimeField(auto_now=True, null=True, blank=True)


class PredioCultivo(models.Model):
    codigo_predio = models.ForeignKey(Predio, on_delete=models.DO_NOTHING)
    id_cultivo =  models.ForeignKey(TipoCultivo, on_delete=models.DO_NOTHING)
    area_cultivo = models.DecimalField(max_digits=11, decimal_places=4, validators=[MinValueValidator(1)])
    fecha_inicio = models.DateTimeField()
    usuario_registro = models.ForeignKey(User, related_name='CPusuarioregistro',null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    usuario_modifica = models.ForeignKey(User, related_name='CPusuariomodifica', null=True, blank=True)
    fecha_modifica = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        unique_together = (('codigo_predio', 'id_cultivo'),)

    def __unicode__(self):  # __unicode__ for Python 2
        return self.id_cultivo.nombre_cultivo

class Canales(models.Model):
    CANALRIEGO = 1
    CANALDRENAJE = 2
    CANAL_CHOICES = (
        (CANALRIEGO, 'Canal de Riego'),
        (CANALDRENAJE, 'Canal de Drenaje'),
    )
    tipo_canal = models.PositiveSmallIntegerField(choices=CANAL_CHOICES)
    nombre_canal = models.CharField(max_length=100)
    logitud = models.DecimalField(max_digits=3, decimal_places=3)
    capacidad = models.DecimalField(max_digits=6, decimal_places=0)
    revestido  = models.BooleanField ()
    logitudrevestido = models.DecimalField(max_digits=3, decimal_places=3)

    def __unicode__(self):  # __unicode__ for Python 2
        return self.nombre_canal

class MetodoRiego(models.Model):
    nombre_metodoriego = models.CharField(max_length=100)

    def __unicode__(self):  # __unicode__ for Python 2
        return self.nombre_metodoriego

class PredioCanal (models.Model):
    codigo_predio = models.ForeignKey(Predio, on_delete=models.DO_NOTHING)
    id_canal = models.ForeignKey(Canales, on_delete=models.DO_NOTHING)
    abscisa = models.IntegerField()
    usuario_registro = models.ForeignKey(User, related_name='PCusuarioregistro',null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    usuario_modifica = models.ForeignKey(User, related_name='PCusuariomodifica', null=True, blank=True)
    fecha_modifica = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        unique_together = (('codigo_predio', 'id_canal', 'abscisa'),)

    def __unicode__(self):  # __unicode__ for Python 2
        return self.id_canal.nombre_canal

class RegistroRiego (models.Model):
    codigo_predio = models.ForeignKey(Predio, on_delete=models.DO_NOTHING)
    id_canal = models.ForeignKey(PredioCanal, on_delete=models.DO_NOTHING)
    id_metodoRiego = models.ForeignKey(MetodoRiego, on_delete=models.DO_NOTHING)
    id_cultivo =  models.ForeignKey(TipoCultivo, on_delete=models.DO_NOTHING)
    fecha_inicio = models.DateField()
    fecha_final = models.DateField(null=True, blank=True)
    hora_inicio = models.TimeField()
    hore_final = models.TimeField(null=True, blank=True)
    dotacion_inicial =  models.IntegerField(null=True, blank=True, validators=[MaxValueValidator(999)])
    dotacion_final =  models.IntegerField(null=True, blank=True, validators=[MaxValueValidator(999)])
    volumen_agua = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    duracion_riego =  models.DecimalField(null=True, blank=True, max_digits=6, decimal_places=2)
    usuario_registro = models.ForeignKey(User, related_name='Rusuarioregistro',null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    usuario_modifica = models.ForeignKey(User, related_name='RCusuariomodifica', null=True, blank=True)
    fecha_modifica = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        unique_together = (('codigo_predio', 'id_cultivo','fecha_inicio'))

class CoordenadasPredio(models.Model):
    obs = models.CharField(max_length=50)
    id_lote = models.CharField(max_length=50)
    zona = models.CharField(max_length=10)

    met_riego = models.CharField(max_length=30)
    prop = models.CharField(max_length=50)
    fecha_siem = models.CharField(max_length=30)
    code_predi = models.CharField(max_length=254)
    month = models.CharField(max_length=254)
    year = models.IntegerField()
    area_ha = models.FloatField()
    geom = models.MultiPolygonField(srid=21896)

    def __unicode__(self):
        return self.code_predi

class Point(models.Model):
    code_predi = models.CharField(max_length=200)
    geom = models.PointField('longitude/latitude',srid=21896 ,blank=True, null=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return self.code_predi


class HistoriaPredioCultivo (models.Model):
    anno = models.IntegerField()
    mes = models.SmallIntegerField()
    sem = models.IntegerField()
    area_cultivo = models.DecimalField(max_digits=11, decimal_places=4, validators=[MinValueValidator(1)])
    codigo_predio = models.ForeignKey(Predio, on_delete=models.DO_NOTHING)
    id_cultivo =  models.ForeignKey(TipoCultivo, on_delete=models.DO_NOTHING)
    Consumo = models.DecimalField(max_digits=11, decimal_places=4)
    lamina  = models.DecimalField(max_digits=6, decimal_places=3)
    usuario_registro = models.ForeignKey(User, related_name='HPCusuarioregistro',null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    usuario_modifica = models.ForeignKey(User, related_name='HPCusuariomodifica', null=True, blank=True)
    fecha_modifica = models.DateTimeField(auto_now=True, null=True, blank=True)

    @property
    def json(self):
        if self.sem == 1:
            return {
                    'codigo_predio' : self.codigo_predio.codigo_predio,
                    'id_cultivo': self.id_cultivo.nombre_cultivo,
                    'area_cultivo' : self.area_cultivo,
                    'Consumo' : self.Consumo,
                    'anno' : self.anno,
                    'sem': 'A',
                    'mes' : self.mes,

                    }
        else:
            return {
                    'codigo_predio' : self.codigo_predio.codigo_predio,
                    'id_cultivo': self.id_cultivo.nombre_cultivo,
                    'area_cultivo' : self.area_cultivo,
                    'Consumo' : self.Consumo,
                    'anno' : self.anno,
                    'sem':'B',
                    'mes' : self.mes,
                    }

class InspectorZona (models.Model):
    id_usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    codigo_zona = models.ForeignKey(Zonas, on_delete=models.DO_NOTHING)
    usuario_registro = models.ForeignKey(User, related_name='IZusuarioregistro',null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    usuario_modifica = models.ForeignKey(User, related_name='IZusuariomodifica', null=True, blank=True)
    fecha_modifica = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        unique_together = (('id_usuario', 'codigo_zona',))

class PredioZona (models.Model):
    codigo_predio = models.ForeignKey(Predio, on_delete=models.DO_NOTHING)
    codigo_zona = models.ForeignKey(Zonas, on_delete=models.DO_NOTHING)
    usuario_registro = models.ForeignKey(User, related_name='PZusuarioregistro',null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    usuario_modifica = models.ForeignKey(User, related_name='PZusuariomodifica', null=True, blank=True)
    fecha_modifica = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        unique_together = (('codigo_predio', 'codigo_zona',))

