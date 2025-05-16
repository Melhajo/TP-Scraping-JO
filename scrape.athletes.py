
import requests
from bs4 import BeautifulSoup
import json
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "https://olympics-statistics.com"
ALPHABET = [chr(i) for i in range(97, 123)] + ["special"]
medal_map = {"1": "or", "2": "argent", "3": "bronze"}

def get_athletes_for_letter(letter):
    url = f"{BASE_URL}/olympic-athletes/{letter}"
    print(f"🔠 Lettre '{letter}' : chargement des athlètes...")
    try:
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        cards = soup.select("a.card.athlet.visible")
        athletes = []
        for card in cards:
            first_name = card.select_one(".vn").text.strip()
            last_name = card.select_one(".n").text.strip()
            profile_url = BASE_URL + card["href"]
            athletes.append((first_name, last_name, profile_url))
        print(f"✅ {len(athletes)} athlètes trouvés pour '{letter}'")
        return athletes
    except Exception as e:
        print(f"❌ Erreur chargement lettre '{letter}' : {e}")
        return []

def scrape_profile(info):
    first_name, last_name, profile_url = info
    palmares = []
    country = None

    for attempt in range(5):
        try:
            resp = requests.get(profile_url, timeout=20)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            medals = soup.select(".medaille.visible")
            for block in medals:
                medal_tag = block.select_one(".the-medal")
                medal = medal_map.get(medal_tag["data-medal"], "inconnu") if medal_tag else "inconnu"
                sport = block.select_one(".m-sport")
                event = block.select_one(".m-eventname")
                city = block.select_one(".m-event-stadt")
                if not country:
                    try:
                        country = block.select_one("img.f")["title"]
                    except:
                        country = None
                palmares.append({
                    "medal": medal,
                    "sport": sport.text.strip() if sport else "",
                    "event": event.text.strip() if event else "",
                    "city": city.text.strip() if city else ""
                })
            print(f"🎯 {first_name} {last_name} → {len(palmares)} médaille(s)")
            return {
                "first_name": first_name,
                "last_name": last_name,
                "country": country,
                "palmares": palmares
            }
        except Exception as e:
            print(f"⚠️ Tentative {attempt+1}/5 échouée pour {first_name} {last_name} — {e}")
            time.sleep(random.uniform(1, 2))
    print(f"❌ Échec après 5 tentatives : {first_name} {last_name}")
    return None

def process_letter(letter):
    athletes_list = get_athletes_for_letter(letter)
    if not athletes_list:
        return []

    results = []
    print(f"🚀 Traitement de {len(athletes_list)} athlètes avec 5 threads...")

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(scrape_profile, athlete) for athlete in athletes_list]
        for fut in as_completed(futures):
            r = fut.result()
            if r:
                results.append(r)

    print(f"✅ Lettre '{letter}' terminée — {len(results)} athlètes traités.\n")
    return results

if __name__ == "__main__":
    all_athletes = []
    for letter in ALPHABET:
        results = process_letter(letter)
        all_athletes.extend(results)

    with open("athletes_all.json", "w", encoding="utf-8") as f:
        json.dump(all_athletes, f, ensure_ascii=False, indent=2)

    print("🎉 Tous les athlètes ont été enregistrés dans 'athletes_all.json'")
