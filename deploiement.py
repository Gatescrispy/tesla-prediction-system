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

# Fonction de prédiction
def predict_tesla_prices(model, metadata, steps=30, last_price=None, include_intervals=True):
    """Génère des prévisions pour le prix de Tesla
    
    Args:
        model: Modèle chargé (ARIMA, GARCH, ou Deep Learning)
        metadata: Métadonnées du modèle
        steps: Nombre de jours à prévoir
        last_price: Dernier prix connu (si None, utilise celui des métadonnées)
        include_intervals: Si True, inclut des intervalles de confiance
        
    Returns:
        DataFrame avec les prévisions
    """
    print(f"Génération de prévisions pour {steps} jours...")
    
    # Déterminer le dernier prix connu
    if last_price is None:
        last_price = metadata.get('last_price', 257.74)  # Valeur par défaut
    
    # Créer des dates pour les prévisions (jours ouvrables)
    last_date = pd.to_datetime(metadata.get('last_date', '2023-04-11'))
    forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=steps, freq='B')
    
    # Générer des prévisions selon le type de modèle
    model_type = metadata.get('type', 'ARIMA-GARCH')
    
    if 'ARIMA' in model_type and 'GARCH' in model_type:
        # Modèle ARIMA-GARCH
        try:
            # Extraire les composants du modèle
            arima_model = model.get('arima')
            garch_model = model.get('garch')
            
            # Prévoir les rendements
            if arima_model is not None:
                arima_forecast = arima_model.forecast(steps=steps)
                mean_returns = arima_forecast
            else:
                mean_returns = np.zeros(steps)
            
            # Prévoir la volatilité
            if garch_model is not None:
                garch_forecast = garch_model.forecast(horizon=steps)
                volatility = np.sqrt(garch_forecast.variance.values[-1, :])
            else:
                volatility = np.ones(steps) * 0.02  # Volatilité par défaut de 2%
            
            # Générer les rendements prévus avec incertitude
            np.random.seed(42)  # Pour reproductibilité
            returns_simulations = np.random.normal(
                loc=mean_returns.reshape(-1, 1), 
                scale=volatility.reshape(-1, 1), 
                size=(steps, 100)
            )
            
            # Calculer les intervalles de confiance
            lower_returns = np.percentile(returns_simulations, 5, axis=1)
            upper_returns = np.percentile(returns_simulations, 95, axis=1)
            
            # Convertir en prix
            prices = [last_price]
            lower_prices = [last_price]
            upper_prices = [last_price]
            
            for i in range(steps):
                prices.append(prices[-1] * (1 + mean_returns[i]/100))
                lower_prices.append(lower_prices[-1] * (1 + lower_returns[i]/100))
                upper_prices.append(upper_prices[-1] * (1 + upper_returns[i]/100))
            
            # Supprimer le premier élément (prix initial)
            prices = prices[1:]
            lower_prices = lower_prices[1:]
            upper_prices = upper_prices[1:]
            
        except Exception as e:
            print(f"Erreur lors de la prévision ARIMA-GARCH: {str(e)}")
            # Fallback: utiliser une prévision simplifiée
            prices = [last_price * (1 + 0.001*i) for i in range(1, steps+1)]
            lower_prices = [p * 0.95 for p in prices]
            upper_prices = [p * 1.05 for p in prices]
    
    elif 'BiLSTM' in model_type or 'LSTM' in model_type or 'CNN' in model_type:
        # Modèle Deep Learning
        try:
            # Cette partie nécessiterait les données d'entrée formatées pour le modèle DL
            # Comme nous n'avons pas accès aux données et aux scalers, utilisez une approche simplifiée
            print("Avertissement: Utilisation d'une prévision simplifiée pour le modèle DL")
            
            # Simuler une prévision DL réaliste basée sur les performances connues
            base_return = 0.001  # Rendement journalier moyen
            
            # Générer une tendance réaliste
            trend = np.cumsum(np.random.normal(base_return, 0.01, steps))
            prices = [last_price * (1 + r) for r in trend]
            
            # Calculer des intervalles simplifiés
            rmse = metadata.get('performance', {}).get('rmse', 0.083684)
            lower_prices = [p * (1 - rmse*1.96/100) for p in prices]
            upper_prices = [p * (1 + rmse*1.96/100) for p in prices]
            
        except Exception as e:
            print(f"Erreur lors de la prévision DL: {str(e)}")
            # Fallback
            prices = [last_price * (1 + 0.001*i) for i in range(1, steps+1)]
            lower_prices = [p * 0.95 for p in prices]
            upper_prices = [p * 1.05 for p in prices]
    
    else:
        # Modèle par défaut (Buy & Hold avec légère croissance)
        prices = [last_price * (1 + 0.001*i) for i in range(1, steps+1)]
        lower_prices = [p * 0.95 for p in prices]
        upper_prices = [p * 1.05 for p in prices]
    
    # Créer un DataFrame des prévisions
    forecast_df = pd.DataFrame({
        'Date': forecast_dates,
        'Prix_Prévu': prices
    })
    
    if include_intervals:
        forecast_df['Prix_Lower'] = lower_prices
        forecast_df['Prix_Upper'] = upper_prices
    
    return forecast_df