#! /usr/bin/env python
# -*- coding: utf-8 -*-	

import sys
sys.path[0:0] = ['src']	#pour pouvoir importer le module depuis un dossier différent

import dexlex	#importe le module définie dans Ressources
from urllib import urlopen	#permet d'ouvrir une URL

#fonction de contrôle qui appelle la fonction indexe pour chaque ligne

def pilote(url, dex, hrefs, compteur) : #pilote() prend un argument de plus, la liste vide de hrefs
	if url[-3:] == '-go' : 
		url = url[:-3]
		switchList = True
	elif url[-5:] == '-stop' : 
		url = url[:-5]
		switchList = False
	else : 
		if dexlex.golist : switchList = True
		else : switchList = False
	try :	#si le lien n'est mort
		flux = urlopen(url)
		charset = dexlex.get_charset(flux)
		page = flux.read().decode(charset)
		for n, texte in enumerate(page.split()) :
			dex = dexlex.indexe(dex, texte.split(), url, switchList)	#crée l'index
			if dexlex.get_href(texte) : hrefs.append(dexlex.get_href(texte).encode('utf-8'))# si le mot soumis est un lien on le met dans une liste
		flux.close()
		print 7*'\n', '\t','PAGE - ' + url	#mise en forme
		print '\t','--------------------------------------------', '\n'
		print'\n', '\t', 'LIENS', '\n'
		if hrefs : #s'il existe des liens
			for x in hrefs : print '\t', x	#on les imprime
		else : print '\t', 'Aucun lien'
		dexlex.prd(dex)	#on imprime l'index
		compteur-=1 #on enlève 1 au compteur. Quand le compteur est à zero, il n'y a plus de récursions
		recursionLiens(hrefs, compteur)	#on récurse avec la fonction recursionLiens
		return	#on arrête la fonction
	except IOError: #si le lien est mort
			print '\n', '\t', "Le lien " + url + " ne fonctionne pas"
			return
	except: return

def recursionLiens(liens, compteur)	:
	if compteur : #tant que compteur n'est pas vide
		for x in liens : #Pour chaque lien dans href peuplé par la fonction pilote() appelé précédemment, on appelle la fonction pilote. Ainsi, on a les liens des liens
			pilote(x, {}, [], compteur)
	else : return	#si le compteur est vide, il ne se passe rien



import sys
if len(sys.argv) > 1 :
	for x in sys.argv[1:]:
 		pilote(x, {}, [], 2)
else : print "Veuillez entrer le nom d'une ou plusieurs URL. Vous pouvez utiliser la golist ou la stoplist. Par défaut, la golist est utilisé sauf si elle est vide ou inexistante"
