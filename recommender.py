"""
Moduł systemu rekomendacji filmów

Odpowiada za:
- Analizę ocen użytkownika
- Znajdowanie podobnych filmów
- Generowanie rekomendacji na podstawie preferencji użytkownika
- Wykorzystanie generatorów i list składanych do filtrowania filmów
- Implementację algorytmów rekomendacji z wykorzystaniem numpy
"""

import numpy as np
from collections import Counter
from typing import List, Dict, Tuple, Generator
from models import User, Movie
from api import search_movies, movie_for_id


class MovieRecommender:
    """
    Klasa odpowiedzialna za generowanie rekomendacji filmów
    wykorzystująca algorytmy oparte na preferencjach użytkownika
    """
    
    def __init__(self, user: User):
        """
        Inicjalizacja systemu rekomendacji
        
        Args:
            user: Obiekt użytkownika z ocenami i historią oglądania
        """
        self.user = user
        self.genre_weights = {}
        self.favorite_genres = []
        self._analyze_user_preferences()
    
    def _analyze_user_preferences(self) -> None:
        """
        Analizuje preferencje użytkownika na podstawie ocen filmów
        wykorzystuje listy składane do przetwarzania danych
        """
        if not self.user.user_ratings:
            return
            
        # Lista składana do wyodrębnienia gatunków z ocenionych filmów
        rated_movies_genres = [
            movie_for_id(movie_id).genres.split(', ')
            for movie_id in self.user.user_ratings.keys()
            if movie_for_id(movie_id) is not None
        ]
        
        # Generator do przetwarzania gatunków z ocenami
        def genre_rating_generator():
            for movie_id, rating in self.user.user_ratings.items():
                movie = movie_for_id(movie_id)
                if movie and movie.genres:
                    for genre in movie.genres.split(', '):
                        yield genre.strip(), rating
        
        # Obliczanie wag gatunków na podstawie ocen
        genre_scores = {}
        for genre, rating in genre_rating_generator():
            if genre not in genre_scores:
                genre_scores[genre] = []
            genre_scores[genre].append(rating)
        
        # Lista składana do obliczania średnich ocen dla gatunków
        self.genre_weights = {
            genre: np.mean(scores) 
            for genre, scores in genre_scores.items()
        }
        
        # Sortowanie gatunków według preferencji
        self.favorite_genres = sorted(
            self.genre_weights.keys(),
            key=lambda x: self.genre_weights[x],
            reverse=True
        )
    
    def get_user_favorite_movies(self) -> Generator[Movie, None, None]:
        """
        Generator zwracający ulubione filmy użytkownika (ocena >= 7)
        
        Yields:
            Movie: Film z wysoką oceną użytkownika
        """
        for movie_id, rating in self.user.user_ratings.items():
            if rating >= 7:
                movie = movie_for_id(int(movie_id))  # Konwertuj string na int dla API
                if movie:
                    yield movie
    
    def get_movies_by_genre(self, genre: str, limit: int = 10) -> List[Movie]:
        """
        Wyszukuje filmy z określonego gatunku używając list składanych
        
        Args:
            genre: Nazwa gatunku do wyszukania
            limit: Maksymalna liczba wyników
            
        Returns:
            List[Movie]: Lista filmów z danego gatunku
        """
        # Wyszukiwanie filmów z gatunku
        search_results = search_movies(genre)
        
        # Lista składana do filtrowania filmów z określonym gatunkiem
        genre_movies = [
            Movie.from_api_data(movie_data)
            for movie_data in search_results
            if Movie.from_api_data(movie_data).is_in_genres(genre)
        ]
        
        # Sortowanie według średniej oceny i zwrócenie top wyników
        sorted_movies = sorted(
            genre_movies,
            key=lambda x: x.avg_rating,
            reverse=True
        )
        
        return sorted_movies[:limit]
    
    def calculate_movie_score(self, movie: Movie) -> float:
        """
        Oblicza wynik rekomendacji dla filmu na podstawie preferencji użytkownika
        
        Args:
            movie: Film do oceny
            
        Returns:
            float: Wynik rekomendacji (wyższy = lepsza rekomendacja)
        """
        if not movie.genres:
            return 0.0
        
        movie_genres = movie.genres.split(', ')
        
        # Obliczanie wyniku na podstawie gatunków
        genre_score = sum(
            self.genre_weights.get(genre, 0) * 0.5
            for genre in movie_genres
        )
        
        # Normalizacja wyniku gatunku
        if movie_genres:
            genre_score /= len(movie_genres)
        
        # Wynik z TMDb (średnia ocena)
        tmdb_score = movie.avg_rating / 10.0
        
        # Kombinacja wyników (70% preferencje użytkownika, 30% ocena TMDb)
        final_score = (genre_score * 0.7) + (tmdb_score * 0.3)
        
        return final_score
    
    def get_recommendations(self, limit: int = 10) -> List[Tuple[Movie, float]]:
        """
        Generuje rekomendacje filmów na podstawie preferencji użytkownika
        
        Args:
            limit: Maksymalna liczba rekomendacji
            
        Returns:
            List[Tuple[Movie, float]]: Lista filmów z wynikami rekomendacji
        """
        if not self.user.user_ratings:
            return []
        
        # Generator do pobierania filmów z ulubionych gatunków
        def recommendation_candidates():
            for genre in self.favorite_genres[:3]:  # Top 3 gatunki
                movies = self.get_movies_by_genre(genre, limit=20)
                for movie in movies:
                    # Wyklucz filmy już ocenione przez użytkownika
                    if movie.movie_id not in self.user.user_ratings:
                        yield movie
        
        # Lista składana do obliczania wyników rekomendacji
        scored_movies = [
            (movie, self.calculate_movie_score(movie))
            for movie in recommendation_candidates()
        ]
        
        # Sortowanie według wyniku rekomendacji
        sorted_recommendations = sorted(
            scored_movies,
            key=lambda x: x[1],
            reverse=True
        )
        
        return sorted_recommendations[:limit]
    
    def get_rewatch_recommendations(self, limit: int = 5) -> List[Tuple[Movie, float]]:
        """
        Generuje rekomendacje filmów do ponownego obejrzenia
        (filmy z wysokimi ocenami użytkownika)
        
        Args:
            limit: Maksymalna liczba rekomendacji
            
        Returns:
            List[Tuple[Movie, float]]: Lista filmów do ponownego obejrzenia
        """
        # Generator do pobierania ulubionych filmów
        favorite_movies = list(self.get_user_favorite_movies())
        
        # Lista składana do tworzenia rekomendacji ponownego obejrzenia
        rewatch_candidates = [
            (movie, self.user.user_ratings[str(movie.movie_id)] / 10.0)
            for movie in favorite_movies
            if str(movie.movie_id) in self.user.user_ratings
        ]
        
        # Sortowanie według oceny użytkownika
        sorted_rewatch = sorted(
            rewatch_candidates,
            key=lambda x: x[1],
            reverse=True
        )
        
        return sorted_rewatch[:limit]
    
    def get_similar_movies(self, movie_id: int, limit: int = 5) -> List[Movie]:
        """
        Znajduje podobne filmy na podstawie gatunków
        
        Args:
            movie_id: ID filmu referencyjnego
            limit: Maksymalna liczba podobnych filmów
            
        Returns:
            List[Movie]: Lista podobnych filmów
        """
        reference_movie = movie_for_id(movie_id)
        if not reference_movie or not reference_movie.genres:
            return []
        
        # Generator do wyszukiwania podobnych filmów
        def similar_movies_generator():
            for genre in reference_movie.genres.split(', '):
                movies = self.get_movies_by_genre(genre.strip(), limit=10)
                for movie in movies:
                    if movie.movie_id != movie_id:
                        yield movie
        
        # Lista składana do filtrowania unikalnych filmów
        similar_movies = list({
            movie.movie_id: movie
            for movie in similar_movies_generator()
        }.values())
        
        # Sortowanie według podobieństwa gatunków i oceny
        sorted_similar = sorted(
            similar_movies,
            key=lambda x: (
                len(set(x.genres.split(', ')) & set(reference_movie.genres.split(', '))),
                x.avg_rating
            ),
            reverse=True
        )
        
        return sorted_similar[:limit]
    
    def get_user_statistics(self) -> Dict[str, any]:
        """
        Generuje statystyki użytkownika na podstawie ocen i historii
        
        Returns:
            Dict[str, any]: Statystyki użytkownika
        """
        if not self.user.user_ratings:
            return {
                'total_rated': 0,
                'average_rating': 0,
                'favorite_genre': None,
                'total_watched': len(self.user.user_watch_history)
            }
        
        # Lista składana do obliczania statystyk
        ratings = list(self.user.user_ratings.values())
        
        # Obliczanie statystyk z numpy
        stats = {
            'total_rated': len(ratings),
            'average_rating': float(np.mean(ratings)),
            'rating_std': float(np.std(ratings)),
            'favorite_genre': self.favorite_genres[0] if self.favorite_genres else None,
            'total_watched': len(self.user.user_watch_history),
            'top_genres': self.favorite_genres[:3]
        }
        
        return stats


# Funkcja pomocnicza do tworzenia instancji rekomendera
def create_recommender(user: User) -> MovieRecommender:
    """
    Tworzy instancję systemu rekomendacji dla użytkownika
    
    Args:
        user: Obiekt użytkownika
        
    Returns:
        MovieRecommender: Instancja systemu rekomendacji
    """
    return MovieRecommender(user)
    
    

