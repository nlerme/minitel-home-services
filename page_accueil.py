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
from utils import is_a_number


#----------------------------------------------------
# Classe de gestion de la page d'accueil
#----------------------------------------------------
class PageAccueil:
	def __init__( self, titre, version, auteur ):
		self.minitel = Minitel()
		self.minitel.deviner_vitesse()
		self.minitel.identifier()
		self.minitel.definir_vitesse(9600)
		self.minitel.definir_mode('VIDEOTEX')
		self.minitel.configurer_clavier(etendu = True, curseur = False, minuscule = True)
		self.minitel.echo(False)
		self.minitel.curseur(False)
		self.services = []
		self.titre    = titre
		self.version  = version
		self.auteur   = auteur

	def ajouter_service( self, service ):
		self.services += [service]

	def executer( self ):
		self.effacer()
		self.afficher()

	def effacer( self ):
		self.minitel.effacer('vraimenttout')

	def afficher( self ):
		message = []

		for k in range(len(self.services)):
			message += ['%d. %s'%(k+1,self.services[k].nom)]

		self.label1   = Label(self.minitel, 0.1, 0.0, [self.titre,'-------------','v%s - %s'%(self.version,self.auteur)], 0.7, 0.22, True, 'centre')
		self.label2   = Label(self.minitel, 0.1, 0.4, message, 0.7, 0.0, True, 'gauche')
		self.ligne1   = Ligne(self.minitel, 0.0, 0.95, 1.0, 'h', 'blanc')
		self.bouton1  = Bouton(self.minitel, 0.9, 0.99, 0.1, 'ENVOI')
		self.label3   = Label(self.minitel, 0.0, 0.99, ['Choix :'])
		self.champ1   = ChampTexte(self.minitel, 0.2, 0.99, 2, 2, '')
		self.elements = Conteneur(self.minitel, 0.0, 0.0, 1.0, 1.0, 'blanc', 'noir')
		self.elements.ajouter(self.label1)
		self.elements.ajouter(self.label2)
		self.elements.ajouter(self.ligne1)
		self.elements.ajouter(self.bouton1)
		self.elements.ajouter(self.label3)
		self.elements.ajouter(self.champ1)
		self.elements.afficher()
		self.elements.executer({'ENVOI':self.valider})

	def valider( self ):
		if not is_a_number(self.champ1.valeur):
			self.minitel.bip()
			return

		choix = int(self.champ1.valeur)

		if choix<1 or choix>len(self.services):
			self.minitel.bip()
			return

		self.services[choix-1].executer()

	def __del__( self ):
		self.minitel.stopper()
