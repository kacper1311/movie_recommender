"""
Moduł komunikacji z API filmowym

Zawiera funkcje do pobierania danych o filmach z The Movie Database API.
Obsługuje wyszukiwanie filmów, pobieranie szczegółów i czasu trwania.
Wykorzystuje klucz API z pliku konfiguracyjnego.
"""

import requests
from config import API_KEY, BASE_URL, LANGUAGE

def call_api(endpoint, params=None):
    """
    Wykonuje zapytanie HTTP do API TMDb
    
    Args:
        endpoint: Endpoint API do wywołania (np. "/search/movie")
        params: Parametry zapytania jako słownik
        
    Returns:
        dict: Odpowiedź z API jako słownik lub None w przypadku błędu
    """
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
    """
    Wyszukuje filmy na podstawie zapytania tekstowego
    
    Args:
        query: Tekst do wyszukania (tytuł filmu)
        
    Returns:
        list: Lista filmów pasujących do zapytania lub pusta lista
    """
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
    """
    Pobiera czas trwania filmu na podstawie jego ID
    
    Args:
        id: ID filmu z TMDb
        
    Returns:
        int: Czas trwania w minutach lub 0 w przypadku błędu
    """
    endpoint = f"/movie/{id}"
    
    result = call_api(endpoint, params={})
    
    if result and 'runtime' in result:
        return result['runtime']
    else:
        return 0
    
def movie_for_id(id):
    """
    Pobiera pełne dane filmu na podstawie jego ID
    Tworzy obiekt Movie z danych z API
    
    Args:
        id: ID filmu z TMDb
        
    Returns:
        Movie: Obiekt filmu lub None w przypadku błędu
    """
    from models import Movie
    endpoint = f"/movie/{id}"  # Endpoint do pobierania szczegółów filmu
    
    # Pobranie wyników z API
    results = call_api(endpoint, params={})
    
    # Ekstrakcja danych filmu i utworzenie obiektu
    if results and 'id' in results:
            movie = Movie.from_api_data(results)
            return movie
    else:
        return None