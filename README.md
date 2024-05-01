# Réalisez une analyse de sentiments grâce au Deep Learning

## Objectif du Projet

Ce projet a pour but de développer une API qui prédit le sentiment d'un tweet. L'API prend un tweet en entrée et renvoie une prédiction de sentiment (positif ou négatif). Les prédictions sont basées sur un modèle de machine learning entraîné sur un ensemble de données de tweets.

## Structure du Projet

Le projet est organisé en plusieurs fichiers :

- Model : Ce dossier contient le modèle de machine learning et le vectoriseur utilisés pour transformer les tweets en vecteurs. Le modèle a été entraîné en dehors de ce projet et est chargé à partir d'un fichier pickle.

- API.py : Ce fichier contient le code de l'API FastAPI. L'API a une seule route, `/predict`, qui prend un tweet en entrée et renvoie une prédiction de sentiment. 

- stream.py : Ce fichier permet de communiquer avec l'API déployé sur le cloud. 

- test_app.py : Ce fichier contient les tests unitaires pour l'API. Les tests vérifient que l'API renvoie les bonnes prédictions pour un ensemble de tweets de test lors du déploiement continu. Il vérifie les bonnes prédictions de 2 mots (love et hate) avant le déploiement après un nouveau push.

- requirements.txt : Ce fichier liste les librairies nécessaires au bon fonctionnement de l'application.

- Les autres fichiers permettent le bon fonctionnement du déploiement continu sur la plateforme cloud.


## Utilisation
-Télécharger le fichier stream.py ainsi que le fichier requirements.txt ou cloner directement tout le repository avec git clone.
- Définir un nouvel environnement.
- Installer les librairies dans le nouvel environnement en executant "pip install -r requirements.txt"
- Executer le script stream.py en utilisant streamlit. Dans le terminal executer "streamlit run strem.py"
- L'interface utilisateur s'ouvre et vous demande de saisir un tweet. L'application est réalisé pour travailler sur des tweets en anglais.
- Saisissez un tweet et appuyer sur la touche entrée.
- Après quelques seconde le sentiment du tweet est affiché.
- Pour un suivi optimal, il vous est ensuite demandé de dire si oui ou non le sentiment annoncé par le modèle correspond au sentiment réél du tweet que vous avez saisi.
