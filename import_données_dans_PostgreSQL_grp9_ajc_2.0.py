#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  4 10:38:55 2021

@author: formateur
"""

#!/usr/bin/python3


import yaml, requests, pprint  # import librairies
import psycopg2 
import psycopg2.extras
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


# -----------------------------------------------------------

# connexion à postgres
conf = confAll['postgres']
#print('conf:', conf)

# connection à PG
conn = psycopg2.connect(database="bdd_projet9_ajc", user=conf['user'], password=conf['password'], host=conf['host']) 

conn.autocommit = True
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)# session

# ----------------------------------------------------

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
                            
                    print(f"Region {region} - {mot_cle} - {resultats['id']} {resultats['appellationlibelle']} - {resultats['lieuTravail']['libelle']}")
                    
                    # resultats['id'])
                    # resultats['intitule']
                    desc = resultats['description'] if ('description' in resultats) else "NULL"
                    #resultats['dateCreation']
                    datAct = resultats['dateActualisation'] if ('dateActualisation' in resultats) else resultats['dateCreation'] 
                    lieuLi = resultats['lieuTravail']['libelle'] if ('lieuTravail' in resultats)and('libelle' in resultats['lieuTravail']) else "NULL"
                    lieuLa = resultats['lieuTravail']['latitude'] if ('lieuTravail' in resultats)and('latitude' in resultats['lieuTravail']) else 0
                    lieuLo = resultats['lieuTravail']['longitude'] if ('lieuTravail' in resultats)and('longitude' in resultats['lieuTravail']) else 0
                    lieuCod = resultats['lieuTravail']['codePostal'] if ('lieuTravail' in resultats)and('codePostal' in resultats['lieuTravail']) else 0
                    lieuCom = resultats['lieuTravail']['commune'] if ('lieuTravail' in resultats)and('commune' in resultats['lieuTravail']) else 0
                    romCod = resultats['romeCode'] if ('romeCode' in resultats) else "NULL"
                    romLib = resultats['romeLibelle'] if ('romeLibelle' in resultats) else "NULL"
                    appelLi = resultats['appellationlibelle'] if ('appellationlibelle' in resultats) else "NULL"
                    entNo = resultats['entreprise']['nom'] if ('entreprise' in resultats)and('nom' in resultats['entreprise']) else "NULL"
                    # resultats['typeContrat']
                    # resultats['typeContratLibelle']
                    natCo = resultats['natureContrat'] if ('natureContrat' in resultats) else "NULL"
                    expEx = resultats['experienceExige'] if ('experienceExige' in resultats) else "NULL"
                    expLi = resultats['experienceLibelle'] if ('experienceLibelle' in resultats) else "NULL"
                    formDom = resultats['formations']['domaineLibelle'] if ('formations' in resultats)and('domaineLibelle' in resultats['formations']) else "NULL"
                    formNiv = resultats['formations']['niveauLibelle'] if ('formations' in resultats)and('niveauLibelle' in resultats['formations']) else "NULL"
                    lalLi = resultats['langues']['libelle'] if ('langues' in resultats)and('libelle' in resultats['langues']) else "NULL"
                    compLib = resultats['competences']['libelle'] if ('competences' in resultats)and('libelle' in resultats['competences']) else "NULL"
                    salLi = resultats['salaire']['libelle'] if ('salaire' in resultats)and('libelle' in resultats['salaire']) else "NULL"
                    durTrLi = resultats['dureeTravailLibelleConverti'] if ('dureeTravailLibelleConverti' in resultats) else "NULL"
                    altern = resultats['alternance'] if ('alternance' in resultats) else False
                    nomPost = resultats['nombrePostes'] if ('nombrePostes' in resultats) else 0
                    accesTH = resultats['accessibleTH'] if ('accessibleTH' in resultats) else False
                    # resultats['origineOffre']['origine']
                    # resultats['origineOffre']['urlOrigine']
                
                    print(resultats['id'], resultats['appellationlibelle'], resultats['lieuTravail']['libelle'], "--", resultats['dateCreation'])
                    cur.execute("""INSERT INTO public."projet_Job_IO_ajc" VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;""",    
                    (resultats['id'], 
                     resultats['intitule'], 
                     resultats['description'], 
                     resultats['dateCreation'], 
                     datAct,
                     lieuLi,
                     lieuLa,
                     lieuLo,
                     lieuCod,
                     lieuCom,
                     romCod,
                     romLib,
                     appelLi,
                     entNo,
                     resultats['typeContrat'],
                     resultats['typeContratLibelle'],
                     natCo,
                     expEx,
                     expLi,
                     formDom,
                     formNiv,
                     lalLi,
                     compLib,
                     salLi,
                     durTrLi,
                     altern,
                     nomPost,
                     accesTH,
                     resultats['origineOffre']['origine'],
                     resultats['origineOffre']['urlOrigine'] )) # INSERT avec paramètres
                    
                print()
                nom_result = len(resp["resultats"])
                print(f"résultats = {nom_result}")
                        
                print("-------------------------------------------------")
                i += 1
                debut = i*100
                fin = i*100 + 105
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    