import requests
import json
import html # Module utile pour "nettoyer" du texte contenant 
            # des caractères HTML (ex: &nbsp;, &amp;)

# --- Infos de connexion à l'API Algolia utilisée par Instant Gaming ---
# On les a récupérées en observant l'onglet "Réseau" du navigateur (F12).
# C'est une clé PUBLIQUE en lecture seule (pas un mot de passe secret),
# donc pas de souci à l'utiliser ici.

APPLICATION_ID = "QKNHP8TC3Y"
API_KEY = "93946b91c013211f842ddf1819ea880b"
INDEX_NAME = "produits_fr_spotlighted_desc" # Le "dossier" de données dans lequel Algolia va chercher

# On construit l'URL de l'API dynamiquement avec une f-string 
url = f"https://{APPLICATION_ID.lower()}-dsn.algolia.net/1/indexes/{INDEX_NAME}/query"



headers = {
    "X-Algolia-Application-Id": APPLICATION_ID, # Dit à Algolia quel client (quel site) fait la demande
    "X-Algolia-API-Key": API_KEY, # La clé qui autorise l'accès à cet index
    "Content-Type": "application/json",
# Prévient le serveur : "je t'envoie du JSON, pas du texte brut
        # Le Referer indique "d'où" vient la requête (quelle page l'a déclenchée).
    # Algolia vérifie cette info pour bloquer les requêtes venant d'ailleurs que du vrai site.
    "Referer": "https://www.instant-gaming.com/",

    # L'Origin est proche du Referer : il indique le domaine d'où part la requête.
    # Certains serveurs vérifient l'un, l'autre, ou les deux.
    "Origin": "https://www.instant-gaming.com",

    # Le User-Agent fait croire au serveur qu'on est un vrai navigateur (Chrome sous Linux ici)
    # plutôt qu'un script Python, ce qui évite d'être bloqué par certaines protections anti-bot.
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
}

def get_game_price(nom_du_jeu):
        # Le "payload" est le contenu réel de notre demande : on dit à Algolia
    # "cherche-moi ce texte" (query) et "donne-moi au maximum 5 résultats" (hitsPerPage).
    payload = {
        "query": nom_du_jeu,
        "hitsPerPage": 20
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print("Status:", response.status_code)

    if response.status_code == 200:
        data = response.json()
        for hit in data.get("hits", []):
            prix = html.unescape(hit.get("price_formatted", "")).replace("\xa0", " ")
            print(f"{hit.get('fullname')} — {prix} ({hit.get('platform')} — stock: {hit.get('has_stock')})")
    else:
        print("Erreur:", response.text)

get_game_price("")