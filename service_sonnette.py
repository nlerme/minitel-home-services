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


#----------------------------------------------------
# Classe du service sonnette
#----------------------------------------------------
class ServiceSonnette(InterfaceService):
	# Constructeur
	def __init__( self, pa, nom ):
		super().__init__(pa, nom)

	# Page d'affichage
	def afficher( self ):
		self.ligne1   = Ligne(self.pa.minitel, 0.0, 0.95, 1.0, 'h', 'blanc')
		self.bouton1  = Bouton(self.pa.minitel, 0.0, 0.99, 0.0, 'SOMMAIRE')
		self.elements = Conteneur(self.pa.minitel, 0.0, 0.0, 1.0, 1.0, 'blanc', 'noir')
		self.elements.ajouter(self.ligne1)
		self.elements.ajouter(self.bouton1)
		self.elements.afficher()
		self.elements.executer({'SOMMAIRE':self.pa.executer})
