import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import os

def run_exploration():
    print("[ETAPE 1] Chargement des donnees...")
    df = pd.read_csv('data/raw/Loan_default.csv')
    
    # Selection stricte du nouveau perimetre (8 variables + Cible)
    cols = ['Age', 'Income', 'LoanAmount', 'MonthsEmployed', 'NumCreditLines', 'InterestRate', 'LoanTerm', 'DTIRatio']
    df_reduit = df[cols + ['Default']]
    
    os.makedirs('reports/figures', exist_ok=True)
    
    print("[ETAPE 2] Generation Analyse Univariee...")
    plt.figure(figsize=(15, 10))
    for i, col in enumerate(cols):
        plt.subplot(3, 3, i+1)
        sns.histplot(df_reduit[col], bins=30, kde=True, color='skyblue')
        plt.title(f'Distribution : {col}')
    plt.tight_layout()
    plt.savefig('reports/figures/univar_numeriques.png')
    plt.close()

    print("[ETAPE 3] Generation Analyse Bivariee (Boxplots)...")
    plt.figure(figsize=(15, 10))
    for i, col in enumerate(cols):
        plt.subplot(3, 3, i+1)
        sns.boxplot(x='Default', y=col, data=df_reduit, palette='Set2')
        plt.title(f'{col} par Default')
    plt.tight_layout()
    plt.savefig('reports/figures/bivar_numeriques.png')
    plt.close()

    print("[ETAPE 4] Generation Matrice de Correlation...")
    plt.figure(figsize=(10, 8))
    correlation_matrix = df_reduit.corr()
    sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Matrice de Correlation (Pearson)')
    plt.tight_layout()
    plt.savefig('reports/figures/correlation_matrix.png')
    plt.close()
    
    print("[ETAPE 5] Calcul de l'importance des variables (Machine Learning)...")
    X = df_reduit[cols]
    y = df_reduit['Default']
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    rf = RandomForestClassifier(n_estimators=50, max_depth=7, random_state=42)
    rf.fit(X_scaled, y)
    
    plt.figure(figsize=(10, 6))
    importances = pd.Series(rf.feature_importances_, index=cols).sort_values(ascending=False)
    sns.barplot(x=importances.values, y=importances.index, palette='viridis')
    plt.title('Importance des Variables (Random Forest)')
    plt.xlabel('Poids dans la decision')
    plt.tight_layout()
    plt.savefig('reports/figures/feature_importance_rf.png')
    plt.close()
    
    print("[ETAPE 6] Generation du Credit Score IA (0-1000)...")
    proba_defaut = rf.predict_proba(X_scaled)[:, 1]
    df_reduit['AI_Risk_Index'] = (proba_defaut * 1000).astype(int)
    
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data=df_reduit[df_reduit['Default']==0], x='AI_Risk_Index', fill=True, label='0: Bons Payeurs', color='teal')
    sns.kdeplot(data=df_reduit[df_reduit['Default']==1], x='AI_Risk_Index', fill=True, label='1: Faillites', color='coral')
    plt.title('Distribution de notre NOUVEL Indice de Risque IA (0 - 1000)')
    plt.xlabel('AI Risk Index (Points de Risque)')
    plt.xlim(0, 1000)
    plt.legend()
    plt.tight_layout()
    plt.savefig('reports/figures/risk_index_ml.png')
    plt.close()
    
    print("TOUTES LES IMAGES ONT ETE GENEREES ET ECRASENT LES ANCIENNES !")

if __name__ == "__main__":
    run_exploration()
