import pandas as pd

try:
    # Chargement des données
    df = pd.read_csv('C:/Users/DAVID PC/Documents/credit-risk-scoring/data/raw/Loan_default.csv')
    
    # Nouveau périmètre strict (sans CreditScore ni variables catégorielles)
    colonnes_gardees = ['Age', 'Income', 'LoanAmount', 'MonthsEmployed', 'NumCreditLines', 'InterestRate', 'LoanTerm', 'DTIRatio', 'Default']
    df_reduit = df[colonnes_gardees]
    
    print("=== MEDIANES EXACTES ===")
    print(df_reduit.groupby('Default').median())
    
    print("\n=== CORRELATIONS AVEC LE DEFAUT ===")
    print(df_reduit.corr()['Default'].sort_values(ascending=False).round(3))

except Exception as e:
    print(f"Erreur : {e}")
