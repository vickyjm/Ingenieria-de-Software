# -*- coding: utf-8 -*-

from django.core.validators import RegexValidator
from django.db import models
from django.forms import ModelForm


class Estacionamiento(models.Model):
	# propietario=models.ForeignKey(Propietario)
	Propietario = models.CharField(max_length = 50, help_text = "Nombre Propio")
	Nombre = models.CharField(max_length = 50)
	Direccion = models.TextField(max_length = 120)

	Telefono_1 = models.CharField(blank = True, null = True, max_length = 30)
	Telefono_2 = models.CharField(blank = True, null = True, max_length = 30)
	Telefono_3 = models.CharField(blank = True, null = True, max_length = 30)

	Email_1 = models.EmailField(blank = True, null = True)
	Email_2 = models.EmailField(blank = True, null = True)

	Rif = models.CharField(max_length = 12)

	Tarifa = models.DecimalField(max_digits = 9, decimal_places = 2)
	opciones_esquema = (("Por hora", " Por hora"), ("Por minuto"," Por minuto"), (("Por hora Y fraccion"), ("Hora y fracción")), ("Diferenciado por hora","Diferenciado por hora"))
	Esquema = models.CharField(max_length = 20, choices = opciones_esquema)
	Apertura = models.TimeField(blank = True, null = True)
	Cierre = models.TimeField(blank = True, null = True)
	Reservas_Inicio = models.TimeField(blank = True,null = True)
	Reservas_Cierre = models.TimeField(blank = True, null = True)
	NroPuesto = models.IntegerField(blank = True, null = True)
	Pico_Ini = models.TimeField(blank = True,null = True)
	Pico_Fin = models.TimeField(blank = True, null = True)
	TarifaPico = models.DecimalField(max_digits = 9, decimal_places = 2)


# class ExtendedModel(models.Model):
# 	Estacionamiento = models.ForeignKey(Estacionamiento, primary_key = True)

# class EstacionamientoModelForm(EstacionamientoForm):
# 	class Meta:
# 		model = EstacionamientoModel
# 		fields = ['propietario', 'nombre', 'direccion', 'telefono_1', 'telefono_2', 'telefono_3', 'email_1',
# 				'email_2', 'rif', 'tarifa', 'horarioin', 'horariout', 'horario_resein', 'horario_reserout']

# class Propietario(models.Model):
	# nombre = models.CharField(max_length = 50, help_text = "Nombre Propio")

# class EstadoEstacionamiento(models.Model):
	#

# class PuestosModel(models.Model):
# 	estacionamiento = models.ForeignKey(ExtendedModel)

class ReservasModel(models.Model):
	Estacionamiento = models.ForeignKey(Estacionamiento)
	Puesto = models.IntegerField()
	InicioReserva = models.DateTimeField()
	FinalReserva = models.DateTimeField()
