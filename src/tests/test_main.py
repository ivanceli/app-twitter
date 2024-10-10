import pytest
from ..main_prueba2 import save_tweets_to_csv
from twikit import Client

@pytest.fixture
def mock_client():
    client = Client(language='en-US')
    client.load_cookies('cookies.json')
    return client

def test_save_tweets_last_month(mock_client):
    tweet_count, filename = save_tweets_to_csv(mock_client, '1')  # Último mes
    assert tweet_count >= 20, f"Se obtuvieron menos de 90 tweets: {tweet_count}"
    assert filename == 'tweets_de_corrientes_del_ultimo_mes.csv'

def test_save_tweets_last_year(mock_client):
    tweet_count, filename = save_tweets_to_csv(mock_client, '2')  # Último año
    assert tweet_count >= 20, f"Se obtuvieron menos de 90 tweets: {tweet_count}"
    assert filename == 'tweets_de_corrientes_del_ultimo_año.csv'


