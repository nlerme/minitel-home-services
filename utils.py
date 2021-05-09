#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Packages
import re
import subprocess


# Retourne True si la chaîne de caractères représente un nombre (entier ou réel), False sinon
def is_a_number(str):
	try: 
		float(str)
	except ValueError: 
		return False
	return True

# Retourne la liste des appareils connectés au réseau local
def appareils_connectes( adresses_ip, longueur_max_nom_appareil=0 ):
	appareils = []
	sortie    = subprocess.run("nmap -sL %s | grep \(1 | tr -d \"()\" | awk '{print $6\"|\"$5}'"%adresses_ip, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

	for ligne in sortie.stdout.decode('utf-8').split('\n'):
		if ligne:
			ip,nom = ligne.split('|')
			nom    = nom.rsplit('.', 1)[0]
			if longueur_max_nom_appareil>0 and len(nom)>longueur_max_nom_appareil:
				nom = nom[0:longueur_max_nom_appareil]+'...'
			appareils = appareils+[{'nom':nom,'ip':ip}]

	return appareils

# Retourne le SSID réseau actuel
def ssid_wifi_actuel():
	sortie = subprocess.run('iwgetid -r', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
	return sortie.stdout.decode('utf-8')

# Change le mot de passe d'un réseau wifi donné
def changer_mot_passe_wifi( ssid, mot_passe ):
	sortie = subprocess.run('wicd-cli --wireless -c "%s" "%s"'%(ssid, mot_passe))
