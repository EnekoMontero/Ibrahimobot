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

url = ''
urlweb = ''
ruta = ''
equipos = ["alaves","athletic","atletico","barcelona","betis","celta","deportivo","espanyol","eibar","getafe","girona","laspalmas","leganes","levante","malaga",
"realmadrid","realsociedad","sevilla","valencia","villarreal"]
for equipo in equipos:
#Se crea la instancia de BS pasando la URL con urllib2.
#Para extraer los comentarios de la pagina
	urlweb = "http://www.infocomunio.es/2017/07/alineacion-probable-"+equipo+".html"
	if equipo == "realsociedad":
		urlweb = "http://www.infocomunio.es/2017/07/alineacion-probable-real-sociedad.html"
	elif equipo == "barcelona":
		urlweb = "http://www.infocomunio.es/2017/07/alineacion-probable-atletico_31.html"
	elif equipo == "laspalmas":
		urlweb = "http://www.infocomunio.es/2017/07/alineacion-probable-las-palmas.html"
	elif equipo == "realmadrid":
		urlweb = "http://www.infocomunio.es/2017/07/alineacion-probable-real-madrid.html"
	soup = BeautifulSoup(urllib2.urlopen(urlweb).read(),"html.parser")
	archivo = '/home/pi/telegram/alineacion'+equipo+'.txt'
	f = open(archivo,'w')
	cadena = "Estos datos se han actualizado en: Fecha y hora: "+time.strftime("%c")+'\n'
	f.write(cadena)
	for valor in soup.find_all('b'):#'div',{ 'style' : "text-align:center;"}):#'b'):
		print valor.getText().encode('utf-8')
		f.write(valor.getText().encode('utf-8')+'\n')
	f.close()
	print "Guardados comentarios de "+equipo
#Para extraer las imagenes de las páginas.
	for link in soup.find_all('a'):
		if link.get('imageanchor'):
			url = link.get('href')
	ruta = '/home/pi/telegram/alineacion'+equipo+'.png'
	urllib.urlretrieve(url, ruta)
	print "imagen "+equipo+" descargada"

print "Fecha y hora " + time.strftime("%c")
