mport yaml, requests, pprint

conf = yaml.safe_load(open('/home/goudot/config.yml', 'r'))
print(conf)
conf = conf['pole_emploi']
print('conf:', conf)

# On renseigne les variables utilisées pour la requète POST
URL = 'https://entreprise.pole-emploi.fr/connexion/oauth2/access_token'
app = 'api_anoteav1 api_evenementsv1 evenements'
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
print("-------------------------------------------------")

# Utilisation du token pour faire une requête anotea
# https://pole-emploi.io/data/api/anotea?tabgroup-api=documentation&doc-section=api-doc-section-rechercher-les-notes-et-avis-d$
URL = 'https://api.emploi-store.fr/partenaire/anotea/v1/avis'
params={"page":"1", "items_par_page":"10", "certif_info":"88141"}
headers = {"Authorization": "Bearer "+token}

req = requests.get(URL, params=params, headers=headers)
resp = req.json()

for avis in resp['avis']:
    print(avis['id'], avis['date'])

#~ pprint.pprint(resp)

print("-------------------------------------------------")