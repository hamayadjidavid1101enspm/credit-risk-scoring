# Credit Risk Scoring

Projet PAEI (Gehmit) — David Janvion HAMAYADJI NGOMNA, encadré par Archange KOUMBA MOUITY.

## Objectif

Construire un modèle de Machine Learning capable de prédire le risque de défaut de
remboursement d'un emprunteur (classification binaire supervisée), à partir du
Loan Default Prediction Dataset (Kaggle).

- **Variable cible** : `Default` (0 = pas de défaut, 1 = défaut)
- **Colonnes de travail** : les 18 colonnes du fichier `Loan_default.csv`
  (`LoanID` conservé comme identifiant, exclu des features du modèle)

## Structure du dépôt

```
credit-risk-scoring/
├── data/
│   ├── raw/              # Loan_default.csv (dataset original, jamais modifié)
│   └── processed/        # jeux de données nettoyés / transformés
├── notebooks/             # notebooks d'exploration et de modélisation
├── src/
│   ├── data/              # scripts de chargement / préparation des données
│   ├── features/          # scripts de feature engineering
│   └── models/            # scripts d'entraînement / évaluation des modèles
├── reports/
│   └── figures/           # graphiques générés pour le rapport
├── docs/                  # notes, synthèse de littérature, etc.
├── requirements.txt
└── README.md
```

## Installation

```bash
python3 -m venv venv
source venv/bin/activate        # Windows : venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

Vérification :

```bash
python3 -c "import pandas, numpy, matplotlib, seaborn, sklearn; print('OK')"
```

## Avancement

Voir `Chronogramme_PAEI_Gehmit.xlsx` pour le suivi séance par séance.
