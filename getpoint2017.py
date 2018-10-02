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
'celta','deportivo','eibar','espanyol','getafe','girona',
'laspalmas','leganes','levante','malaga','realmadrid',
'realsociedad','sevilla','valencia','villarreal']

#juegos fantasy que soporta este script
fantasy = ['C','AS','FMPR','FME','FMM','FMPI'] 

#empezamos borrando los ficheros
for x in equipos:
	for v in fantasy:
		try:
			os.remove('/home/pi/telegram/puntos'+x+v+'.txt')
			print('borrados '+x+v+'.txt')
		except:
			print('puntos'+x+v+'.txt no existe')

lista = []
index = 0 #aqui llevamos la cuenta
linea = '' #valor en el que almacenaremos la informacion temporal de cada linea comun a todos los ficheros
ordenequipos = [] #array donde almacenamos los equipos que ya han disputado la jornada
n=-1

#página web a la que vamos a hacer web scrapping
urlweb = 'http://www.comuniazo.com/comunio/puntos'
soup = BeautifulSoup(urllib2.urlopen(urlweb).read(),"html.parser")

#Cogemos el orden de los nombres de los equipos y creamos los ficheros
for valor in soup.find_all('h2'):
	v = valor.getText().encode('utf-8').replace('é','e').replace('á','a').replace(' ','').lower()
	print v
        ordenequipos.append(v)
	for x in fantasy:
		print 'creando fichero puntos'+v+x+'.txt'
		f = open('/home/pi/telegram/puntos'+v+x+'.txt','w')
		f.write(v+'\n')
		f.close() 
porteros = 'Andrés Prieto Francis Uzoho Bono Pantilimon Pacheco Sivera Ioritz Landeta Kepa Arrizabalaga Herrerín Unai Simón Moyá Oblak Axel Werner Ter Stegen Cillessen Ortolá Dani Giménez Adán Manu Herrera Sergio Álvarez Rubén Blanco Iván Villar Tyton Rubén Yoel Riesgo Dmitrovic Pau López Diego López Damián Martínez Guaita Filip Manojlovic José Aurelio Suárez Iraizoz Bounou Lizoain Leandro Chichizola Pichu Cuéllar Serante Nereo Champagne Raúl Fernández Oier Roberto Jiménez Gönen Andrés Fernández Prieto Albert Rulli Ramírez Keylor Navas Kiko Casilla Rubén Martínez Yáñez David Soria Juan Soriano Jaume Neto Asenjo Andrés Barbosa Sergio Rico'
#buscamos los jugadores, posiciones y puntos
#for valor in soup.find_all(['td','h2']):
for valor in soup.find_all('td'):
	valor = valor.getText().encode('utf-8')
	#print valor
	#grupos de 8 datos: 0. Posicion 1. Nombre 2. P Comunio 3. AS 4. P FM Prensa 5. P FM estadísticas 6. P FM mixto 7. P FM picas
	if valor != '':
		if index%7 == 0:
			linea = valor 
			if porteros.find(linea)>=0:
				n += 1
				print linea
		else:
			#print fantasy[index%7-2]+ordenequipos[n]
			f = open('/home/pi/telegram/puntos'+ordenequipos[n]+fantasy[index%7-1]+'.txt','a')
			#print linea+' '+valor+'\n'
			f.write(linea+' '+valor+'\n')
			f.close()
		#print 'index = '+str(index)
		index+=1
f.close()
print 'puntos actualizados'
#
