import pandas as pd
import numpy as np
import joblib
import json
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

def run_pipeline():
    print("[DEBUT] Pipeline Final de Credit Risk Scoring (Nouvelle Architecture)...")
    
    # 1. Chargement des données
    print("Chargement des donnees brutes...")
    data_path = 'data/raw/Loan_default.csv'
    df = pd.read_csv(data_path)
    
    # 2. Périmètre strict : 8 variables explicatives + Cible
    cols_features = ['Age', 'Income', 'LoanAmount', 'MonthsEmployed', 'NumCreditLines', 'InterestRate', 'LoanTerm', 'DTIRatio']
    
    X = df[cols_features]
    y = df['Default']
    
    # 3. Split Train/Test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # 4. Standardisation (Z-Score)
    print("Normalisation des donnees...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 5. Entraînement du Random Forest
    print("Entrainement du modele Random Forest...")
    rf_model = RandomForestClassifier(n_estimators=50, max_depth=7, random_state=42)
    rf_model.fit(X_train_scaled, y_train)
    
    rf_auc = roc_auc_score(y_test, rf_model.predict_proba(X_test_scaled)[:, 1])
    print(f"[OK] Random Forest AUC: {rf_auc:.4f}")
    
    # 6. Entraînement de la Régression Logistique
    print("Entrainement du modele de Regression Logistique (Production)...")
    lr_model = LogisticRegression(random_state=42)
    lr_model.fit(X_train_scaled, y_train)
    
    lr_auc = roc_auc_score(y_test, lr_model.predict_proba(X_test_scaled)[:, 1])
    print(f"[OK] Logistic Regression AUC: {lr_auc:.4f}")
    
    # 7. Sauvegarde des modèles, du Scaler, ET du nouveau dataset score
    print("Sauvegarde des livrables...")
    os.makedirs('models', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    
    joblib.dump(scaler, 'models/scaler.pkl')
    joblib.dump(rf_model, 'models/random_forest_model.pkl')
    joblib.dump(lr_model, 'models/logistic_regression_model.pkl')
    
    # Creation de la colonne AI_Credit_Score dans le dataset pour les livrer
    proba_defaut = rf_model.predict_proba(X_scaled)[:, 1] if 'X_scaled' in locals() else rf_model.predict_proba(scaler.fit_transform(X))[:, 1]
    # On utilise toutes les donnees X pour generer le fichier final
    proba_full = rf_model.predict_proba(scaler.transform(X))[:, 1]
    
    # INDICE DE RISQUE PUR (0 à 1000)
    # 0 = Aucun risque / 1000 = Risque maximal
    df['AI_Risk_Index'] = (proba_full * 1000).round().astype(int)
    
    df.to_csv('data/processed/Loan_default_scored_AI.csv', index=False)
    print("Dataset avec AI_Credit_Score sauvegarde dans data/processed/")
    
    # 8. Exportation des Poids pour le Front-End (Web)
    # On exporte la moyenne et l'échelle du StandardScaler, et les coefficients de la LogReg
    js_weights = {
        "columns": cols_features,
        "mean": scaler.mean_.tolist(),
        "scale": scaler.scale_.tolist(),
        "coef": lr_model.coef_[0].tolist(),
        "intercept": lr_model.intercept_[0]
    }
    
    with open('models/js_model_weights.json', 'w') as f:
        json.dump(js_weights, f, indent=2)
        
    print("[FIN] PIPELINE TERMINE AVEC SUCCES !")

if __name__ == "__main__":
    run_pipeline()
