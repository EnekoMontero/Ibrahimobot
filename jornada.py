#!/usr/bin/env python
# -*- coding: utf-8 -*-

#################################################################
# Author: Eneko Montero
# Year: 2016 - 2018
# License: CC-BY-SA 4.0
#################################################################

from bs4 import BeautifulSoup
from urlparse import urlparse
import urllib2
import urllib
import re
import time
import os

index = 1

urlweb = 'http://www.comuniazo.com/liga-bbva'
soup = BeautifulSoup(urllib2.urlopen(urlweb).read(),"html.parser")

#Cogemos el orden de los nombres de los equipos
def reemplazar(cadena):
        cadena = cadena.replace("Barcelona"," FCB ")
        cadena = cadena.replace("Atlético"," ATM ")
        cadena = cadena.replace("Real Madrid"," RMA ")
        cadena = cadena.replace("Villarreal"," VIL ")
        cadena = cadena.replace("Sevilla"," SEV ")
        cadena = cadena.replace("Eibar"," EIB ")
        cadena = cadena.replace("Athletic"," ATH ")
        cadena = cadena.replace("Celta"," CEL ")
        #cadena = cadena.replace("Deportivo"," DEP ")
        #cadena = cadena.replace("Málaga"," MAL ")
        cadena = cadena.replace("Real Sociedad"," RSO ")
        cadena = cadena.replace("Valencia"," VAL ")
        cadena = cadena.replace("Leganés"," LEG ")
        cadena = cadena.replace("Betis"," BET ")
        cadena = cadena.replace("Alavés"," ALA ")
        #cadena = cadena.replace("Sporting"," SPO ")
        cadena = cadena.replace("Espanyol"," ESP ")
        #cadena = cadena.replace("Las Palmas"," PAL ")
        #cadena = cadena.replace("Osasuna"," OSA ")
        #cadena = cadena.replace("Granada"," GRA ")
	cadena = cadena.replace("Girona"," GIR ")
	cadena = cadena.replace("Levante"," LEV ")
	cadena = cadena.replace("Getafe"," GET ")
	cadena = cadena.replace("En juego", "Min")
        cadena = cadena.replace("Huesca", " HUE ")
	cadena = cadena.replace("Valladolid", " VAD ")
	cadena = cadena.replace("Rayo Vallecano", " RAY ")	
	return cadena

#abrimos un fichero tmp para evitar error
#f=open('/home/pi/telegram/puntos.txt','w')
f1 = open('/home/pi/telegram/estajornada.txt','w')
f2 = open('/home/pi/telegram/jornadapasada.txt','w')
f3 = open('/home/pi/telegram/clasificacion.txt','w')

for valor in soup.find_all('h2'):
	if index == 1:
		f3.write(valor.getText().encode('utf-8')+'\n')
	if index == 2:
		f2.write(valor.getText().encode('utf-8')+'\n')
	if index == 3:
		f1.write(valor.getText().encode('utf-8')+'\n')
	index = index+1

#buscamos los jugadores, posiciones y puntos
index = 1
tmpalto=10
tmpbajo=10
tmpclas=1
for valor in soup.find_all('tr'):
	if index > 1 and index < 22:
		cadena = valor.getText().encode('utf-8')
		cadena = reemplazar(cadena)
		if tmpclas < 20: #este limitante para los equipos que tengan menos de 10 puntos si abajo hay un 7
			cadena =  cadena[:(cadena.find(' ')+7)]# cambiar por 6 cambiar por 7 cuando el primer equipo 10 puntos o mas
			tmpbajo = int(cadena[len(cadena)-2])#cambiar por 1 cambiar por 2 cuando el primer equipo 10 puntos o mas
		else:
			cadena = cadena[:(cadena.find(' ')+6)]
			tmpbajo = int(cadena[len(cadena)-1])
		#print cadena
		#print ' tmpb = '+str(tmpbajo)+'     tmpa = '+str(tmpalto)
		if tmpbajo > tmpalto:
			#print 'trunco  cadena'
			cadena = cadena[:len(cadena)-1]
		else:
			#print 'actualizo valor'
			tmpalto = tmpbajo
		print cadena
		tmpclas = tmpclas+1
		f3.write(cadena+'\n')
	if index > 21 and index < 32:
                cadena = valor.getText().encode('utf-8')
                cadena = reemplazar(cadena)
		print cadena
                f2.write(cadena+'\n')
	if index > 31 and index < 42:
		cadena = valor.getText().encode('utf-8')
        	cadena = reemplazar(cadena)
		print cadena
		f1.write(cadena+'\n')
	index=index+1
f1.close()
f2.close()
f3.close()
