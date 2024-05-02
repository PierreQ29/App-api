import streamlit as st
import requests
from applicationinsights import TelemetryClient

st.title('Prédiction de sentiment de tweet')

# Créer une boîte de texte pour l'entrée de l'utilisateur
tweet = st.text_input('Entrez votre tweet ici:')

# Initialiser st.session_state si nécessaire
if 'prediction' not in st.session_state:
    st.session_state['prediction'] = None

# Ajouter un bouton "Soumettre"
if st.button('Soumettre') and tweet:
    # Envoyer une requête à l'API
    response = requests.post('http://localhost:8000/predict', json={'text': tweet})

    # Vérifier que la requête a réussi
    if response.status_code == 200:
        # Extraire la prédiction de la réponse
        st.session_state['prediction'] = response.json()['sentiment']

        # Afficher la prédiction
        st.write(f"Ce tweet a un sentiment **{st.session_state['prediction']}**.")
    else:
        st.write('Une erreur s\'est produite lors de la prédiction du sentiment.')

# Demander à l'utilisateur si la prédiction était correcte
if st.session_state['prediction'] is not None:
    feedback = st.selectbox('La prédiction était-elle correcte ?', ('Sélectionnez une option', 'Oui', 'Non'))

    # Si l'utilisateur a fourni un feedback "Non", envoyer une requête à l'API de feedback
    if feedback == 'Non':
        requests.post('http://localhost:8000/feedback', json={'text': tweet, 'prediction': st.session_state['prediction'], 'feedback': feedback})









