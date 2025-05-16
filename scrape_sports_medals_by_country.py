import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import time

# Configuration principale
BASE = "https://olympics-statistics.com"
ENDPOINT = "/olympic-sports"
FICHIER_SORTIE = "export_medals.json"
CODES_MEDAILLE = {"1": "gold", "2": "silver", "3": "bronze"}

print("📡 Initialisation du scraping olympique...")

try:
    print("🔗 Récupération de la page des sports...")
    res = requests.get(urljoin(BASE, ENDPOINT))
    res.raise_for_status()
    doc = BeautifulSoup(res.text, "html.parser")

    sports = [
        {
            "nom": tag.select_one(".bez").text.strip(),
            "lien": urljoin(BASE, tag.get("href"))
        }
        for tag in doc.select("a.card.sport.visible")
    ]

    print(f"✅ {len(sports)} sports trouvés.")

    resultat_final = []

    for sp in sports:
        print(f"\n🎯 {sp['nom']}...")
        try:
            r = requests.get(sp["lien"])
            r.raise_for_status()
            s = BeautifulSoup(r.text, "html.parser")
            bloc = s.select_one('div.top[data-which="n"]')

            donnees = []
            if bloc:
                cartes = bloc.select("div.card.nation.visible")
                for carte in cartes:
                    pays = carte.select_one("img.f")
                    nom_pays = pays["title"].strip() if pays else "Inconnu"

                    med = {"gold": 0, "silver": 0, "bronze": 0}
                    for icone in carte.select("div.the-medal"):
                        code = icone.get("data-medal")
                        conteneur = icone.find_parent("div")
                        nombre = int(conteneur.select_one("span.mal").text.strip())
                        if code in CODES_MEDAILLE:
                            med[CODES_MEDAILLE[code]] = nombre

                    donnees.append({"pays": nom_pays, **med})

            resultat_final.append({"discipline": sp["nom"], "medailles": donnees})
            time.sleep(0.5)  # Pause légère pour respect du serveur

        except Exception as erreur:
            print(f"⚠️ Erreur avec {sp['nom']} : {erreur}")

    with open(FICHIER_SORTIE, "w", encoding="utf-8") as out:
        json.dump(resultat_final, out, indent=2, ensure_ascii=False)

    print("\n📁 Export JSON terminé avec succès !")

except Exception as global_err:
    print(f"❌ Erreur globale : {global_err}")
