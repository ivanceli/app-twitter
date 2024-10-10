from twikit import Client, TooManyRequests
import time
from datetime import datetime, timedelta
import csv
from random import randint

MINIMUM_TWEETS = 90

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

def get_tweets(tweets):
    if tweets is None:
        tweets = client.search_tweet(QUERY, product='Top')
    else:
        wait_time = randint(5, 10)
        time.sleep(wait_time)
        tweets = tweets.next()

    return tweets

client = Client(language='en-US')
client.load_cookies('cookies.json')

# Definir una lista de opciones para iterar
options = ['1', '2']  # '1' para el último mes y '2' para el último año

for user_option in options:
    SINCE_DATE, UNTIL_DATE, FILENAME = calculate_dates(user_option)
    QUERY = f'lang:es geocode:-27.4692,-58.8306,50km until:{UNTIL_DATE} since:{SINCE_DATE}'

    tweet_count = 0
    tweets = None

    print(f"{datetime.now()} - Comenzando a obtener tweets para la opción: {user_option} ({'Último mes' if user_option == '1' else 'Último año'})")
    
    # Crear el archivo CSV y abrirlo una vez
    with open(FILENAME, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Cuenta_Twitter', 'Usuario', 'Texto', 'Creado en', 'Retweets', 'Likes'])

        while tweet_count < MINIMUM_TWEETS:
            try:
                tweets = get_tweets(tweets)
            except TooManyRequests as e:
                rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
                wait_time = rate_limit_reset - datetime.now()
                print(f'{datetime.now()} - Límite de solicitudes alcanzado. Esperando hasta {rate_limit_reset}')
                time.sleep(wait_time.total_seconds())
                continue
            except ConnectionError as e:
                print(f'{datetime.now()} - Error de conexión: {e}. Intentando de nuevo en 30 segundos.')
                time.sleep(30)
                continue
            except Exception as e:
                print(f'{datetime.now()} - Ocurrió un error inesperado: {e}.')
                break

            if not tweets:
                print(f'{datetime.now()} - No se encontraron más tweets')
                break

            for tweet in tweets:
                try:
                    tweet_count += 1
                    tweet_data = [tweet.user.screen_name, tweet.user.name, tweet.text, tweet.created_at, tweet.retweet_count, tweet.favorite_count]
                    writer.writerow(tweet_data)
                except Exception as e:
                    print(f'{datetime.now()} - Error al procesar un tweet: {e}')
                    continue

        print(f'{datetime.now()} - Se han obtenido {tweet_count} tweets para la opción: {user_option}')

if tweet_count < MINIMUM_TWEETS:
    print(f'Solo se obtuvieron {tweet_count} tweets en total, menos del mínimo requerido de {MINIMUM_TWEETS}.')
else:
    print(f'{datetime.now()} - ¡Listo! Se han obtenido un total de {tweet_count} tweets.')

