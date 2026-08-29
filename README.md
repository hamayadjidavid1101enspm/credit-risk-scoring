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
├── app/
│   └── simulateur_scoring_credit.html # Simulateur Web (Régression Logistique)
├── data/
│   ├── raw/              # Loan_default.csv (dataset original)
│   └── processed/        # Données avec Risk Index après pipeline
├── models/               # Modèles entraînés (.pkl et .json pour l'app web)
├── notebooks/            # Notebooks d'exploration
├── src/
│   ├── main_pipeline.py      # 🚀 SCRIPT FINAL : Bout-en-bout (Features, Train, Export)
│   └── exploration_scoring.py # Script d'analyse (Univariée, Bivariée, ACP, ML)
├── reports/
│   └── figures/          # Graphiques d'analyse générés automatiquement
├── docs/                 # Documentation
├── requirements.txt
└── README.md
```

## Installation & Exécution (Projet Final)

1. Créer l'environnement virtuel et installer les dépendances :
```bash
python -m venv venv
# Windows : venv\Scripts\activate
# Mac/Linux : source venv/bin/activate
pip install -r requirements.txt
```

2. **Lancer le Pipeline Final** : 
Le script `main_pipeline.py` exécute le Feature Engineering, entraîne les modèles (Random Forest et Régression Logistique), calcule l'indice de risque et sauvegarde les livrables dans `models/` et `data/processed/`.
```bash
cd src
python main_pipeline.py
```

3. **Générer les Visuels d'Exploration** (Analyse de la relation variables/risque) :
```bash
python exploration_scoring.py
```

## Avancement & Finalisation
✅ Le projet est **terminé**. Le workflow complet est automatisé.
✅ L'application Web de simulation (`app/simulateur_scoring_credit.html`) intègre directement les poids du modèle issu du pipeline, permettant d'avoir une décision immédiate et hautement interprétable sur l'acceptation ou le refus d'un crédit.
