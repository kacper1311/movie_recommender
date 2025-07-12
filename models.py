"""
Moduł definiujący modele danych

Zawiera:
- Klasę Movie reprezentującą film i jego atrybuty
- Klasę User reprezentującą użytkownika i jego preferencje
- Metody do zarządzania ocenami filmów
- Metody do zapisywania i wczytywania danych
- Mapowanie gatunków filmowych z ID na nazwy polskie
"""
from api import runtime
from api import movie_for_id
import json

# Mapowanie ID gatunków z TMDb na polskie nazwy
GENRE_MAPPING = {
    28: "Akcja",
    12: "Przygodowy",
    16: "Animacja",
    35: "Komedia",
    80: "Kryminał",
    99: "Dokumentalny",
    18: "Dramat",
    10751: "Familijny",
    14: "Fantasy",
    36: "Historyczny",
    27: "Horror",
    10402: "Muzyczny",
    9648: "Tajemnica",
    10749: "Romans",
    878: "Science Fiction",
    10770: "Film TV",
    53: "Thriller",
    10752: "Wojenny",
    37: "Western"
}

class Movie:
    """
    Klasa reprezentująca film z jego podstawowymi atrybutami
    Zawiera metody do porównywania filmów i sprawdzania gatunków
    """
    
    def __init__(self, movie_id: int, title: str, year: int, avg_rating: float, runtime: int, genres: str):
        """
        Inicjalizacja obiektu filmu
        
        Args:
            movie_id: Unikalny identyfikator filmu z TMDb
            title: Tytuł filmu
            year: Rok produkcji filmu
            avg_rating: Średnia ocena filmu z TMDb
            runtime: Czas trwania filmu w minutach
            genres: Gatunki filmu jako string oddzielone przecinkami
        """
        self.movie_id = movie_id
        self.title = title
        self.avg_rating = avg_rating
        self.year = year
        self.runtime = runtime
        self.genres = genres

    def __str__(self):
        """
        Reprezentacja string filmu do wyświetlania użytkownikowi
        
        Returns:
            str: Sformatowany opis filmu
        """
        return f"{self.title} ({self.year}): \n-ID filmu: {self.movie_id} \n-Średnia ocena: {self.avg_rating if self.avg_rating else "Brak ocen"} \n-Gatunek: {self.genres if self.genres else "Nie przypisano"} \n-Czas trwania: {self.runtime} minut\n"

    def __repr__(self):
        """
        Reprezentacja techniczna filmu do debugowania
        
        Returns:
            str: Reprezentacja techniczna obiektu
        """
        return f"Movie({self.movie_id}, '{self.title}', {self.year}, {self.avg_rating}, '{self.runtime}', '{self.genres}')"

    @classmethod
    def from_api_data(cls, api_data):
        """
        Tworzy obiekt Movie z danych otrzymanych z API TMDb
        
        Args:
            api_data: Słownik z danymi filmu z API
            
        Returns:
            Movie: Nowy obiekt filmu
        """
        # Pobieramy rok z release_date (jeśli istnieje)
        release_date = api_data.get('release_date', '')
        year = int(release_date[:4]) if release_date else 0
        
        movie_id = api_data.get('id', 0)
        movie_runtime = runtime(movie_id)
        
        # Pobieramy gatunki jako string
        genre_ids = api_data.get('genre_ids', [])
    
        if not genre_ids and 'genres' in api_data:
            genre_ids = [genre['id'] for genre in api_data['genres']]
        
        # Mapowanie ID gatunków na polskie nazwy
        genres = ', '.join(GENRE_MAPPING.get(genre_id, "Nieznany") for genre_id in genre_ids)
        
        return cls(
            movie_id=api_data.get('id', 0),
            title=api_data.get('title', 'Brak tytułu'),
            year=year,
            avg_rating=api_data.get('vote_average', 0.0),
            runtime=movie_runtime,
            genres=genres
        )

    def is_in_genres(self, genre: str) -> bool:
        """
        Sprawdza czy film należy do określonego gatunku
        
        Args:
            genre: Nazwa gatunku do sprawdzenia
            
        Returns:
            bool: True jeśli film należy do gatunku, False w przeciwnym razie
        """
        return genre in self.genres      
    
    def has_similar_genres(self, other_movie):
        """
        Sprawdza czy dwa filmy mają identyczne gatunki
        
        Args:
            other_movie: Inny obiekt Movie do porównania
            
        Returns:
            bool: True jeśli filmy mają identyczne gatunki
        """
        return self.genres.split(', ') == other_movie.genres.split(', ')


class User:
    """
    Klasa reprezentująca użytkownika systemu rekomendacji
    Zawiera metody do zarządzania ocenami, historią oglądania i danymi użytkownika
    """
    
    def __init__(self, user_id: int, user_name: str) -> None:
        """
        Inicjalizacja użytkownika
        
        Args:
            user_id: Unikalny identyfikator użytkownika
            user_name: Nazwa użytkownika
        """
        self.user_id = user_id
        self.user_name = user_name
        self.user_ratings = {}  # Słownik {movie_id: rating}
        self.user_watch_history = []  # Lista ID obejrzanych filmów
        self.load_ratings()  # Wczytanie danych przy inicjalizacji
        
    def save_user_data(self):
        """
        Zapisuje dane użytkownika do pliku JSON
        Obsługuje błędy serializacji i zapisu
        """
        try:
            user_data = {
                "user_id": self.user_id,
                "user_name": self.user_name,
                "ratings": self.user_ratings,
                "watch_history": self.user_watch_history
            }

            with open("user_data.json","w") as f:
                json.dump(user_data, f)
                
            print("Zapisano dane.")
        except TypeError as e:
            print(f"Błąd podczas serializacji danych do JSON: {e}")
        except Exception as e:
            print(f"Nieoczekiwany błąd: {e}")

    def load_user_data(self):
        """
        Wczytuje dane użytkownika z pliku JSON
        Obsługuje błędy odczytu i dekodowania
        
        Returns:
            dict: Dane użytkownika lub None w przypadku błędu
        """
        try:
            with open("user_data.json","r") as f:
                user_data = json.load(f)
            
            self.user_id = user_data["user_id"]
            self.user_name = user_data["user_name"]
            self.user_ratings = user_data["ratings"]
            self.user_watch_history = user_data["watch_history"]
        except FileNotFoundError:
            print(f"Plik nie istnieje: {'user_data.json'}")
            return None
        except json.JSONDecodeError as e:
            print(f"Błąd podczas dekodowania JSON: {e}")
            return None
        except Exception as e:
            print(f"Nieoczekiwany błąd: {e}")
            return None

    def rate_movie(self, movie_id):
        """
        Pozwala użytkownikowi ocenić film
        Sprawdza czy film jest w historii oglądania przed oceną
        
        Args:
            movie_id: ID filmu do oceny
            
        Returns:
            str: Komunikat o wyniku oceniania
        """
        if movie_id not in self.user_watch_history:
            print("Najpierw dodaj ten film do historii oglądania!")
            return
        while True:
            try:
                user_rate = float(input("\nPodaj ocenę od 1 do 10: "))

                if not (1 <= user_rate <= 10) :
                    print(f"\nOcena {user_rate} jest nieprawidłowa.")
                else:
                    # Konwertuj movie_id na string dla zapisu w user_ratings
                    self.user_ratings[str(movie_id)] = user_rate
                    self.save_user_data()
                    return f"\nOcena {user_rate} została dodana."
            except ValueError:
                return "\nNieprawidłowy znak, zeby ocenic wpisz cyfre."

    def change_movie_rating(self, movie_id):
        """
        Pozwala użytkownikowi zmienić ocenę już ocenionego filmu
        
        Args:
            movie_id: ID filmu do zmiany oceny
            
        Returns:
            str: Komunikat o wyniku zmiany oceny
        """
        # Konwertuj movie_id na string dla porównania z user_ratings
        movie_id_str = str(movie_id)
        
        if movie_id_str not in self.user_ratings:
            print("Ten film nie został jeszcze oceniony!")
            return
        
        current_rating = self.user_ratings[movie_id_str]
        
        while True:
            try:
                new_rating = float(input("\nPodaj nową ocenę od 1 do 10: "))

                if not (1 <= new_rating <= 10):
                    print(f"\nOcena {new_rating} jest nieprawidłowa.")
                else:
                    self.user_ratings[movie_id_str] = new_rating
                    self.save_user_data()
                    return f"\nOcena została zmieniona z {current_rating} na {new_rating}."
            except ValueError:
                return "\nNieprawidłowy znak, żeby ocenić wpisz cyfrę."

    def get_rating(self, movie_id):
        """
        Pobiera ocenę użytkownika dla określonego filmu
        
        Args:
            movie_id: ID filmu
            
        Returns:
            str: Informacja o ocenie lub jej braku
        """
        if movie_id in self.user_ratings:
            return f"Oceniłeś juz ten film. Twoja ocena to: {self.user_ratings[movie_id]}"
        else: 
            return "Film nie został jeszcze przez ciebie oceniony."
        
        
    def load_ratings(self):
        """
        Wczytuje i wyświetla wszystkie oceny użytkownika
        Pokazuje szczegółowe informacje o ocenionych filmach
        """
        self.load_user_data()
        print("\nTwoje oceny filmów:\n")
        
        if not self.user_ratings:
            print("\nNie oceniono jeszcze zadnego filmu.")
            
        for i, rate_id in enumerate(self.user_ratings, 1):            
            movie = movie_for_id(rate_id)
            user_rating = self.user_ratings[rate_id]
            print(f"{i}. {movie.title} ({movie.year}) - twoja ocena: {user_rating}/10 \nŚrednia ocena filmu to: {movie.avg_rating}\n")
        
        
    def add_to_history(self, movie_id):
        """
        Dodaje film do historii oglądania użytkownika
        Sprawdza czy film nie jest już w historii
        
        Args:
            movie_id: ID filmu do dodania
        """
        try:
            
            if movie_id not in self.user_watch_history:
                self.user_watch_history.append(movie_id)
                self.save_user_data()
                print("Dodano film do historii oglądania.")
            else:
                print("Taki film jest juz w historii oglądania.")
        except TypeError as e:
            print(f"Błąd podczas serializacji danych do JSON: {e}")
        except Exception as e:
            print(f"Nieoczekiwany błąd: {e}")

    def load_watch_history(self):
        """
        Wczytuje i wyświetla historię oglądania użytkownika
        Pokazuje szczegółowe informacje o obejrzanych filmach
        """
        self.load_user_data()
        print("\nLista obejrzanych filmów:\n")   
        
        if not self.user_watch_history:
            print("Nie ma jeszcze filmów w historii oglądania.")
            return 
        
        for i, movie_id in enumerate(self.user_watch_history, 1):        
            movie = movie_for_id(movie_id)
            print(f"{i}. {movie}")