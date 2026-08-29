import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
import joblib
import warnings

warnings.filterwarnings('ignore')

def run_pipeline():
    print("🚀 Début du Pipeline Final de Credit Risk Scoring...")
    
    # 1. Configuration et chemins
    DATA_RAW = "../data/raw/Loan_default.csv"
    DATA_PROC = "../data/processed/Loan_default_scored.csv"
    MODELS_DIR = "../models/"
    REPORTS_DIR = "../reports/figures/"
    
    for d in ["../data/processed", MODELS_DIR, REPORTS_DIR]:
        os.makedirs(d, exist_ok=True)
        
    # 2. Chargement des données
    print("⏳ Chargement des données brutes...")
    df = pd.read_csv(DATA_RAW)
    df = df.drop(columns=['LoanID'])
    
    num_cols = df.select_dtypes(include=['int64', 'float64']).columns.drop('Default').tolist()
    
    # 3. Création des variables synthétiques (Feature Engineering)
    print("⚙️ Feature Engineering...")
    df['AgeEmploymentIncoherent'] = (df['MonthsEmployed'] > (df['Age'] - 16) * 12).astype(int)
    df['LoanToIncomeRatio'] = df['LoanAmount'] / df['Income']
    
    # 4. Encodage et Préparation pour le Machine Learning
    df_encoded = pd.get_dummies(df, drop_first=True)
    X = df_encoded.drop(columns=['Default'])
    y = df_encoded['Default']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # 5. Entraînement du Modèle Random Forest (Pour l'analyse d'importance)
    print("🌲 Entraînement du modèle Random Forest...")
    rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    rf_auc = roc_auc_score(y_test, rf.predict_proba(X_test)[:, 1])
    print(f"✅ Random Forest AUC: {rf_auc:.4f}")
    
    # Sauvegarde de l'importance des variables
    importances = rf.feature_importances_
    indices = np.argsort(importances)[::-1][:10]
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=importances[indices], y=X.columns[indices], palette="viridis")
    plt.title("Top 10 des Variables (Random Forest)", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(REPORTS_DIR, "feature_importance_rf.png"), dpi=300)
    plt.close()
    
    # 6. Entraînement de la Régression Logistique (Pour l'interface Web / API)
    print("📈 Entraînement du modèle de Régression Logistique (Production)...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    lr = LogisticRegression(C=100, random_state=42)
    lr.fit(X_train_scaled, y_train)
    lr_auc = roc_auc_score(y_test, lr.predict_proba(X_test_scaled)[:, 1])
    print(f"✅ Logistic Regression AUC: {lr_auc:.4f}")
    
    # 7. Génération de l'Indice de Risque (Scoring global)
    print("📊 Création des Indices de Risque Finaux...")
    # Indice ML (basé sur RF)
    df['RiskIndex_ML'] = rf.predict_proba(X)[:, 1] * 100
    
    # 8. Sauvegarde des modèles et des données traitées
    print("💾 Sauvegarde des livrables...")
    joblib.dump(rf, os.path.join(MODELS_DIR, "random_forest_model.pkl"))
    joblib.dump(lr, os.path.join(MODELS_DIR, "logistic_regression_model.pkl"))
    joblib.dump(scaler, os.path.join(MODELS_DIR, "scaler.pkl"))
    
    df.to_csv(DATA_PROC, index=False)
    
    # Extraction des poids pour l'application Web Javascript
    js_model_weights = {
        "columns": list(X.columns),
        "mean": list(scaler.mean_),
        "scale": list(scaler.scale_),
        "coef": list(lr.coef_[0]),
        "intercept": lr.intercept_[0]
    }
    with open(os.path.join(MODELS_DIR, "js_model_weights.json"), "w") as f:
        json.dump(js_model_weights, f)
        
    print(f"✅ Modèles sauvegardés dans {MODELS_DIR}")
    print(f"✅ Données scorees sauvegardées dans {DATA_PROC}")
    print("🎉 PIPELINE TERMINÉ AVEC SUCCÈS !")

if __name__ == "__main__":
    run_pipeline()
