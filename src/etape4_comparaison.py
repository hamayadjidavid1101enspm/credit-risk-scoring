import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

try:
    # 1. Chargement
    df = pd.read_csv('C:/Users/DAVID PC/Documents/credit-risk-scoring/data/raw/Loan_default.csv')
    cols = ['Age', 'Income', 'LoanAmount', 'MonthsEmployed', 'NumCreditLines', 'InterestRate', 'LoanTerm', 'DTIRatio']
    X = df[cols]
    y = df['Default']
    
    # 2. Entraînement
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    rf = RandomForestClassifier(n_estimators=50, max_depth=10, random_state=42)
    rf.fit(X_scaled, y)
    
    # 3. LE NOUVEAU SCORE DU MODÈLE (Echelle 300 - 850)
    # L'IA génère la probabilité de défaut.
    proba_defaut = rf.predict_proba(X_scaled)[:, 1]
    
    # L'Indice de Risque pur (0 à 1000)
    # C'est simplement la probabilité brute multipliée par 1000 (Aucun bricolage).
    df['AI_Risk_Index'] = (proba_defaut * 1000).round().astype(int)
    
    # 4. COMPARAISON
    print("=== CORRÉLATION AVEC LA RÉALITÉ DU DÉFAUT ===")
    print(f"L'ancien CreditScore (Fichier Excel)   : {df['CreditScore'].corr(df['Default']):.4f}  <-- Inutile (Aveugle)")
    print(f"NOTRE AI_Risk_Index sur 1000 points    : {df['AI_Risk_Index'].corr(df['Default']):.4f}  <-- Puissant")
    
    print("\n=== ANALYSE SUR LES CLIENTS QUI ONT FAIT FAILLITE (Default = 1) ===")
    print(f"Que disait l'ancien Excel ? Score moyen de : {df[df['Default']==1]['CreditScore'].mean():.0f} / 850 (Score moyen et illisible)")
    print(f"Que dit notre IA Python ?   Indice de Risque : {df[df['Default']==1]['AI_Risk_Index'].mean():.0f} / 1000 points de danger")

except Exception as e:
    print(f"Erreur : {e}")
