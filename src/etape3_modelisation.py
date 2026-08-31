import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier

try:
    # 1. Chargement et Préparation
    df = pd.read_csv('C:/Users/DAVID PC/Documents/credit-risk-scoring/data/raw/Loan_default.csv')
    cols = ['Age', 'Income', 'LoanAmount', 'MonthsEmployed', 'NumCreditLines', 'InterestRate', 'LoanTerm', 'DTIRatio']
    X = df[cols]
    y = df['Default']

    # Standardisation obligatoire (Moyenne=0, Ecart-type=1)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 2. Méthode 1 : ACP (Analyse en Composantes Principales)
    pca = PCA(n_components=1)
    pca.fit(X_scaled)
    print(f"=== ACP ===")
    print(f"Variance expliquée par le 1er Axe : {pca.explained_variance_ratio_[0]*100:.2f} %")

    # 3. Méthode 2 : Random Forest
    rf = RandomForestClassifier(n_estimators=50, max_depth=7, random_state=42)
    rf.fit(X_scaled, y)
    
    print("\n=== IMPORTANCE DES VARIABLES (MACHINE LEARNING) ===")
    importances = pd.Series(rf.feature_importances_, index=cols).sort_values(ascending=False)
    for col, imp in importances.items():
        print(f"{col} : {imp*100:.2f} %")

except Exception as e:
    print(f"Erreur : {e}")
