#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import telepot
import os

equipos = ["alaves","athletic","atletico","barcelona","betis","celta","deportivo","espanyol","eibar","granada","laspalmas","leganes","malaga","osasuna",
"realmadrid","realsociedad","sevilla","sporting","valencia","villarreal"]

idAdmin = #rellenar con tu id de telegram

def handle(msg):
	userExist = 0
	chat_id = msg['from']['id']
	command = msg['text']
	user = str(chat_id)+'\n'
	print chat_id
	print('Mensaje: %s'%command)
	command = command.lower()
	
	if command == '/start': #guardamos el nuevo id para llevar un seguimiento de la cantidad de usuarios que utilizan el bot
                f= open('/home/pi/telegram/id.txt','a')
                f.write(user)
                f.close()
                print 'nuevo usuario guardado: '+user
                bot.sendMessage(chat_id,'Bienvenido a este chat. INFO: http://haudahau.com/vadedos/?p=1189')
	elif '/contacto' in command :
                bot.sendMessage(chat_id,'Mensaje enviado con exito:\n'+command)
                bot.sendMessage(idAdmin,str(chat_id)+'\n'+command)
	elif command == '/ping':
		bot.sendMessage(chat_id, 'pong')
	elif command == '/clasificacion':
		cadena=enviarFichero('clasificacion')
		bot.sendMessage(chat_id,cadena)
	elif command=='/resultados':
		cadena=enviarFichero('jornadapasada')
		bot.sendMessage(chat_id,cadena)
	elif command=='/jornada':
		cadena = enviarFichero('estajornada')
		bot.sendMessage(chat_id,cadena)	
	elif command[0:11] == "/alineacion":
		flag = 0
		for equipo in equipos:
			if equipo in command:
				flag = 1
				cadena=enviarFichero('alineacion'+equipo)
               			cadena = cadena.replace("\n\n","\n")
				bot.sendMessage(chat_id,cadena)
				p = open('/home/pi/telegram/alineacion'+equipo+'.png','rb')
				bot.sendPhoto(chat_id,p)
				p.close()
		if flag == 0:
			bot.sendMessage(chat_id,'No has seleccionado ningún equipo.\nPara visualizar la alineación probable de un equipo introduce "/alineacion equipo"\nPor ejemplo:\n/alineacion athletic\nPuedes introducir varios equipos en el mismo comando.\n/alineacion malaga realmadrid')
	elif command[0:7] == "/puntos":
		flag = 0
		for equipo in equipos:
                        if equipo in command:
				flag = 1
        			cadena = enviarFichero('puntos'+equipo)
        			if equipo in cadena:
					bot.sendMessage(chat_id,cadena)
				else:
					bot.sendMessage(chat_id,equipo+': '+cadena)
		if flag == 0:
			bot.sendMessage(chat_id,'No has seleccionado ningun equipo.\nPara visualizar los puntos de un equipo introduce "/puntos equipo1 ..."\nPor ejemplo, si quieres visualizar los puntos del Betis y del Leganes debes escribir:\n/puntos betis leganes')
	elif command == "/onceideal" or command == "/11ideal":
		cadena = enviarFichero('onceideal')
        	bot.sendMessage(chat_id,cadena)
	elif command == "/ayuda":
		bot.sendMessage(chat_id,'Toda la información sobre el bot aquí: http://wp.me/p4yM52-jb')
	else:
		bot.sendMessage(chat_id,'Ese comando no es valido, prueba otra vez o escribe /ayuda')

def enviarFichero(fichero):
	tmp = ''
	try:
		f=open('/home/pi/telegram/'+fichero+'.txt','r')
		for x in f.readlines():	
               		tmp = tmp+x
		f.close()
		return tmp
	except:
		return "Aún no están disponibles estos datos"


bot = telepot.Bot('SECRET_TOKEN') #En SECRET_TOKEN introduce el que te corresponda
bot.notifyOnMessage(handle)

while 1:
	time.sleep(10)
