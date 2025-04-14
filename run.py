import sys
import os
import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser(description="Interface de gestion du système de déploiement Tesla")
    
    # Options principales
    parser.add_argument('action', type=str, choices=['setup', 'init', 'deploy', 'update', 'retrain', 'all'],
                        help='Action à exécuter')
    
    # Options supplémentaires
    parser.add_argument('--port', type=int, default=5050,
                        help='Port pour le serveur API (défaut: 5050)')
    parser.add_argument('--no-browser', action='store_true',
                        help="Ne pas ouvrir automatiquement le navigateur")
    parser.add_argument('--debug', action='store_true',
                        help="Activer le mode debug")
    
    args = parser.parse_args()
    
    # Exécuter l'action demandée
    if args.action == 'setup':
        print("Configuration du système...")
        if os.name == 'nt':  # Windows
            result = subprocess.run(['setup.bat'], shell=True)
        else:  # Linux/Mac
            result = subprocess.run(['bash', 'setup.sh'])
        
        if result.returncode != 0:
            print("Erreur lors de la configuration.")
            sys.exit(1)
    
    elif args.action == 'init':
        print("Initialisation du système...")
        result = subprocess.run([sys.executable, 'init_deployment.py'])
        
        if result.returncode != 0:
            print("Erreur lors de l'initialisation.")
            sys.exit(1)
    
    elif args.action == 'update':
        print("Mise à jour des données...")
        result = subprocess.run([sys.executable, 'update_data.py'])
        
        if result.returncode != 0:
            print("Erreur lors de la mise à jour des données.")
            sys.exit(1)
    
    elif args.action == 'retrain':
        print("Réentraînement du modèle...")
        result = subprocess.run([sys.executable, 'retrain_model.py'])
        
        if result.returncode != 0:
            print("Erreur lors du réentraînement du modèle.")
            sys.exit(1)
    
    elif args.action == 'deploy':
        print(f"Démarrage du système sur le port {args.port}...")
        # Ajouter des arguments pour deploy.py
        deploy_args = [sys.executable, 'deploy.py']
        if args.port != 5050:
            deploy_args.extend(['--port', str(args.port)])
        if args.debug:
            deploy_args.append('--debug')
        if not args.no_browser:
            deploy_args.append('--open-browser')
        
        # Exécuter deploy.py
        subprocess.run(deploy_args)
    
    elif args.action == 'all':
        print("Exécution complète: mise à jour, réentraînement et déploiement...")
        
        # Mise à jour des données
        print("\n1. Mise à jour des données...")
        result = subprocess.run([sys.executable, 'update_data.py'])
        if result.returncode != 0:
            print("Erreur lors de la mise à jour des données.")
            sys.exit(1)
        
        # Réentraînement du modèle
        print("\n2. Réentraînement du modèle...")
        result = subprocess.run([sys.executable, 'retrain_model.py'])
        if result.returncode != 0:
            print("Erreur lors du réentraînement du modèle.")
            sys.exit(1)
        
        # Déploiement
        print(f"\n3. Démarrage du système sur le port {args.port}...")
        deploy_args = [sys.executable, 'deploy.py']
        if args.port != 5050:
            deploy_args.extend(['--port', str(args.port)])
        if args.debug:
            deploy_args.append('--debug')
        if not args.no_browser:
            deploy_args.append('--open-browser')
        
        subprocess.run(deploy_args)

if __name__ == "__main__":
    main()