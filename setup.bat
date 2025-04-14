@echo off
echo =====================================================
echo Installation du systeme de deploiement Tesla
echo =====================================================

REM Vérifier si Python est installé
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Erreur: Python n'est pas installe ou n'est pas dans le PATH.
    echo Veuillez installer Python 3.7 ou superieur.
    exit /b 1
)

echo Utilisation de:
python --version

REM Vérifier si pip est installé
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Erreur: pip n'est pas installe.
    echo Veuillez installer pip pour Python.
    exit /b 1
)

REM Créer un environnement virtuel
echo Creation d'un environnement virtuel...
python -m venv venv
if %errorlevel% neq 0 (
    echo Erreur lors de la creation de l'environnement virtuel.
    echo Tentative d'installation sans environnement virtuel...
    set USE_VENV=false
) else (
    set USE_VENV=true
)

REM Activer l'environnement virtuel
if "%USE_VENV%"=="true" (
    if exist venv\Scripts\activate.bat (
        call venv\Scripts\activate.bat
        echo Environnement virtuel active.
    ) else (
        echo Erreur: Impossible d'activer l'environnement virtuel.
        echo Tentative d'installation sans environnement virtuel...
        set USE_VENV=false
    )
)

REM Installer les dépendances
echo Installation des dependances...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Erreur lors de l'installation des dependances.
    exit /b 1
)

REM Initialiser le système
echo Initialisation du systeme de deploiement...
python init_deployment.py
if %errorlevel% neq 0 (
    echo Erreur lors de l'initialisation du systeme.
    exit /b 1
)

echo =====================================================
echo Installation terminee avec succes!
echo.
echo Pour demarrer le systeme:
if "%USE_VENV%"=="true" (
    echo 1. Activez l'environnement virtuel: venv\Scripts\activate
    echo 2. Executez: python deploy.py
) else (
    echo Executez: python deploy.py
)
echo =====================================================

pause