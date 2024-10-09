from datetime import datetime, timedelta
from src.main import calculate_dates  # Importa tu función real

# probar que la función calculate_dates 
# para ver si esta generando las consultas correctamente según la opción seleccionada.

def test_calculate_dates_month():
    today = datetime.today().strftime('%Y-%m-%d')
    expected_since = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')
    since_date, until_date, filename = calculate_dates('1')  # Último mes
    
    assert since_date == expected_since
    assert until_date == today
    assert filename == 'tweets_de_corrientes_del_ultimo_mes.csv'

def test_calculate_dates_year():
    today = datetime.today().strftime('%Y-%m-%d')
    expected_since = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')
    since_date, until_date, filename = calculate_dates('2')  # Último año
    
    assert since_date == expected_since
    assert until_date == today
    assert filename == 'tweets_de_corrientes_del_ultimo_año.csv'

def test_calculate_dates_today():
    today = datetime.today().strftime('%Y-%m-%d')
    since_date, until_date, filename = calculate_dates('3')  # Hoy
    
    assert since_date == today
    assert until_date == today
    assert filename == 'tweets_de_corrientes_de_hoy.csv'
