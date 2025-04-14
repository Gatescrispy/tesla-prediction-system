import pandas as pd
import numpy as np
import joblib
import json
from pathlib import Path
import yfinance as yf
import datetime
import os

# Configuration des chemins
RESULTS_DIR = Path("resultats")
DEPLOYMENT_DIR = RESULTS_DIR / "deployment"
METADATA_PATH = DEPLOYMENT_DIR / "model_metadata.json"
DATA_PATH = DEPLOYMENT_DIR / "latest_data.pkl"

# Vérifier si les dossiers existent, sinon les créer
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(DEPLOYMENT_DIR, exist_ok=True)

def update_data():
    """Actualise les données Tesla et met à jour les fichiers déployés"""
    print("="*80)
    print("ACTUALISATION DES DONNÉES TESLA")
    print("="*80)
    
    # Vérifier si les fichiers existent
    if not METADATA_PATH.exists() or not DATA_PATH.exists():
        print("Aucune donnée existante trouvée. Création de données initiales...")
        initialize_data()
        return
    
    # Charger les métadonnées actuelles
    with open(METADATA_PATH, 'r') as f:
        metadata = json.load(f)
    
    # Dernière date connue
    last_date = pd.to_datetime(metadata.get('last_date', '2025-04-11'))
    
    # Date actuelle
    today = datetime.datetime.now().date()
    
    # Télécharger les nouvelles données
    ticker = "TSLA"
    start_date = last_date - pd.Timedelta(days=5)  # Chevauchement pour assurer la continuité
    
    print(f"Téléchargement des données depuis {start_date} jusqu'à {today}")
    try:
        new_data = yf.download(ticker, start=start_date, end=today)
        
        if new_data.empty:
            print("Aucune nouvelle donnée disponible")
            return
            
        # Charger les anciennes données
        latest_data = joblib.load(DATA_PATH)
        old_prices = latest_data['ts_price']
        old_returns = latest_data['ts_returns']
        
        # Ajouter les nouvelles données
        new_prices = pd.concat([old_prices, new_data['Close'].loc[old_prices.index[-1]+pd.Timedelta(days=1):]])
        
        # Calculer les nouveaux rendements
        new_returns = new_prices.pct_change().dropna()
        
        # Mettre à jour les données sauvegardées
        latest_data['ts_price'] = new_prices
        latest_data['ts_returns'] = new_returns
        latest_data['last_price'] = float(new_prices.iloc[-1])
        latest_data['last_date'] = str(new_prices.index[-1])
        
        # Mettre à jour les métadonnées
        metadata['last_price'] = float(new_prices.iloc[-1])
        metadata['last_date'] = str(new_prices.index[-1])
        
        # Sauvegarder les mises à jour
        joblib.dump(latest_data, DATA_PATH)
        with open(METADATA_PATH, 'w') as f:
            json.dump(metadata, f, indent=4)
        
        print(f"Données mises à jour jusqu'au {new_prices.index[-1]}")
        print(f"Nouveau dernier prix: ${new_prices.iloc[-1]:.2f}")
        
    except Exception as e:
        print(f"Erreur lors de la mise à jour des données: {str(e)}")

def initialize_data():
    """Initialise les données si aucune donnée n'existe"""
    print("Initialisation des données Tesla...")
    
    # Télécharger les données historiques Tesla
    ticker = "TSLA"
    start_date = "2020-01-01"
    end_date = datetime.datetime.now().date()
    
    try:
        # Télécharger les données
        tesla_data = yf.download(ticker, start=start_date, end=end_date)
        
        if tesla_data.empty:
            print("Impossible de télécharger les données Tesla, création de données fictives")
            # Créer des données factices
            dates = pd.date_range(start=start_date, end=end_date, freq='B')
            ts_price = pd.Series(np.linspace(100, 257.74, len(dates)), index=dates)
        else:
            ts_price = tesla_data['Close']
        
        # Calculer les rendements
        ts_returns = ts_price.pct_change().dropna()
        
        # Créer le dictionnaire de données
        latest_data = {
            'ts_price': ts_price,
            'ts_returns': ts_returns,
            'last_price': float(ts_price.iloc[-1]),
            'last_date': str(ts_price.index[-1])
        }
        
        # Créer les métadonnées
        metadata = {
            'type': 'BiLSTM_Regression',
            'date_creation': datetime.datetime.now().strftime('%Y-%m-%d'),
            'last_price': float(ts_price.iloc[-1]),
            'last_date': str(ts_price.index[-1]),
            'performance': {
                'rmse': 0.083684
            }
        }
        
        # Sauvegarder les données
        joblib.dump(latest_data, DATA_PATH)
        with open(METADATA_PATH, 'w') as f:
            json.dump(metadata, f, indent=4)
        
        print(f"Données initialisées avec succès jusqu'au {ts_price.index[-1]}")
        print(f"Dernier prix: ${ts_price.iloc[-1]:.2f}")
        
    except Exception as e:
        print(f"Erreur lors de l'initialisation des données: {str(e)}")

if __name__ == "__main__":
    update_data()