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
params={"realm":"/partenaire","range":"10"}

post_data = {"grant_type": "client_credentials",
        "client_id": conf2['id_client'],
        "client_secret": conf2['Cle_S'],
        "scope": scope}
headers = {"content-type": "application/x-www-form-urlencoded"}

# Exc Requête
req = requests.post(URL, params=params, data = post_data, headers=headers)
resp = req.json()
token = resp['access_token']


# Affiche le token print('Token :' ,token)
#----------------------------------------------------

# Utilisation l'API du token pour réaliser la requête 

URL_2 = 'https://api.emploi-store.fr/partenaire/offresdemploi/v2/offres/search'
params={"page":"1", "items_par_page":"10", "certif_info":"88141"}
headers = {"Authorization": "Bearer "+token}

req = requests.get(URL_2, params=params, headers=headers)
response = req.json()



for e in response['resultats']:
    print('_________________________________')
    print(pprint.pprint(e))
#---------------------------------------------------

# Insert données dans mongo
conf_Mongo2 = conf_Mongo['mongo']

co = 'mongodb://%s:%s@%s/?authSource=%s' % (conf_Mongo2['user'], conf_Mongo2['password'], conf_Mongo2['host'], conf_Mongo2['authSource'])

client = MongoClient(co)

#db = client['Datalab2020']
#collec = db['TeamFrite_2']
#collec.insert_one({"TeamFrite_2": response})