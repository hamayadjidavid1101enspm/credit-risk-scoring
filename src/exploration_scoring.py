import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import os
import warnings

warnings.filterwarnings('ignore')

# ==========================================
# 0. CONFIGURATION & CHARGEMENT
# ==========================================
# Style visuel pour des graphiques professionnels
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_context("notebook", font_scale=1.1)
sns.set_palette(["#2ecc71", "#e74c3c"]) # Vert = 0 (Bon payeur), Rouge = 1 (Défaut)

DATA_PATH = "../data/raw/Loan_default.csv"
OUTPUT_DIR = "../reports/figures/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Chargement des données...")
df = pd.read_csv(DATA_PATH)
df = df.drop(columns=['LoanID']) # Identifiant inutile pour l'analyse

# Séparation des types de variables
num_cols = df.select_dtypes(include=['int64', 'float64']).columns.drop('Default').tolist()
cat_cols = df.select_dtypes(include=['object']).columns.tolist()

# ==========================================
# 1. ANALYSE UNIVARIÉE
# ==========================================
print("\n--- 1. Analyse Univariée ---")
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle("Distribution des Variables Numériques Clés", fontsize=16, fontweight='bold')
features_to_plot = ['Age', 'Income', 'LoanAmount', 'CreditScore', 'InterestRate', 'NumCreditLines']

for ax, feature in zip(axes.flatten(), features_to_plot):
    sns.histplot(df[feature], kde=True, ax=ax, color='#3498db', bins=30)
    ax.set_title(feature)
    ax.set_ylabel('')

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "univar_numeriques.png"), dpi=300)
plt.close()
print("-> Graphique univarié sauvegardé : univar_numeriques.png")

# ==========================================
# 2. ANALYSE BIVARIÉE (vs Default)
# ==========================================
print("\n--- 2. Analyse Bivariée ---")
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle("Impact des Variables sur le Défaut de Paiement", fontsize=16, fontweight='bold')

sns.boxplot(x='Default', y='Income', data=df, ax=axes[0])
axes[0].set_title("Revenu vs Défaut")

sns.boxplot(x='Default', y='InterestRate', data=df, ax=axes[1])
axes[1].set_title("Taux d'intérêt vs Défaut")

sns.boxplot(x='Default', y='CreditScore', data=df, ax=axes[2])
axes[2].set_title("Score de Crédit vs Défaut")

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "bivar_numeriques.png"), dpi=300)
plt.close()
print("-> Graphique bivarié sauvegardé : bivar_numeriques.png")

# Matrice de corrélation
plt.figure(figsize=(12, 10))
corr = df[num_cols + ['Default']].corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap='coolwarm', vmin=-1, vmax=1, square=True)
plt.title("Matrice de Corrélation (Variables Numériques)", fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "correlation_matrix.png"), dpi=300)
plt.close()
print("-> Matrice de corrélation sauvegardée : correlation_matrix.png")

# ==========================================
# 3. CONSTRUCTION DE L'INDICE DE RISQUE : ACP
# ==========================================
print("\n--- 3. Indice de Risque basé sur l'ACP ---")
# On utilise uniquement les variables numériques pour l'ACP
X_num = df[num_cols]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_num)

pca = PCA(n_components=1)
pc1 = pca.fit_transform(X_scaled)

# L'ACP peut inverser le sens. On vérifie la corrélation avec 'Default'
corr_pca_default = np.corrcoef(pc1.flatten(), df['Default'])[0, 1]
if corr_pca_default < 0:
    pc1 = -pc1  # On s'assure qu'un score élevé = risque élevé

# Mise à l'échelle de l'indice de 0 à 100
minmax = MinMaxScaler(feature_range=(0, 100))
risk_index_pca = minmax.fit_transform(pc1)
df['RiskIndex_PCA'] = risk_index_pca

plt.figure(figsize=(8, 5))
sns.histplot(data=df, x='RiskIndex_PCA', hue='Default', bins=50, kde=True, common_norm=False)
plt.title("Distribution de l'Indice de Risque (ACP) selon le Défaut", fontsize=14, fontweight='bold')
plt.savefig(os.path.join(OUTPUT_DIR, "risk_index_pca.png"), dpi=300)
plt.close()
print("-> Graphique Indice ACP sauvegardé : risk_index_pca.png")

# ==========================================
# 4. CONSTRUCTION DE L'INDICE DE RISQUE : MACHINE LEARNING
# ==========================================
print("\n--- 4. Indice de Risque basé sur l'Importance des Variables (ML) ---")
# Encodage rapide pour le Random Forest
df_encoded = pd.get_dummies(df.drop(columns=['RiskIndex_PCA']), drop_first=True)
X = df_encoded.drop(columns=['Default'])
y = df_encoded['Default']

# Séparation pour éviter le sur-apprentissage sur l'évaluation
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)

# Importance des variables
importances = rf.feature_importances_
indices = np.argsort(importances)[::-1][:10] # Top 10

plt.figure(figsize=(10, 6))
sns.barplot(x=importances[indices], y=X.columns[indices], palette="viridis")
plt.title("Top 10 des Variables les plus Importantes (Random Forest)", fontsize=14, fontweight='bold')
plt.xlabel("Importance relative")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "feature_importance_rf.png"), dpi=300)
plt.close()
print("-> Graphique Importance ML sauvegardé : feature_importance_rf.png")

# Création du score de risque ML basé sur la probabilité de prédiction
# predict_proba renvoie [Prob_Non_Defaut, Prob_Defaut]. On prend la 2ème colonne * 100
df['RiskIndex_ML'] = rf.predict_proba(X)[:, 1] * 100

plt.figure(figsize=(8, 5))
sns.histplot(data=df, x='RiskIndex_ML', hue='Default', bins=50, kde=True, common_norm=False)
plt.title("Distribution de l'Indice de Risque (Machine Learning) selon le Défaut", fontsize=14, fontweight='bold')
plt.savefig(os.path.join(OUTPUT_DIR, "risk_index_ml.png"), dpi=300)
plt.close()
print("-> Graphique Indice ML sauvegardé : risk_index_ml.png")

print("\n🎉 ANALYSE TERMINÉE ! Les graphiques ont été générés dans le dossier 'reports/figures/'.")
print("Interprétation rapide pour la prise de décision :")
print("- Si l'Indice ML d'un emprunteur est > 50, il présente un profil à fort risque de défaut.")
print("- Utilisez les variables du Top 3 (voir feature_importance_rf.png) pour justifier le refus ou l'acceptation d'un prêt.")
