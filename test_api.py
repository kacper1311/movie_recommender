import json
from api import search_movies
from models import Movie
"""
movies = search_movies("Matrix")


if movies:
    print(json.dumps(movies[0], indent=4))
""" 



def test_api():
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

if __name__ == "__main__":
    test_api()    


def test_movie_creation():
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

if __name__ == "__main__":
    test_movie_creation()

