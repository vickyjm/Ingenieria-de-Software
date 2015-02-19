# -*- coding: utf-8 -*-

# Archivo con funciones de control para SAGE

from decimal import Decimal
import datetime
from math import floor

# Las Tuplas de cada puesto deben tener los horarios de inicio y de cierre para que
# pueda funcionar [(7:00,7:00), (19:00,19:00)]




# Suponiendo que cada estacionamiento tiene una estructura "matricial" lista de listas
# donde si m es una matriz, m[i,j] las i corresponden a los puestos y las j corresponden a tuplas
# con el horario inicio y fin de las reservas
# [[(horaIn,horaOut),(horaIn,horaOut)],[],....]

# chequeo de horarios de extended


def HorarioEstacionamiento(HoraInicio, HoraFin, ReservaInicio, ReservaFin):

    if HoraInicio >= HoraFin:
        return (False, 'El horario de apertura debe ser menor al horario de cierre')
    if ReservaInicio >= ReservaFin:
        return (False, 'El horario de inicio de reserva debe ser menor al horario de cierre')
    if ReservaInicio < HoraInicio:
        return (False, 'El horario de inicio de reserva debe mayor o igual al horario de apertura del estacionamiento')
    if ReservaInicio > HoraFin:
        return (False, 'El horario de comienzo de reserva debe ser menor al horario de cierre del estacionamiento')
    if ReservaFin < HoraInicio:
        return (False, 'El horario de apertura de estacionamiento debe ser menor al horario de finalizacion de reservas')
    if ReservaFin > HoraFin:
        return (False, 'El horario de cierre de estacionamiento debe ser mayor o igual al horario de finalizacion de reservas')
    return (True, '')

def marzullo(tabla,puestos):
    best = 0
    cnt = 0
    listaOut = []
    beststart = 0
    bestend = 0
    for i in range(len(tabla)-1) :
        if (tabla[i][1] == -1) :  
            cnt = cnt+1
        else :
            cnt = cnt-1
        
        if (cnt > best) :
            best = cnt
            beststart=tabla[i][0]
            bestend = tabla[i+1][0]
        elif (best == cnt) and (best == puestos) :
            if (listaOut.count([tabla[i][0],tabla[i+1][0]]) == 0) and (tabla[i][0] != tabla[i+1][0]) :
                listaOut.append([tabla[i][0],tabla[i+1][0]])
        
    listaOut.append([beststart,bestend])
    listaOut.append([best,0])
    return listaOut

def reservar(horaIni,horaFin,tabla,puestos) :

    # Verificacion de entrada
    if ((horaIni.date == horaFin.date) and (horaFin.hour-horaIni.hour <= 0)):
        return False

    reservaOrdenada = tabla

    reservaOrdenada.sort()
    reservaOrdenada.sort(key=lambda k: (k[0],-k[1]))
    
    listaIntervalo = marzullo(reservaOrdenada,puestos) # Devuelve la lista de todos los intervalos maximos
    best = listaIntervalo[len(listaIntervalo)-1][0] # Aqui esta el best 
        
    if (best == puestos):
        i = 0
        while (i<len(listaIntervalo)-1):
            if (((listaIntervalo[i][0] <= horaIni < listaIntervalo[i][1]) or (listaIntervalo[i][0] <  horaFin <= listaIntervalo[i][1])) or ((horaIni < listaIntervalo[i][0]) and (horaFin > listaIntervalo[i][1]))):
                return False
            i = i + 1
    tabla.append([horaIni,-1]) # Se agregan las horas aceptadas a la lista de las reservas
    tabla.append([horaFin,1])
    return True
    
def calculoTarifaHora(iniR,finR,tarifa):
    
    assert(finR > iniR)
    assert(tarifa > 0)
    assert(finR >= iniR + datetime.timedelta(hours = 1))
    assert(finR <= iniR + datetime.timedelta(days = 7))
    
    temp1=(finR-iniR).days*24 + (finR - iniR).seconds//3600
    temp2=(finR-iniR).days*24 + (finR - iniR).seconds/3600
    
    if temp1<temp2:
        temp1+=1
        
    return tarifa*temp1

def calculoTarifaMinuto (iniR, finR, tarifa):
    
    assert(finR > iniR)
    assert(tarifa > 0)
    assert(finR >= iniR + datetime.timedelta(hours = 1))
    assert(finR <= iniR + datetime.timedelta(days = 7))
    
    temp1 = (finR-iniR).days*24 + (finR - iniR).seconds//3600
    temp2 = (finR-iniR).days*24 + (finR - iniR).seconds/3600
    minextra = temp2 - temp1
    fraccion = tarifa*minextra
    
    return round(tarifa * temp1 + fraccion,2) 

def validarHorarioReserva(ReservaInicio, ReservaFin, HorarioApertura, HorarioCierre,fechaActual):
    hIni = datetime.time(ReservaInicio.hour,ReservaInicio.minute)
    hFin = datetime.time(ReservaFin.hour,ReservaFin.minute)
    inicioBorde = datetime.time(0,0)
    finBorde = datetime.time(23,59)
    delta = ReservaFin - ReservaInicio
    deltaActual = ReservaInicio - fechaActual
    
    if (delta.days == 0) and (delta.seconds < 3600) :
        return (False, 'El tiempo de reserva debe ser al menos de 1 hora')
    else:
        if (ReservaInicio >= ReservaFin):
            return (False, 'El horario de inicio de reserva debe ser menor que le horario de fin de reserva')
    if hFin > HorarioCierre:
        return (False, 'El horario de inicio de reserva debe estar en un horario valido')
    if hIni < HorarioApertura:
        return (False, 'El horario de cierre de reserva debe estar en un horario valido')
    if ((delta.days == 7) and (delta.seconds > 0)) or (delta.days > 7):
        return (False, 'El tiempo de reserva no puede ser mayor a 7 días')
    elif (delta.days > 0) and ((HorarioApertura != inicioBorde) or (HorarioCierre != finBorde)): # Mayor a un dia y no 24h
        return (False, 'Este estacionamiento no trabaja 24 horas')
    elif (delta.days==7) and (ReservaInicio > fechaActual):
        return (False, 'La reserva debe estar en un intervalo dentro de los próximos 7 días')
    elif (delta.days > 7):
        return (False, 'La reserva no puede ser mayor a 7 días')
    if (deltaActual.days < 0):
        return (False, 'La fecha ingresada para su reserva ya pasó')
    elif (deltaActual.days > 7) or ((deltaActual.days == 7) and (deltaActual.seconds > 0)):
        return (False, 'La reserva puede ser máximo hasta dentro de 7 días')            
    return (True, '')

