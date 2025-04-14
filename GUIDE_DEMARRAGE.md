# Guide de Démarrage Rapide: Système de Déploiement Tesla

Ce guide vous permettra de démarrer rapidement avec le système de prévision du prix de l'action Tesla.

## Présentation

Le système de déploiement Tesla est une solution complète pour:
- Déployer un modèle prédictif pour le prix de l'action Tesla
- Générer des prévisions à différents horizons temporels (1 à 90 jours)
- Visualiser les prévisions via une interface web interactive
- Mettre à jour automatiquement les données et réentraîner le modèle

## Installation rapide

### Sous Windows:
1. Ouvrez une invite de commande
2. Naviguez vers le dossier du projet
3. Exécutez `setup.bat`

### Sous Linux/macOS:
1. Ouvrez un terminal
2. Naviguez vers le dossier du projet
3. Exécutez `bash setup.sh`

## Utilisation simplifiée

Le script `run.py` permet d'exécuter facilement toutes les fonctionnalités du système:

```bash
# Configurer le système (première utilisation)
python run.py setup

# Initialiser le système
python run.py init

# Mettre à jour les données
python run.py update

# Réentraîner le modèle
python run.py retrain

# Démarrer le système
python run.py deploy

# Faire tout (mise à jour, réentraînement, déploiement)
python run.py all
```

## Accès à l'interface web

Une fois le système démarré, l'interface web est accessible à l'adresse:
http://127.0.0.1:5050

Cette interface permet de:
- Générer des prévisions pour différents horizons temporels
- Visualiser les prévisions sous forme de graphiques
- Obtenir les données brutes au format JSON

## Exemples d'utilisation

### Exemple 1: Mise en place initiale
```bash
python run.py setup
python run.py init
python run.py deploy
```

### Exemple 2: Mise à jour complète
```bash
python run.py all
```

### Exemple 3: Accès programmatique à l'API
```python
import requests
response = requests.get('http://127.0.0.1:5050/predict?steps=30&format=json')
forecasts = response.json()
print(f"Prix prévu dans 30 jours: ${forecasts['forecasts'][-1]['Prix_Prévu']:.2f}")
```

## Structure des fichiers

- `deploy.py`: Script principal de déploiement
- `update_data.py`: Mise à jour des données
- `retrain_model.py`: Réentraînement du modèle
- `init_deployment.py`: Initialisation du système
- `run.py`: Interface simplifiée
- `setup.sh`/`setup.bat`: Scripts d'installation
- `requirements.txt`: Dépendances requises
- `README.md`: Documentation complète

## Aide et support

Pour plus de détails, consultez le fichier `README.md`.

---

**Avertissement**: Ce système est fourni à titre informatif uniquement et ne constitue pas un conseil d'investissement.