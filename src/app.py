from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os

app = Flask(__name__)

# Définition des chemins (adapté pour le serveur et le test local)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, '../models/random_forest_model.pkl')
SCALER_PATH = os.path.join(BASE_DIR, '../models/scaler.pkl')

# Chargement du modèle et du scaler en mémoire au démarrage
print("Chargement du modèle ML...")
try:
    rf_model = joblib.load(MODEL_PATH)
    # Le Random Forest n'a techniquement pas besoin de Scaler, 
    # mais si vous vouliez utiliser la Régression Logistique, on chargerait le scaler ici.
    print("Modèle chargé avec succès !")
except Exception as e:
    print(f"Erreur lors du chargement : {e}")

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Bienvenue sur l'API de Scoring de Crédit (PAEI)",
        "status": "API Active"
    })

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Récupération des données envoyées par l'utilisateur (format JSON)
        data = request.get_json()
        
        # Transformation en DataFrame (attendu par le modèle scikit-learn)
        # On suppose que le client envoie exactement les 26 colonnes attendues
        df_client = pd.DataFrame([data])
        
        # Prédiction de la probabilité de défaut (Classe 1)
        proba_defaut = rf_model.predict_proba(df_client)[0][1]
        score_risque = round(proba_defaut * 100, 2)
        
        # Décision métier simple
        if score_risque < 35:
            decision = "Approbation (Risque Faible)"
        elif score_risque < 65:
            decision = "Analyse Manuelle (Risque Modéré)"
        else:
            decision = "Refus Conseillé (Risque Élevé)"
            
        return jsonify({
            "score_risque_pourcentage": score_risque,
            "decision": decision
        })
        
    except Exception as e:
        return jsonify({"erreur": str(e)}), 400

if __name__ == '__main__':
    # Lancement du serveur en local (sans Docker)
    app.run(debug=True, host='0.0.0.0', port=5000)
