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

#lista de equipos liga santander temporada 16/17
equipos = ['alaves','athletic','atletico','barcelona','betis',
'celta','deportivo','eibar','espanyol','granada',
'laspalmas','leganes','malaga','osasuna','realmadrid',
'realsociedad','sevilla','sporting','valencia','villarreal']

#empezamos borrando los ficheros
for x in equipos:
	try:
		os.remove('/home/pi/telegram/puntos'+x+'JP.txt')
		print('borrados '+x+v+'.txt')
	except:
                print('puntos'+x+'JP.txt no existe')

lista = []
index = 0 #aqui llevamos la cuenta
linea = '' #valor en el que almacenaremos la informacion temporal de cada linea comun a todos los ficheros
ordenequipos = [] #array donde almacenamos los equipos que ya han disputado la jornada
n=1

#página web a la que vamos a hacer web scrapping
urlweb = 'http://www.jornadaperfecta.com/puntos'
soup = BeautifulSoup(urllib2.urlopen(urlweb).read(),"html.parser")

#Cogemos el orden de los nombres de los equipos y creamos los ficheros
for valor in soup.select('div[class="hide-on-pc"]'):
	v = ''.join(valor.getText().encode('utf-8').replace('é','e').replace('á','a').replace(' ','').replace('Barça','barcelona').lower().replace('puntosde','').split())
	print v
        ordenequipos.append(v)
	print 'creando fichero puntos'+v+'JP.txt'
	f = open('/home/pi/telegram/puntos'+v+'JP.txt','w')
	f.write(v+'\n')
	f.close() 
porteros = 'Guillermo Ochoa Javi Varas Rulli Sirigu Cuéllar Pacheco Sergio Rico Sergio Asenjo Diego Alves Yoel Moyà Herrerín Ter Stegen Iraizoz Kameni Diego López Keylor Navas Adán Sergio Álvarez Tyton Andrés Fernández Oblak Germán Lux Kepa Arrizabalaga Raúl Lizoain'
#buscamos los jugadores, posiciones y puntos
for x in soup.select('div[class="puntos-jugador"]'):
	x = x.getText().encode('utf-8').split()
	if porteros.find(x[1])>=0:
		if 'Sergi Diego Javi Sergio Andrés Raúl'.find(x[1])>=0:
			if porteros.find(x[1]+' '+x[2])>=0:
				n+=1
				print 'siguiente fichero - '+x[1]+' '+x[2]
		else:	 
			n+=1
			print 'siguiente fichero - '+x[1]
		#print ordenequipos[n]
	x = ' '.join(x)
	if x == 'Puntuaciones por determinar':
		n+=1
	#print x
	else:
		f = open('/home/pi/telegram/puntos'+ordenequipos[n]+'JP.txt','a')
		print ordenequipos[n]+'\t '+x
		f.write(x+'\n')
		f.close()
#f.close()
print 'puntos actualizados'
