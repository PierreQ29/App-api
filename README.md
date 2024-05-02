# Réalisez une analyse de sentiments grâce au Deep Learning

## Objectif du Projet

Ce projet a pour but de développer une API qui prédit le sentiment d'un tweet. L'API prend un tweet en entrée et renvoie une prédiction de sentiment (positif ou négatif). Les prédictions sont basées sur un modèle de machine learning entraîné sur un ensemble de données de tweets en anglais.

## Structure du Projet

L'API est déployé sur Heroku à l'adresse : https://apiappocp7-dde30b3da808.herokuapp.com/

Si vous souhaitez déployer votre propre modèle, n'oubliez pas de changer l'adresse de l'API dans le fichier stream.py au niveau de l'appel des 2 routes /predict et /feedback.

Le projet est organisé en plusieurs fichiers :

- Model : Dossier contenant le modèle et le vectoriseur utilisés pour transformer les tweets en vecteurs. Le modèle a été entraîné en dehors de ce projet et est chargé à partir d'un fichier pickle. 

- API.py : Ce fichier contient le code de l'API FastAPI. L'API a une seule route, `/predict`, qui prend un tweet en entrée et renvoie une prédiction de sentiment. 

- Procfile : Fichier utilisé par Heroku pour déterminer comment éxecuter l'application.

- app.json : Contient la configuration de l’application pour Heroku, y compris les add-ons et autres paramètres nécessaires au déploiement.

- stream.py : Ce fichier permet de communiquer avec l'API déployé sur le cloud. Il est a executer en local.

- requirements.txt : Ce fichier liste les librairies nécessaires au bon fonctionnement de l'application.

- nltk.txt : Contient les librairies nltk à télécharger.

- pytest.ini : Fichier de configuration pour pytest.

- test_app.py: Contient les tests unitaires pour vérifier que l’application fonctionne comme prévu.

- runtime.txt : Spécifie la version de Python à utiliser lors de l’exécution de l’application sur Heroku.



## Utilisation

- Téléchargez le fichier stream.py ainsi que le fichier requirements.txt ou cloner directement tout le repository avec git clone.

- Définir un nouvel environnement.

- Installer les librairies dans le nouvel environnement en executant "pip install -r requirements.txt".

- Executer le script stream.py en utilisant streamlit. Dans le terminal executer "streamlit run strem.py".

- L'interface utilisateur s'ouvre et vous demande de saisir un tweet. L'application est réalisée pour travailler sur des tweets en anglais.

- Saisissez un tweet puis cliquez sur soumettre.

- Après quelques seconde le sentiment du tweet est affiché.

- Pour un suivi optimal, il vous est ensuite demandé de dire si oui ou non le sentiment annoncé par le modèle correspond au sentiment réél du tweet que vous avez saisi.

- Si un trop grand nombre de mauvaise prédiction est réalisé (3 mauvaise prédiction en moins de 5 min), une alerte est créé et un mail est envoyé. Une application Azure Application Insights à été créé pour le suivi.


## Déploiement conitnu

La plateforme Heroku a été configuré pour un déploiement continu pour cette application. A chaque push sur Github, une vérification est lancée avec Heroku CI avant de redéployer l'application sur Heroku.
Cette vérification effectue 2 tests pour valider le bon fonctionnement du modèle. Il vérifie si la prédiction du mot love est bien positive et que la prédiction du mot hate est bien négative.
Une fois ces vérifications réalisée, Heroku redéploie le modèle actualisée automatiquement.


