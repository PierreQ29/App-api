import streamlit as st
import requests

st.title('Prédiction de sentiment de tweet')

# Créer une boîte de texte pour l'entrée de l'utilisateur
tweet = st.text_input('Entrez votre tweet ici:')

if tweet:
    # Envoyer une requête à l'API
    response = requests.post('http://localhost:8000/predict', json={'text': tweet})

    # Vérifier que la requête a réussi
    if response.status_code == 200:
        # Extraire la prédiction de la réponse
        prediction = response.json()['sentiment']

        # Afficher la prédiction
        st.write(f'Ce tweet a un sentiment **{prediction}**.')
    else:
        st.write('Une erreur s\'est produite lors de la prédiction du sentiment.')