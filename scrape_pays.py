
import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Base URL du site
BASE_URL = "https://olympics-statistics.com"
URL_NATIONS = urljoin(BASE_URL, "/nations")
FICHIER_JSON = "donnees_pays_medailes.json"

# Traduction des codes médailles HTML → texte lisible
CODE_MEDAILLE = {
    "1": "or",
    "2": "argent",
    "3": "bronze"
}

def charger_page_nations():
    response = requests.get(URL_NATIONS)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def recuperer_liens_pays(soup):
    resultats = []
    blocs = soup.select("a.card.nation.visible")
    for bloc in blocs:
        nom_pays = bloc.select_one("div.bez").text.strip()
        lien_relatif = bloc["href"]
        url_complet = urljoin(BASE_URL, lien_relatif)
        resultats.append((nom_pays, url_complet))
    return resultats

def extraire_statistiques(url_pays):
    reponse = requests.get(url_pays)
    reponse.raise_for_status()
    page = BeautifulSoup(reponse.text, "html.parser")

    stats = {"or": 0, "argent": 0, "bronze": 0}
    section = page.select_one(".rnd.teaser")
    if section:
        blocs = section.select("div:has(div.the-medal)")
        for bloc in blocs:
            code = bloc.select_one("div.the-medal")["data-medal"]
            quantite = int(bloc.select_one("span.mal").text.strip())
            if code in CODE_MEDAILLE:
                stats[CODE_MEDAILLE[code]] = quantite
    return stats

def lancer_collecte():
    soup = charger_page_nations()
    pays_et_liens = recuperer_liens_pays(soup)

    donnees = []
    for nom, url in pays_et_liens:
        medailles = extraire_statistiques(url)
        donnees.append({"pays": nom, **medailles})
        print(f"✅ {nom} → 🥇 {medailles['or']} | 🥈 {medailles['argent']} | 🥉 {medailles['bronze']}")

    with open(FICHIER_JSON, "w", encoding="utf-8") as sortie:
        json.dump(donnees, sortie, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    lancer_collecte()
