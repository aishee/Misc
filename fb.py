#!/usr/bin/python
# cookie.txt & ids.txt REQUIRED!

import sys, os, urllib, urllib2, fileinput
from bs4 import BeautifulSoup 

f = open('cookie.txt','r')
c00kie = f.read()


def add():

	with open('ids.txt') as lista_ids:
		for x, line in enumerate(lista_ids):

			data2post = urllib.urlencode({'to_friend':str(line),'action':'add_friend','how_found':'requests_page_pymk',
							'ref_param':'none','logging_location':'friend_browser',
							'no_flyout_on_click':'true','__user':'1492825438','__a':'1',
							'__dyn':'7n8ahyj35zoSt2u6aOGeEwlyp9EbEyGgSmEVF4WpUpBxCdz8','__req':'m',
							'fb_dtsg':'AQEcSPNP8cux','ttstamp':'265816999838078805699117120',
							'__rev':'1252742'})

			url = 'https://www.facebook.com/ajax/add_friend/action.php'

			pedido = urllib2.Request(url, data2post, headers={"Cookie" : c00kie})
			resposta = urllib2.urlopen(pedido)
			resultado = resposta.read()

			#print resultado

			if 'success' in resultado:
   				print('\033[92mPedido enviado\033[0m - ' + str(line) + "\n")
			elif 'Already Sent' in resultado:
				print('\033[0mPedido repetido\033[0m - ' + str(line) + "\n")
			elif 'prevent spammers' in resultado: # HATE CAPTCHAZ!
				print('\033[91mPedidos bloqueados!\033[0m - ' + str(line) + "\n")
				return
			else:
				print('\033[0mPedido n\u00e3o enviado\033[0m - ' + str(line) + "\n")


def cancel():

	with open('ids.txt') as lista_ids:
		for x, line in enumerate(lista_ids):

			data2post = urllib.urlencode({'subject_id':str(line),'ref_param':'outgoing_requests',
							'fb_dtsg':'AQG5fx5DhBu_','__dyn':'1Z3p40x84193FQ8xO4oydyoqxLw',
							'__req':'d','__user':'1492825438'})

			url = 'https://m.facebook.com/a/friendrequest/cancel/index.php'

			pedido = urllib2.Request(url, data2post, headers={"Cookie" : c00kie})
			resposta = urllib2.urlopen(pedido)
			resultado = resposta.read()

			#print resultado

			if 'already canceled' in resultado:
   				print('\033[0mPedido inexistente\033[0m - ' + str(line) + "\n")
			elif 'process this request right now' in resultado:
   				print('\033[91mErro ao cancelar\033[0m - ' + str(line) + "\n")
				return
			else:
				print('\033[92mPedido cancelado\033[0m - ' + str(line) + "\n")



def poke():

	with open('ids.txt') as lista_ids:
		for x, line in enumerate(lista_ids):

			data2post = urllib.urlencode({'__user':'1492825438', '__a':'1', 'fb_dtsg':'AQFpfTye1hqD'})

			url = 'https://www.facebook.com/pokes/dialog/?poke_target=' + str(line)

			pedido = urllib2.Request(url, data2post, headers={"Cookie" : c00kie})
			resposta = urllib2.urlopen(pedido)
			resultado = resposta.read()

			#print resultado
			#print url

			if 'You poked' in resultado:
   				print('\033[92mToque enviado\033[0m - ' + str(line) + "\n")
			elif 'has not responded' in resultado:
				print('\033[0mToque repetido\033[0m - ' + str(line) + "\n")
			elif 'Unable to poke this person' in resultado:
				print('\033[91mToques bloqueados\033[0m - ' + str(line) + "\n")
				return
			else:
				print('\033[91mToque n\u00e3o enviado\033[0m - ' + str(line) + "\n")


def crawl():

	url = "https://www.facebook.com/friends/requests/"

	pedido = urllib2.Request(url, headers={"Cookie" : c00kie})
	resposta = urllib2.urlopen(pedido)
	pagina = resposta.read()
	soup = BeautifulSoup(pagina)

	f = open('x.txt', 'w')
	links = soup.find_all('a')
	for link in links:
    		info = str(link.get('data-hovercard'))
    		f.write(info + "\n")
	f.close()

	delete_list = ["None", "&extragetparams=%7B%22hc_location%22%3A%22friend_browser%22%2C%22fref%22%3A%22pymk%22%7D", "/ajax/hovercard/user.php?id="]

	y = open('y.txt', 'w')
	x = open('x.txt') #stupid IO error, have to re-open
	for line in x:
		for word in delete_list:
        		line = line.replace(word, "")
		y.write(line)


# 1337 menu
while 1:

	menu = raw_input("\n"+"[\033[94mcrawl\033[0m] para aglomerar perfis\n" + "[\033[95mpoke\033[0m] para enviar toques\n" 
			+ "[\033[92madd\033[0m] para adicionar amigos\n" + "[\033[93mcancel\033[0m] para cancelar pedidos\n" 
			+ "[\033[91mexit\033[0m] para sair do script\n\n")

	if menu == "add":
		print "\n" #estetica
		add()
	elif menu == "poke":
		print "\n"	
		poke()
	elif menu == "cancel":
		print "\n"
		cancel()
	elif menu == "crawl":
		print "\n"
		crawl()
	elif menu == "exit":
		print "\n"
		sys.exit()
	else:
		print (u"\033[91mOp\u00e7\u00e3o inv\u00e1lida!\033[0m\n")