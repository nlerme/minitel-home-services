#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Packages
from minitel.constantes import (RETOUR,SUITE,ENVOI,SOMMAIRE,GUIDE,ANNULATION,CORRECTION)
from minitel.Minitel import Minitel
from minitel.ui.Conteneur import Conteneur
from minitel.ui.ChampTexte import ChampTexte
from minitel.ui.Label import Label
from minitel.ui.Bouton import Bouton
from minitel.ui.Ligne import Ligne
from interface_service import InterfaceService
from time import sleep
from pprint import pprint
from utils import *
from datetime import datetime
import requests
import geocoder
import locale


#----------------------------------------------------
# Classe du service météo
#----------------------------------------------------
class ServiceMeteo(InterfaceService):
	# Constructeur
	def __init__( self, pa, nom ):
		super().__init__(pa, nom)
		self.pages = {'saisie':self.afficher_page_saisie,'resultats':self.afficher_page_resultats}
		self.page_actuelle = 'saisie'
		self.numero_page_resultats = 0
		self.nb_pages_resultats = 4
		locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

	# Execution du service
	def executer( self ):
		# On efface d'abord l'écran
		self.effacer()

		# On affiche la page courante
		if self.page_actuelle in self.pages:
			self.pages[self.page_actuelle]()

	###################################################################################

	# Affichage de la page de saisie
	def afficher_page_saisie( self ):
		self.label1   = Label(self.pa.minitel, 0.05, 0.1, ['Veuillez saisir la commune','et le pays ou les coordonnées','géographiques désirées'], 0.8, 0.2, True, 'centre')
		self.label2   = Label(self.pa.minitel, 0.05, 0.4, ['  Commune :','     Pays :',' Latitude :','Longitude :'], 0.8, 0.27, True, 'gauche')
		self.champ1   = ChampTexte(self.pa.minitel, 0.4, 0.51, 20, 30, geocoder.ip('me').city)
		self.champ2   = ChampTexte(self.pa.minitel, 0.4, 0.54, 20, 30, geocoder.ip('me').country)
		self.champ3   = ChampTexte(self.pa.minitel, 0.4, 0.57, 20, 30, '')
		self.champ4   = ChampTexte(self.pa.minitel, 0.4, 0.61, 20, 30, '')
		self.ligne1   = Ligne(self.pa.minitel, 0.0, 0.95, 1.0, 'h', 'blanc')
		self.bouton1  = Bouton(self.pa.minitel, 0.0, 0.99, 0.0, 'SOMMAIRE')
		self.bouton2  = Bouton(self.pa.minitel, 0.9, 0.99, 0.0, 'ENVOI')
		self.elements = Conteneur(self.pa.minitel, 0.0, 0.0, 1.0, 1.0, 'blanc', 'noir')
		self.elements.ajouter(self.label1)
		self.elements.ajouter(self.label2)
		self.elements.ajouter(self.champ1)
		self.elements.ajouter(self.champ2)
		self.elements.ajouter(self.champ3)
		self.elements.ajouter(self.champ4)
		self.elements.ajouter(self.ligne1)
		self.elements.ajouter(self.bouton1)
		self.elements.ajouter(self.bouton2)
		self.elements.afficher()
		self.elements.executer({'SOMMAIRE':self.pa.executer,'ENVOI':self.valider_page_saisie})

	# Validation de la saisie
	def valider_page_saisie( self ):
		# On stocke la valeur des champs texte dans des variables
		commune     = self.champ1.valeur
		pays        = self.champ2.valeur
		latitude    = self.champ3.valeur
		longitude   = self.champ4.valeur

		# On vérifie si les données saisies sont au bon format
		if len(latitude)>0 and not is_a_number(latitude):
			self.pa.minitel.erreur(1, 20, "La latitude n'est pas au bon format")
			self.elements.element_actif.gerer_arrivee()
			return

		if len(longitude)>0 and not is_a_number(longitude):
			self.pa.minitel.erreur(1, 20, "La longitude n'est pas n'est pas au bon format")
			self.elements.element_actif.gerer_arrivee()
			return

		if (len(latitude)>0 and len(longitude)==0) or (len(latitude)==0 and len(longitude)>0):
			self.pa.minitel.erreur(1, 20, "Veuillez saisir latitude et longitude")
			self.elements.element_actif.gerer_arrivee()
			return

		if (len(commune)>0 and len(latitude)>0):
			self.pa.minitel.erreur(1, 20, "Choisir entre commune et latitude/longitude")
			self.elements.element_actif.gerer_arrivee()
			return

		if len(commune)>0 and len(pays)==0:
			self.pa.minitel.erreur(1, 20, "Veuillez indiquer le pays avec la commune")
			self.elements.element_actif.gerer_arrivee()
			return

		# On récupère la latitude/longitude de la commune si nécessaire
		url_base    = 'http://api.openweathermap.org/data/2.5/onecall'
		owm_cle_api = 'c453a548b4d6e77c20f077fa39042c01'

		if len(commune)>0:
			g = geocoder.arcgis('%s, %s'%(commune,pays))
			if g==None:
				self.pa.minitel.erreur(1, 20, "Commune et/ou pays inconnu(s)")
				self.elements.element_actif.gerer_arrivee()
				return
			(latitude,longitude) = g.latlng
		else:
			latitude  = float(latitude)
			longitude = float(longitude)

		# On récupère les données météo
		url        = "%s?lat=%f&lon=%f&appid=%s&units=metric&lang=fr"%(url_base,latitude,longitude,owm_cle_api)
		contenu    = requests.get(url)
		self.meteo  = contenu.json()

		if 'cod' in self.meteo and int(self.meteo['cod'])==401:
			self.pa.minitel.erreur(1, 20, "Clé API OpenWeatherMap inconnue")
			self.elements.element_actif.gerer_arrivee()
			return
		else:
			self.page_actuelle = 'resultats'
			self.numero_page_resultats = 0
			self.executer()

	###################################################################################

	# Affichage des résultats
	def afficher_page_resultats( self ):
		# On met en forme la page courante sur les données météo
		message      = []
		n            = int(len(self.meteo['daily'])/self.nb_pages_resultats)
		indice_debut = n*self.numero_page_resultats
		indice_fin   = indice_debut+n

		for jour in self.meteo['daily'][indice_debut:indice_fin]:
			date           = datetime.fromtimestamp(jour['dt']).strftime('%A %-d %B')
			temps          = jour['weather'][0]['description']
			pluie          = float(jour['pop'])
			min_temp       = int(round(jour['temp']['min']))
			max_temp       = int(round(jour['temp']['max']))
			pression       = int(round(jour['pressure']))
			humidite       = int(round(jour['humidity']))
			vitesse_vent   = int(round(jour['wind_speed']))
			direction_vent = jour['wind_deg']
			lever_soleil   = datetime.fromtimestamp(jour['sunrise']).strftime('%Hh%M')
			coucher_soleil = datetime.fromtimestamp(jour['sunset']).strftime('%Hh%M')
			message       += ['* %s : %s'%(date,temps)]
			message       += ['  * Probabilité pluie : %.2f'%(pluie)]
			message       += ['  * Températures      : %d°C, %d°C'%(min_temp,max_temp)]
			message       += ['  * Pression          : %d hPa'%(pression)]
			message       += ['  * Humidité          : %d%%'%(humidite)]
			message       += ['  * Direction du vent : %d°'%(direction_vent)]
			message       += ['  * Vitesse du vent   : %d m/s'%(vitesse_vent)]
			message       += ['  * Lever soleil      : %s'%(lever_soleil)]
			message       += ['  * Coucher soleil    : %s'%(coucher_soleil)]
			message       += [' ']

		# On affiche les informations
		self.label1   = Label(self.pa.minitel, 0.1, 0.1, message, 0.8, 0.0, False, 'gauche')
		self.ligne1   = Ligne(self.pa.minitel, 0.0, 0.95, 1.0, 'h', 'blanc')
		self.bouton1  = Bouton(self.pa.minitel, 0.0, 0.99, 0.0, 'SOMMAIRE')
		self.bouton2  = Bouton(self.pa.minitel, 0.33, 0.99, 0.0, 'RETOUR')
		self.bouton3  = Bouton(self.pa.minitel, 0.57, 0.99, 0.0, 'SUITE')
		self.bouton4  = Bouton(self.pa.minitel, 0.77, 0.99, 0.0, 'CORRECTION')
		self.elements = Conteneur(self.pa.minitel, 0.0, 0.0, 1.0, 1.0, 'blanc', 'noir')
		self.elements.ajouter(self.label1)
		self.elements.ajouter(self.ligne1)
		self.elements.ajouter(self.bouton1)
		self.elements.ajouter(self.bouton2)
		self.elements.ajouter(self.bouton3)
		self.elements.ajouter(self.bouton4)
		self.elements.afficher()
		self.elements.executer({'SOMMAIRE':self.pa.executer,'RETOUR':self.precedent_page_resultats,'SUITE':self.suivant_page_resultats,'CORRECTION':self.valider_page_resultats})

	# Affichage de la page précédente
	def precedent_page_resultats( self ):
		if self.numero_page_resultats==0:
			self.pa.minitel.bip()
			return
		self.numero_page_resultats -= 1
		self.afficher_page_resultats()

	# Affichage de la page suivante
	def suivant_page_resultats( self ):
		if self.numero_page_resultats==(self.nb_pages_resultats-1):
			self.pa.minitel.bip()
			return
		self.numero_page_resultats += 1
		self.afficher_page_resultats()

	# Validation des résultats
	def valider_page_resultats( self ):
		self.page_actuelle = 'saisie'
		self.executer()
