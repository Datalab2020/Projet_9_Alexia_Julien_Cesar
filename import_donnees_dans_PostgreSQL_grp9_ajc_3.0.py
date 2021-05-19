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
import re

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
                    
                    # Nous recherchons le numéro de département de chaque entrée
                    test_uno = re.findall(r'\d\d', resultats['lieuTravail']['libelle'])
                    
                    # S'il y a un numéro de région:
                    if test_uno:
                      Insee_departement = test_uno[0]
                      
                      if Insee_departement == "18":
                          departement = "Cher"
                      elif Insee_departement == "28":
                          departement = "Eure-et-Loir"
                      elif Insee_departement == "36":
                          departement = "Indre"
                      elif Insee_departement == "37":
                          departement = "Indre-et-Loire"
                      elif Insee_departement == "41":
                          departement = "Loir-et-Cher"
                      elif Insee_departement == "45":
                          departement = "Loiret"
                      elif Insee_departement == "75":
                          departement = "Paris"
                      elif Insee_departement == "77":
                          departement = "Seine-et-Marne"
                      elif Insee_departement == "78":
                          departement = "Yvelines"
                      elif Insee_departement == "91":
                          departement = "Essonne"
                      elif Insee_departement == "92":
                          departement = "Hauts-de-Seine"
                      elif Insee_departement == "93":
                          departement = "Seine-Saint-Denis"
                      elif Insee_departement == "94":
                          departement = "Val-de-Marne"
                      elif Insee_departement == "95":
                          departement = "Val-d'Oise"
                        
                    # S'il n'y a pas de numéro de région:
                    elif resultats['lieuTravail']['libelle'] == "Ile-de-France":
                        departement = None
                        Insee_departement = None
                    
                     
                        
                            
                    #print(f" {Insee_departement} - {departement} - Département / Insee region - {region} Region - {nom_region} ")
                    
                    
                    
                    # resultats['id'])
                    # resultats['intitule']
                    desc = resultats['description'] if ('description' in resultats) else None
                    #resultats['dateCreation']
                    datAct = resultats['dateActualisation'] if ('dateActualisation' in resultats) else None 
                    lieuLi = resultats['lieuTravail']['libelle'] if ('lieuTravail' in resultats)and('libelle' in resultats['lieuTravail']) else None
                    lieuLa = resultats['lieuTravail']['latitude'] if ('lieuTravail' in resultats)and('latitude' in resultats['lieuTravail']) else None
                    lieuLo = resultats['lieuTravail']['longitude'] if ('lieuTravail' in resultats)and('longitude' in resultats['lieuTravail']) else None
                    lieuCod = resultats['lieuTravail']['codePostal'] if ('lieuTravail' in resultats)and('codePostal' in resultats['lieuTravail']) else None
                    romCod = resultats['romeCode'] if ('romeCode' in resultats) else None
                    romLib = resultats['romeLibelle'] if ('romeLibelle' in resultats) else None
                    appelLi = resultats['appellationlibelle'] if ('appellationlibelle' in resultats) else None
                    entNo = resultats['entreprise']['nom'] if ('entreprise' in resultats)and('nom' in resultats['entreprise']) else None
                    # resultats['typeContrat']
                    # resultats['typeContratLibelle']
                    natCo = resultats['natureContrat'] if ('natureContrat' in resultats) else None
                    expEx = resultats['experienceExige'] if ('experienceExige' in resultats) else None
                    expLi = resultats['experienceLibelle'] if ('experienceLibelle' in resultats) else None
                    #** formDom = resultats['formations']['domaineLibelle'] if ('formations' in resultats)and('domaineLibelle' in resultats['formations']) else None
                    #** formNiv = resultats['formations']['niveauLibelle'] if ('formations' in resultats)and('niveauLibelle' in resultats['formations']) else None
                    #** lalLi = resultats['langues']['libelle'] if ('langues' in resultats)and('libelle' in resultats['langues']) else None
                    #** compLib = resultats['competences']['libelle'] if ('competences' in resultats)and('libelle' in resultats['competences']) else None
                    salLi = resultats['salaire']['libelle'] if ('salaire' in resultats)and('libelle' in resultats['salaire']) else None
                    durTrLi = resultats['dureeTravailLibelleConverti'] if ('dureeTravailLibelleConverti' in resultats) else None
                    altern = resultats['alternance'] if ('alternance' in resultats) else None
                    nomPost = resultats['nombrePostes'] if ('nombrePostes' in resultats) else None
                    accesTH = resultats['accessibleTH'] if ('accessibleTH' in resultats) else None
                    # resultats['origineOffre']['origine']
                    # resultats['origineOffre']['urlOrigine']
                
                    #print(resultats['id'], resultats['appellationlibelle'], resultats['lieuTravail']['libelle'], "--", resultats['dateCreation'])
                    
                    
                    
                    if salLi != None:
                        test_Salaire = re.findall(r'\d\d\d\d\d', salLi) # ici je recherche s'il y a un nombre à 5 chiffres dans le texte
                        if test_Salaire:
                            
                            if len(test_Salaire) == 1:  
                                SalaireAnnuel1 = test_Salaire[0]
                                SalaireAnnuel2 = None
                                SalaireMensuel1 = int(test_Salaire[0])/12
                                SalaireMensuel2 = None
                                SalaireHoraire1 = SalaireMensuel1/(4.5*35)
                                SalaireHoraire2 = None
                                print(f" Salaire annuel- {SalaireAnnuel1}/{SalaireAnnuel2} || Salaire Mensuel- {SalaireMensuel1}/{SalaireMensuel2} || Salaire Horaire- {SalaireHoraire1}/{SalaireHoraire2}")
                            else:
                                SalaireAnnuel1 = test_Salaire[0]
                                SalaireAnnuel2 = test_Salaire[1]
                                SalaireMensuel1 = int(test_Salaire[0])/12
                                SalaireMensuel2 = int(test_Salaire[1])/12
                                SalaireHoraire1 = SalaireMensuel1/(4.5*35)
                                SalaireHoraire2 = SalaireMensuel2/(4.5*35)
                                print(f" Salaire annuel- {SalaireAnnuel1}/{SalaireAnnuel2} || Salaire Mensuel- {SalaireMensuel1}/{SalaireMensuel2} || Salaire Horaire- {SalaireHoraire1}/{SalaireHoraire2}")
                        else:
                            test_Salaire = re.findall(r'\d\d\d\d', salLi) # ici je recherche s'il y a un nombre à 4 chiffres dans le texte
                            if test_Salaire: 
                                
                                if len(test_Salaire) == 1:
                                    SalaireAnnuel1 = int(test_Salaire[0])*12
                                    SalaireAnnuel2 = None
                                    SalaireMensuel1 = test_Salaire[0]
                                    SalaireMensuel2 = None
                                    SalaireHoraire1 = int(test_Salaire[0])/(35*4.5)
                                    SalaireHoraire2 = None
                                    print(f" Salaire annuel- {SalaireAnnuel1}/{SalaireAnnuel2} || Salaire Mensuel- {SalaireMensuel1}/{SalaireMensuel2} || Salaire Horaire- {SalaireHoraire1}/{SalaireHoraire2}")
                                else:
                                    SalaireAnnuel1 = int(test_Salaire[0])*12
                                    SalaireAnnuel2 = int(test_Salaire[1])*12
                                    SalaireMensuel1 = test_Salaire[0]
                                    SalaireMensuel2 = test_Salaire[1]
                                    SalaireHoraire1 = int(test_Salaire[0])/(35*4.5)
                                    SalaireHoraire2 = int(test_Salaire[1])/(35*4.5)
                                        
                                    print(f" Salaire annuel- {SalaireAnnuel1}/{SalaireAnnuel2} || Salaire Mensuel- {SalaireMensuel1}/{SalaireMensuel2} || Salaire Horaire- {SalaireHoraire1}/{SalaireHoraire2} ")
                                
                            
                            else:
                                test_Salaire = re.findall(r"\b\d\d,\d\d", salLi) # ici, je cherche s'il y a un nombre qui commence par deux chiffres, qui a une virgule et qui a ensuite deux autres chiffres
                                if test_Salaire:
                                    
                                    if len(test_Salaire) == 1:
                                        SalaireAnnuel1 = 35*52*float(re.sub(",", ".", test_Salaire[0])) # ici je passe les unités décimales de ',' à '.' Pour pouvoir faire des calculs, alors je multiplie par 35 (heures hebdomadaires), puis par 52 (semaines dans l'année)
                                        SalaireAnnuel2 = None
                                        SalaireMensuel1 = SalaireAnnuel1/12
                                        SalaireMensuel2 = None
                                        SalaireHoraire1 = re.sub(",", ".", test_Salaire[0])
                                        SalaireHoraire2 = None
                                        
                                        print(f" Salaire annuel- {SalaireAnnuel1}/{SalaireAnnuel2} || Salaire Mensuel- {SalaireMensuel1}/{SalaireMensuel2} || Salaire Horaire- {SalaireHoraire1}/{SalaireHoraire2}")
                                    else:
                                        SalaireAnnuel1 = 35*52*float(re.sub(",", ".", test_Salaire[0])) 
                                        SalaireAnnuel2 = 35*52*float(re.sub(",", ".", test_Salaire[1]))
                                        SalaireMensuel1 = SalaireAnnuel1/12
                                        SalaireMensuel2 = SalaireAnnuel2/12
                                        SalaireHoraire1 = re.sub(",", ".", test_Salaire[0])
                                        SalaireHoraire2 = re.sub(",", ".", test_Salaire[1])
                                        
                                        print(f" Salaire annuel- {SalaireAnnuel1}/{SalaireAnnuel2} || Salaire Mensuel- {SalaireMensuel1}/{SalaireMensuel2} || Salaire Horaire- {SalaireHoraire1}/{SalaireHoraire2}")
                                    
                                    #print(f" Salaire Horaire - {test_Salaire} ")
                                    # re.sub(",", ".", test_Salaire[0])
                            
                                #else:
                                    #None
                    else:
                        SalaireAnnuel1 = None
                        SalaireAnnuel2 = None
                        SalaireMensuel1 = None
                        SalaireMensuel2 = None
                        SalaireHoraire1 = None
                        SalaireHoraire2 = None
                        print(f" Salaire annuel- {SalaireAnnuel1}/{SalaireAnnuel2} || Salaire Mensuel- {SalaireMensuel1}/{SalaireMensuel2} || Salaire Horaire- {SalaireHoraire1}/{SalaireHoraire2}")
                    
                    
                    
                    cur.execute("""INSERT INTO public."projet_Job_IO_ajc_2" VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;""",    
                    (resultats['id'], 
                     resultats['intitule'], 
                     resultats['description'], 
                     resultats['dateCreation'], 
                     datAct,
                     lieuLi,
                     Insee_departement,
                     departement,
                     region,
                     nom_region,
                     lieuLa,
                     lieuLo,
                     lieuCod,                     
                     romCod,
                     romLib,
                     appelLi,
                     entNo,
                     resultats['typeContrat'],
                     resultats['typeContratLibelle'],
                     natCo,
                     expEx,
                     expLi,                     
                     salLi,
                     SalaireAnnuel1,
                     SalaireAnnuel2,
                     SalaireMensuel1,
                     SalaireMensuel2,
                     SalaireHoraire1,
                     SalaireHoraire2,
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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    