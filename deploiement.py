# PARTIE C : DÉPLOIEMENT DU MODÈLE
import pandas as pd
import numpy as np
import joblib
import json
import matplotlib
# Utiliser le backend 'Agg' qui ne nécessite pas d'interface graphique
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import os
import datetime
import warnings
from flask import Flask, request, jsonify, render_template
import threading
import schedule
import time

# Configuration des chemins
RESULTS_DIR = Path("resultats")
DEPLOYMENT_DIR = RESULTS_DIR / "deployment"

# Vérifier si les dossiers existent, sinon les créer
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(DEPLOYMENT_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR / "reports", exist_ok=True)
os.makedirs(RESULTS_DIR / "templates", exist_ok=True)

# Définir un chemin de modèle par défaut si aucun n'existe
default_model_path = DEPLOYMENT_DIR / "default_model.pkl"
try:
    MODEL_PATH = list(DEPLOYMENT_DIR.glob("*_model.pkl"))[0]  # Prendre le premier modèle trouvé
except IndexError:
    # Créer un modèle fictif pour le déploiement de démonstration
    print("Aucun modèle trouvé, création d'un modèle de démonstration...")
    MODEL_PATH = default_model_path

METADATA_PATH = DEPLOYMENT_DIR / "model_metadata.json"
DATA_PATH = DEPLOYMENT_DIR / "latest_data.pkl"

print("="*80)
print("PARTIE C : DÉPLOIEMENT DU MODÈLE TESLA")
print("="*80)

# Fonction pour charger les données sauvegardées
def load_deployment_data():
    """Charge les données nécessaires au déploiement"""
    print("Chargement des données de déploiement...")
    
    # Si les fichiers n'existent pas, créer des données fictives pour la démonstration
    if not MODEL_PATH.exists():
        # Créer un modèle fictif
        model = {
            'arima': None,
            'garch': None
        }
        joblib.dump(model, MODEL_PATH)
        print(f"Modèle de démonstration créé: {MODEL_PATH}")
    else:
        # Charger le modèle
        model = joblib.load(MODEL_PATH)
    
    if not METADATA_PATH.exists():
        # Créer des métadonnées fictives
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
        print(f"Métadonnées de démonstration créées: {METADATA_PATH}")
    else:
        # Charger les métadonnées
        with open(METADATA_PATH, 'r') as f:
            metadata = json.load(f)
    
    if not DATA_PATH.exists():
        # Créer des données factices
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
        print(f"Données de démonstration créées: {DATA_PATH}")
    else:
        # Charger les dernières données
        latest_data = joblib.load(DATA_PATH)
    
    return model, metadata, latest_data