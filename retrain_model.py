import pandas as pd
import numpy as np
import joblib
import json
from pathlib import Path
import statsmodels.api as sm
from arch import arch_model
import datetime

# Configuration des chemins
RESULTS_DIR = Path("resultats")
DEPLOYMENT_DIR = RESULTS_DIR / "deployment"
METADATA_PATH = DEPLOYMENT_DIR / "model_metadata.json"
DATA_PATH = DEPLOYMENT_DIR / "latest_data.pkl"
default_model_path = DEPLOYMENT_DIR / "default_model.pkl"

# Trouver le modèle ou utiliser le chemin par défaut
try:
    MODEL_PATH = list(DEPLOYMENT_DIR.glob("*_model.pkl"))[0]
except IndexError:
    MODEL_PATH = default_model_path

def retrain_model():
    """Réentraîne le modèle avec les données les plus récentes"""
    print("Réentraînement du modèle Tesla...")
    
    # Charger les métadonnées
    with open(METADATA_PATH, 'r') as f:
        metadata = json.load(f)
    
    # Charger les données
    latest_data = joblib.load(DATA_PATH)
    ts_price = latest_data['ts_price']
    ts_returns = latest_data['ts_returns']
    
    # Déterminer le type de modèle
    model_type = metadata.get('type', 'ARIMA-GARCH')
    
    if 'ARIMA' in model_type and 'GARCH' in model_type:
        # Réentraîner le modèle ARIMA-GARCH
        print("Réentraînement du modèle ARIMA-GARCH...")
        
        # Paramètres ARIMA
        arima_order = (1, 0, 1)  # Exemple - ajuster selon les besoins
        
        # Entraîner ARIMA
        arima_model = sm.tsa.ARIMA(ts_returns, order=arima_order)
        arima_results = arima_model.fit()
        
        # Entraîner GARCH sur les résidus
        residuals = arima_results.resid
        garch_model = arch_model(residuals, vol='Garch', p=1, q=1)
        garch_results = garch_model.fit(disp='off')
        
        # Sauvegarder le nouveau modèle
        new_model = {
            'arima': arima_results,
            'garch': garch_results
        }
        
        # Mise à jour des métadonnées
        metadata['date_creation'] = datetime.datetime.now().strftime('%Y-%m-%d')
        if 'performance' not in metadata:
            metadata['performance'] = {}
        metadata['performance']['rmse'] = np.sqrt(np.mean(residuals**2))
        
    elif 'BiLSTM' in model_type or 'LSTM' in model_type or 'CNN' in model_type:
        print("Le réentraînement des modèles Deep Learning nécessite des ressources spécifiques.")
        print("Veuillez utiliser le notebook d'origine pour réentraîner ces modèles.")
        return
    
    else:
        # Modèle par défaut simple
        print("Utilisation d'un modèle ARIMA simple par défaut...")
        
        arima_model = sm.tsa.ARIMA(ts_returns, order=(1, 0, 1))
        arima_results = arima_model.fit()
        
        new_model = {
            'arima': arima_results,
            'garch': None
        }
        
        # Mise à jour des métadonnées
        metadata['type'] = 'ARIMA'
        metadata['date_creation'] = datetime.datetime.now().strftime('%Y-%m-%d')
        if 'performance' not in metadata:
            metadata['performance'] = {}
        metadata['performance']['rmse'] = np.sqrt(np.mean(arima_results.resid**2))
    
    # Sauvegarder le modèle réentraîné
    joblib.dump(new_model, MODEL_PATH)
    
    # Sauvegarder les métadonnées mises à jour
    with open(METADATA_PATH, 'w') as f:
        json.dump(metadata, f, indent=4)
    
    print(f"Modèle réentraîné et sauvegardé: {MODEL_PATH}")
    print(f"Date du réentraînement: {metadata['date_creation']}")
    print(f"RMSE du modèle: {metadata['performance']['rmse']:.6f}")

if __name__ == "__main__":
    retrain_model()