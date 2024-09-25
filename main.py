from twikit import Client, TooManyRequests
import time
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint


MINIMUM_TWEETS = 30
# Consulta para obtener tweets geolocalizados por zona
QUERY = 'lang:es geocode:-27.4692,-58.8306,50km until:2024-08-25 since:2024-01-01'

# definimos una funcion para obtener los tweets
def get_tweets(tweets):
    if tweets is None:
        #* get tweets
        print(f'{datetime.now()} - Getting tweets...')
        tweets = client.search_tweet(QUERY, product='Top')
    else:
        wait_time = randint(5, 10)
        print(f'{datetime.now()} - Getting next tweets after {wait_time} seconds ...')
        time.sleep(wait_time)
        tweets = tweets.next()

    return tweets

# Crea un archivo csv vacio, alli cargaremos los tweets
with open('tweets de corrientes.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Cuenta_Twitter', 'Usuario', 'Texto', 'Created At', 'Retweets', 'Likes'])



# Leemos el archivo cookies.json
client = Client(language='en-US')
client.load_cookies('cookies.json')

# Tambien agregue esto, El resto del código permanece igual.
# tweets = client.search_tweet(QUERY, product='Top')

tweet_count = 0
tweets = None

while tweet_count < MINIMUM_TWEETS:

    try:
        tweets = get_tweets(tweets)
    except TooManyRequests as e:
        rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
        print(f'{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset}')
        wait_time = rate_limit_reset - datetime.now()
        time.sleep(wait_time.total_seconds())
        continue

    if not tweets:
        print(f'{datetime.now()} - No more tweets found')
        break

    for tweet in tweets:
        tweet_count += 1
        tweet_data = [tweet_count, tweet.user.name, tweet.text, tweet.created_at, tweet.retweet_count, tweet.favorite_count]
      
       # Esto no funciono
       # with open('tweets.csv', 'a', newline='') as file:
       #     writer = csv.writer(file)
       #     writer.writerow(tweet_data)
       #     writer.writerow(tweet_data)

        with open('tweets de corrientes.csv', 'a', newline='', encoding='utf-8') as file:
             writer = csv.writer(file)
             writer.writerow(tweet_data)


    print(f'{datetime.now()} - Got {tweet_count} tweets')


print(f'{datetime.now()} - Done! Got {tweet_count} tweets found')