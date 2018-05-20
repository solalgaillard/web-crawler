#! /usr/bin/env python
# -*- coding: utf-8 -*-	

from os import chdir	#permet d'accéder au dossier où sont contenus les fichier externes
chdir('../Ressources')

encodings = ['utf-8', 'iso-8859-1'] #pour gérer plusieurs encodings, deux ici mais on pourrait en rajouter

#fonction qui sort les mots un à un et les transmet à ajoute

def indexe(dex, mots, ligne, switch) :	#le paramètre ligne prend maintenant l'URL, je ne l'ai pas changé
	for mot in mots :
		mot = nettoie(filtrerBalises(nettoie(mot.lower()))) #Nettoie avant et après qu'on retire les balises
		if mot and switch :
			if mot in golist : dex = ajoute(dex, mot.encode('utf-8'), ligne)	#réencode les mots en utf-8 après manipulation
		elif mot :
			if mot in stoplist or mot in ponctuation : pass
			else : dex = ajoute(dex, mot.encode('utf-8'), ligne)
	return dex


#fonction qui va peupler le dictionnaire

def ajoute(dex, mot, ligne) :
	if mot in dex :
		if ligne in dex[mot] : pass	#si le mot a déjà été indexé sous une URL, il ne le sera pas à nouveau
		else : dex[mot].append(ligne)
	else : dex[mot] = [ligne]	#indexe avec valeur de la clé mot, l'URL
	return dex


#fonction qui nettoie les mots

def nettoie(mot) :
	if len(mot) == 0 : return mot
	elif mot[-1] in ponctuation : mot = nettoie(mot[:-1])
	elif mot[0] in ponctuation : mot = nettoie(mot[1:])
	return mot

#fonction qui enlève les mots avec balises tout en gardant les mots qui peuvent se trouver à l'intérieur

def filtrerBalises(mot) :
	for x in baliseListe :	#pour tous les mots dans la liste
		motTraite = mot.find(x)	#trouver l'emplacement de début (-1, veut dire que le mot n'est pas dans la liste)
		if motTraite >= 0 : #si on trouve un mot
			if x[-2:] == '="' or x[-2:] == "='"  :	#quand ce mot balise se termine '="'
				mot = mot[: motTraite] + mot[len(x) + motTraite + mot[len(x) + motTraite :].find('"') + 1:] #on enlève tout même ce qui est entre guillemets
			else : mot = mot[: motTraite] + mot[len(x) + motTraite :] #sinon on enlève juste le mot
	return mot

#fonction qui récupère le charset. En cas de problème, renvoie 8859-1 car il ne produit pas d'erreurs en conversion vers unicode même quand il n'est pas le bon codage et il y a des chances que ce soit le bon.Ainsi la page n'est pas perdue et ses liens non plus.

def get_charset(url) : 
	try :
		if any('charset' in i for i in dict(url.info()).values()) : #cherche dans les valeurs du dictionnaire
			return dict(url.info())['content-type'].split()[1].split('=')[1]	#renvoie la valeur
		else : return 'iso-8859-1'	#s'il ne trouve pas mais qu'il n'y a pas d'erreurs, renvoie 'iso-8859-1'
	except : return 'iso-8859-1'	#s'il y a une erreur, renvoie 'iso-8859-1'


#fonction permettant de récupérer les liens grâce à la présence de la balise 'href='

def get_href(ligne) :
	x = ligne.find('href=')	#cherche pour "href"
	if x < 0 : return	#on arrête si rien
	ref = ligne[x+6:].split('"')[0]	#sinon on prend tout entre le premier guillemet et le dernier
	if ref.startswith('http:') : return ref	#si ce segment commence par http, on le renvoie


#fonction de présentation des mots. Elle imprime les mots et fait appel à la fonction ancillaire presentation()

def prd(d) :
	if not d : return
	print '\n', '\t', 'INDEX', '\n'
	for c in sorted(d) :
		print '\t', c, ':', presentation(d[c])

#fonction qui organise la numérotation des lignes

def presentation(liste) :
	l = []
	s = ""
	for n in range(len(liste)) :
		if n < len(liste) - 1 and not liste[n + 1] - liste[n] - 1   :
			l += [liste[n]]
		else :
			if l : s += str(l[0]) + '-' + str(l[len(l) - 1] + 1) + ', '
			else : s += str(liste[n]) + ', ' 
			l = []	
	return s[:-2]


#fonction qui permet de peupler un fichier avec une liste

def put_list (fichier, liste) :
	flux = open(fichier, 'w')
	flux.write('\n'.join(liste))
	flux.close()

#fonction qui permet de créer une liste à partir du contenu d'un fichier

def get_list (fichier) :
	try :
		flux = open(fichier, 'r')
		stoplist = flux.read().decode('utf-8').split()
		flux.close()
		if not stoplist : return False
		else : return stoplist
	except IOError : return False




stoplist = get_list('stop.list')	#peuple la stoplist
golist = get_list('go.list')	#peuple la golist
baliseListe = get_list('balise.list')	#peuple la liste des balises

ponctuation = u'(,.):“ €▪▾;–»«}/>{|©[-~^]*\'"'	#liste des signes de ponctuation
