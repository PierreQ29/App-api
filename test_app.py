import requests
import time

def wait_for_app_to_be_ready():
    while True:
        try:
            response = requests.get('https://apiappocp7-dde30b3da808.herokuapp.com/health')
            if response.status_code == 200:
                break
        except:
            pass
        time.sleep(1)

def test_predict_sentiment():
    wait_for_app_to_be_ready()

    # Test pour le mot "love"
    response = requests.post('https://apiappocp7-dde30b3da808.herokuapp.com/predict', json={'text': 'love'})
    assert response.status_code == 200
    assert response.json()['sentiment'] == 'positif'

    # Test pour le mot "hate"
    response = requests.post('https://apiappocp7-dde30b3da808.herokuapp.com/predict', json={'text': 'hate'})
    assert response.status_code == 200
    assert response.json()['sentiment'] == 'négatif'
