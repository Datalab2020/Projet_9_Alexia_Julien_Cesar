#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  3 19:11:26 2021

@author: garcia
"""
import pprint
import requests
import yaml
from pymongo import MongoClient
# Lecture du ficier conf 
conf = yaml.safe_load(open('conf.yml', 'r'))
conf2 = conf['pole_emploi']

# Mongo_db
conf_Mongo = yaml.safe_load(open('conf.yml', 'r'))

#----------------------------------------------- Partie 1
# Variable Params  Post 
URL = 'https://entreprise.pole-emploi.fr/connexion/oauth2/access_token'
app ='api_offresdemploiv2 o2dsoffre'

scope= f"application_{conf2['id_client']} {app}"

params1={"realm":"/partenaire"}

post_data = {"grant_type": "client_credentials",
        "client_id": conf2['id_client'],
        "client_secret": conf2['Cle_S'],
        "scope": scope}
headers = {"content-type": "application/x-www-form-urlencoded"}

# Exc Requête
req = requests.post(URL, params=params1, data = post_data, headers=headers)
resp = req.json()
token = resp['access_token']


# Affiche le token print('Token :' ,token)
#----------------------------------------------------

# Utilisation l'API du token pour réaliser la requête 

cpt = -1

for loops in range(0, 2):

    nb_avant = loops * 10
    nb_apres = (loops * 10) + 10

    nb_avant_text = str(nb_avant)
    nb_apres_text = str(nb_apres)
    
    URL_2 = 'https://api.emploi-store.fr/partenaire/offresdemploi/v2/offres/search'
    params2= {"page":"1", "items_par_page":"10", "certif_info":"88141", "range":f"{nb_avant_text}-{nb_apres_text}"}
    print(params2)
       
    headers2 = {"Authorization": "Bearer "+ token}
    req = requests.get(URL_2, params=params2, headers=headers2)

    response = req.json()
    
    for element in response['resultats']:
    
        print(element['intitule'])
        print('----------------')
        print('avant:' , nb_avant)
        print('apres:' , nb_apres)
    
        #cpt = cpt + 1
        #print(element['intitule'])
 
        #print(cpt)'''''
#---------------------------------------------------

# Insert données dans MONGO
    conf_Mongo2 = conf_Mongo['mongo']
    co = 'mongodb://%s:%s@%s/?authSource=%s' % (conf_Mongo2['user'], conf_Mongo2['password'], conf_Mongo2['host'], conf_Mongo2['authSource'])
    client = MongoClient(co)

#db = client['Datalab2020']
#collec = db['TeamFrite_2']
#collec.insert_one({"TeamFrite_2": response})