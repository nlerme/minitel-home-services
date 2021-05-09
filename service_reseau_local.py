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
# Classe du service réseau local
#----------------------------------------------------
class ServiceReseauLocal(InterfaceService):
	# Constructeur
	def __init__( self, pa, nom ):
		super().__init__(pa, nom)

	# Page d'affichage
	def afficher( self ):
		# On récupère la liste des appareils connectés au réseau local
		appareils = appareils_connectes('192.168.0.*', 15)
		message   = []

		for k in range(len(appareils)):
			message += ['%s : %s'%(appareils[k]['ip'],appareils[k]['nom'])]

		# On afficheg la page
		self.label1   = Label(self.pa.minitel, 0.05, 0.1, message, 0.8, 0.45, True, 'gauche')
		self.label2   = Label(self.pa.minitel, 0.58, 0.99, ['Rafraîchir :'], 0.0, 0.0, False, 'gauche')
		self.ligne    = Ligne(self.pa.minitel, 0.0, 0.95, 1.0, 'h', 'blanc')
		self.bouton1  = Bouton(self.pa.minitel, 0.0, 0.99, 0.0, 'SOMMAIRE')
		self.bouton2  = Bouton(self.pa.minitel, 0.9, 0.99, 0.0, 'ENVOI')
		self.elements = Conteneur(self.pa.minitel, 0.0, 0.0, 1.0, 1.0, 'blanc', 'noir')
		self.elements.ajouter(self.label1)
		self.elements.ajouter(self.label2)
		self.elements.ajouter(self.ligne)
		self.elements.ajouter(self.bouton1)
		self.elements.ajouter(self.bouton2)
		self.elements.afficher()
		self.elements.executer({'SOMMAIRE':self.pa.executer,'ENVOI':self.executer})
