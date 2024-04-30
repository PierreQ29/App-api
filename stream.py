import streamlit as st
import requests
from applicationinsights import TelemetryClient

# Initialisation du client Application Insights
instrumentation_key = '43e208fa-70a1-4839-9d08-920a10b88db7'   # Remplacez par votre clé d'instrumentation
client = TelemetryClient(instrumentation_key)
st.title('Prédiction de sentiment de tweet')

# Créer une boîte de texte pour l'entrée de l'utilisateur
tweet = st.text_input('Entrez votre tweet ici:')

if tweet:
    # Envoyer une requête à l'API
    response = requests.post('https://apiappocp7-dde30b3da808.herokuapp.com/predict', json={'text': tweet})

    # Vérifier que la requête a réussi
    if response.status_code == 200:
        # Extraire la prédiction de la réponse
        prediction = response.json()['sentiment']

        # Afficher la prédiction
        st.write(f'Ce tweet a un sentiment **{prediction}**.')

        # Demander à l'utilisateur si la prédiction était correcte
        feedback = st.selectbox('La prédiction était-elle correcte ?', ('Sélectionnez une option', 'Oui', 'Non'))

        # Si l'utilisateur a donné son feedback, l'envoyer à Application Insights
        if feedback != 'Sélectionnez une option':
            client.track_trace('feedback', {'tweet': tweet, 'prediction': prediction, 'feedback': feedback})
            client.flush()

    else:
        st.write('Une erreur s\'est produite lors de la prédiction du sentiment.')
