import requests

def test_predict_sentiment():
    # Test pour le mot "love"
    response = requests.post('https://testapiapp-5f6b29d3d155.herokuapp.com/predict', json={'text': 'love'})
    assert response.status_code == 200
    assert response.json()['sentiment'] == 'positif'

    # Test pour le mot "hate"
    response = requests.post('https://testapiapp-5f6b29d3d155.herokuapp.com/predict', json={'text': 'hate'})
    assert response.status_code == 200
    assert response.json()['sentiment'] == 'négatif'
