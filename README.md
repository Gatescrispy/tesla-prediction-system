# Système de Prédiction TESLA

Ce dépôt contient un système complet de déploiement pour les modèles prédictifs du prix de l'action Tesla. Le système permet de déployer un modèle, de générer des prévisions et d'exposer ces prévisions via une API web interactive.

## Structure du système

Le système comprend les composants suivants :

- `deploiement.py` : Cœur du système avec toutes les fonctionnalités principales
- `deploy.py` : Script principal pour démarrer le système
- `update_data.py` : Script pour mettre à jour les données avec les prix récents de Tesla
- `retrain_model.py` : Script pour réentraîner le modèle avec les données les plus récentes
- `init_deployment.py` : Script pour initialiser le système
- `run.py` : Interface de commande unifiée pour toutes les fonctionnalités
- `setup.sh` / `setup.bat` : Scripts d'installation pour Linux/Mac et Windows
- `requirements.txt` : Liste des dépendances requises

## Prérequis

- Python 3.7 ou supérieur
- Les packages listés dans `requirements.txt`

## Installation rapide

### Sous Windows:
```bash
setup.bat
```

### Sous Linux/macOS:
```bash
bash setup.sh
```

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

## Structure des dossiers

```
resultats/
├── deployment/   # Contient les modèles, métadonnées et données
├── reports/      # Contient les rapports de prévision générés
└── templates/    # Contient les templates HTML pour l'interface web
```

Ces dossiers sont créés automatiquement lors de la première exécution.

## API Web

Une fois le système démarré, l'API web est accessible à l'adresse http://127.0.0.1:5050.

L'API propose les fonctionnalités suivantes:

- Page d'accueil (`/`): Interface utilisateur pour générer des prévisions
- Endpoint de prévision (`/predict`): Génère des prévisions avec les paramètres suivants:
  - `steps`: Nombre de jours à prévoir (défaut: 30)
  - `last_price`: Dernier prix connu (optionnel)
  - `format`: Format de sortie - 'html' ou 'json' (défaut: 'html')

Exemple d'utilisation programmatique:
```python
import requests
import pandas as pd

# Obtenir des prévisions pour les 60 prochains jours au format JSON
response = requests.get('http://127.0.0.1:5050/predict?steps=60&format=json')
data = response.json()

# Convertir les prévisions en DataFrame
forecasts = pd.DataFrame(data['forecasts'])
print(forecasts.head())
```

## Automatisation

Pour une utilisation en production, vous pouvez automatiser les tâches suivantes:

1. Mise à jour quotidienne des données (update_data.py)
2. Réentraînement hebdomadaire du modèle (retrain_model.py)
3. Redémarrage du système après chaque mise à jour majeure

Exemple de configuration cron (Linux/macOS):
```
# Mise à jour quotidienne des données à 18h00
0 18 * * * cd /chemin/vers/projet && python update_data.py

# Réentraînement hebdomadaire du modèle le dimanche à 20h00
0 20 * * 0 cd /chemin/vers/projet && python retrain_model.py
```

## Les modèles supportés

Le système prend en charge plusieurs types de modèles:

1. **ARIMA-GARCH**: Modèle statistique pour la prévision des rendements et de la volatilité
2. **Deep Learning (simulation)**: Simulation de prévisions basées sur des modèles DL comme BiLSTM

Le système est conçu pour être facilement extensible à d'autres modèles.

## Dépannage

### Problèmes courants

- **Le modèle ne se charge pas**: Vérifiez que les fichiers existent dans le dossier `resultats/deployment/`
- **Erreur d'importation de modules**: Vérifiez que toutes les dépendances sont installées
- **L'API ne démarre pas**: Vérifiez qu'aucun autre service n'utilise le port 5050

### Logs

Le système affiche des informations détaillées dans la console. Pour sauvegarder les logs:

```bash
python deploy.py > deployment_log.txt 2>&1
```

## Extension du système

Le système peut être étendu de plusieurs façons:

1. **Ajout de nouveaux modèles**: Modifiez la fonction de prédiction dans `deploiement.py`
2. **Intégration de sources de données alternatives**: Modifiez le script `update_data.py`
3. **Amélioration de l'interface utilisateur**: Modifiez les templates HTML dans le dossier templates

## Guide de démarrage rapide

Pour une mise en route rapide, consultez le [Guide de Démarrage](GUIDE_DEMARRAGE.md).

## Contribuer

Les contributions sont les bienvenues! Vous pouvez contribuer de plusieurs façons:

1. Signaler des bugs
2. Suggérer des améliorations
3. Soumettre des pull requests

## Licence

Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.

---

**Avertissement**: Ce système est fourni à titre informatif uniquement. Les prévisions générées ne constituent pas des conseils d'investissement.