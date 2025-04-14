import sys
import os
from pathlib import Path

# Importer les fonctionnalités du module principal
from deploiement import load_deployment_data, predict_tesla_prices, plot_tesla_forecast, save_forecast_report, app

def main():
    """Fonction principale pour le déploiement"""
    # Afficher le message de bienvenue
    print("="*80)
    print("DÉPLOIEMENT DU MODÈLE PRÉDICTIF TESLA")
    print("="*80)
    
    # Charger les données
    model, metadata, latest_data = load_deployment_data()
    
    if model is None:
        print("ERREUR: Impossible de continuer sans modèle.")
        return
    
    # Afficher les informations du modèle
    print("\nInformations du modèle:")
    print(f"Type: {metadata.get('type', 'Inconnu')}")
    print(f"Date de création: {metadata.get('date_creation', 'Inconnue')}")
    print(f"Dernier prix: ${metadata.get('last_price', 0):.2f}")
    print(f"Dernière date: {metadata.get('last_date', 'Inconnue')}")
    
    # Générer un rapport initial
    print("\nGénération du rapport initial...")
    
    try:
        # Générer les prévisions
        last_price = metadata.get('last_price', 257.74)
        forecast_df = predict_tesla_prices(model, metadata, steps=30, last_price=last_price)
        
        # Générer le graphique
        plot = plot_tesla_forecast(forecast_df, last_price, title="Prévision Initiale du Prix Tesla")
        
        # Afficher une synthèse
        final_price = forecast_df['Prix_Prévu'].iloc[-1]
        change_pct = (final_price / last_price - 1) * 100
        
        print(f"\nSynthèse de la prévision à 30 jours:")
        print(f"Prix actuel: ${last_price:.2f}")
        print(f"Prix prévu dans 30 jours: ${final_price:.2f}")
        print(f"Variation prévue: {change_pct:.2f}%")
        
        # Sauvegarder le rapport
        report_path = save_forecast_report(forecast_df, last_price, metadata, plot)
        
        # Démarrer l'API Flask
        print("\nDémarrage de l'API de prévision...")
        print("Accédez à l'interface via http://127.0.0.1:5050")
        
        # Utiliser un port différent pour éviter les conflits
        app.run(debug=False, host='0.0.0.0', port=5050)
        
    except Exception as e:
        print(f"Erreur lors de la génération du rapport initial: {str(e)}")
        import traceback
        traceback.print_exc()

# Exécuter la fonction principale si ce script est exécuté directement
if __name__ == "__main__":
    main()