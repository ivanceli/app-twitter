import pytest
from src.main import get_tweets

def test_get_tweets():
    # Configuración de la prueba
    cantidad_esperada = 30  # Ajusta este valor según lo que esperas
    
    # Llamamos a la función que obtiene los tweets
    tweets = get_tweets()

    # Verificamos que se hayan obtenido al menos 'cantidad_esperada' tweets
    assert len(tweets) >= cantidad_esperada, f"Se obtuvieron {len(tweets)} tweets, pero se esperaban al menos {cantidad_esperada}"

