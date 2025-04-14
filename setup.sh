#!/bin/bash

# Script d'installation pour le système de déploiement Tesla

echo "====================================================="
echo "Installation du système de déploiement Tesla"
echo "====================================================="

# Vérifier si Python est installé
if command -v python3 &>/dev/null; then
    PYTHON_CMD=python3
elif command -v python &>/dev/null; then
    PYTHON_CMD=python
else
    echo "Erreur: Python n'est pas installé."
    echo "Veuillez installer Python 3.7 ou supérieur."
    exit 1
fi

echo "Utilisation de: $($PYTHON_CMD --version)"

# Vérifier si pip est installé
if ! $PYTHON_CMD -m pip --version &>/dev/null; then
    echo "Erreur: pip n'est pas installé."
    echo "Veuillez installer pip pour Python."
    exit 1
fi

# Créer un environnement virtuel
echo "Création d'un environnement virtuel..."
$PYTHON_CMD -m venv venv || {
    echo "Erreur lors de la création de l'environnement virtuel."
    echo "Tentative d'installation sans environnement virtuel..."
    USE_VENV=false
}

# Activer l'environnement virtuel
if [ "$USE_VENV" != "false" ]; then
    if [ -f venv/bin/activate ]; then
        source venv/bin/activate
        echo "Environnement virtuel activé."
    elif [ -f venv/Scripts/activate ]; then
        source venv/Scripts/activate
        echo "Environnement virtuel activé."
    else
        echo "Erreur: Impossible d'activer l'environnement virtuel."
        echo "Tentative d'installation sans environnement virtuel..."
        USE_VENV=false
    fi
fi

# Installer les dépendances
echo "Installation des dépendances..."
pip install -r requirements.txt || {
    echo "Erreur lors de l'installation des dépendances."
    exit 1
}

# Initialiser le système
echo "Initialisation du système de déploiement..."
$PYTHON_CMD init_deployment.py || {
    echo "Erreur lors de l'initialisation du système."
    exit 1
}

echo "====================================================="
echo "Installation terminée avec succès!"
echo ""
echo "Pour démarrer le système:"
if [ "$USE_VENV" != "false" ]; then
    echo "1. Activez l'environnement virtuel: source venv/bin/activate (Linux/Mac) ou venv\\Scripts\\activate (Windows)"
    echo "2. Exécutez: python deploy.py"
else
    echo "Exécutez: python deploy.py"
fi
echo "====================================================="