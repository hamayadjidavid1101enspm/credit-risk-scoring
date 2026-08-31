# CoreBanking RiskSystem - Moteur de Scoring de Crédit

Un système professionnel d'évaluation du risque de crédit bancaire, conçu pour calculer la probabilité de défaut de paiement (Indice de Risque) à partir des données financières d'un demandeur.

Ce projet remplace les méthodes de scoring traditionnelles par un pipeline de Machine Learning transparent, éthique et déployable sans infrastructure serveur lourde.

---

## 🚀 Fonctionnalités Clés

* **Scoring 100% Financier (IA Éthique) :** Le modèle exclut volontairement les variables sociodémographiques (statut marital, niveau d'études) pour éviter les biais algorithmiques. Il se concentre strictement sur 8 variables financières : Age, Income, LoanAmount, MonthsEmployed, NumCreditLines, InterestRate, LoanTerm, DTIRatio.
* **Indice de Risque Transparent (0-1000) :** Finies les formules "Boîte Noire". Le modèle calcule la probabilité de défaut exacte via une fonction sigmoïde, puis la convertit en un indice lisible de 0 (Sain) à 1000 (Danger).
* **Architecture Serverless (Front-End) :** L'interface de simulation web est codée en HTML/Vanilla JS. Elle intègre "en dur" les poids mathématiques générés par le modèle Python, permettant une exécution locale immédiate et sécurisée (les données client ne quittent pas le navigateur).

---

## 🧠 Modélisation et Performance

1. **Random Forest (Analyse & Explicabilité) :** 
   * Utilisé en phase de recherche pour confirmer la "Feature Importance". Le modèle a prouvé que le Taux d'intérêt, le Revenu et le Montant du prêt sont les vecteurs principaux de la faillite (contrairement à l'âge).
2. **Régression Logistique (Production) :** 
   * Modèle équivalent à un **Perceptron (Réseau de Neurones à 1 couche)**. 
   * Choisi pour sa transparence absolue et sa légèreté. Il produit les coefficients exacts et l'Intercept qui sont exportés vers l'interface Web.
   * **Corrélation :** L'Indice de Risque généré possède une corrélation de +0.389 avec la réalité des défauts de paiement (contre -0.034 pour l'ancien score manuel de la base de données).

---

## 📁 Architecture du Projet

`	ext
credit-risk-scoring/
├── data/
│   └── raw/                   # Jeu de données d'origine Kaggle (Loan_default.csv)
│
├── src/
│   ├── main_pipeline.py       # Pipeline ML (Standardisation, Entraînement, Export des Poids)
│   ├── exploration_scoring.py # Scripts d'Analyse Exploratoire (Boxplots, Corrélation, EDA)
│   └── etape4_comparaison.py  # Script d'analyse comparative avec l'ancien système
│
├── reports/
│   └── figures/               # Graphiques générés (Univariée, Bivariée, Matrices)
│
└── app/
    └── simulateur_scoring_credit.html # Portail d'Évaluation des Risques (Interface UI)
`

---

## ⚙️ Comment utiliser ce projet ?

### 1. Entraîner le Modèle (Pipeline Python)
Assurez-vous d'avoir installé les dépendances via pip install -r requirements.txt.
Pour relancer l'entraînement, la standardisation et extraire les nouveaux poids :
`ash
python src/main_pipeline.py
`
Pour générer les graphiques d'analyse exploratoire :
`ash
python src/exploration_scoring.py
`

### 2. Lancer l'Application Bancaire (Interface)
L'application ne requiert **aucun serveur backend**.
1. Allez dans le dossier pp/.
2. Double-cliquez sur simulateur_scoring_credit.html pour l'ouvrir dans n'importe quel navigateur Web moderne.
3. Saisissez les données d'un client et cliquez sur "Lancer l'Évaluation du Risque".
