# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.files.storage import default_storage

from django.db.models.fields.files import FieldFile
from django.views.generic import CreateView, FormView, ListView, DetailView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, Context, loader
from django.shortcuts import render_to_response
from django.db import connection
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from forms import *
from models import *
from django.db.models import Sum
from django.core.exceptions import ValidationError
from django.contrib.auth import update_session_auth_hash
from django.db import IntegrityError
from decimal import Decimal
from django.core.serializers import serialize
from django.core.cache import cache
import json
from django.core.serializers.json import DjangoJSONEncoder

# http://yuji.wordpress.com/2013/01/30/django-form-field-in-initial-data-requires-a-fieldfile-instance/
class FakeField(object):
	storage = default_storage


fieldfile = FieldFile(None, FakeField, 'dummy.txt')

def HomePageView(request):
	predioRiegoPendiente = RegistroRiego.objects.filter(fecha_final= None)
	cursor = connection.cursor()
	cursor.callproc("spInicio")
	result = cursor.fetchall()
	result_list = []
	cursor.close()
	for row in result:
		p = RegistroRiego(dotacion_final=row[3], volumen_agua=row[4], duracion_riego=row[5], fecha_inicio=row[6], codigo_predio_id=row[9], id_canal_id=row[10])
		result_list.append(p)
	return render(request, 'SIRICWEB/index.html', {'result': result_list , 'predioRiegoPendiente':predioRiegoPendiente })


class UsuarioList(ListView):
	model = User
	template_name = 'SIRICWEB/Administracion/listarUsuarios.html'

class RegistroUsuario(CreateView):
	model = User
	template_name = 'SIRICWEB/Administracion/RegistroUsuario.html'
	form_class = RegistroForm
	second_form_class = RolForm
	success_url = '/SIRICWEB/lista'

	def get_context_data(self, **kwargs):
		context = super(RegistroUsuario, self).get_context_data(**kwargs)
		if 'form' not in context:
			context['form'] = self.form_class(self.request.GET)
		if 'form2' not in context:
			context['form2'] = self.second_form_class(self.request.GET)
		return context

	def post(self, request, *args, **kwargs):
			self.object = self.get_object
			form = self.form_class(request.POST)
			form2 = self.second_form_class(request.POST)
			if form.is_valid() and form2.is_valid():
				rol = form2.save(commit=False)
				rol.user = form.save()
				rol.save()
				return HttpResponseRedirect(self.get_success_url())
			else:
				return self.render_to_response(self.get_context_data(form=form, form2=form2))  

class ModificarUsuario(UpdateView):
	model = AuthUser
	second_model = Profile
	template_name = 'SIRICWEB/Administracion/ModificarUsuario.html'
	form_class = UpdateForm
	second_form_class = RolForm
	success_url = '/SIRICWEB/lista'
	

	def get_context_data(self, **kwargs):
		context = super(ModificarUsuario, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk',0)
		modificar = self.model.objects.get(id=pk)
		rol = self.second_model.objects.get(user_id=modificar.id)
		if 'form' not in context:
			context['form'] = self.form_class()
		if 'form2' not in context:
			context['form2'] = self.second_form_class(instance=rol)
		context['id'] = pk
		return context

	def post(self, request, *args, **kwargs):
		if request.method == 'POST':
			self.object = self.get_object
			id_persona = kwargs['pk']
			modificar = self.model.objects.get(id=id_persona)
			rol = self.second_model.objects.get(user_id=modificar.id)
			form = self.form_class(request.POST, instance=modificar)
			form2 = self.second_form_class(request.POST, instance=rol)
			if form.is_valid() and form2.is_valid():
				form.save()
				form2.save()
				return HttpResponseRedirect(self.get_success_url())
			else:
				messages.error(request, 'Error al Modificar los datos del usuario.')
		return render(request, 'SIRICWEB/Administracion/ModificarUsuario.html', {'form': form , 'form2':form2})    

class DatosUsuario(UpdateView):
	model = AuthUser
	form_class = DatosUsuarioForm
	template_name = 'SIRICWEB/Administracion/DatosUsuario.html'
	success_url = '/SIRICWEB/'

def change_password_usuario(request, id_usuario):
	if request.method == 'POST':
		usuario = User.objects.get(id=id_usuario)
		form = PasswordForm(usuario, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, usuario)  # Important!
			return redirect('/SIRICWEB/lista')
		else:
			messages.error(request, 'Contraseñas no son iguales.')
	else:
		usuario = User.objects.get(id=id_usuario)
		form = PasswordForm(usuario)
	return render(request, 'SIRICWEB/Administracion/CambiarContrasena.html', {'form': form})

def change_password(request, id_usuario):
	if request.method == 'POST':
		usuario = User.objects.get(id=id_usuario)
		form = PasswordForm(usuario, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, usuario)  # Important!
			return redirect('/SIRICWEB/lista')
		else:
			messages.error(request, 'Contraseñas no son iguales.')
	else:
		usuario = User.objects.get(id=id_usuario)
		form = PasswordForm(usuario)
	return render(request, 'SIRICWEB/Administracion/CambiarContrasena.html', {'form': form})

class TerceroList(TemplateView):
	template_name = 'SIRICWEB/Terceros/listarTerceros.html'

def JSONTerceroList_view(request):
	datoster = Tercero.objects.all()
	datosterceros = json.dumps([datos.json for datos in datoster ],cls=DjangoJSONEncoder)
	return HttpResponse(datosterceros, content_type='application/json')

class RegistroTercero(CreateView):
	model = Tercero
	template_name = 'SIRICWEB/Terceros/RegistroTercero.html'
	form_class = DatosTerceroForm
	success_url = '/SIRICWEB/listarTerceros'

class ModificarTercero(UpdateView):
	model = Tercero
	form_class = DatosTerceroForm
	template_name = 'SIRICWEB/Terceros/ModificarTercero.html'
	success_url = '/SIRICWEB/listarTerceros'

class PredioList(ListView):
	model = Predio
	template_name = 'SIRICWEB/Predios/listarPredios.html'

class RegistroPredio(CreateView):
	model = Predio
	template_name = 'SIRICWEB/Predios/RegistroPredio.html'
	form_class = DatosPredioForm
	success_url = '/SIRICWEB/listarPredios'

class ModificarPredio(UpdateView):
	model = Predio
	form_class = DatosPredioForm
	template_name = 'SIRICWEB/Predios/ModificarPredio.html'
	success_url = '/SIRICWEB/listarPredios'

def RegistroPredioPropietario(request, codigo_predio):
	predioPropietario = PredioPropietario.objects.filter(codigo_predio= codigo_predio)
	tercero = Tercero.objects.all()
	totalderecho =  PredioPropietario.objects.filter(codigo_predio= codigo_predio).aggregate(Sum('derecho')).values()[0]
	if totalderecho == None:
		totalderecho = 0
	if request.method == 'POST':
		form = DatosPredioPropietarioForm(request.POST)
		if form.is_valid():
			derecho = form['derecho'].value()
			if (Decimal(totalderecho) + Decimal(derecho)) <= 100 :
				form.save()
				return redirect('/SIRICWEB/registroPredioPropietario/'+ codigo_predio)
			else:
				messages.error(request,'El derecho total para el predio debe ser del 100%. ' + 'Derecho total a registrar '+str(Decimal(totalderecho) + Decimal(derecho))+'%')
		else:
			messages.error(request,'Registro ya existe')
	else:
		form = DatosPredioPropietarioForm()
	return render(request, 'SIRICWEB/Predios/registroPredioPropietario.html', {'form': form, 'predioPropietarios':predioPropietario, 'terceros': tercero ,'cod': codigo_predio})

class TipoIdentificacionList(ListView):
	model = TipoIdentificacion
	template_name = 'SIRICWEB/Maestros/listarTipoIdentificacion.html'

class RegistroTipoIdentificacion(CreateView):
	model = TipoIdentificacion
	template_name = 'SIRICWEB/Maestros/RegistroTipoIdentificacion.html'
	form_class = DatosTipoIdentificacionForm
	success_url = '/SIRICWEB/listarTipoIdentificacion'

class ModificarTipoIdentificacion(UpdateView):
	model = TipoIdentificacion
	template_name = 'SIRICWEB/Maestros/ModificarTipoIdentificacion.html'
	form_class = DatosTipoIdentificacionForm
	success_url = '/SIRICWEB/listarTipoIdentificacion'

class EliminarTipoIdentificacion(DeleteView):
	model = TipoIdentificacion
	template_name = 'SIRICWEB/Maestros/EliminarTipoIdentificacion.html'
	form_class = DatosTipoIdentificacionForm
	success_url = '/SIRICWEB/listarTipoIdentificacion'

	def post(self, request, *args, **kwargs):
			self.object = self.get_object
			id_tipo = kwargs['pk']
			eliminar = self.model.objects.get(id=id_tipo)
			if request.method == 'POST':
				try:
					eliminar.delete()
					return HttpResponseRedirect(self.get_success_url())
				except IntegrityError:
					messages.error(request, 'No se puede eliminar, por que existen registros asociados a este')
			return render(request, 'SIRICWEB/Maestros/EliminarTipoIdentificacion.html', {'eliminar': eliminar })

class TipoCultivoList(ListView):
	model = TipoCultivo
	template_name = 'SIRICWEB/Maestros/listarTipoCultivo.html'

class RegistroTipoCultivo(CreateView):
	model = TipoCultivo
	template_name = 'SIRICWEB/Maestros/RegistroTipoCultivo.html'
	form_class = DatosTipoCultivoForm
	success_url = '/SIRICWEB/listarTipoCultivo'

class ModificarTipoCultivo(UpdateView):
	model = TipoCultivo
	template_name = 'SIRICWEB/Maestros/ModificarTipoCultivo.html'
	form_class = DatosTipoCultivoForm
	success_url = '/SIRICWEB/listarTipoCultivo'

class EliminarTipoCultivo(DeleteView):
	model = TipoCultivo
	template_name = 'SIRICWEB/Maestros/EliminarTipoCultivo.html'
	form_class = DatosTipoCultivoForm
	success_url = '/SIRICWEB/listarTipoCultivo'

	def post(self, request, *args, **kwargs):
			self.object = self.get_object
			id_tipo = kwargs['pk']
			eliminar = self.model.objects.get(id=id_tipo)
			if request.method == 'POST':
				try:
					eliminar.delete()
					return HttpResponseRedirect(self.get_success_url())
				except IntegrityError:
					messages.error(request, 'No se puede eliminar, por que existen registros asociados a este')
			return render(request, 'SIRICWEB/Maestros/EliminarTipoCultivo.html', {'eliminar': eliminar })

class CultivoList(ListView):
	model = Cultivo
	template_name = 'SIRICWEB/Cultivos/listarCultivos.html'

class RegistroCultivo(CreateView):
	model = Cultivo
	template_name = 'SIRICWEB/Cultivos/RegistroCultivos.html'
	form_class = DatosCultivoForm
	success_url = '/SIRICWEB/listarCultivos'

class ModificarCultivo(UpdateView):
	model = Cultivo
	template_name = 'SIRICWEB/Cultivos/ModificarCultivos.html'
	form_class = DatosCultivoForm
	success_url = '/SIRICWEB/listarCultivos'

def RegistroPredioCultivo(request, codigo_predio):
	predioCultivo = PredioCultivo.objects.filter(codigo_predio= codigo_predio)
	totalCultivo =  PredioCultivo.objects.filter(codigo_predio= codigo_predio).aggregate(Sum('area_cultivo')).values()[0]
	if totalCultivo == None:
		totalCultivo = 0
	if request.method == 'POST':
		form = DatosPredioCultivoForm(request.POST)
		if form.is_valid():
			areaCultivo = form['area_cultivo'].value()
			if (Decimal(totalCultivo) + Decimal(areaCultivo)) >= Decimal(totalCultivo) :
				form.save()
				return redirect('/SIRICWEB/registroPredioCultivo/'+ codigo_predio)
			else:
				messages.error(request,'El área cultivada no puede ser mayor al área total cultivada ')
		else:
			messages.error(request,'Registro ya existe')
	else:
		form = DatosPredioCultivoForm()
	return render(request, 'SIRICWEB/Predios/RegistrorPredioCultivo.html', {'form': form, 'predioCultivo':predioCultivo ,'cod': codigo_predio, 'totalCultivo':totalCultivo})

class CanalesList(ListView):
	model = Canales
	template_name = 'SIRICWEB/Maestros/listarCanales.html'

class RegistroCanales(CreateView):
	model = Canales
	template_name = 'SIRICWEB/Maestros/RegistroCanales.html'
	form_class = DatosCanalesForm
	success_url = '/SIRICWEB/listarCanales'

class ModificarCanales(UpdateView):
	model = Canales
	template_name = 'SIRICWEB/Maestros/ModificarCanales.html'
	form_class = DatosCanalesForm
	success_url = '/SIRICWEB/listarCanales'

class EliminarCanales(DeleteView):
	model = Canales
	template_name = 'SIRICWEB/Maestros/EliminarCanales.html'
	form_class = DatosCanalesForm
	success_url = '/SIRICWEB/listarCanales'

	def post(self, request, *args, **kwargs):
			self.object = self.get_object
			id_tipo = kwargs['pk']
			eliminar = self.model.objects.get(id=id_tipo)
			if request.method == 'POST':
				try:
					eliminar.delete()
					return HttpResponseRedirect(self.get_success_url())
				except IntegrityError:
					messages.error(request, 'No se puede eliminar, por que existen registros asociados a este')
			return render(request, 'SIRICWEB/Maestros/EliminarCanales.html', {'eliminar': eliminar })

class MetodoRiegoList(ListView):
	model = MetodoRiego
	template_name = 'SIRICWEB/Maestros/listarMetodoRiego.html'

class RegistroMetodoRiego(CreateView):
	model = MetodoRiego
	template_name = 'SIRICWEB/Maestros/RegistroMetodoRiego.html'
	form_class = DatosMetodoRiegoForm
	success_url = '/SIRICWEB/listarMetodoRiego'

class ModificarMetodoRiego(UpdateView):
	model = MetodoRiego
	template_name = 'SIRICWEB/Maestros/ModificarMetodoRiego.html'
	form_class = DatosMetodoRiegoForm
	success_url = '/SIRICWEB/listarMetodoRiego'

class EliminarMetodoRiego(DeleteView):
	model = MetodoRiego
	template_name = 'SIRICWEB/Maestros/EliminarMetodoRiego.html'
	form_class = DatosMetodoRiegoForm
	success_url = '/SIRICWEB/listarMetodoRiego'

	def post(self, request, *args, **kwargs):
			self.object = self.get_object
			id_tipo = kwargs['pk']
			eliminar = self.model.objects.get(id=id_tipo)
			if request.method == 'POST':
				try:
					eliminar.delete()
					return HttpResponseRedirect(self.get_success_url())
				except IntegrityError:
					messages.error(request, 'No se puede eliminar, por que existen registros asociados a este')
			return render(request, 'SIRICWEB/Maestros/EliminarMetodoRiego.html', {'eliminar': eliminar })

def RegistroPredioCanal(request, codigo_predio):
	prediocanal = PredioCanal.objects.filter(codigo_predio= codigo_predio)
	if request.method == 'POST':
		form = DatosPredioCanalForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/SIRICWEB/registroPredioCanal/'+ codigo_predio)
		else:
			messages.error(request,'Registro ya existe')
	else:
		form = DatosPredioCanalForm()
	return render(request, 'SIRICWEB/Predios/RegistrorPredioCanal.html', {'form': form, 'prediocanal':prediocanal ,'cod': codigo_predio})

class PrediosRiegoList(TemplateView):
	template_name = 'SIRICWEB/Datos/listarPrediosRiego.html'

def JSONPrediosRiegoList_view(request):
	datosprediop = PredioPropietario.objects.all()
	datosprediopropietario = json.dumps([datos.json for datos in datosprediop ],cls=DjangoJSONEncoder)
	return HttpResponse(datosprediopropietario, content_type='application/json')

def RegistroRiegoDiario(request, codigo_predio):
	if request.method == 'POST':
		form = DatosRegistroRiegoForm(codigo_predio,request.POST)
		if form.is_valid():
			try:
				form.save()
				return redirect('/SIRICWEB/listarPrediosRiego')
			except IntegrityError:
				messages.error(request, 'Registro ya existe')
	else:
		form = DatosRegistroRiegoForm(codigo_predio, initial={'codigo_predio': codigo_predio})
	return render(request, 'SIRICWEB/Datos/RegistroRiegoDiario.html', {'form': form})

class ModificarRiegoDiario(UpdateView):
	model = RegistroRiego
	template_name = 'SIRICWEB/Datos/RegistroRiegoDiarioFinal.html'
	form_class = DatosModificarRiegoForm
	success_url = '/SIRICWEB/listarRiegosDiarioPentientes'

class RiegoDiarioList(ListView):
	model = RegistroRiego
	template_name = 'SIRICWEB/Datos/listarRiegosDiario.html'

def points_view(request):
    points_as_geojson = serialize('geojson', CoordenadasPredio.objects.all())
    return HttpResponse(points_as_geojson, content_type='json')
    
class MapaView(TemplateView):
    template_name = 'SIRICWEB/VisorMapa.html'

def HistoriaPredioCultivoList(request, codigo_predio):
	prediocultivo = HistoriaPredioCultivo.objects.filter(codigo_predio= codigo_predio)
	DatosPredio = Predio.objects.filter(codigo_predio= codigo_predio)
	return render(request, 'SIRICWEB/Historico/listarHistoriaPredioCultivo.html', {'prediocultivo':prediocultivo ,'cod': codigo_predio, 'datos': DatosPredio})

class HistoriaPredioList(ListView):
	model = Predio
	template_name = 'SIRICWEB/Historico/listarHistoriaPredio.html'

def GraficaHistoriaPredioConsumo(request, codigo_predio):
	DatosPredio = Predio.objects.filter(codigo_predio= codigo_predio)
	cursor = connection.cursor()
	args = [codigo_predio]
	cursor.callproc("spHistoricoGraficaConsumoSemestrePredio",args)
	result = cursor.fetchall()
	result_list = []
	cursor.close()
	for row in result:
		p = HistoriaPredioCultivo(anno=row[0], sem=row[1], codigo_predio_id=row[2], id_cultivo_id=row[3], Consumo=row[4] )
		result_list.append(p)
	return render(request, 'SIRICWEB/Historico/GraficaHistoriaPredioConsumo.html', {'result': result_list, 'cod': codigo_predio, 'datos': DatosPredio})

def GraficaHistoriaConsumo(request):
	if request.method == 'POST':
		form = DatosFiltroGraficoForm(request.POST)
		cursor = connection.cursor()
		vigencia = request.POST.get('anno')
		semestre = request.POST.get('sem')
		args = [vigencia, semestre]
		cursor.callproc("spConsumoTotalCultivo", args)
		result = cursor.fetchall()
		result_list = []
		cursor.close()
		for row in result:
			p = HistoriaPredioCultivo(anno=row[0], sem=row[1] , id_cultivo_id=row[2], Consumo=row[3])
			result_list.append(p)
		return render(request, 'SIRICWEB/Graficas/GraficaHistoriaConsumo.html', {'form': form,'result': result_list })
	else:
		form = DatosFiltroGraficoForm()
	return render(request, 'SIRICWEB/Graficas/GraficaHistoriaConsumo.html', {'form': form})
	

def RegistroRiegoPendienteList(request):
	predioRiegoPendiente = RegistroRiego.objects.filter(fecha_final= None)
	return render(request, 'SIRICWEB/Datos/listarRiegosDiarioPentientes.html', {'predioRiegoPendiente':predioRiegoPendiente })

def datos_view(request):
    datos = serialize('json', Predio.objects.all())
    return HttpResponse(datos, content_type='application/json')

def jsonhistoriaPredio_view(request, codigo_predio):
	historiaPredioCultivo = HistoriaPredioCultivo.objects.filter(codigo_predio= codigo_predio)
	datosHistoria = json.dumps([historia.json for historia in historiaPredioCultivo ],cls=DjangoJSONEncoder)
	return HttpResponse(datosHistoria, content_type='application/json')

class ZonasList(ListView):
	model = Zonas
	template_name = 'SIRICWEB/Maestros/listarZonas.html'

class RegistroZonas(CreateView):
	model = Zonas
	template_name = 'SIRICWEB/Maestros/RegistroZonas.html'
	form_class = DatosZonaForm
	success_url = '/SIRICWEB/listarZonas'

class ModificarZonas(UpdateView):
	model = Zonas
	template_name = 'SIRICWEB/Maestros/ModificarZonas.html'
	form_class = DatosZonaForm
	success_url = '/SIRICWEB/listarZonas'

class EliminarZonas(DeleteView):
	model = Zonas
	template_name = 'SIRICWEB/Maestros/EliminarZonas.html'
	form_class = DatosZonaForm
	success_url = '/SIRICWEB/listarZonas'

	def post(self, request, *args, **kwargs):
			self.object = self.get_object
			id_tipo = kwargs['pk']
			eliminar = self.model.objects.get(codigo_zona=id_tipo)
			if request.method == 'POST':
				try:
					eliminar.delete()
					return HttpResponseRedirect(self.get_success_url())
				except IntegrityError:
					messages.error(request, 'No se puede eliminar, por que existen registros asociados a este')
			return render(request, 'SIRICWEB/Maestros/EliminarZonas.html', {'eliminar': eliminar })

class InpectorList(ListView):
	model = User
	template_name = 'SIRICWEB/Maestros/listarInspector.html'

def InspectorZonaList(request, id_usuario):
	inspector_Zona = InspectorZona.objects.filter(id_usuario= id_usuario)
	return render(request, 'SIRICWEB/Maestros/listarInspectorZona.html', {'inspector_Zona':inspector_Zona, 'id_inspector':id_usuario})

def RegistroInspectorZona(request, id_usuario):
	instanceNombre = User.objects.values('first_name').filter(id = id_usuario)[0]
	instanceApellido = User.objects.values('last_name').filter(id = id_usuario)[0]
	inspector = instanceNombre['first_name'] +' '+instanceApellido['last_name']
	if request.method == 'POST':
		form = DatosInspectorZonaForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/SIRICWEB/listarInspectorZona/'+ id_usuario)
		else:
			messages.error(request,'Registro ya existe')
	else:
		form = DatosInspectorZonaForm()
	return render(request, 'SIRICWEB/Maestros/RegistroInspectorZonas.html', {'form': form, 'id_inspector': id_usuario , 'inspector':inspector})

def RegistroPredioZona(request, codigo_predio):
	prediozona = PredioZona.objects.filter(codigo_predio= codigo_predio)
	if request.method == 'POST':
		form = DatosPredioZonaForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/SIRICWEB/registroPredioZona/'+ codigo_predio)
		else:
			messages.error(request,'Registro ya existe')
	else:
		form = DatosPredioZonaForm(initial={'codigo_predio': codigo_predio})
	return render(request, 'SIRICWEB/Predios/RegistrorPredioZona.html', {'form': form, 'prediozona':prediozona ,'cod': codigo_predio})

def ReporteDiarioDotacion(request):
	if request.method == 'POST':
		form = ReporteDiarioForm(request.POST)
		fechaini = request.POST.get('fecha_inicio')
		fechafin = request.POST.get('fecha_final')
		rutaRerpote = "http://13.59.205.159:8080/jasperserver/flow.html?_flowId=viewReportFlow&reportUnit=/reports/siricweb/ReporteRiegoDiario&decorate=no&j_acegi_security_check?decorate=no&j_username=consulta&j_password=consulta&output=pdf" + "&fechaini="+ fechaini + "&fechafin="+ fechafin 
		return render(request, 'SIRICWEB/Reportes/ReporteDiarioDotacion.html', {'form': form,'url': rutaRerpote })
	else:
		form = ReporteDiarioForm()
	return render(request, 'SIRICWEB/Reportes/ReporteDiarioDotacion.html', {'form': form})