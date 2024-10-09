from src.main import MINIMUM_TWEETS, get_tweets

def test_minimum_tweets_retrieved():
    tweet_count = 0
    tweets = None
    
    while tweet_count < MINIMUM_TWEETS:
        tweets = get_tweets(tweets)
        tweet_count += len(tweets)
    
    assert tweet_count >= MINIMUM_TWEETS
