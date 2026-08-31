# Credit Risk Scoring System

Ce projet propose un système d'évaluation du risque de crédit bancaire basé sur l'apprentissage automatique (Machine Learning). Il remplace les méthodes de scoring traditionnelles par un modèle prédictif évaluant la probabilité de défaut de paiement.

## Méthodologie

Le modèle se concentre exclusivement sur des variables financières afin d'éviter tout biais algorithmique lié aux données sociodémographiques. Les 8 variables utilisées sont : Age, Income, LoanAmount, MonthsEmployed, NumCreditLines, InterestRate, LoanTerm et DTIRatio.

Le résultat final n'est pas une boîte noire : le pipeline calcule une probabilité de défaut qui est ensuite transposée sur un indice de risque allant de 0 (sain) à 1000 (critique).

## Modèles utilisés

1. Random Forest : Utilisé pour l'analyse exploratoire et l'extraction de l'importance des variables (Feature Importance).
2. Régression Logistique : Utilisé pour la mise en production. Sa structure mathématique permet une grande transparence et une extraction facile des poids (coefficients) pour un déploiement léger.

L'indice généré par le modèle présente une corrélation de +0.389 avec les défauts de paiement réels, surpassant largement l'ancien score manuel de la base de données.

## Architecture du projet

```text
credit-risk-scoring/
├── data/
│   └── raw/                   # Jeu de données d'origine (Loan_default.csv)
├── src/
│   ├── main_pipeline.py       # Pipeline ML (Standardisation, Entraînement)
│   ├── exploration_scoring.py # Scripts d'analyse exploratoire (EDA)
│   └── etape4_comparaison.py  # Script d'analyse comparative
├── reports/
│   └── figures/               # Graphiques générés
└── app/
    └── simulateur_scoring_credit.html # Interface utilisateur front-end
```

## Exécution du projet

### 1. Entraînement du modèle (Python)
Installez les dépendances nécessaires :
```bash
pip install -r requirements.txt
```

Lancez le pipeline principal pour entraîner le modèle et extraire les poids :
```bash
python src/main_pipeline.py
```

Générez les graphiques d'analyse :
```bash
python src/exploration_scoring.py
```

### 2. Interface utilisateur (Web)
L'application fonctionne entièrement côté client (Serverless).
1. Ouvrez le dossier `app/`.
2. Lancez le fichier `simulateur_scoring_credit.html` dans un navigateur web.
3. Saisissez les données financières pour générer l'évaluation du risque en temps réel.
