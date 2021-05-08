#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  4 10:38:55 2021

@author: formateur
"""

#!/usr/bin/python3

import yaml, requests, pprint
import pymongo
from pymongo import MongoClient
from datetime import datetime

print("#################################################")
print("#################################################")
print()
print(f"{datetime.now()} (Date d'importation des données)")
print()

confAll = yaml.safe_load(open('/home/formateur/uno/projet_9/config.yml', 'r'))
#print(confAll)

options_mot_cle = ("Data", "données", "python")
option_region =  (11, 24)

# Régions en France (Code INSEE):
# Auvergne-Rhône-Alpes - 84, Bourgogne-Franche-Comté - 27, Bretagne - 53, 
# Centre-Val de Loire - 24, Corse - 94, Grand Est - 44, Hauts-de-France - 32, 
# Île-de-France - 11, Normandie - 28, 
# Nouvelle-Aquitaine - 75, Occitanie - 76, Pays de la Loire - 52, Provence-Alpes-Côte d'Azur - 93


conf = confAll['mongo']
str = 'mongodb://%s:%s@%s/?authSource=%s' % (conf['user'], conf['password'], conf['host'], conf['authSource'])
#print("mongo conn:", str)
client = MongoClient(str)
db = client['bdd_projet9_ajc']
collec = db['Jobs_data_regions_Centre_et_Ile_de_France']
# collec.save({"pole_emploi_1": "test"})

conf = confAll['pole_emploi']
#print('conf:', conf)

# On renseigne les variables utilisées pour la requète POST
URL_token = 'https://entreprise.pole-emploi.fr/connexion/oauth2/access_token'
app = 'api_offresdemploiv2 o2dsoffre'
scope="application_"+conf['PAR']+" "+app
#print('scope: ', scope)

params_token={"realm":"/partenaire"}
post_data = {"grant_type": "client_credentials",
        "client_id": conf['PAR'],
        "client_secret": conf['SEC'],
        "scope": scope}
headers_token = {"content-type": "application/x-www-form-urlencoded"}

# Execution de la requète
req_token = requests.post(URL_token, params=params_token, data=post_data, headers=headers_token)
resp_token = req_token.json()
#pprint.pprint(resp)
status = req_token.status_code
print(f"Génération de token, status = {status}")
print()

# Le token !!!
token = resp_token['access_token']
#print("access token: ", token)

print("-------------------------------------------------")

 


for region in option_region:            # effectue tout le processus qui suit pour chacune des options de la liste option_region
    
    if region == 11:
        nom_region = "Île-de-France"
    elif region == 24:
        nom_region = "Centre-Val de Loire"
        
        
    for mot_cle in options_mot_cle:     # effectue tout le processus qui suit pour chacune des options de la liste options_mot_cle
        #print(mot_cle)
        i = 0
        debut = 0
        fin = 100
        nom_result = 100
        while nom_result >= 100:        # cette boucle while permet rechercher tous les résultats en les retournant par groupes de 100
            print(f"{debut} - {fin} / option: {mot_cle}, région: {nom_region}")
            print()
            URL = 'https://api.emploi-store.fr/partenaire/offresdemploi/v2/offres/search'
            params={"motsCles":mot_cle, "region":region, "range":f"{debut}-{fin}", "sort":1}
            headers = {"Authorization": "Bearer "+token}
            
            req = requests.get(URL, params=params, headers=headers)
            resp = req.json()
            try:                                    # teste s'il y a une erreur
                resp_bucle = resp['resultats'] 
            except:                                  # avec cette instruction, cette partie est terminée si en raison de la boucle, de mauvais paramètres sont entrés (le nombre à l'entrée ne peut excéder mille)
                pprint.pprint(resp)
                print()
                print("-------------------------------------------------")                
                break                              
            else:              
                  
                for resultats in resp_bucle:
                    try:                            # teste s'il y a une erreur
                        collec.save(resultats)
                        
                    except pymongo.errors.DuplicateKeyError:                        # s'il y a une erreur d'insertion due à l'index unique, le programme ignore cette entrée
                        #print(f"Region {region} - {mot_cle} déjà dans la bdd")
                        continue
                    
                    else:        
                        print(f"Region {region} - {mot_cle} - {resultats['id']} {resultats['appellationlibelle']} - {resultats['lieuTravail']['libelle']}")
                print()
                nom_result = len(resp["resultats"])
                print(f"résultats = {nom_result}")
                        
                print("-------------------------------------------------")
                i += 1
                debut = i*100
                fin = i*100 + 105
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    