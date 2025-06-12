"""
Moduł definiujący modele danych

Zawiera:
- Klasę Movie reprezentującą film i jego atrybuty
- Klasę User reprezentującą użytkownika i jego preferencje
- Metody do zarządzania ocenami filmów
- Metody do zapisywania i wczytywania danych
"""
from api import runtime
from api import movie_for_id
import json

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
    def __init__(self, movie_id: int, title: str, year: int, avg_rating: float, runtime: int, genres: str):
        self.movie_id = movie_id
        self.title = title
        self.avg_rating = avg_rating
        self.year = year
        self.runtime = runtime
        self.genres = genres

    def __str__(self):
        return f"{self.title} ({self.year}): \n-ID filmu: {self.movie_id} n-Średnia ocena: {self.avg_rating if self.avg_rating else "Brak ocen"} \n-Gatunek: {self.genres if self.genres else "Nie przypisano"} \n-Czas trwania: {self.runtime} minut\n"

    def __repr__(self):
        return f"Movie({self.movie_id}, '{self.title}', {self.year}, {self.avg_rating}, '{self.runtime}', '{self.genres}')"

    @classmethod
    def from_api_data(cls, api_data):
        # Pobieramy rok z release_date (jeśli istnieje)
        release_date = api_data.get('release_date', '')
        year = int(release_date[:4]) if release_date else 0
        
        movie_id = api_data.get('id', 0)
        movie_runtime = runtime(movie_id)
        
        # Pobieramy gatunki jako string
        genre_ids = api_data.get('genre_ids', [])
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
        return genre in self.genres      
    
    def has_similar_genres(self, other_movie):
        return self.genres.split(', ') == other_movie.genres.split(', ')


class User:
    def __init__(self, user_id: int, user_name: str) -> None:
        self.user_id = user_id
        self.user_name = user_name
        self.user_ratings = {}
        self.user_watch_history = []
        self.load_ratings()
        
    def save_user_data(self):
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
        try:
            user_rate = float(input("Podaj ocenę od 1 do 10: "))

            if not (1 <= user_rate <= 10) :
                print(f"Podaj ocene od 1 do 10. {user_rate} jest nieprawidłowe.")
            else:
                self.user_ratings[movie_id] = user_rate
                self.save_user_data()
                return f"Ocena {user_rate} została dodana."
        except ValueError:
            return "Nieprawidłowy znak, zeby ocenic wpisz cyfre."

    def get_rating(self, movie_id):
        if movie_id in self.user_ratings:
            return f"Oceniłeś juz ten film. Twoja ocena to: {self.user_ratings[movie_id]}"
        else: 
            return "Film nie został jeszcze przez ciebie oceniony."
        
    def load_ratings(self):
        self.load_user_data()
        print(self.user_ratings)
        
    def add_to_history(self, movie_id):
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
        self.load_user_data()
        print("\nLista obejrzanych filmów:\n")   
        
        if not self.user_watch_history:
            print("Nie ma jeszcze filmów w historii oglądania.")
            return 
        
        for i, movie_id in enumerate(self.user_watch_history, 1):        
            movies = movie_for_id(movie_id)
            movie = Movie.from_api_data(movies)
            
            print(f"{i}. {movie}")