#!/usr/bin/env python
# -*- coding: utf-8 -*-


#----------------------------------------------------
# Interface des services minitel
#----------------------------------------------------
class InterfaceService:
	# Constructeur (à appeler dans la classe héritière)
	def __init__( self, pa, nom ):
		self.pa  = pa
		self.nom = nom

	# Méthode lancée à l'exécutation d'un service (méthode pouvant être surchargée; utile lorsque le service comporte plusieurs pages)
	def executer( self ):
		self.effacer()
		self.afficher()

	# Effacement (méthode pouvant être surchargée)
	def effacer( self ):
		self.pa.minitel.effacer('vraimenttout')
		self.pa.minitel.curseur(False)
		self.pa.minitel.ligne_etat(1, self.nom)

	# Affichage (méthode à surcharger obligatoirement)
	def afficher( self ):
		pass
