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

equipos = ['alaves','athletic','atletico','barcelona','betis',
'celta','deportivo','eibar','espanyol','granada',
'laspalmas','leganes','malaga','osasuna','realmadrid',
'realsociedad','sevilla','sporting','valencia','villarreal']

for x in equipos:
	try:
		os.remove('/home/pi/telegram/puntos'+x+'.txt')
	except:
		print('puntos'+x+'.txt no existe')

lista = []
index = 0
linea = ''
ordenequipos = []
n=0

urlweb = 'http://www.comuniazo.com/comunio/puntos'
soup = BeautifulSoup(urllib2.urlopen(urlweb).read(),"html.parser")

#Cogemos el orden de los nombres de los equipos
for valor in soup.find_all('h2'):
	print valor.getText().encode('utf-8').replace('é','e').replace('á','a').replace(' ','').lower()
        ordenequipos.append(valor.getText().encode('utf-8').replace('é','e').replace('á','a').replace(' ','').lower())

#abrimos un fichero tmp para evitar error
f=open('/home/pi/telegram/puntos.txt','w')

#buscamos los jugadores, posiciones y puntos
for valor in soup.find_all('td'):
	print valor.getText()
	if valor.getText() != '':
		if index == 0:
			linea = valor.getText().encode('utf-8')
			index=index+1
			if linea[0] == 'P':
				f.close()
				print "abriendo fichero de "+ordenequipos[n]
				f=open('/home/pi/telegram/puntos'+ordenequipos[n]+'.txt','w')
				f.write(ordenequipos[n]+'\n')
				n=n+1
		elif index == 3:
			#print linea
			f.write(linea+'\n')
			index = 0
		else:
			linea = linea+' '+valor.getText().encode('utf-8')
			index=index+1
f.close()
print 'puntos actualizados'

