from twikit import Client, TooManyRequests
import time
from datetime import datetime, timedelta
import csv
from random import randint

MINIMUM_TWEETS = 90

# Definir una función para calcular las fechas dinámicamente
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

# Solicitar al usuario la opción deseada
print("Seleccione una opción:")
print("1: Obtener tweets del último mes")
print("2: Obtener tweets del último año")
user_option = input("Ingrese el número de su elección: ")

# Calcular las fechas y obtener el nombre del archivo según la opción del usuario
SINCE_DATE, UNTIL_DATE, FILENAME = calculate_dates(user_option)

# Construir la consulta basada en la opción del usuario
QUERY = f'lang:es geocode:-27.4692,-58.8306,50km until:{UNTIL_DATE} since:{SINCE_DATE}'

# Definimos una función para obtener tweets
def get_tweets(tweets):
    if tweets is None:
        print(f'{datetime.now()} - Obteniendo tweets...')
        tweets = client.search_tweet(QUERY, product='Top')
    else:
        wait_time = randint(5, 10)
        print(f'{datetime.now()} - Obteniendo más tweets después de {wait_time} segundos...')
        time.sleep(wait_time)
        tweets = tweets.next()

    return tweets

# Crea un archivo CSV vacío
with open(FILENAME, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Cuenta_Twitter', 'Usuario', 'Texto', 'Creado en', 'Retweets', 'Likes'])

# Cargar las cookies
client = Client(language='en-US')
client.load_cookies('cookies.json')

tweet_count = 0
tweets = None

# Abrimos el archivo CSV una vez para evitar repetir operaciones de IO
with open(FILENAME, 'a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    while tweet_count < MINIMUM_TWEETS:
        try:
            tweets = get_tweets(tweets)
        except TooManyRequests as e:
            rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
            print(f'{datetime.now()} - Límite de solicitudes alcanzado. Esperando hasta {rate_limit_reset}')
            wait_time = rate_limit_reset - datetime.now()
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

        print(f'{datetime.now()} - Se han obtenido {tweet_count} tweets')

print(f'{datetime.now()} - ¡Listo! Se han obtenido {tweet_count} tweets')