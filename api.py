"""
Moduł komunikacji z API filmowym

Zawiera funkcje do pobierania danych o filmach z The Movie Database API.
"""

import requests
from config import API_KEY, BASE_URL, LANGUAGE

def call_api(endpoint, params=None):
    # Inicjalizacja parametrów
    if params is None:
        params = {}
        
    # Dodanie wymaganych parametrów autoryzacji
    params['api_key'] = API_KEY
    params['language'] = LANGUAGE
    
    # Kompletny URL zapytania
    url = BASE_URL + endpoint
    
    try:
        # Wykonanie zapytania HTTP
        response = requests.get(url, params=params)
        response.raise_for_status()  # Sprawdzenie statusu odpowiedzi
        return response.json()  # Konwersja JSON na słownik
    except requests.exceptions.RequestException as e:
        print(f"Błąd podczas komunikacji z API: {e}")
        return None
    
def search_movies(query):
    endpoint = "/search/movie"  # Endpoint do wyszukiwania filmów
    params = {"query": query}  # Parametr wyszukiwania
    
    # Pobranie wyników z API
    results = call_api(endpoint, params)
    
    # Ekstrakcja listy filmów z odpowiedzi
    if results and 'results' in results:
        return results['results']
    else:
        return []
    
def runtime(id):
    endpoint = f"/movie/{id}"
    
    result = call_api(endpoint, params={})
    
    if result and 'runtime' in result:
        return result['runtime']
    else:
        return 0
    
def movie_for_id(id):
    from models import Movie
    endpoint = f"/movie/{id}"  # Endpoint do wyszukiwania filmów
    
    # Pobranie wyników z API
    results = call_api(endpoint, params={})
    
    # Ekstrakcja listy filmów z odpowiedzi
    if results and 'id' in results:
            movie = Movie.from_api_data(results)
            return movie
    else:
        return None