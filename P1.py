# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 11:04:16 2015

@author: paco
"""

#PTC
#Francisco González López
#7665662P

import numpy

import matplotlib.dates as md
import matplotlib


#Parte 2: Funciones de utilidad

def bytesToString(entrada):
    return entrada.decode('UTF-8')
    
def convertir_fecha_a_ordinal(fecha):
	"Devuelve el ordinal asociado con la fecha (en bytes, como lo da loadtxt), contando desde el 1 enero de 2015"
	return (md.datestr2num(bytesToString(fecha))-md.datestr2num("2015-1-1"))

eventos = ['Niebla','Lluvia','Tormenta']
dic_eventos = {'Niebla':0,'Lluvia':1,'Tormenta':2}
dic_codigos = {v: k for k, v in dic_eventos.items()}

def convertir_evento_a_entero(nombre_evento):
    "Convierte un evento a entero- 1 niebla|2 lluvia|3 tormenta"
    event_code=[]
    if(type(nombre_evento) == numpy.bytes_):
        nombre_evento=nombre_evento.decode()
    
    string = nombre_evento.split('-')
    
    for evento in string:
        if(evento != ''):
            event_code.append(dic_eventos[evento])
    
    return event_code

    #Si encontramos el evento...
    #Como dice a entero, en lugar de lista, vamos a pasar un número codificándolo
    if(nombre_evento.find("Niebla") != -1):
        event_code=event_code*10 + 1
    if(nombre_evento.find("Lluvia") != -1):
        event_code=event_code*10 + 2
    if(nombre_evento.find("Tormenta") != -1):
        event_code=event_code*10 + 3
        
    return event_code
    
def coeficiente_determinacion(valores_actuales, valores_ideales):
    "Devuelve el coef. de determinación"
    media_actual=numpy.mean(valores_actuales)

    dev_actual=0
    dev_ideal=0

    for i in range(valores_actuales.shape[0]):
        dev_ideal+=(valores_ideales[i]-media_actual)*(valores_ideales[i]-media_actual)
        dev_actual+=(valores_actuales[i]-media_actual)*(valores_actuales[i]-media_actual)

    return dev_ideal/dev_actual
 
 
 #Parte 1: Función de lectura
def leerTemperaturas(nombre_fichero):
    "Lee las temperaturas del fichero indicado"
    data=numpy.loadtxt(fname=nombre_fichero, dtype={'names': ('day','tMax','tAvg','tMin','event'), 'formats': ('f4','f4','f4','f4','S48')}, converters={0 : convertir_fecha_a_ordinal}, delimiter=',', skiprows=1, usecols=(0,1,2,3,21))
    return data
    
    
filepath="historico-temperaturas-granada-oct-2015.txt"
leidos=leerTemperaturas(filepath)


#Parte 3: Gráfica de puntos con las t. medias
def grafica_temperatura_media_dia(fechas, temperaturas_medias):
    "Dibuja la gŕafica de temperaturas medias de cada día"
    matplotlib.pyplot.figure(0)
    matplotlib.pyplot.xlabel('Dia del año')
    matplotlib.pyplot.ylabel('Media Temperatura (C)')
    matplotlib.pyplot.title('Temperaturas en Granada Octubre 2015')
    matplotlib.pyplot.legend(loc='best')
    matplotlib.pyplot.plot(fechas,temperaturas_medias,"bo",fechas,temperaturas_medias,"k")
    matplotlib.pyplot.show()
    return

grafica_temperatura_media_dia(leidos['day'],leidos['tAvg'])

#Parte 4: Gráfica de puntos con las t. medias con regresión lineal

#Funciones de utilidad
def ajustar_recta(val_x, val_y, grado):
    "Ajustamos con pol. grado 1"
    return numpy.polyfit(val_x,val_y,deg=1)
    
def f_tendencia_lineal(pendiente, ord_origen,x_eval):
    "Nos devuelve el resultado de evaluar para x=x_eval la función f(x)=pendiente*x+ord_origen"
    return pendiente*x_eval+ord_origen
    
def calcular_valores_ideales(pendiente, ord_origen, valores_x):
    "Calculamos los valores ideales ajustados para los valores de x en la recta"
    n_items=valores_x.shape[0]
    ideales=numpy.zeros(n_items)
    for i in range(n_items):
        ideales[i]=f_tendencia_lineal(pendiente, ord_origen, valores_x[i])
        
    return ideales
        
#Dibujado de la gráfica con el aj. lineal
def grafica_temperatura_media_dia_tendencia (fechas, temperaturas_medias):
    "Dibujamos la gráfica de temperaturas medias con la línea de tendencia"
    #Ajustamos un modelo lineal a los datos
    fit=ajustar_recta(fechas,temperaturas_medias,1)
    
    r_cuadrado=coeficiente_determinacion(temperaturas_medias,calcular_valores_ideales(fit[0],fit[1],fechas))
    
    matplotlib.pyplot.figure(0)
    matplotlib.pyplot.xlabel('Dia del año')
    matplotlib.pyplot.ylabel('Media Temperatura (C)')
    matplotlib.pyplot.title('Temperaturas en Granada Octubre 2015')
    matplotlib.pyplot.legend(loc='best')
    matplotlib.pyplot.text(297.5,19.5,r'$R^2 = $'+str('%.2f' % r_cuadrado) )

    
    #Dibujamos los puntos y las líneas
    matplotlib.pyplot.plot(fechas,temperaturas_medias,"bo")
    matplotlib.pyplot.plot(fechas,temperaturas_medias,"k")
    #Dibujamos el ajuste lineal con linea discontinua
    matplotlib.pyplot.plot(fechas, f_tendencia_lineal(fit[0],fit[1],fechas),'r--',label=("Ajuste lineal (" + str('%.2f' % fit[0]) +")"))
        
    matplotlib.pyplot.legend()
    matplotlib.pyplot.show()
    return

grafica_temperatura_media_dia_tendencia(leidos['day'],leidos['tAvg'])

#Parte 5: Gráfica de puntos con las t. medias con ajuste lineal y barras de max/min
def grafica_temperatura_media_dia_tendencia_barras (fechas, temperaturas_medias, temperaturas_minimas, temperaturas_maximas):
    "Dibuja el gráfico de barras de la temperatura, incluyendo el ajuste"
    #Ajustamos un modelo lineal a los datos
    fit=ajustar_recta(fechas,temperaturas_medias,1)
    #Cuidado de no hacer valores negativos
    diferencias_minimas=numpy.absolute(temperaturas_minimas-temperaturas_medias)
    diferencias_maximas=numpy.absolute(temperaturas_maximas-temperaturas_medias)
    diferencias=numpy.vstack((diferencias_minimas,diferencias_maximas))
    
    r_cuadrado=coeficiente_determinacion(temperaturas_medias,calcular_valores_ideales(fit[0],fit[1],fechas))
    
    matplotlib.pyplot.figure(0)
    matplotlib.pyplot.xlabel('Dia del año')
    matplotlib.pyplot.ylabel('Media Temperatura (C)')
    matplotlib.pyplot.title('Temperaturas en Granada Octubre 2015 (max/min)')
    matplotlib.pyplot.legend(loc='best')
    matplotlib.pyplot.text(271,2,r'$R^2 = $'+str('%.6f' % r_cuadrado) )

    #Dibujamos los puntos y las líneas
    matplotlib.pyplot.plot(fechas,temperaturas_medias,"bo")
    matplotlib.pyplot.plot(fechas,temperaturas_medias,"k")
    #Dibujamos el ajuste lineal con linea discontinua
    matplotlib.pyplot.plot(fechas, f_tendencia_lineal(fit[0],fit[1],fechas),'r--',label=("Ajuste lineal (" + str('%.2f' % fit[0]) +")"))
    #Dibujamos las barras de máximo/mínimo
    matplotlib.pyplot.errorbar(fechas,temperaturas_medias,yerr=diferencias,fmt='--o')
    
    matplotlib.pyplot.legend()
    matplotlib.pyplot.show()
    return
    
grafica_temperatura_media_dia_tendencia_barras(leidos['day'],leidos['tAvg'],leidos['tMin'],leidos['tMax'])


#Parte 6: Histograma de eventos

#Primero, calculamos las frecuencias semanales de cada evento
def contar_eventos_semanas(eventos_diarios):
    "Contamos los eventos por semanas del vector de eventos que nos llegue"
    import math
    semana=1

    lista_eventos=[[],[],[]]
    
    for i in range(eventos_diarios.shape[0]):
        event_code=convertir_evento_a_entero(eventos_diarios[i])
        
        for event in event_code:
            if(event != ''):
                lista_eventos[event].append(semana)
            
        if i%7 == 0 and i > 0:
            semana+=1

            
    return lista_eventos
        

def histograma_eventos(fechas, eventos):
    
    eventos_semana=contar_eventos_semanas(eventos)
    
    n_semanas = eventos.shape[0]/7
    n_semanas = math.ceil(n_semanas)
    
    x_values=[]
    for i in range(n_semanas+1):
        x_values.append(i+1)
        
    # Lista de 1 a 6
    bins=x_values
    

    matplotlib.pyplot.hist(eventos_semana,bins=bins,histtype='bar',color=['red','blue','green'],label=['Niebla','Lluvia','Tormenta'])
    
    matplotlib.pyplot.xticks(x_values)
    matplotlib.pyplot.xlabel('Semana')
    matplotlib.pyplot.ylabel('#Eventos')
    matplotlib.pyplot.title('Eventos Meteorológicos en Granada Octubre 2015')
    matplotlib.pyplot.legend()
    
    matplotlib.pyplot.show()
    
    return

histograma_eventos(leidos['day'],leidos['event'])
