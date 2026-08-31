import pandas as pd

try:
    df = pd.read_csv('C:/Users/DAVID PC/Documents/credit-risk-scoring/data/raw/Loan_default.csv')
    
    print("=== MEDIANES PAR CLASSE (0=Sain, 1=Défaut) ===")
    print(df.groupby('Default')[['Income', 'InterestRate', 'LoanAmount', 'CreditScore', 'Age']].median())
    
    print("\n=== CORRELATIONS AVEC LE DEFAUT ===")
    print(df[['Income', 'InterestRate', 'LoanAmount', 'CreditScore', 'Age', 'MonthsEmployed', 'NumCreditLines', 'Default']].corr()['Default'].round(3))
    
except Exception as e:
    print(f"Erreur : {e}")
