import pytest
from src.main import get_tweets, TooManyRequests

def test_too_many_requests_handling(monkeypatch):
    class MockClient:
        def search_tweet(self, query, product):
            raise TooManyRequests(rate_limit_reset=1622650000)
    
    # Simular un cliente que lanza TooManyRequests
    monkeypatch.setattr('src.main.client', MockClient())
    
    with pytest.raises(TooManyRequests):
        get_tweets(None)
