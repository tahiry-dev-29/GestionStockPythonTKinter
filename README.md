# GestionStockPythonTKinter

### Creer Env Virtuel

python3 -m venv venv

### Active Env Virtuel avec Dans Fish

. venv/bin/activate.fish

### Installer des paquets dans l'environnement virtuel

pip install -r requirements.txt

### Désactiver l'environnement virtuel

deactivate

### Lister

pip list

### si une probleme sur linstallation de tk sur ubuntu

sudo apt-get install python3-tk

# Gestion de Stock Python Tkinter

Une application de gestion de stock développée avec Python et Tkinter.

## Prérequis

-  Python 3.x
-  SQLite3
-  Tkinter

## Installation

1. Clonez le repository :

```bash
git clone https://github.com/tahiry-dev-29/GestionStockPythonTKinter.git
cd GestionStockPythonTKinter
```

2. Créez un environnement virtuel (optionnel mais recommandé surtout sur UBUNTU) :

```bash
python -m venv venv
source venv/bin/activate  # Sur Linux/Mac
# ou
venv\Scripts\activate  # Sur Windows
```

3. Installez les dépendances :

```bash
pip install -r requirements.txt
```

## Lancement de l'application

Pour lancer l'application, exécutez :

```bash
python main.py
```

## Structure du projet

```
GestionStockPythonTKinter/
│
├── database/
│   ├── __init__.py
│   └── db_manager.py
│
├── models/
│   ├── __init__.py
│   └── product.py
│
├── views/
│   ├── __init__.py
│   └── main_window.py
│
├── main.py
├── requirements.txt
└── README.md
```

## Fonctionnalités

-  Ajout de produits
-  Modification des quantités
-  Consultation du stock
-  Gestion des prix
