#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  3 21:51:05 2021

@author: formateur
"""

import yaml, requests, pprint

conf = yaml.safe_load(open('/home/formateur/uno/projet_8/config.yml', 'r'))
print(conf)
print('conf:', conf)

# On renseigne les variables utilisées pour la requète POST
URL = 'https://entreprise.pole-emploi.fr/connexion/oauth2/access_token'
app = 'api_offresdemploiv2 o2dsoffre'
scope="application_"+conf['PAR']+" "+app
print('scope: ', scope)

params={"realm":"/partenaire"}
post_data = {"grant_type": "client_credentials",
        "client_id": conf['PAR'],
        "client_secret": conf['SEC'],
        "scope": scope}
headers = {"content-type": "application/x-www-form-urlencoded"}

# Execution de la requète
req = requests.post(URL, params=params, data=post_data, headers=headers)
resp = req.json()
pprint.pprint(resp)

# Le token !!!
token = resp['access_token']
print("access token: ", token)
print()
print("-------------------------------------------------")

# Utilisation du token pour faire une requête anotea
# https://pole-emploi.io/data/api/anotea?tabgroup-api=documentation&doc-section=api-doc-section-rechercher-les-notes-et-avis-d$
URL = 'https://api.emploi-store.fr/partenaire/offresdemploi/v2/offres/search'
params={"page":"1", "items_par_page":"10", "certif_info":"88141"}
             # demander d'où viennent ces paramètres
headers = {"Authorization": "Bearer "+token}

req = requests.get(URL, params=params, headers=headers)
resp = req.json()

#pprint.pprint(resp)

for resultats in resp['resultats']:
    print(resultats['id'], resultats['appellationlibelle'])

#~ pprint.pprint(resp)

print("-------------------------------------------------")