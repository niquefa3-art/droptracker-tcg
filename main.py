from flask import Flask, render_template
import json
import os
import scraper

app = Flask(__name__)

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(THIS_FOLDER, "data.json")

def lire_donnees():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

@app.route('/')
def home():
    produits = lire_donnees()
    return render_template('index.html', produits=produits)

# --- NOTRE PORTE SECRÈTE ---
@app.route('/update-veille-secrete-777')
def lancer_mise_a_jour():
    scraper.faire_la_veille()
    return "✅ Succès : La veille a été lancée et la base de données est à jour !"

if __name__ == '__main__':
    # Configuration spéciale pour que ça marche sur Render
    app.run(host='0.0.0.0', port=10000)
