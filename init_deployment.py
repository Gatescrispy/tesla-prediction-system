import os
import sys
from pathlib import Path
import shutil
import json
import pandas as pd
import numpy as np
import joblib
import datetime

print("="*80)
print("INITIALISATION DU SYSTÈME DE DÉPLOIEMENT TESLA")
print("="*80)

# Configuration des chemins
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = SCRIPT_DIR
RESULTS_DIR = ROOT_DIR / "resultats"
DEPLOYMENT_DIR = RESULTS_DIR / "deployment"
REPORTS_DIR = RESULTS_DIR / "reports"
TEMPLATES_DIR = RESULTS_DIR / "templates"

# Vérifier si les dossiers existent, sinon les créer
print("Configuration des dossiers...")
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(DEPLOYMENT_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)

# Chemin des fichiers de déploiement
MODEL_PATH = DEPLOYMENT_DIR / "default_model.pkl"
METADATA_PATH = DEPLOYMENT_DIR / "model_metadata.json"
DATA_PATH = DEPLOYMENT_DIR / "latest_data.pkl"

# Vérifier si les données existent déjà
if METADATA_PATH.exists() and DATA_PATH.exists() and MODEL_PATH.exists():
    print("Le système est déjà initialisé. Les fichiers existants ont été détectés:")
    print(f"- Modèle: {MODEL_PATH}")
    print(f"- Métadonnées: {METADATA_PATH}")
    print(f"- Données: {DATA_PATH}")
    
    # Charger les métadonnées pour afficher des informations
    with open(METADATA_PATH, 'r') as f:
        metadata = json.load(f)
    
    print("\nInformations du modèle existant:")
    print(f"Type: {metadata.get('type', 'Inconnu')}")
    print(f"Date de création: {metadata.get('date_creation', 'Inconnue')}")
    print(f"Dernier prix: ${metadata.get('last_price', 0):.2f}")
    
    overwrite = input("\nVoulez-vous réinitialiser le système? (O/N): ").strip().upper()
    if overwrite != 'O':
        print("Initialisation annulée. Le système existant reste inchangé.")
        sys.exit(0)
    
    print("Réinitialisation du système...")

# Créer un modèle fictif
print("Création d'un modèle de démonstration...")
model = {
    'arima': None,
    'garch': None
}
joblib.dump(model, MODEL_PATH)

# Créer des métadonnées fictives
print("Création des métadonnées...")
metadata = {
    'type': 'BiLSTM_Regression',
    'date_creation': datetime.datetime.now().strftime('%Y-%m-%d'),
    'last_price': 257.74,
    'last_date': '2025-04-11 00:00:00',
    'performance': {
        'rmse': 0.083684
    }
}
with open(METADATA_PATH, 'w') as f:
    json.dump(metadata, f, indent=4)

# Créer des données factices
print("Création des données de démonstration...")
dates = pd.date_range(start='2020-01-01', end='2025-04-11', freq='B')
ts_price = pd.Series(np.linspace(100, 257.74, len(dates)), index=dates)
ts_returns = ts_price.pct_change().dropna()

latest_data = {
    'ts_price': ts_price,
    'ts_returns': ts_returns,
    'last_price': 257.74,
    'last_date': '2025-04-11 00:00:00'
}
joblib.dump(latest_data, DATA_PATH)

print("\nInitialisation terminée avec succès!")
print("Le système est prêt à être démarré avec 'python deploy.py'")
print("="*80)

# Étapes suivantes
print("\nÉtapes suivantes recommandées:")
print("1. Mettez à jour les données avec 'python update_data.py'")
print("2. Entraînez un modèle avec 'python retrain_model.py'")
print("3. Démarrez le système avec 'python deploy.py'")
print("="*80)