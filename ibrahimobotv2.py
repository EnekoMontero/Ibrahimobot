#!/usr/bin/env python
# -*- coding: utf-8 -*-

#################################################################
# Author: Eneko Montero
# Year: 2016 - 2018
# License: CC-BY-SA 4.0
#################################################################

import time
import telepot
import os
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent

equipos = ["alaves","athletic","atletico","barcelona","betis","celta","deportivo","espanyol","eibar","getafe","girona","laspalmas","leganes","levante","malaga",
"realmadrid","realsociedad","sevilla","valencia","villarreal"]

idAdmin = #rellenar con tu id de telegram

def on_chat_message(msg):
	userExist = 0
	chat_id = msg['from']['id']
	command = msg['text']
	user = str(chat_id)+'\n'
	logs = open('/home/pi/telegram/logs.txt','a')
	logs.write(str(chat_id).encode('utf-8')+' - '+command.encode('utf-8')+'\n')
	logs.close()
	print chat_id
	print('Mensaje: %s'%command)

	if command[0] in '0123456789' and chat_id == idAdmin:
		cadena = command.split('%')
		bot.sendMessage(cadena[0],cadena[1])
	elif command[0]!='/' and chat_id == idAdmin:
		f=open('/home/pi/telegram/id.txt','r')
		print 'enviando mensaje a:'
		for x in f.readlines():
			print(x)
			try:
				bot.sendMessage(x,command)
			except:
				bot.sendMessage(idAdmin, x+'-> ERROR. Eliminar de la lista')
			else:
				bot.sendMessage(idAdmin, x+'-> Mensaje enviado con exito')
				f.close()

	command = command.lower()
	if command == '/start':
		f = open('/home/pi/telegram/id.txt','a')
		f.write(user)
		f.close()
		print 'nuevo usuario guardado: '+user
		bot.sendMessage(chat_id,'Bienvenido a este chat. INFO: http://haudahau.com/vadedos/?p=1189')
		bot.sendMessage(chat_id, 'Escoge una opción', reply_markup=
		ReplyKeyboardMarkup(keyboard=[
		[KeyboardButton(text='/ping'), KeyboardButton(text='/ayuda')],
		[KeyboardButton(text='/clasificacion'),KeyboardButton(text='/11ideal')],
		[KeyboardButton(text='/resultados'), KeyboardButton(text='/jornada')],
		[KeyboardButton(text='/alineacion'), KeyboardButton(text='/puntos')],
		[KeyboardButton(text='/contacto')],
		]))
	elif command == '/teclado' or command == '/volver':
		bot.sendMessage(chat_id, 'Escoge una opción', reply_markup=
		ReplyKeyboardMarkup(keyboard=[
		[KeyboardButton(text='/ping'), KeyboardButton(text='/ayuda')],
		[KeyboardButton(text='/resultados'), KeyboardButton(text='/jornada')],
		[KeyboardButton(text='/alineacion'), KeyboardButton(text='/puntos')],
		[KeyboardButton(text='/clasificacion'),KeyboardButton(text='/11ideal')],
		[KeyboardButton(text='/contacto')],
		]))
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
			bot.sendMessage(chat_id, 'Escoge una opción', reply_markup=
			ReplyKeyboardMarkup(keyboard=[
			[KeyboardButton(text='/volver')],
			[KeyboardButton(text='/alineacion alaves'), KeyboardButton(text='/alineacion athletic')],
			[KeyboardButton(text='/alineacion atletico'), KeyboardButton(text='/alineacion barcelona')],
			[KeyboardButton(text='/alineacion betis'), KeyboardButton(text='/alineacion celta')],
			[KeyboardButton(text='/alineacion deportivo'), KeyboardButton(text='/alineacion espanyol')],
			[KeyboardButton(text='/alineacion eibar'), KeyboardButton(text='/alineacion getafe')],
			[KeyboardButton(text='/alineacion girona'), KeyboardButton(text='/alineacion laspalmas')],
			[KeyboardButton(text='/alineacion leganes'), KeyboardButton(text='/alineacion levante')],
			[KeyboardButton(text='/alineacion malaga'), KeyboardButton(text='/alineacion realmadrid')],
			[KeyboardButton(text='/alineacion realsociedad'), KeyboardButton(text='/alineacion sevilla')],
			[KeyboardButton(text='/alineacion valencia'), KeyboardButton(text='/alineacion villarreal')],
			]))
	elif command[0:11] == "/puntosfmpi":
		flag = 0
		for equipo in equipos:
			if equipo in command:
				flag = 1
				cadena = enviarFichero('puntos'+equipo+'FMPI')
				if equipo in cadena:
					bot.sendMessage(chat_id,cadena)
				else:
					bot.sendMessage(chat_id,equipo+': '+cadena)
		if flag == 0:
			bot.sendMessage(chat_id,'No has seleccionado ningun equipo.\nPara visualizar los puntos de un equipo introduce "/puntosFMPI equipo1 ..."\nPor ejemplo, si quieres visualizar los puntos del Betis y del Leganes debes escribir:\n/puntosFMPI betis leganes')
	elif command[0:11] == "/puntosfmpr":
		flag = 0
		for equipo in equipos:
			if equipo in command:
				flag = 1
				cadena = enviarFichero('puntos'+equipo+'FMPR')
				if equipo in cadena:
					bot.sendMessage(chat_id,cadena)
				else:
					bot.sendMessage(chat_id,equipo+': '+cadena)
		if flag == 0:
			bot.sendMessage(chat_id,'No has seleccionado ningun equipo.\nPara visualizar los puntos de un equipo introduce "/puntosFMPR equipo1 ..."\nPor ejemplo, si quieres visualizar los puntos del Betis y del Leganes debes escribir:\n/puntosFMPR betis leganes')
	elif command[0:10] == "/puntosfme":
		flag = 0
		for equipo in equipos:
			if equipo in command:
				flag = 1
				cadena = enviarFichero('puntos'+equipo+'FME')
				if equipo in cadena:
					bot.sendMessage(chat_id,cadena)
				else:
					bot.sendMessage(chat_id,equipo+': '+cadena)
		if flag == 0:
			bot.sendMessage(chat_id,'No has seleccionado ningun equipo.\nPara visualizar los puntos de un equipo introduce "/puntosFME equipo1 ..."\nPor ejemplo, si quieres visualizar los puntos del Betis y del Leganes debes escribir:\n/puntosFME betis leganes')
	elif command[0:10] == "/puntosfmm":
		flag = 0
		for equipo in equipos:
			if equipo in command:
				flag = 1
				cadena = enviarFichero('puntos'+equipo+'FMM')
				if equipo in cadena:
					bot.sendMessage(chat_id,cadena)
				else:
					bot.sendMessage(chat_id,equipo+': '+cadena)
		if flag == 0:
			bot.sendMessage(chat_id,'No has seleccionado ningun equipo.\nPara visualizar los puntos de un equipo introduce "/puntosFMM equipo1 ..."\nPor ejemplo, si quieres visualizar los puntos del Betis y del Leganes debes escribir:\n/puntosFMM betis leganes')
	elif command[0:9] == "/puntosas":
		flag = 0
		for equipo in equipos:
			if equipo in command:
				flag = 1
				cadena = enviarFichero('puntos'+equipo+'AS')
				if equipo in cadena:
					bot.sendMessage(chat_id,cadena)
				else:
					bot.sendMessage(chat_id,equipo+': '+cadena)
		if flag == 0:
			bot.sendMessage(chat_id,'No has seleccionado ningun equipo.\nPara visualizar los puntos de un equipo introduce "/puntosFMM equipo1 ..."\nPor ejemplo, si quieres visualizar los puntos del Betis y del Leganes debes escribir:\n/puntosAS betis leganes')
	elif command[0:9] == "/puntosjp":
		flag = 0
		for equipo in equipos:
			if equipo in command:
				flag = 1
				cadena = enviarFichero('puntos'+equipo+'JP')
				if equipo in cadena:
					bot.sendMessage(chat_id,cadena)
				else:
					bot.sendMessage(chat_id,equipo+': '+cadena)
		if flag == 0:
			bot.sendMessage(chat_id,'No has seleccionado ningun equipo.\nPara visualizar los puntos de un equipo introduce "/puntosJP equipo1 .."\nPor ejemplo, si quieres visualizar los puntos del Betis y del Leganes debes escribir:\n/puntosJP betis leganes')
	elif command[0:8] == "/puntosc":
		flag = 0
		for equipo in equipos:
			if equipo in command:
				flag = 1
				cadena = enviarFichero('puntos'+equipo+'C')
				if equipo in cadena:
					bot.sendMessage(chat_id,cadena)
				else:
					bot.sendMessage(chat_id,equipo+': '+cadena)
		if flag == 0:
			bot.sendMessage(chat_id,'No has seleccionado ningun equipo.\nPara visualizar los puntos de un equipo introduce "/puntosJP equipo1 .."\nPor ejemplo, si quieres visualizar los puntos del Betis y del Leganes debes escribir:\n/puntosJP betis leganes')

	elif command[0:7] == "/puntos":
		flag = 0
		for equipo in equipos:
			if equipo in command:
				flag = 1
				cadena = enviarFichero('puntos'+equipo+'C')
				if equipo in cadena:
					bot.sendMessage(chat_id,cadena)
				else:
					bot.sendMessage(chat_id,equipo+': '+cadena)
		if flag == 0:
			global message_with_inline_keyboard
			message_with_inline_keyboard = bot.sendMessage(chat_id, 'Selecciona tu modo de juego', reply_markup=
			InlineKeyboardMarkup(inline_keyboard=[
			[InlineKeyboardButton(text='Comunio', callback_data='c')],
			[InlineKeyboardButton(text='Diario AS', callback_data='as')],
			[InlineKeyboardButton(text='Futmondo Prensa', callback_data='fmpr')],
			[InlineKeyboardButton(text='Futmondo Estadísticas', callback_data='fme')],
			[InlineKeyboardButton(text='Futmondo Mixto', callback_data='fmm')],
			[InlineKeyboardButton(text='Futmondo Picas', callback_data='fmpi')],
			[InlineKeyboardButton(text='Jornada Perfecta', callback_data='jp')],
			#[InlineKeyboardButton(text='Callback - show notification', callback_data='notification')],
			#[dict(text='Callback - show alert', callback_data='alert')],
			#[InlineKeyboardButton(text='Callback - edit message', callback_data='edit')],
			#[dict(text='Switch to using bot inline', switch_inline_query='initial query')],
			]))
			msg_idf = telepot.message_identifier(message_with_inline_keyboard)
	elif command == "/onceideal" or command == "/11ideal":
		cadena = enviarFichero('onceideal')
		bot.sendMessage(chat_id,cadena)
	elif command == "/ayuda":
		bot.sendMessage(chat_id,'Toda la información sobre el bot aquí: http://wp.me/p4yM52-jb \nFormato equipos: alaves, athletic, atletico, barcelona, betis, celta, deportivo, espanyol, eibar, getafe, girona, laspalmas, leganes, levante, malaga, realmadrid, realsociedad, sevilla, valencia, villarreal')
	else:
		bot.sendMessage(idAdmin,str(chat_id)+'\n'+command)

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

			#funcion para reeemplar los nombres de tal forma que entren en el mensaje sin saltar la linea
def reemplazar(cadena):
	cadena = cadena.replace(" ","")
	cadena = cadena.replace("POINTS", "PTS")
	cadena = cadena.replace("FCBarcelona"," FCB ")
	cadena = cadena.replace("ClubAtléticodeMadrid"," ATM ")
	cadena = cadena.replace("RealMadridCF"," RMA ")
	cadena = cadena.replace("VillarrealCF"," VIL ")
	cadena = cadena.replace("SevillaFC"," SEV ")
	cadena = cadena.replace("SDEibar"," EIB ")
	cadena = cadena.replace("AthleticClub"," ATH ")
	cadena = cadena.replace("RCCeltadeVigo"," CEL ")
	cadena = cadena.replace("RCDeportivoLaCoruna"," DEP ")
	cadena = cadena.replace("MálagaCF"," MAL ")
	cadena = cadena.replace("RealSociedaddeFútbol"," RSO ")
	cadena = cadena.replace("ValenciaCF"," VAL ")
	cadena = cadena.replace("GetafeCF"," GET ")
	cadena = cadena.replace("RealBetis"," BET ")
	cadena = cadena.replace("RayoVallecanodeMadrid"," RAY ")
	cadena = cadena.replace("SportingGijón"," SPO ")
	cadena = cadena.replace("RCDEspanyol"," ESP ")
	cadena = cadena.replace("UDLasPalmas"," PAL ")
	cadena = cadena.replace("LevanteUD"," LEV ")
	cadena = cadena.replace("GranadaCF"," GRA ")
	cadena = cadena.replace("vs"," - ")
	cadena = cadena.replace("LLIGA","Resultados")
	cadena = cadena.replace("=","")
	cadena = cadena.replace("\n\n","\n")
	return cadena

def on_callback_query(msg):
	query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
	print('Callback query:', query_id, from_id, data)

	if data == 'c':
		global message_with_inline_keyboard
		if message_with_inline_keyboard:
			msg_idf = telepot.message_identifier(message_with_inline_keyboard)
			bot.editMessageText(msg_idf, 'Modo Comunio escogido')
			bot.sendMessage(from_id, 'Escoge los puntos que quieres ver desde el teclado', reply_markup=
			ReplyKeyboardMarkup(keyboard=[
			[KeyboardButton(text='/volver')],
			[KeyboardButton(text='/puntosc alaves'), KeyboardButton(text='/puntosc athletic')],
			[KeyboardButton(text='/puntosc atletico'), KeyboardButton(text='/puntosc barcelona')],
			[KeyboardButton(text='/puntosc betis'), KeyboardButton(text='/puntosc celta')],
			[KeyboardButton(text='/puntosc deportivo'), KeyboardButton(text='/puntosc espanyol')],
			[KeyboardButton(text='/puntosc eibar'), KeyboardButton(text='/puntosc getafe')],
			[KeyboardButton(text='/puntosc girona'), KeyboardButton(text='/puntosc laspalmas')],
			[KeyboardButton(text='/puntosc leganes'), KeyboardButton(text='/puntosc levante')],
			[KeyboardButton(text='/puntosc malaga'), KeyboardButton(text='/puntosc realmadrid')],
			[KeyboardButton(text='/puntosc realsociedad'), KeyboardButton(text='/puntosc sevilla')],
			[KeyboardButton(text='/puntosc valencia'), KeyboardButton(text='/puntosc villarreal')],
			]))
		else:
			bot.answerCallbackQuery(query_id, text='Algo no ha salido como estaba previsto')
	elif data == 'as':
		global message_with_inline_keyboard
		if message_with_inline_keyboard:
			msg_idf = telepot.message_identifier(message_with_inline_keyboard)
			bot.editMessageText(msg_idf, 'Modo Diario AS escogido')
			bot.sendMessage(from_id, 'Escoge los puntos que quieres ver desde el teclado', reply_markup=
			ReplyKeyboardMarkup(keyboard=[
			[KeyboardButton(text='/volver')],
			[KeyboardButton(text='/puntosas alaves'), KeyboardButton(text='/puntosas athletic')],
			[KeyboardButton(text='/puntosas atletico'), KeyboardButton(text='/puntosas barcelona')],
			[KeyboardButton(text='/puntosas betis'), KeyboardButton(text='/puntosas celta')],
			[KeyboardButton(text='/puntosas deportivo'), KeyboardButton(text='/puntosas espanyol')],
			[KeyboardButton(text='/puntosas eibar'), KeyboardButton(text='/puntosas getafe')],
			[KeyboardButton(text='/puntosas girona'), KeyboardButton(text='/puntosas laspalmas')],
			[KeyboardButton(text='/puntosas leganes'), KeyboardButton(text='/puntosas levante')],
			[KeyboardButton(text='/puntosas malaga'), KeyboardButton(text='/puntosas realmadrid')],
			[KeyboardButton(text='/puntosas realsociedad'), KeyboardButton(text='/puntosas sevilla')],
			[KeyboardButton(text='/puntosas valencia'), KeyboardButton(text='/puntosas villarreal')],
			]))
		else:
			bot.answerCallbackQuery(query_id, text='Algo no ha salido como estaba previsto')
	elif data == 'fmpr':
		global message_with_inline_keyboard
		if message_with_inline_keyboard:
			msg_idf = telepot.message_identifier(message_with_inline_keyboard)
			bot.editMessageText(msg_idf, 'Modo Futmondo Prensa escogido')
			bot.sendMessage(from_id, 'Escoge los puntos que quieres ver desde el teclado', reply_markup=
			ReplyKeyboardMarkup(keyboard=[
			[KeyboardButton(text='/volver')],
			[KeyboardButton(text='/puntosfmpr alaves'), KeyboardButton(text='/puntosfmpr athletic')],
			[KeyboardButton(text='/puntosfmpr atletico'), KeyboardButton(text='/puntosfmpr barcelona')],
			[KeyboardButton(text='/puntosfmpr betis'), KeyboardButton(text='/puntosfmpr celta')],
			[KeyboardButton(text='/puntosfmpr deportivo'), KeyboardButton(text='/puntosfmpr espanyol')],
			[KeyboardButton(text='/puntosfmpr eibar'), KeyboardButton(text='/puntosfmpr getafe')],
			[KeyboardButton(text='/puntosfmpr girona'), KeyboardButton(text='/puntosfmpr laspalmas')],
			[KeyboardButton(text='/puntosfmpr leganes'), KeyboardButton(text='/puntosfmpr levante')],
			[KeyboardButton(text='/puntosfmpr malaga'), KeyboardButton(text='/puntosfmpr realmadrid')],
			[KeyboardButton(text='/puntosfmpr realsociedad'), KeyboardButton(text='/puntosfmpr sevilla')],
			[KeyboardButton(text='/puntosfmpr valencia'), KeyboardButton(text='/puntosfmpr villarreal')],
			]))
		else:
			bot.answerCallbackQuery(query_id, text='Algo no ha salido como estaba previsto')
	elif data == 'fme':
		global message_with_inline_keyboard
		if message_with_inline_keyboard:
			msg_idf = telepot.message_identifier(message_with_inline_keyboard)
			bot.editMessageText(msg_idf, 'Modo Futmondo Estadísticas escogido')
			bot.sendMessage(from_id, 'Escoge los puntos que quieres ver desde el teclado', reply_markup=
			ReplyKeyboardMarkup(keyboard=[
			[KeyboardButton(text='/volver')],
			[KeyboardButton(text='/puntosfme alaves'), KeyboardButton(text='/puntosfme athletic')],
			[KeyboardButton(text='/puntosfme atletico'), KeyboardButton(text='/puntosfme barcelona')],
			[KeyboardButton(text='/puntosfme betis'), KeyboardButton(text='/puntosfme celta')],
			[KeyboardButton(text='/puntosfme deportivo'), KeyboardButton(text='/puntosfme espanyol')],
			[KeyboardButton(text='/puntosfme eibar'), KeyboardButton(text='/puntosfme getafe')],
			[KeyboardButton(text='/puntosfme girona'), KeyboardButton(text='/puntosfme laspalmas')],
			[KeyboardButton(text='/puntosfme leganes'), KeyboardButton(text='/puntosfme levante')],
			[KeyboardButton(text='/puntosfme malaga'), KeyboardButton(text='/puntosfme realmadrid')],
			[KeyboardButton(text='/puntosfme realsociedad'), KeyboardButton(text='/puntosfme sevilla')],
			[KeyboardButton(text='/puntosfme valencia'), KeyboardButton(text='/puntosfme villarreal')],
			]))
		else:
			bot.answerCallbackQuery(query_id, text='Algo no ha salido como estaba previsto')
	elif data == 'fmm':
		global message_with_inline_keyboard
		if message_with_inline_keyboard:
			msg_idf = telepot.message_identifier(message_with_inline_keyboard)
			bot.editMessageText(msg_idf, 'Modo Futmondo Mixto escogido')
			bot.sendMessage(from_id, 'Escoge los puntos que quieres ver desde el teclado', reply_markup=
			ReplyKeyboardMarkup(keyboard=[
			[KeyboardButton(text='/volver')],
			[KeyboardButton(text='/puntosfmm alaves'), KeyboardButton(text='/puntosfmm athletic')],
			[KeyboardButton(text='/puntosfmm atletico'), KeyboardButton(text='/puntosfmm barcelona')],
			[KeyboardButton(text='/puntosfmm betis'), KeyboardButton(text='/puntosfmm celta')],
			[KeyboardButton(text='/puntosfmm deportivo'), KeyboardButton(text='/puntosfmm espanyol')],
			[KeyboardButton(text='/puntosfmm eibar'), KeyboardButton(text='/puntosfmm getafe')],
			[KeyboardButton(text='/puntosfmm girona'), KeyboardButton(text='/puntosfmm laspalmas')],
			[KeyboardButton(text='/puntosfmm leganes'), KeyboardButton(text='/puntosfmm levante')],
			[KeyboardButton(text='/puntosfmm malaga'), KeyboardButton(text='/puntosfmm realmadrid')],
			[KeyboardButton(text='/puntosfmm realsociedad'), KeyboardButton(text='/puntosfmm sevilla')],
			[KeyboardButton(text='/puntosfmm valencia'), KeyboardButton(text='/puntosfmm villarreal')],
			]))
		else:
			bot.answerCallbackQuery(query_id, text='Algo no ha salido como estaba previsto')
	elif data == 'fmpi':
		global message_with_inline_keyboard
		if message_with_inline_keyboard:
			msg_idf = telepot.message_identifier(message_with_inline_keyboard)
			bot.editMessageText(msg_idf, 'Modo Futmondo Picas escogido')
			bot.sendMessage(from_id, 'Escoge los puntos que quieres ver desde el teclado', reply_markup=
			ReplyKeyboardMarkup(keyboard=[
			[KeyboardButton(text='/volver')],
			[KeyboardButton(text='/puntosfmpi alaves'), KeyboardButton(text='/puntosfmpi athletic')],
			[KeyboardButton(text='/puntosfmpi atletico'), KeyboardButton(text='/puntosfmpi barcelona')],
			[KeyboardButton(text='/puntosfmpi betis'), KeyboardButton(text='/puntosfmpi celta')],
			[KeyboardButton(text='/puntosfmpi deportivo'), KeyboardButton(text='/puntosfmpi espanyol')],
			[KeyboardButton(text='/puntosfmpi eibar'), KeyboardButton(text='/puntosfmpi getafe')],
			[KeyboardButton(text='/puntosfmpi girona'), KeyboardButton(text='/puntosfmpi laspalmas')],
			[KeyboardButton(text='/puntosfmpi leganes'), KeyboardButton(text='/puntosfmpi levante')],
			[KeyboardButton(text='/puntosfmpi malaga'), KeyboardButton(text='/puntosfmpi realmadrid')],
			[KeyboardButton(text='/puntosfmpi realsociedad'), KeyboardButton(text='/puntosfmpi sevilla')],
			[KeyboardButton(text='/puntosfmpi valencia'), KeyboardButton(text='/puntosfmpi villarreal')],
			]))
		else:
			bot.answerCallbackQuery(query_id, text='Algo no ha salido como estaba previsto')
	elif data == 'jp':
		global message_with_inline_keyboard
		if message_with_inline_keyboard:
			msg_idf = telepot.message_identifier(message_with_inline_keyboard)
			bot.editMessageText(msg_idf, 'Modo Jornada Perfecta escogido')
			bot.sendMessage(from_id, 'Escoge los puntos que quieres ver desde el teclado', reply_markup=
			ReplyKeyboardMarkup(keyboard=[
			[KeyboardButton(text='/volver')],
			[KeyboardButton(text='/puntosjp alaves'), KeyboardButton(text='/puntosjp athletic')],
			[KeyboardButton(text='/puntosjp atletico'), KeyboardButton(text='/puntosjp barcelona')],
			[KeyboardButton(text='/puntosjp betis'), KeyboardButton(text='/puntosjp celta')],
			[KeyboardButton(text='/puntosjp deportivo'), KeyboardButton(text='/puntosjp espanyol')],
			[KeyboardButton(text='/puntosjp eibar'), KeyboardButton(text='/puntosjp getafe')],
			[KeyboardButton(text='/puntosjp girona'), KeyboardButton(text='/puntosjp laspalmas')],
			[KeyboardButton(text='/puntosjp leganes'), KeyboardButton(text='/puntosjp levante')],
			[KeyboardButton(text='/puntosjp malaga'), KeyboardButton(text='/puntosjp realmadrid')],
			[KeyboardButton(text='/puntosjp realsociedad'), KeyboardButton(text='/puntosjp sevilla')],
			[KeyboardButton(text='/puntosjp valencia'), KeyboardButton(text='/puntosjp villarreal')],
			]))
		else:
			bot.answerCallbackQuery(query_id, text='Algo no ha salido como estaba previsto')


bot = telepot.Bot('SECRET_TOKEN') # Introducir el correspondiente
answerer = telepot.helper.Answerer(bot)

MessageLoop(bot, {'chat': on_chat_message,
'callback_query': on_callback_query,}).run_as_thread()
print('Escuchando ...')

# Keep the program running.
while 1:
	time.sleep(10)
