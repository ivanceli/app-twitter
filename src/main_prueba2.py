from twikit import Client, TooManyRequests
import time
from datetime import datetime, timedelta
import csv
from random import randint

MINIMUM_TWEETS = 20

def calculate_dates(option):
    today = datetime.today()
    
    if option == '1':  # Último mes
        since_date = (today - timedelta(days=30)).strftime('%Y-%m-%d')
        filename = 'tweets_de_corrientes_del_ultimo_mes.csv'
    elif option == '2':  # Último año
        since_date = (today - timedelta(days=365)).strftime('%Y-%m-%d')
        filename = 'tweets_de_corrientes_del_ultimo_año.csv'
    else:
        raise ValueError("Opción no válida")
    
    until_date = today.strftime('%Y-%m-%d')
    return since_date, until_date, filename

def get_tweets(client, tweets, query):
    if tweets is None:
        tweets = client.search_tweet(query, product='Top')
    else:
        time.sleep(randint(5, 10))
        tweets = tweets.next()

    return tweets

def save_tweets_to_csv(client, user_option):
    SINCE_DATE, UNTIL_DATE, FILENAME = calculate_dates(user_option)
    QUERY = f'lang:es geocode:-27.4692,-58.8306,50km until:{UNTIL_DATE} since:{SINCE_DATE}'

    tweet_count = 0
    tweets = None

    with open(FILENAME, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Cuenta_Twitter', 'Usuario', 'Texto', 'Creado en', 'Retweets', 'Likes'])

        while tweet_count < MINIMUM_TWEETS:
            try:
                tweets = get_tweets(client, tweets, QUERY)
            except TooManyRequests as e:
                rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
                wait_time = rate_limit_reset - datetime.now()
                time.sleep(wait_time.total_seconds())
                continue
            except ConnectionError as e:
                time.sleep(30)
                continue
            except Exception as e:
                break

            if not tweets:
                break

            for tweet in tweets:
                try:
                    tweet_count += 1
                    tweet_data = [tweet.user.screen_name, tweet.user.name, tweet.text, tweet.created_at, tweet.retweet_count, tweet.favorite_count]
                    writer.writerow(tweet_data)
                except Exception as e:
                    continue

    return tweet_count, FILENAME

if __name__ == "__main_prueba2__":
    client = Client(language='en-US')
    client.load_cookies('cookies.json')
    # Puedes elegir la opción aquí
    save_tweets_to_csv(client, '1')  # Opción 1: Último mes
