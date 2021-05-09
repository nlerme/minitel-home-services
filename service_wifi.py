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
from utils import *


#----------------------------------------------------
# Classe du service wifi
#----------------------------------------------------
class ServiceWifi(InterfaceService):
	# Constructeur
	def __init__( self, pa, nom ):
		super().__init__(pa, nom)

	# Page d'accueil du service
	def afficher( self ):
		self.label1   = Label(self.pa.minitel, 0.05, 0.1, ['Veuillez saisir les informations','ci-dessous pour changer le','mot de passe réseau wifi'], 0.8, 0.2, True, 'centre')
		self.label2   = Label(self.pa.minitel, 0.05, 0.4, ['    SSID réseau wifi :',' Mot de passe actuel :','Nouveau mot de passe :','        Confirmation :'], 0.8, 0.24, True, 'gauche')
		self.champ1   = ChampTexte(self.pa.minitel, 0.67, 0.51, 9, 100, ssid_wifi_actuel())
		self.champ2   = ChampTexte(self.pa.minitel, 0.67, 0.54, 9, 100, '', None, True)
		self.champ3   = ChampTexte(self.pa.minitel, 0.67, 0.57, 9, 100, '', None, True)
		self.champ4   = ChampTexte(self.pa.minitel, 0.67, 0.61, 9, 100, '', None, True)
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
		self.elements.executer({'SOMMAIRE':self.pa.executer,'ENVOI':self.valider})

	# Validation de la page d'accueil du service
	def valider( self ):
		# On récupère la valeur des champs
		ssid_reseau            = self.champ1.valeur
		mot_passe_actuel       = self.champ2.valeur
		nouveau_mot_passe      = self.champ3.valeur
		confirmation_mot_passe = self.champ4.valeur

		# On vérifie que les champs soient non vides
		if len(ssid_reseau)==0 or len(mot_passe_actuel)==0 or len(nouveau_mot_passe)==0 or len(confirmation_mot_passe)==0:
			self.pa.minitel.erreur(1, 20, "Merci de remplir tous les champs")
			self.elements.element_actif.gerer_arrivee()
			return

		# On vérifie que le mot de passe est bien confirmé
		if nouveau_mot_passe!=confirmation_mot_passe:
			self.pa.minitel.erreur(1, 20, "Le nouveau mot de passe doit être confirmé")
			self.elements.element_actif.gerer_arrivee()
			return

		# On change le mot de passe (TODO)
		#change_mot_passe_wifi(ssid_reseau)
