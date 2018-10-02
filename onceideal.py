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

lista = []
index = 0
linea = ''
ordenequipos = []
n=0

urlweb = 'http://www.comuniazo.com/comunio/once-ideal'
soup = BeautifulSoup(urllib2.urlopen(urlweb).read(),"html.parser")

f=open('/home/pi/telegram/onceideal.txt','w')
n = 0
linea = ''
#buscamos los jugadores, posiciones y puntos
for x in soup.find_all('td'):
#        print '-------------------------------------------'
#	print n 
#	print ' (operando-->) '
#	print (n-4)%6
#	print x.getText()
	if n < 4 or n > 72:
		z=0
	elif (n-4)%6 == 0:
#		print x.getText()
		linea = x.getText().encode('utf-8')
	elif (n-4)%6 == 2:
#		print x.getText()
		linea = linea + ' ' + x.getText().encode('utf-8')
	elif (n-4)%6 == 4:
		linea = linea+' '+x.getText().encode('utf-8')+'pts '
	elif (n-4)%6 == 5:
#		print x.getText()
		linea = linea+'\n['+x.getText().encode('utf-8')+'€]\n'
		f.write(linea)
	n=n+1
f.close()
