"""
Moduł testów dla systemu rekomendacji filmów

Zawiera testy jednostkowe dla:
- Komunikacji z API TMDb
- Tworzenia obiektów Movie
- Algorytmu rekomendacji
- Funkcjonalności użytkownika
"""

import json
from api import search_movies
from models import Movie, User
from recommender import create_recommender

def test_api():
    """
    Test funkcjonalności wyszukiwania filmów w API
    Pozwala użytkownikowi przetestować wyszukiwanie
    """
    user_movie = input("Podaj nazwę jakiegoś filmu: ")
    
    # Wywołujemy funkcję search_movies z podanym tytułem
    movies = search_movies(user_movie)
    
    # Sprawdzamy, czy coś znaleziono
    if movies:
        print(f"Znaleziono {len(movies)} filmów pasujących do zapytania '{user_movie}':")
        # Wyświetlamy informacje o każdym znalezionym filmie
        for i, movie in enumerate(movies[:5], 1):  # Pokazujemy max 5 wyników
            title = movie.get('title', 'Brak tytułu')
            year = movie.get('release_date', '')[:4] if movie.get('release_date') else 'Brak daty'
            rating = movie.get('vote_average', 'Brak oceny')
            print(f"{i}. {title} ({year}) - Ocena: {rating}/10")
    else:
        print(f"Nie znaleziono filmów pasujących do '{user_movie}'.")

def test_movie_creation():
    """
    Test tworzenia obiektów Movie z danych API
    Sprawdza poprawność mapowania danych i tworzenia obiektów
    """
    # 1. Wyszukaj film
    movies = search_movies("Matrix")
    
    if movies:
        # 2. Weź pierwszy znaleziony film
        first_movie = movies[0]
        
        # 3. Stwórz obiekt Movie używając from_api_data
        movie = Movie.from_api_data(first_movie)
        
        # 4. Sprawdź czy wszystkie pola są poprawnie wypełnione
        print("\nTest tworzenia obiektu Movie:")
        print(f"ID: {movie.movie_id}")
        print(f"Tytuł: {movie.title}")
        print(f"Rok: {movie.year}")
        print(f"Ocena: {movie.avg_rating}")
        print(f"Czas trwania: {movie.runtime}")
        print(f"Gatunki: {movie.genres}")
        
        # 5. Sprawdź czy wartości są sensowne
        assert movie.movie_id > 0, "ID filmu powinno być większe od 0"
        assert movie.title != "Brak tytułu", "Tytuł nie powinien być domyślny"
        assert movie.year > 1900, "Rok powinien być sensowny"
        assert 0 <= movie.avg_rating <= 10, "Ocena powinna być między 0 a 10"
        assert movie.runtime >= 0, "Czas trwania nie powinien być ujemny"
        assert movie.genres != "", "Gatunki nie powinny być puste"
        
        print("\nWszystkie testy przeszły pomyślnie!")
    else:
        print("Nie znaleziono filmów do testowania")

def test_user_functionality():
    """
    Test funkcjonalności użytkownika
    Sprawdza zarządzanie ocenami i historią oglądania
    """
    print("\n--- Test funkcjonalności użytkownika ---")
    
    # Tworzenie testowego użytkownika
    test_user = User(999, "TestUser")
    
    # Test dodawania filmu do historii
    print("Test dodawania filmu do historii...")
    test_user.add_to_history(550)  # Fight Club
    
    # Test oceniania filmu
    print("Test oceniania filmu...")
    # Symulacja oceny (w rzeczywistym teście użytkownik wpisałby ocenę)
    test_user.user_ratings[550] = 9.0
    test_user.save_user_data()
    
    print("Testy użytkownika zakończone pomyślnie!")

def test_recommendation_algorithm():
    """
    Test algorytmu rekomendacji
    Sprawdza generowanie rekomendacji na podstawie preferencji
    """
    print("\n--- Test algorytmu rekomendacji ---")
    
    # Tworzenie testowego użytkownika z ocenami
    test_user = User(888, "TestRecommender")
    
    # Dodanie przykładowych ocen (filmy z różnych gatunków)
    test_ratings = {
        550: 9.0,  # Fight Club (Dramat, Thriller)
        13: 8.5,   # Forrest Gump (Dramat, Romans)
        238: 8.0,  # The Godfather (Dramat, Kryminał)
    }
    
    test_user.user_ratings = test_ratings
    test_user.save_user_data()
    
    # Tworzenie rekomendera
    recommender = create_recommender(test_user)
    
    # Test generowania rekomendacji
    print("Generowanie rekomendacji...")
    recommendations = recommender.get_recommendations(limit=5)
    
    if recommendations:
        print(f"Znaleziono {len(recommendations)} rekomendacji:")
        for i, (movie, score) in enumerate(recommendations[:3], 1):
            print(f"{i}. {movie.title} - Wynik: {score:.2f}")
    else:
        print("Nie znaleziono rekomendacji")
    
    # Test statystyk użytkownika
    print("\nTest statystyk użytkownika...")
    stats = recommender.get_user_statistics()
    print(f"Średnia ocena: {stats['average_rating']:.2f}")
    print(f"Ulubiony gatunek: {stats['favorite_genre']}")
    
    print("Test algorytmu rekomendacji zakończony!")

def run_all_tests():
    """
    Uruchamia wszystkie testy w kolejności
    """
    print("=== URUCHAMIANIE TESTÓW SYSTEMU REKOMENDACJI ===\n")
    
    try:
        # Test 1: API
        print("1. Test API...")
        test_api()
        
        # Test 2: Tworzenie obiektów Movie
        print("\n2. Test tworzenia obiektów Movie...")
        test_movie_creation()
        
        # Test 3: Funkcjonalność użytkownika
        print("\n3. Test funkcjonalności użytkownika...")
        test_user_functionality()
        
        # Test 4: Algorytm rekomendacji
        print("\n4. Test algorytmu rekomendacji...")
        test_recommendation_algorithm()
        
        print("\n=== WSZYSTKIE TESTY ZAKOŃCZONE POMYŚLNIE ===")
        
    except Exception as e:
        print(f"\nBłąd podczas testowania: {e}")
        print("=== TESTY ZAKOŃCZONE Z BŁĘDAMI ===")

if __name__ == "__main__":
    # Wybór testu do uruchomienia
    print("Wybierz test do uruchomienia:")
    print("1. Test API")
    print("2. Test tworzenia obiektów Movie")
    print("3. Test funkcjonalności użytkownika")
    print("4. Test algorytmu rekomendacji")
    print("5. Uruchom wszystkie testy")
    
    choice = input("\nWpisz numer (1-5): ")
    
    if choice == "1":
        test_api()
    elif choice == "2":
        test_movie_creation()
    elif choice == "3":
        test_user_functionality()
    elif choice == "4":
        test_recommendation_algorithm()
    elif choice == "5":
        run_all_tests()
    else:
        print("Nieprawidłowy wybór. Uruchamiam test API...")
        test_api()

