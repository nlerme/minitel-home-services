#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Packages
from page_accueil import PageAccueil
from service_meteo import ServiceMeteo
from service_annuaire import ServiceAnnuaire
from service_reseau_local import ServiceReseauLocal
from service_tel_fixe import ServiceTelFixe
from service_minitel import ServiceMinitel
from service_sonnette import ServiceSonnette
from service_wifi import ServiceWifi
from service_volets import ServiceVolets


#----------------------------------------------------
# Fonction principale
#----------------------------------------------------
if __name__ == '__main__':
	pa = PageAccueil('Minitel Home Services', '1.0', 'Nicolas Lermé')
	pa.ajouter_service(ServiceMeteo(pa, 'Prévisions météo'))
	pa.ajouter_service(ServiceAnnuaire(pa, 'Annuaire téléphonique'))
	pa.ajouter_service(ServiceReseauLocal(pa, 'Réseau local'))
	pa.ajouter_service(ServiceTelFixe(pa, 'Messages / appels'))
	pa.ajouter_service(ServiceMinitel(pa, 'Informations système'))
	pa.ajouter_service(ServiceSonnette(pa, 'Historique sonnette'))
	pa.ajouter_service(ServiceWifi(pa, 'Réglages wifi'))
	pa.ajouter_service(ServiceVolets(pa, 'Pilotage volets'))
	pa.executer()
