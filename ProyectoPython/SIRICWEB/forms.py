# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django import forms
from models import *
from django.forms import ModelForm, ModelChoiceField
from datetime import *
from decimal import Decimal
import os, sys
from bootstrap3_datetime.widgets import DateTimePicker

class RegistroForm(UserCreationForm):


	email = forms.EmailField(widget=forms.TextInput(attrs={'size':'48', 'class':'form-control'}))
	password1 = forms.CharField(label='Contrasena nueva', widget=forms.PasswordInput(attrs={'class':'form-control'}))
	password2 = forms.CharField(label='Contrasena nueva (confirmar)', widget=forms.PasswordInput(attrs={'class':'form-control'}))

	class Meta:
		model = User
		fields = [
				'username',
				'first_name',
				'last_name',
				'email',
				'is_active',
				'password1',
				'password2',
			]
		labels	= {
				'username' : 'Nombre de usuario',
				'first_name' : 'Nombre',
				'last_name' : 'Apellidos',
				'email' : 'Correo',
				'is_active' : 'Activo',
				'password1' : 'Contraseña',
				'password2' : 'Contraseña (Confirmación)',

			}
		help_texts = {
            'username': 'Requiere. 150 caracteres o menos. letras, dígitos.',
        }
		widgets = {
				'username' : forms.TextInput(attrs={'class':'form-control'}),
				'first_name' : forms.TextInput(attrs={'class':'form-control'}),
				'last_name' : forms.TextInput(attrs={'class':'form-control'}),
				'email' : forms.TextInput(attrs={'class':'form-control'}),
				'is_active' : forms.CheckboxInput(),
			}

class PasswordForm(SetPasswordForm):

	new_password1 = forms.CharField(label='Contrasena nueva', widget=forms.PasswordInput(attrs={'class':'form-control'}))
	new_password2 = forms.CharField(label='Contrasena nueva (confirmar)', widget=forms.PasswordInput(attrs={'class':'form-control'}))

	class Meta:
		model = User
		fields = [
				'new_password1',
				'new_password2',
			]
		labels	= {
				'new_password2' : 'Contrasena nueva',
				'new_password2' : 'Contrasena nueva (confirmar)',

			}

class UpdateForm(ModelForm):

	email = forms.EmailField(widget=forms.TextInput(attrs={'size':'48', 'class':'form-control'}))

	class Meta:
		model = User
		fields = [
				'username',
				'first_name',
				'last_name',
				'email',
				'is_active'
			]
		labels	= {
				'username' : 'Nombre de usuario',
				'first_name' : 'Nombre',
				'last_name' : 'Apellidos',
				'email' : 'Correo',
				'is_active' : 'Activo'
			}
		widgets = {
				'username' : forms.TextInput(attrs={'class':'form-control'}),
				'first_name' : forms.TextInput(attrs={'class':'form-control'}),
				'last_name' : forms.TextInput(attrs={'class':'form-control'}),
				'email' : forms.TextInput(attrs={'class':'form-control'}),
			}

class DatosUsuarioForm(ModelForm):

	email = forms.EmailField(widget=forms.TextInput(attrs={'size':'48', 'class':'form-control'}))

	class Meta:
		model = User
		fields = [
				'username',
				'first_name',
				'last_name',
				'email',
			]
		labels	= {
				'username' : 'Nombre de usuario',
				'first_name' : 'Nombre',
				'last_name' : 'Apellidos',
				'email' : 'Correo',
			}
		widgets = {
				'username' : forms.TextInput(attrs={'class':'form-control'}),
				'first_name' : forms.TextInput(attrs={'class':'form-control'}),
				'last_name' : forms.TextInput(attrs={'class':'form-control'}),
				'email' : forms.TextInput(attrs={'class':'form-control'}),
			}

class RolForm(ModelForm):

	class Meta:
		model = Profile
		fields = [
				'cargo',
				'role',
			]
		labels	= {
				'cargo' : 'Cargo',
				'role' : 'Rol',
			}

		widgets = {
				'cargo' : forms.TextInput(attrs={'class':'form-control'}),
				'role' : forms.Select(attrs={'class':'form-control'}),
			}

class DatosTerceroForm(ModelForm):

	correo = forms.EmailField(widget=forms.TextInput(attrs={'size':'48', 'class':'form-control'})),
	correo_razon_social = forms.EmailField(widget=forms.TextInput(attrs={'size':'48', 'class':'form-control'})),

	class Meta:
		model = Tercero
		fields = [
				'tipo_identificacion',
				'identificacion',
				'pirme_nombre',
				'segundo_nombre',
				'primer_apellido',
				'segundo_apellido',
				'telefono',
				'celular',
				'correo',
				'direccion',
    			'razon_social',
    			'identificacion_representante',
    			'tipo_identificacion_representante',
    			'telefono_razon_social',
    			'celular_razon_social',
    			'correo_razon_social',
    			'direccion_razon_social',
				'activo'
			]
		labels	= {
				'tipo_identificacion' : 'Tipo Identificación',
				'identificacion' : 'Identificación',
				'pirme_nombre' : 'Primer Nombre',
				'segundo_nombre' : 'Segundo Nombre',
				'primer_apellido' : 'Primer Apellido',
				'segundo_apellido' : 'Segundo Apellido',
				'telefono' : 'Teléfono',
				'celular' : 'Celular',
				'correo' : 'Correo',
				'direccion' : 'Dirección',
    			'razon_social' : 'Razón Social',
    			'identificacion_representante' : 'Identificación Representante Legal',
    			'tipo_identificacion_representante' : 'Tipo Identificación Representante Legal',
    			'telefono_razon_social' : 'Teléfono Razón Social',
    			'celular_razon_social' : 'Celular Razón Social',
    			'correo_razon_social' : 'Correo Razón Social',
    			'direccion_razon_social' : 'Dirección Razón Social',
				'activo' : 'Activo',

				

			}
		widgets = {
				'tipo_identificacion' : forms.Select(attrs={'class':'form-control'}),
				'identificacion' : forms.TextInput(attrs={'class':'form-control','pattern':'[0-9]+', 'title':'Ingresar solo numeros'}),
				'pirme_nombre' : forms.TextInput(attrs={'class':'form-control'}),
				'segundo_nombre' : forms.TextInput(attrs={'class':'form-control'}),
				'primer_apellido' : forms.TextInput(attrs={'class':'form-control'}),
				'segundo_apellido' : forms.TextInput(attrs={'class':'form-control'}),
				'telefono' : forms.TextInput(attrs={'class':'form-control','pattern':'[0-9]+', 'title':'Ingresar solo numeros','size':'7'}),
				'celular' : forms.TextInput(attrs={'class':'form-control','pattern':'[0-9]+', 'title':'Ingresar solo numeros','size':'10'}),
				'correo' : forms.TextInput(attrs={'class':'form-control'}),
				'direccion' : forms.TextInput(attrs={'class':'form-control'}),
				'razon_social' : forms.TextInput(attrs={'class':'form-control', 'required': 'true'}),
    			'identificacion_representante' : forms.Select(attrs={'class':'form-control','required': 'true'}),
    			'tipo_identificacion_representante' : forms.TextInput(attrs={'class':'form-control','pattern':'[0-9]+', 'title':'Ingresar solo numeros', 'required': 'true'}),
    			'telefono_razon_social' : forms.TextInput(attrs={'class':'form-control','pattern':'[0-9]+', 'title':'Ingresar solo numeros','size':'7'}),
    			'celular_razon_social' : forms.TextInput(attrs={'class':'form-control','pattern':'[0-9]+', 'title':'Ingresar solo numeros','size':'10'}),
    			'correo_razon_social' : forms.TextInput(attrs={'class':'form-control'}),
    			'direccion_razon_social' : forms.TextInput(attrs={'class':'form-control'}),
				'activo' : forms.CheckboxInput(),
			}

class DatosPredioForm(ModelForm):

	class Meta:
		model = Predio
		fields = [
				'codigo_predio',
				'cedula_catastral',
				'matricula_inmobiliaria',
				'area_total',
				'area_beneficiada',
				'area_cultivada',
				'latitud',
				'logitud',
				'nombre_predio',
				'ubicacion_predio',
				'ruta_escritura',
				'ruta_matricula_inmobiliaria',
				'usuario_registro',
				'usuario_modifica'

			]
		labels	= {
				'codigo_predio' : 'Código',
				'cedula_catastral' : 'Cédula Catastral',
				'matricula_inmobiliaria' : 'Matrícula Inmobiliaria',
				'area_total' : 'Área Total (HA)',
				'area_beneficiada' : 'Área Beneficiada (HA)',
				'area_cultivada' : 'Área Cultivada (HA)',
				'latitud' : 'Latitud',
				'logitud' : 'Logitud',
				'nombre_predio' : 'Nombre',
				'ubicacion_predio' : 'Ubicación',
				'ruta_escritura' : 'PDF Escritura',
				'ruta_matricula_inmobiliaria' : 'PDF Matrícula Inmobiliaria',

			}
		help_texts = {
            'area_total': 'Formato de registro maximo. 7 enteros y 4 decimales, separados por coma.',
            'area_beneficiada': 'Formato de registro maximo. 7 enteros y 4 decimales, separados por coma.',
            'area_cultivada': 'Formato de registro maximo. 7 enteros y 4 decimales, separados por coma.',
            'latitud': 'Formato de registro maximo. 4 enteros y 6 decimales, separados por coma.',
            'logitud': 'Formato de registro maximo. 4 enteros y 6 decimales, separados por coma.',

        }	
		widgets = {
				'codigo_predio' : forms.TextInput(attrs={'class':'form-control'}),
				'cedula_catastral' : forms.TextInput(attrs={'class':'form-control'}),
				'matricula_inmobiliaria' : forms.TextInput(attrs={'class':'form-control'}),
				'area_total' : forms.NumberInput(attrs={'class':'form-control'}),
				'area_beneficiada' : forms.NumberInput(attrs={'class':'form-control'}),
				'area_cultivada' : forms.NumberInput(attrs={'class':'form-control'}),
				'latitud' : forms.NumberInput(attrs={'class':'form-control'}),
				'logitud' : forms.NumberInput(attrs={'class':'form-control'}),
				'nombre_predio' : forms.TextInput(attrs={'class':'form-control'}),
				'ubicacion_predio' : forms.TextInput(attrs={'class':'form-control'}),
				'usuario_registro' : forms.HiddenInput(),
				'usuario_modifica' : forms.HiddenInput(),
			}
	def clean(self):
	    cleaned_data = super(DatosPredioForm, self).clean()
	    area_total = cleaned_data.get('area_total')
	    area_cultivada = cleaned_data.get('area_cultivada')
	    area_beneficiada = cleaned_data.get('area_beneficiada')
	    if area_beneficiada > area_total:
	        self._errors['area_beneficiada'] = self.error_class(['Área beneficiada no puede ser mayor al área total del predio'])
	    elif area_cultivada > area_beneficiada:
	    	self._errors['area_cultivada'] = self.error_class(['Área cultivo no puede ser mayor al área beneficiada'])
	    return cleaned_data


		    
class DatosPredioPropietarioForm(forms.ModelForm):

	class Meta:
		model = PredioPropietario
		fields = [
				'codigo_predio',
				'identificacion_propietario',
				'identificacion_usuario',
				'derecho'

			]
		labels	= {
				'codigo_predio' : 'Código',
				'identificacion_propietario' : 'Propietario',
				'identificacion_usuario' : 'Usuario',
				'derecho' : 'Derecho'


			}
		widgets = {
				'codigo_predio' : forms.TextInput(attrs={'class':'form-control', 'readonly': 'readonly'}),
				'identificacion_propietario' : forms.TextInput(attrs={'class':'form-control'}),
				'identificacion_usuario' : forms.TextInput(attrs={'class':'form-control'}),
				'derecho' : forms.NumberInput(attrs={'class':'form-control'})
			}

class DatosTipoIdentificacionForm(ModelForm):

	class Meta:
		model = TipoIdentificacion
		fields = [
				'nombre'

			]
		labels	= {
				'nombre' : 'Nombre'

			}
		widgets = {
				'nombre' : forms.TextInput(attrs={'class':'form-control'})
			}

class DatosTipoCultivoForm(ModelForm):

	class Meta:
		model = TipoCultivo
		fields = [
				'nombre_cultivo'

			]
		labels	= {
				'nombre_cultivo' : 'Nombre'

			}
		widgets = {
				'nombre_cultivo' : forms.TextInput(attrs={'class':'form-control'})
			}

class DatosCultivoForm(forms.ModelForm):

	class Meta:
		model = Cultivo
		fields = [
				'id_cultivo',
				'consumo_aguaF1',
				'consumo_aguaF2',
				'consumo_aguaF3',
				'consumo_aguaF4',
				'longitud_raizF1',
				'longitud_raizF2',
				'longitud_raizF3',
				'longitud_raizF4',
				'duracion',
				'usuario_registro',
				'usuario_modifica'

			]
		labels	= {
				'id_cultivo': 'Tipo Cultivo',
				'consumo_aguaF1' : 'Consumo de Agua Fase 1',
				'consumo_aguaF2' : 'Consumo de Agua Fase 2',
				'consumo_aguaF3' : 'Consumo de Agua Fase 3',
				'consumo_aguaF4' : 'Consumo de Agua Fase 4',
				'longitud_raizF1' : 'Logitud de Raiz 1',
				'longitud_raizF2' : 'Logitud de Raiz 2',
				'longitud_raizF3' : 'Logitud de Raiz 3',
				'longitud_raizF4' : 'Logitud de Raiz 4',
				'duracion' : 'Duración',
			}

		help_texts = {
            'consumo_aguaF1': 'Formato de registro maximo. 7 enteros y 4 decimales, separados por coma.',
            'consumo_aguaF2': 'Formato de registro maximo. 7 enteros y 4 decimales, separados por coma.',
            'consumo_aguaF3': 'Formato de registro maximo. 7 enteros y 4 decimales, separados por coma.',
            'consumo_aguaF4': 'Formato de registro maximo. 7 enteros y 4 decimales, separados por coma.',
            'longitud_raizF1': 'Formato de registro maximo. 3 enteros y 2 decimales, separados por coma.',
            'longitud_raizF2': 'Formato de registro maximo. 3 enteros y 2 decimales, separados por coma.',
            'longitud_raizF3': 'Formato de registro maximo. 3 enteros y 2 decimales, separados por coma.',
            'longitud_raizF4': 'Formato de registro maximo. 3 enteros y 2 decimales, separados por coma.',
            'duracion': 'Formato de registro maximo. 3 enteros y 2 decimales, separados por coma.',
            }

		widgets = {
				'id_cultivo' : forms.Select(attrs={'class':'form-control'}),
				'consumo_aguaF1' : forms.NumberInput(attrs={'class':'form-control'}),
				'consumo_aguaF2' : forms.NumberInput(attrs={'class':'form-control'}),
				'consumo_aguaF3' : forms.NumberInput(attrs={'class':'form-control'}),
				'consumo_aguaF4' : forms.NumberInput(attrs={'class':'form-control'}),
				'longitud_raizF1' : forms.NumberInput(attrs={'class':'form-control'}),
				'longitud_raizF2' : forms.NumberInput(attrs={'class':'form-control'}),
				'longitud_raizF3' : forms.NumberInput(attrs={'class':'form-control'}),
				'longitud_raizF4' : forms.NumberInput(attrs={'class':'form-control'}),
				'duracion' : forms.NumberInput(attrs={'class':'form-control'}),
				'usuario_registro' : forms.HiddenInput(),
				'usuario_modifica' : forms.HiddenInput(),
			}

class DatosPredioCultivoForm(ModelForm):

	class Meta:
		model = PredioCultivo
		fields = [
				'codigo_predio',
				'id_cultivo',
				'area_cultivo',
				'fecha_inicio',
				'usuario_registro',
				'usuario_modifica',
			]

		labels	= {
				'codigo_predio' : 'Código Predio',
				'id_cultivo' : 'Cultivo',
				'area_cultivo' : 'Área Cultivo (HA)',
				'fecha_inicio' : 'Fecha Inicio',

			}

		widgets = {
				'codigo_predio' : forms.TextInput(attrs={'class':'form-control', 'readonly': 'readonly'}),
				'id_cultivo' : forms.Select(attrs={'class':'form-control'}),
				'area_cultivo' : forms.NumberInput(attrs={'class':'form-control'}),
				'fecha_inicio' :  forms.TextInput(attrs={'class':'form-control datetimepickerCultivo','id': 'datetimepickerCultivo'}),
				'usuario_registro' : forms.HiddenInput(),
				'usuario_modifica' : forms.HiddenInput(),
			}

class DatosCanalesForm(ModelForm):

	class Meta:
		model = Canales
		fields = [
				'tipo_canal',
				'nombre_canal',
				'logitud',
				'capacidad',
				'revestido',
				'logitudrevestido'

			]
		labels	= {
				'tipo_canal' : 'Tipo Canal',
				'nombre_canal' : 'Nombre',
				'logitud' : 'Longitud',
				'capacidad' : 'Capacidad',
				'revestido' : 'Revestido',
				'logitudrevestido' : 'Logitud Revestido'

			}
		widgets = {
				'tipo_canal' : forms.Select(attrs={'class':'form-control'}),
				'nombre_canal' : forms.TextInput(attrs={'class':'form-control'}),
				'logitud' : forms.NumberInput(attrs={'class':'form-control'}),
				'capacidad' : forms.NumberInput(attrs={'class':'form-control'}),
				'revestido' : forms.CheckboxInput(attrs={'disabled': 'true'}),
				'logitudrevestido' : forms.NumberInput(attrs={'class':'form-control', 'disabled': 'true'})
			}

class DatosMetodoRiegoForm(ModelForm):

	class Meta:
		model = MetodoRiego
		fields = [
				'nombre_metodoriego'

			]
		labels	= {
				'nombre_metodoriego' : 'Nombre'

			}
		widgets = {
				'nombre_metodoriego' : forms.TextInput(attrs={'class':'form-control'})
			}

class DatosPredioCanalForm(ModelForm):

	class Meta:
		model = PredioCanal
		fields = [
				'codigo_predio',
				'id_canal',
				'abscisa',
				'usuario_registro',
				'usuario_modifica',
			]

		labels	= {
				'codigo_predio' : 'Código Predio',
				'id_canal' : 'Canal',
				'abscisa' : 'Abscisa',

			}

		widgets = {
				'codigo_predio' : forms.TextInput(attrs={'class':'form-control', 'readonly': 'readonly'}),
				'id_canal' : forms.Select(attrs={'class':'form-control'}),
				'abscisa' : forms.NumberInput(attrs={'class':'form-control'}),
				'usuario_registro' : forms.HiddenInput(),
				'usuario_modifica' : forms.HiddenInput(),
			}

class DatosRegistroRiegoForm(ModelForm):

	def __init__(self, codigo_predio, *args, **kwargs):
		super(DatosRegistroRiegoForm, self).__init__( *args, **kwargs)
        	self.fields['id_canal'] =  ModelChoiceField(queryset=PredioCanal.objects.filter(codigo_predio = codigo_predio), empty_label = "-------", widget=forms.Select(attrs={'class':'form-control'}))

	hora = forms.DateTimeField(required=False, widget=DateTimePicker())

	class Meta:
		model = RegistroRiego
		fields = [
				'codigo_predio',
				'id_canal',
				'id_metodoRiego',
				'id_cultivo',
				'fecha_inicio',
				'fecha_final',
				'hora_inicio',
				'hore_final',
				'dotacion_inicial',
				'duracion_riego',
				'volumen_agua',
				'usuario_registro',
				'usuario_modifica',
			]

		labels	= {
				'codigo_predio' : 'Código Predio',
				'id_canal' : 'Canal',
				'id_metodoRiego' : 'Metodo de Riego',
				'id_cultivo' : 'Cultivo',
				'fecha_inicio': 'Fecha Incio Riego',
				'fecha_final' : 'Fecha Fin Riego',
				'hora_inicio' : 'Hora Inicio Riego',
				'hore_final' : 'Hora Final Riego',
				'dotacion_inicial' : 'Dotación inicial L/s',
				'duracion_riego' : 'Duración de Riego',
				'volumen_agua' : 'Volumen de Agua (M3)',

			}

		help_texts = {
            'duracion_riego': 'Formato de registro maximo. 4 enteros y 2 decimales, separados por coma.',
            'volumen_agua': 'Formato de registro maximo. 8 enteros y 2 decimales, separados por coma.',
            }

		widgets = {
				'codigo_predio' : forms.TextInput(attrs={'class':'form-control', 'readonly': 'readonly'}),
				'id_canal' : forms.Select(attrs={'class':'form-control'}),
				'id_metodoRiego' : forms.Select(attrs={'class':'form-control'}),
				'id_cultivo' : forms.Select(attrs={'class':'form-control'}),
				'fecha_inicio' :  forms.TextInput(attrs={'class':'form-control datetimepickerRiegoInicio','id': 'datetimepickerRiegoInicio'}),
				'fecha_final' :  forms.TextInput(attrs={'class':'form-control datetimepickerRiegoFin','id': 'datetimepickerRiegoFin'}),
				'hora_inicio' :  forms.TextInput(attrs={'class':'form-control datetimepickerHoraInicio','id': 'datetimepickerHoraInicio'}),
				'hore_final' :  forms.TextInput(attrs={'class':'form-control datetimepickerHoraFinal','id': 'datetimepickerHoraFinal'}),
				'dotacion_inicial' : forms.NumberInput(attrs={'class':'form-control'}),
				'duracion_riego' : forms.NumberInput(attrs={'class':'form-control','readonly': 'readonly'}),
				'volumen_agua' : forms.NumberInput(attrs={'class':'form-control','readonly': 'readonly'}),
				'usuario_registro' : forms.HiddenInput(),
				'usuario_modifica' : forms.HiddenInput(),
			}

	def clean(self):
	    cleaned_data = super(DatosRegistroRiegoForm, self).clean()
	    if cleaned_data.get('fecha_final') is None:
	    	return cleaned_data

	    fechafin = datetime.combine(cleaned_data.get('fecha_final'), cleaned_data.get('hore_final'))
	    fechaini = datetime.combine(cleaned_data.get('fecha_inicio'), cleaned_data.get('hora_inicio'))
	    diferencia  = fechafin - fechaini
	    duracion  = float(diferencia.seconds // 3600)
	    minuto =  float(((diferencia.seconds % 3600) // 60))
	    d = float(minuto/60.00)
	    duracionT =  float(duracion + d)
	    self.cleaned_data['duracion_riego'] = format(duracionT, '.2f')
	    dotacion = cleaned_data.get('dotacion_inicial')
	    volumen = Decimal(duracionT) * Decimal(dotacion) * Decimal(3.6)
	    self.cleaned_data['volumen_agua'] = format(volumen, '.2f')
	    if fechafin <= fechaini:
	        self._errors['fecha_final'] = self.error_class(['Fecha final del riego no puede ser menor o igual a la fecha inicial'])
	    return cleaned_data

class DatosModificarRiegoForm(ModelForm):

	hora = forms.DateTimeField(required=False, widget=DateTimePicker())

	class Meta:
		model = RegistroRiego
		fields = [
				'codigo_predio',
				'id_canal',
				'id_metodoRiego',
				'id_cultivo',
				'fecha_inicio',
				'fecha_final',
				'hora_inicio',
				'hore_final',
				'dotacion_inicial',
				'dotacion_final',
				'duracion_riego',
				'volumen_agua',
				'usuario_registro',
				'usuario_modifica',
			]

		labels	= {
				'codigo_predio' : 'Código Predio',
				'id_canal' : 'Canal',
				'id_metodoRiego' : 'Metodo de Riego',
				'id_cultivo' : 'Cultivo',
				'fecha_inicio': 'Fecha Incio Riego',
				'fecha_final' : 'Fecha Fin Riego',
				'hora_inicio' : 'Hora Inicio Riego',
				'hore_final' : 'Hora Final Riego',
				'dotacion_inicial' : 'Dotación inicial L/s',
				'dotacion_final' : 'Dotación final L/s',
				'duracion_riego' : 'Duración de Riego',
				'volumen_agua' : 'Volumen de Agua (M3)',

			}

		help_texts = {
            'duracion_riego': 'Formato de registro maximo. 4 enteros y 2 decimales, separados por coma.',
            'volumen_agua': 'Formato de registro maximo. 8 enteros y 2 decimales, separados por coma.',
            }

		widgets = {
				'codigo_predio' : forms.TextInput(attrs={'class':'form-control', 'readonly': 'readonly'}),
				'id_canal' : forms.Select(attrs={'class':'form-control', 'readonly': 'readonly'}),
				'id_metodoRiego' : forms.Select(attrs={'class':'form-control', 'readonly': 'readonly'}),
				'id_cultivo' : forms.Select(attrs={'class':'form-control', 'readonly': 'readonly'}),
				'fecha_inicio' :  forms.TextInput(attrs={'class':'form-control datetimepickerRiegoInicio','id': 'datetimepickerRiegoInicio'}),
				'fecha_final' :  forms.TextInput(attrs={'class':'form-control datetimepickerRiegoFin','id': 'datetimepickerRiegoFin'}),
				'hora_inicio' :  forms.TextInput(attrs={'class':'form-control datetimepickerHoraInicio','id': 'datetimepickerHoraInicio'}),
				'hore_final' :  forms.TextInput(attrs={'class':'form-control datetimepickerHoraFinal','id': 'datetimepickerHoraFinal'}),
				'dotacion_inicial' : forms.NumberInput(attrs={'class':'form-control'}),
				'dotacion_final' : forms.NumberInput(attrs={'class':'form-control'}),
				'duracion_riego' : forms.NumberInput(attrs={'class':'form-control','readonly': 'readonly'}),
				'volumen_agua' : forms.NumberInput(attrs={'class':'form-control','readonly': 'readonly'}),
				'usuario_registro' : forms.HiddenInput(),
				'usuario_modifica' : forms.HiddenInput(),
			}

	def clean(self):
	    cleaned_data = super(DatosModificarRiegoForm, self).clean()
	    if cleaned_data.get('fecha_final') is None:
	    	return cleaned_data

	    fechafin = datetime.combine(cleaned_data.get('fecha_final'), cleaned_data.get('hore_final'))
	    fechaini = datetime.combine(cleaned_data.get('fecha_inicio'), cleaned_data.get('hora_inicio'))
	    diferencia  = fechafin - fechaini
	    duracion  = float(diferencia.seconds // 3600)
	    minuto =  float(((diferencia.seconds % 3600) // 60))
	    d = float(minuto/60.00)
	    duracionT =  float(duracion + d)
	    self.cleaned_data['duracion_riego'] = format(duracionT, '.2f')
	    dotacion = cleaned_data.get('dotacion_final')
	    volumen = Decimal(duracionT) * Decimal(dotacion) * Decimal(3.6)
	    self.cleaned_data['volumen_agua'] = format(volumen, '.2f')
	    if fechafin <= fechaini:
	        self._errors['fecha_final'] = self.error_class(['Fecha final del riego no puede ser menor o igual a la fecha inicial'])
	    return cleaned_data

class DatosFiltroGraficoForm(ModelForm):

	CHOICES= (('','-------'),('1','A'),('2','B'),)

	sem = forms.ChoiceField(choices = CHOICES, initial='------', widget=forms.Select(attrs={'class':'form-control'}), required=True)

	class Meta:
		model = HistoriaPredioCultivo
		fields = [
				'anno',
				'sem'

			]
		labels	= {
				'anno' : 'Vigencia',
				'sem' : 'Semestre'

			}
		widgets = {
				'anno' : forms.NumberInput(attrs={'class':'form-control','min': 0, 'max': 9999}),
			}

class DatosZonaForm(ModelForm):

	class Meta:
		model = Zonas
		fields = [
				'codigo_zona',
				'nombre_zona',
				'usuario_registro',
				'usuario_modifica',

			]
		labels	= {
				'codigo_zona' : 'Código Zona',
				'nombre_zona' : 'Zona'

			}
		widgets = {
				'codigo_zona' : forms.TextInput(attrs={'class':'form-control'}),
				'nombre_zona' : forms.TextInput(attrs={'class':'form-control'}),
				'usuario_registro' : forms.HiddenInput(),
				'usuario_modifica' : forms.HiddenInput(),
			}

class DatosInspectorZonaForm(ModelForm):

	class Meta:
		model = InspectorZona
		fields = [
				'id_usuario',
				'codigo_zona',
				'usuario_registro',
				'usuario_modifica',

			]
		labels	= {
				'id_usuario' : 'Inspector',
				'codigo_zona' : 'Zona'

			}
		widgets = {
				'id_usuario' : forms.TextInput(attrs={'class':'form-control','readonly': 'readonly'}),
				'codigo_zona' : forms.Select(attrs={'class':'form-control'}),
				'usuario_registro' : forms.HiddenInput(),
				'usuario_modifica' : forms.HiddenInput(),
			}

class DatosPredioZonaForm(ModelForm):

	class Meta:
		model = PredioZona
		fields = [
				'codigo_predio',
				'codigo_zona',
				'usuario_registro',
				'usuario_modifica',

			]
		labels	= {
				'codigo_predio' : 'Código Predio',
				'codigo_zona' : 'Zona'

			}
		widgets = {
				'codigo_predio' : forms.TextInput(attrs={'class':'form-control','readonly': 'readonly'}),
				'codigo_zona' : forms.Select(attrs={'class':'form-control'}),
				'usuario_registro' : forms.HiddenInput(),
				'usuario_modifica' : forms.HiddenInput(),
			}

class ReporteDiarioForm(ModelForm):

	hora = forms.DateTimeField(required=False, widget=DateTimePicker())

	class Meta:
		model = RegistroRiego
		fields = [
				'fecha_inicio',
				'fecha_final',
			]

		labels	= {
				'fecha_inicio': 'Fecha Incio Riego',
				'fecha_final' : 'Fecha Fin Riego',

			}

		widgets = {

				'fecha_inicio' :  forms.TextInput(attrs={'class':'form-control datetimepickerRiegoInicio','id': 'datetimepickerRiegoInicio'}),
				'fecha_final' :  forms.TextInput(attrs={'class':'form-control datetimepickerRiegoFin','id': 'datetimepickerRiegoFin'}),
			}