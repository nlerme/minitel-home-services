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
from minitel.ui.Menu import Menu
from interface_service import InterfaceService
from pprint import pprint
import requests
import base64
import subprocess
from time import sleep


#----------------------------------------------------
# Classe du service volets
#----------------------------------------------------
class ServiceVolets(InterfaceService):
	# Constructeur
	def __init__( self, pa, nom ):
		super().__init__(pa, nom)
		self.pages = {'connection':self.afficher_page_connection,'resultats':self.afficher_page_resultats}
		self.page_actuelle = 'connection'

	# Execution du service
	def executer( self ):
		# On efface d'abord l'écran
		self.effacer()

		# On affiche la page courante
		if self.page_actuelle in self.pages:
			self.pages[self.page_actuelle]()

	###################################################################################

	# Page de connection
	def afficher_page_connection( self ):
		self.label1   = Label(self.pa.minitel, 0.05, 0.1, ['Veuillez saisir les champs','ci-dessous pour piloter','ouverture/fermeture des volets'], 0.8, 0.2, True, 'centre')
		self.label2   = Label(self.pa.minitel, 0.05, 0.4, ['Adresse réseau :','   Identifiant :','  Mot de passe :'], 0.8, 0.2, True, 'gauche')
		self.champ1   = ChampTexte(self.pa.minitel, 0.53, 0.51, 15, 100, '')
		self.champ2   = ChampTexte(self.pa.minitel, 0.53, 0.54, 15, 100, '')
		self.champ3   = ChampTexte(self.pa.minitel, 0.53, 0.57, 15, 100, '', None, True)
		self.ligne1   = Ligne(self.pa.minitel, 0.0, 0.95, 1.0, 'h', 'blanc')
		self.bouton1  = Bouton(self.pa.minitel, 0.0, 0.99, 0.0, 'SOMMAIRE')
		self.bouton2  = Bouton(self.pa.minitel, 0.9, 0.99, 0.0, 'ENVOI')
		self.elements = Conteneur(self.pa.minitel, 0.0, 0.0, 1.0, 1.0, 'blanc', 'noir')
		self.elements.ajouter(self.label1)
		self.elements.ajouter(self.label2)
		self.elements.ajouter(self.champ1)
		self.elements.ajouter(self.champ2)
		self.elements.ajouter(self.champ3)
		self.elements.ajouter(self.ligne1)
		self.elements.ajouter(self.bouton1)
		self.elements.ajouter(self.bouton2)
		self.elements.afficher()
		self.elements.executer({'SOMMAIRE':self.pa.executer,'ENVOI':self.valider_page_connection})

	# Validation des informations de connection
	def valider_page_connection( self ):
		# On récupère la valeur des champs texte
		self.url_base    = self.champ1.valeur
		self.identifiant = self.champ2.valeur
		self.mot_passe   = self.champ3.valeur

		# On vérifie si les champs ne sont pas vides
		if len(self.url_base)==0 or len(self.identifiant)==0 or len(self.mot_passe)==0:
			self.pa.minitel.erreur(1, 20, "Merci de remplir tous les champs")
			self.elements.element_actif.gerer_arrivee()
			return

		# On encode l'identifiant et le mot de passe en base64
		self.identifiant = base64.b64encode(self.identifiant.encode('ascii')).decode('ascii')
		self.mot_passe   = base64.b64encode(self.mot_passe.encode('ascii')).decode('ascii')

		# On affiche la page résultats
		self.page_actuelle = 'resultats'
		self.executer()

	###################################################################################

	# Page d'affichage des résultats
	def afficher_page_resultats( self ):
		# On récupère les données sur les volets
		url     = '%s/json.htm?type=devices&filter=all&used=true&order=Name&username=%s&password=%s'%(self.url_base,self.identifiant,self.mot_passe)
		contenu = requests.get(url)
		donnees = contenu.json()

		# On vérifie si la connection est ok
		if donnees['status']!='OK':
			self.pa.minitel.erreur(1, 20, "Impossible de se connecter")
			self.page_actuelle = 'connection'
			self.executer()
			return

		# On stocke les données sur les volets au bon format
		self.volets = []

		for volet in donnees['result']:
			self.volets += [{'idx':volet['idx'],'etat':('o' if volet['Status']=='Open' else 'f'),'nom':volet['Name']}]

		# On affiche la liste des volets
		options = []

		for k in range(len(self.volets)):
			options += ['%s (%s)'%(self.volets[k]['nom'],self.volets[k]['etat'])]

		self.menu1    = Menu(self.pa.minitel, options, 0.2, 0.3)
		self.ligne1   = Ligne(self.pa.minitel, 0.0, 0.95, 1.0, 'h', 'blanc')
		self.bouton1  = Bouton(self.pa.minitel, 0.0, 0.99, 0.0, 'SOMMAIRE')
		self.label1   = Label(self.pa.minitel, 0.5, 0.99, ['Ouvrir/fermer :'], 0.0, 0.0, False, 'gauche')
		self.bouton2  = Bouton(self.pa.minitel, 0.9, 0.99, 0.0, 'ENVOI')
		self.elements = Conteneur(self.pa.minitel, 0.0, 0.0, 1.0, 1.0, 'blanc', 'noir')
		self.elements.ajouter(self.menu1)
		self.elements.ajouter(self.ligne1)
		self.elements.ajouter(self.label1)
		self.elements.ajouter(self.bouton1)
		self.elements.ajouter(self.bouton2)
		self.elements.afficher()
		self.elements.executer({'SOMMAIRE':self.pa.executer,'ENVOI':self.valider_page_resultats})

	# Page de validation des résultats
	def valider_page_resultats( self ):
		# On récupère l'idx du volet sélectionné
		idx = self.volets[self.menu1.selection]['idx']

		# On choisit l'action à mener sur le volet en fonction de son état
		etat   = self.volets[self.menu1.selection]['etat']
		action = ('On' if etat=='o' else 'Off')

		# On actionne le volet sélectionné
		
		url     = '%s/json.htm?type=command&param=switchlight&idx=%s&switchcmd=%s&username=%s&password=%s'%(self.url_base,idx,action,self.identifiant,self.mot_passe)
		contenu = requests.get(url)
		donnees = contenu.json()

		# On vérifie si tout s'est bien passé
		if donnees['status']!='OK':
			self.pa.minitel.erreur(1, 20, "Impossible d'actionner le volet")
			self.elements.element_actif.gerer_arrivee()
			return
		else:
			sleep(1)
			self.executer()
