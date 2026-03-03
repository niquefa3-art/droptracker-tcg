import json
import os
import datetime
import requests
from bs4 import BeautifulSoup

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(THIS_FOLDER, "data.json")

def faire_la_veille():
    print(f"[{datetime.datetime.now()}] 🚀 Lancement de la veille...")
    nouvelles_donnees = []
    
    # On se déguise en vrai navigateur
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    url_geeky = "https://www.thegeekypop.com/fr/15-pokemon"
    
    try:
        reponse = requests.get(url_geeky, headers=headers)
        
        if reponse.status_code != 200:
            nouvelles_donnees.append({
                "categorie": "🚨 SÉCURITÉ",
                "tagClass": "tag-onepiece",
                "titre": f"Site bloqué (Erreur {reponse.status_code})",
                "date": "Veille échouée",
                "prix": "0.00",
                "boutique": "The Geeky Pop",
                "lien": url_geeky
            })
        else:
            soup = BeautifulSoup(reponse.text, 'html.parser')
            produits_html = soup.find_all('article', class_='product-miniature')
            
            if len(produits_html) == 0:
                nouvelles_donnees.append({
                    "categorie": "⚠️ CODE HTML",
                    "tagClass": "tag-pokemon",
                    "titre": "Balises introuvables",
                    "date": "Le design du site a changé",
                    "prix": "0.00",
                    "boutique": "The Geeky Pop",
                    "lien": url_geeky
                })
            else:
                for prod in produits_html[:4]:
                    titre_tag = prod.find('h3', class_='h3 product-title')
                    titre = titre_tag.text.strip() if titre_tag else "Produit inconnu"
                    
                    prix_tag = prod.find('span', class_='price')
                    prix = prix_tag.text.replace('€', '').strip() if prix_tag else "N/A"
                    
                    lien_tag = prod.find('a')
                    lien_exact = lien_tag['href'] if lien_tag else url_geeky
                    
                    nouvelles_donnees.append({
                        "categorie": "POKÉMON",
                        "tagClass": "tag-pokemon",
                        "titre": titre,
                        "date": "Vérifié avec succès",
                        "prix": prix,
                        "boutique": "The Geeky Pop",
                        "lien": lien_exact
                    })
                    
    except Exception as e:
        nouvelles_donnees.append({
            "categorie": "🐛 BUG",
            "tagClass": "tag-onepiece",
            "titre": f"Erreur de connexion...",
            "date": "Problème technique",
            "prix": "0.00",
            "boutique": "The Geeky Pop",
            "lien": "#"
        })

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(nouvelles_donnees, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    faire_la_veille()
